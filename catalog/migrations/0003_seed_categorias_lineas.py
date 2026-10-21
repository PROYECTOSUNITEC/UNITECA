from django.db import migrations

CATEGORIAS = [
    ("Tesis de Pregrado", "Trabajos especiales de grado para título profesional"),
    ("Tesis de Postgrado", "Trabajos de maestría o doctorado"),
    ("Artículo Científico", "Publicaciones y papers académicos"),
    ("Guía Metodológica", "Manuales, plantillas y formatos de ayuda para la elaboración de tesis"),
]

LINEAS = [
    ("Sistemas de Información y Software", "Desarrollo web, arquitectura y bases de datos"),
    ("Seguridad Informática y Redes", "Ciberseguridad, infraestructura y auditoría"),
    ("Inteligencia Artificial y Datos", "Machine learning, minería de datos y ciencia de datos"),
]


def seed(apps, schema_editor):
    CategoriaDocumento = apps.get_model("catalog", "CategoriaDocumento")
    LineaInvestigacion = apps.get_model("catalog", "LineaInvestigacion")

    for nombre, descripcion in CATEGORIAS:
        CategoriaDocumento.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})

    for nombre, descripcion in LINEAS:
        LineaInvestigacion.objects.get_or_create(nombre=nombre, defaults={"descripcion": descripcion})


def unseed(apps, schema_editor):
    CategoriaDocumento = apps.get_model("catalog", "CategoriaDocumento")
    LineaInvestigacion = apps.get_model("catalog", "LineaInvestigacion")

    CategoriaDocumento.objects.filter(nombre__in=[nombre for nombre, _ in CATEGORIAS]).delete()
    LineaInvestigacion.objects.filter(nombre__in=[nombre for nombre, _ in LINEAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_triggers"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
