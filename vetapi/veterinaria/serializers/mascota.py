from rest_framework import serializers
from veterinaria.models import Mascota


class MascotaSerializer(serializers.ModelSerializer):
    total_vacunas = serializers.SerializerMethodField()

    class Meta:
        model  = Mascota
        fields = [
            'id', 'nombre', 'especie', 'raza',
            'fecha_nacimiento', 'nombre_dueno',
            'telefono_dueno', 'total_vacunas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_vacunas(self, obj):
        return obj.vacunas.count()

    def validate_nombre(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('El nombre de la mascota debe tener al menos 2 caracteres.')
        return value