from rest_framework import serializers
from django.utils.text import slugify
from veterinaria.models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'slug', 'descripcion', 'is_active', 'total_items', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_total_items(self, obj):
        return obj.items.filter(is_active=True).count()

    def validate_slug(self, value):
        return slugify(value)

    def validate_nombre(self, value):
        qs = Servicio.objects.filter(nombre__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un servicio clínico registrado con este nombre.')
        return value