from django.db import migrations

ROLES = [
    ("Administrador", "Acceso total al sistema y gestión global de usuarios y configuraciones"),
    ("Coordinador", "Encargado de la gestión, carga, publicación y auditoría de tesis y documentos de ayuda"),
    ("Tutor", "Docente o investigador que orienta las tesis"),
    ("Estudiante", "Usuario registrado con acceso a consulta y lectura de documentos"),
]


def seed_roles(apps, schema_editor):
    Rol = apps.get_model("accounts", "Rol")
    for nombre, descripcion in ROLES:
        Rol.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})


def unseed_roles(apps, schema_editor):
    Rol = apps.get_model("accounts", "Rol")
    Rol.objects.filter(nombre__in=[nombre for nombre, _ in ROLES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_roles, unseed_roles),
    ]
