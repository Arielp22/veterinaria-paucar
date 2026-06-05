from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from veterinaria.models      import Mascota
from veterinaria.serializers import MascotaSerializer
from veterinaria.permissions import IsStaffOrReadOnly
from veterinaria.filters     import MascotaFilter
from veterinaria.pagination  import StandardPagination


class MascotaViewSet(viewsets.ModelViewSet):
    queryset           = Mascota.objects.all()
    serializer_class   = MascotaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = MascotaFilter
    search_fields      = ['nombre', 'nombre_dueno']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']

    @action(detail=True, methods=['get'], url_path='vacunas')
    def historial_vacunas(self, request, pk=None):
        mascota = self.get_object()
        from veterinaria.serializers import VacunaSerializer
        qs   = mascota.vacunas.all()
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(VacunaSerializer(page, many=True).data)
        return Response(VacunaSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Mascota.objects.all()
        return Response({
            'total':    qs.count(),
            'caninos':  qs.filter(especie='CANINO').count(),
            'felinos':  qs.filter(especie='FELINO').count(),
            'exoticos': qs.filter(especie='EXOTICO').count(),
        })