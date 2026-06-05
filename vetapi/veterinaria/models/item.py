from django.db import models


class ItemClinico(models.Model):
    nombre      = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    servicio    = models.ForeignKey('veterinaria.Servicio', on_delete=models.CASCADE, related_name='items')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Ítem Clínico'
        verbose_name_plural = 'Ítems Clínicos'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

    @property
    def precio_con_iva(self):
        return round(float(self.precio) * 1.15, 2)

    @property
    def en_stock(self):
        return self.stock > 0