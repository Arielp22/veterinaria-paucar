from rest_framework import serializers
from veterinaria.models import ItemClinico
from veterinaria.serializers.servicio import ServicioSerializer

class ItemClinicoSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClinico
        fields = ['id', 'nombre', 'precio', 'stock', 'is_active']

class ItemClinicoSerializer(serializers.ModelSerializer):
    servicio = ServicioSerializer(read_only=True)
    servicio_id = serializers.PrimaryKeyRelatedField(
        source='servicio',
        write_only=True,
        queryset=ItemClinico.objects.none()
    )
    precio_con_iva = serializers.SerializerMethodField()
    en_stock = serializers.SerializerMethodField()

    class Meta:
        model = ItemClinico
        fields = [
            'id', 'nombre', 'description', 'precio', 'precio_con_iva',
            'stock', 'en_stock', 'is_active', 'servicio', 'servicio_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from veterinaria.models import Servicio
        self.fields['servicio_id'].queryset = Servicio.objects.filter(is_active=True)

    def get_precio_con_iva(self, obj):
        return obj.precio_con_iva

    def get_en_stock(self, obj):
        return obj.en_stock

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio del tratamiento debe ser mayor a 0.')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El inventario de insumos no puede ser negativo.')
        return value