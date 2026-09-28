from django.db import migrations


def eliminar_datos_de_ejemplo(apps, schema_editor):
    alias = schema_editor.connection.alias
    Requisito = apps.get_model('serviciosApp', 'Requisito')
    Servicio = apps.get_model('serviciosApp', 'Servicio')
    Categoria = apps.get_model('serviciosApp', 'Categoria')
    Solicitud = apps.get_model('solicitudesApp', 'Solicitud')

    Requisito.objects.using(alias).all().delete()
    Servicio.objects.using(alias).all().delete()
    Categoria.objects.using(alias).all().delete()
    Solicitud.objects.using(alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('serviciosApp', '0007_reponer_datos_iniciales'),
        ('solicitudesApp', '0003_alter_solicitud_id'),
    ]

    operations = [
        migrations.RunPython(eliminar_datos_de_ejemplo, migrations.RunPython.noop),
    ]
