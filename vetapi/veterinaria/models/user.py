from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('VET',   'Veterinario'),
        ('STAFF', 'Personal de Apoyo'),
    ]

    email = models.EmailField(unique=True)
    role  = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VET')

    class Meta:
        verbose_name        = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering            = ['username']

    def __str__(self):
        return f"{self.username} — ({self.get_role_display()})"