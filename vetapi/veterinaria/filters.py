# veterinaria/filters.py
import django_filters
from veterinaria.models import Servicio, ItemClinico, TicketAtencion,Mascota, Vacuna


class ServicioFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Servicio
        fields = ['is_active']

class ItemClinicoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    servicio_nombre = django_filters.CharFilter(field_name='servicio__nombre', lookup_expr='icontains')

    class Meta:
        model = ItemClinico
        fields = ['is_active', 'servicio']

class TicketAtencionFilter(django_filters.FilterSet):
    desde_fecha = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    hasta_fecha = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = TicketAtencion
        fields = ['status', 'mascota']



class MascotaFilter(django_filters.FilterSet):
    nombre       = django_filters.CharFilter(lookup_expr='icontains')
    nombre_dueno = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Mascota
        fields = ['especie']


class VacunaFilter(django_filters.FilterSet):
    nombre_vacuna = django_filters.CharFilter(lookup_expr='icontains')
    desde_fecha   = django_filters.DateFilter(field_name='fecha_aplicacion', lookup_expr='gte')
    hasta_fecha   = django_filters.DateFilter(field_name='fecha_aplicacion', lookup_expr='lte')

    class Meta:
        model  = Vacuna
        fields = ['mascota']