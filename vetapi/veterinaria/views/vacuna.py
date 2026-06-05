# veterinaria/views/vacuna.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from veterinaria.models      import Vacuna
from veterinaria.serializers import VacunaSerializer
from veterinaria.permissions import IsStaffOrReadOnly
from veterinaria.filters     import VacunaFilter
from veterinaria.pagination  import StandardPagination


class VacunaViewSet(viewsets.ModelViewSet):
    queryset           = Vacuna.objects.select_related('mascota', 'veterinario').all()
    serializer_class   = VacunaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = VacunaFilter
    search_fields      = ['nombre_vacuna', 'mascota__nombre']
    ordering_fields    = ['fecha_aplicacion']
    ordering           = ['-fecha_aplicacion']

    def perform_create(self, serializer):
        serializer.save(veterinario=self.request.user)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Vacuna.objects.all()
        return Response({
            'total_aplicadas': qs.count(),
            'resumen_vacunas': [
                {
                    'nombre_vacuna': v['nombre_vacuna'],
                    'cantidad':      v['total'],
                }
                for v in qs.values('nombre_vacuna').annotate(total=Count('id')).order_by('-total')
            ],
        })