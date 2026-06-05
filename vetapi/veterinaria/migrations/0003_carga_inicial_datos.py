from django.db import migrations

def cargar_servicios(apps, schema_editor):

    Servicio = apps.get_model('veterinaria', 'Servicio')
    

    servicios = [
        {"nombre": "Consulta General", "slug": "consulta-general", "descripcion": "Revisión médica general"},
        {"nombre": "Vacunación", "slug": "vacunacion", "descripcion": "Aplicación de vacunas"},
        {"nombre": "Limpieza Dental", "slug": "limpieza-dental", "descripcion": "Limpieza y profilaxis"},
    ]
    

    for s in servicios:
        Servicio.objects.get_or_create(
            nombre=s["nombre"], 
            slug=s["slug"], 
            defaults={'descripcion': s["descripcion"]}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0002_servicio_remove_historialmedicamento_consulta_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar_servicios),
    ]