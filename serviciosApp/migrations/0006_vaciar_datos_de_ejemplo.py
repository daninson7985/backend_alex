from django.db import migrations


# Keep this migration in the graph, but never delete application data on upgrade.
class Migration(migrations.Migration):
    dependencies = [
        ('serviciosApp', '0005_reponer_datos_iniciales'),
        ('solicitudesApp', '0003_alter_solicitud_id'),
    ]

    operations = []