from django.db import models


class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('CANINO',  'Canino'),
        ('FELINO',  'Felino'),
        ('EXOTICO', 'Exótico'),
    ]

    nombre           = models.CharField(max_length=100)
    especie          = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raza             = models.CharField(max_length=100, blank=True, default='')
    fecha_nacimiento = models.DateField()
    nombre_dueno   = models.CharField(max_length=150, default='Sin Asignar')
    telefono_dueno = models.CharField(max_length=20, default='0000000000')
    created_at       = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name        = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.nombre_dueno})"