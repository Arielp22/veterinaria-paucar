from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from veterinaria.models import TicketAtencion, ItemClinico, DetalleAtencion
from veterinaria.serializers import TicketAtencionSerializer, AddItemToTicketSerializer
from veterinaria.permissions import IsOwnerOrStaff
from veterinaria.filters import TicketAtencionFilter
from veterinaria.pagination import StandardPagination

class TicketAtencionViewSet(viewsets.ModelViewSet):
    queryset = TicketAtencion.objects.select_related('user', 'mascota').prefetch_related('detalles__item_clinico').all()
    serializer_class = TicketAtencionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TicketAtencionFilter
    search_fields = ['mascota__nombre', 'user__username', 'status', 'diagnostico_observaciones']
    ordering_fields = ['created_at', 'updated_at', 'total', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or getattr(user, 'role', None) in ['ADMIN', 'VET']:
            return qs
        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status != 'pending':
            return Response({'error': 'No se pueden agregar ítems a un ticket procesado'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = AddItemToTicketSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_clinico_id']
            cantidad = serializer.validated_data['cantidad']
            
            item = ItemClinico.objects.get(id=item_id)
            if item.stock < cantidad:
                return Response({'error': f'Stock insuficiente para {item.nombre}'}, status=status.HTTP_400_BAD_REQUEST)
                
            # Descontar inventario e insertar al detalle
            item.stock -= cantidad
            item.save()
            
            DetalleAtencion.objects.create(
                ticket=ticket,
                item_clinico=item,
                cantidad=cantidad,
                precio_unit=item.precio
            )
            
            # Recalcular total del ticket
            ticket.recalcular_total()
            return Response({'status': 'Ítem agregado correctamente', 'total_actual': ticket.total})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        ticket = self.get_object()
        if ticket.status != 'pending':
            return Response({'error': 'El ticket ya fue confirmado previamente'}, status=status.HTTP_400_BAD_REQUEST)
        ticket.status = 'confirmed'
        ticket.save()
        return Response({'status': 'Atención clínica confirmada y bloqueada'})

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        nuevo_estado = request.data.get('status')
        if nuevo_estado not in ['pending', 'confirmed', 'delivered']:
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        ticket.status = nuevo_estado
        ticket.save()
        return Response({'status': f'Estado cambiado a {nuevo_estado}'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_tickets = self.queryset.count()
        ingresos_totales = self.queryset.filter(status='delivered').aggregate(Sum('total'))['total__sum'] or 0
        return Response({
            'total_orders': total_tickets,
            'total_revenue': round(float(ingresos_totales), 2)
        })