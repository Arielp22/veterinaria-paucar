from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg
from veterinaria.models import ItemClinico
from veterinaria.serializers import ItemClinicoSerializer
from veterinaria.permissions import IsStaffOrReadOnly
from veterinaria.filters import ItemClinicoFilter
from veterinaria.pagination import StandardPagination

class ItemClinicoViewSet(viewsets.ModelViewSet):
    queryset = ItemClinico.objects.select_related('servicio').all()
    serializer_class = ItemClinicoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ItemClinicoFilter
    search_fields = ['nombre', 'description', 'servicio__nombre']
    ordering_fields = ['nombre', 'precio', 'stock', 'created_at']
    ordering = ['nombre']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'restock']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        item = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return Response({'error': 'La cantidad debe ser mayor a 0'}, status=status.HTTP_400_BAD_REQUEST)
            item.stock += cantidad
            item.save()
            return Response({'status': 'Stock actualizado', 'nuevo_stock': item.stock})
        except ValueError:
            return Response({'error': 'Cantidad no válida'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def available(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(stock__gt=0, is_active=True))
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_items = self.queryset.count()
        stock_total = self.queryset.aggregate(Sum('stock'))['stock__sum'] or 0
        precio_promedio = self.queryset.aggregate(Avg('precio'))['precio__avg'] or 0
        return Response({
            'total_products': total_items,
            'total_stock': stock_total,
            'average_price': round(float(precio_promedio), 2)
        })