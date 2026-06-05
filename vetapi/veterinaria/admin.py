from django.contrib import admin
from veterinaria.models import User, Servicio, ItemClinico, TicketAtencion, DetalleAtencion, Mascota, Vacuna

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'is_active']

@admin.register(ItemClinico)
class ItemClinicoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'stock', 'servicio']

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'especie', 'nombre_dueno']

@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ['id', 'mascota', 'nombre_vacuna', 'fecha_aplicacion']

@admin.register(TicketAtencion)
class TicketAtencionAdmin(admin.ModelAdmin):
    list_display = ['id', 'mascota', 'status', 'total']

@admin.register(DetalleAtencion)
class DetalleAtencionAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket', 'item_clinico', 'cantidad']