from rest_framework import serializers
from veterinaria.models import Vacuna


class VacunaSerializer(serializers.ModelSerializer):
    mascota_nombre     = serializers.CharField(source='mascota.nombre', read_only=True)
    veterinario_name   = serializers.CharField(source='veterinario.username', read_only=True)

    class Meta:
        model  = Vacuna
        fields = [
            'id', 'mascota', 'mascota_nombre', 'nombre_vacuna',
            'fecha_aplicacion', 'proxima_dosis', 'veterinario',
            'veterinario_name', 'observaciones',
        ]
        read_only_fields = ['id', 'veterinario']

    def validate(self, data):
        if data.get('proxima_dosis') and data['proxima_dosis'] <= data['fecha_aplicacion']:
            raise serializers.ValidationError({'proxima_dosis': 'La fecha de la próxima dosis debe ser posterior a la aplicación.'})
        return data