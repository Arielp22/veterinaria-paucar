from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketAtencion(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('delivered', 'Entregado'),
    ]

    user                     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    mascota                  = models.ForeignKey('veterinaria.Mascota', on_delete=models.PROTECT, related_name='tickets')
    anamnesis                = models.TextField()
    revision_clinica         = models.TextField()
    temperatura              = models.CharField(max_length=10)
    frecuencia_cardiaca      = models.PositiveIntegerField()
    diagnostico_observaciones= models.TextField(blank=True, default='')
    status                   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total                    = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at               = models.DateTimeField(auto_now_add=True)
    updated_at               = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Ticket de Atención'
        verbose_name_plural = 'Tickets de Atención'
        ordering            = ['-created_at']

    def __str__(self):
        return f"Ticket #{self.id} — {self.mascota.nombre}"

    def recalcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save(update_fields=['total'])


class DetalleAtencion(models.Model):
    ticket       = models.ForeignKey(TicketAtencion, on_delete=models.CASCADE, related_name='detalles')
    item_clinico = models.ForeignKey('veterinaria.ItemClinico', on_delete=models.PROTECT)
    cantidad     = models.PositiveIntegerField(default=1)
    precio_unit  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name        = 'Detalle de Atención'
        verbose_name_plural = 'Detalles de Atención'

    def __str__(self):
        return f"{self.cantidad}x {self.item_clinico.nombre} en Ticket #{self.ticket.id}"

    @property
    def subtotal(self):
        return round(float(self.precio_unit) * self.cantidad, 2)