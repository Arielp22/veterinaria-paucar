from rest_framework import serializers
from veterinaria.models import TicketAtencion, DetalleAtencion, ItemClinico
from veterinaria.serializers.item import ItemClinicoSummarySerializer

class DetalleAtencionSerializer(serializers.ModelSerializer):
    item_clinico = ItemClinicoSummarySerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetalleAtencion
        fields = ['id', 'item_clinico', 'cantidad', 'precio_unit', 'subtotal']
        read_only_fields = ['id', 'precio_unit']

    def get_subtotal(self, obj):
        return obj.subtotal

class TicketAtencionSerializer(serializers.ModelSerializer):
    detalles = DetalleAtencionSerializer(many=True, read_only=True)
    dueno_username = serializers.SerializerMethodField()
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = TicketAtencion
        fields = [
            'id', 'dueno_username', 'mascota', 'mascota_nombre', 'status', 'total', 'total_items',
            'anamnesis', 'revision_clinica', 'temperatura', 'frecuencia_cardiaca',
            'diagnostico_observaciones', 'detalles', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']

    def get_total_items(self, obj):
        return obj.detalles.count()

    def get_dueno_username(self, obj):
        return obj.user.username if obj.user else None

    def to_representation(self, instance):
        """Oculta de forma estricta los precios al Dueño de Mascota (Regla de negocio)"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user.role == 'CLIENT' and not request.user.is_superuser:
                representation.pop('total', None)
                if 'detalles' in representation:
                    for det in representation['detalles']:
                        det.pop('precio_unit', None)
                        det.pop('subtotal', None)
        return representation

class AddItemToTicketSerializer(serializers.Serializer):
    item_clinico_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)

    def validate_item_clinico_id(self, value):
        try:
            ItemClinico.objects.get(pk=value, is_active=True)
        except ItemClinico.DoesNotExist:
            raise serializers.ValidationError(f'El ítem clínico {value} no está registrado o se encuentra inactivo.')
        return value

    def validate(self, data):
        item = ItemClinico.objects.get(pk=data['item_clinico_id'])
        if item.stock < data['cantidad']:
            raise serializers.ValidationError(f'Inventario insuficiente en clínica. Solo quedan {item.stock} unidades de {item.nombre}.')
        return data