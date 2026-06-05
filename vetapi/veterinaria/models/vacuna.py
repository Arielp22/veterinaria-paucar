from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vacuna(models.Model):
    mascota          = models.ForeignKey('veterinaria.Mascota', on_delete=models.CASCADE, related_name='vacunas')
    nombre_vacuna    = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis    = models.DateField(null=True, blank=True)
    veterinario      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vacunas_aplicadas')
    observaciones    = models.TextField(blank=True, default='')

    class Meta:
        verbose_name        = 'Vacuna'
        verbose_name_plural = 'Vacunas'
        ordering            = ['-fecha_aplicacion']

    def __str__(self):
        return f"{self.nombre_vacuna} — {self.mascota.nombre}"