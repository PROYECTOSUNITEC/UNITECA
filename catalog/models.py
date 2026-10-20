from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.db.models.functions import ExtractYear, Now


class CategoriaDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = "categorias_documento"
        verbose_name = "categoría de documento"
        verbose_name_plural = "categorías de documento"

    def __str__(self):
        return self.nombre


class LineaInvestigacion(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = "lineas_investigacion"
        verbose_name = "línea de investigación"
        verbose_name_plural = "líneas de investigación"

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    class Estado(models.TextChoices):
        PUBLICADO = "publicado", "Publicado"
        BORRADOR = "borrador", "Borrador"
        ARCHIVADO = "archivado", "Archivado"

    titulo = models.CharField(max_length=255)
    resumen = models.TextField()
    categoria = models.ForeignKey(
        CategoriaDocumento,
        on_delete=models.PROTECT,
        db_column="categoria_id",
        related_name="documentos",
    )
    linea = models.ForeignKey(
        LineaInvestigacion,
        on_delete=models.PROTECT,
        db_column="linea_id",
        related_name="documentos",
    )
    institucion = models.CharField(max_length=255, default="Universidad / Institución", blank=True)
    anio_publicacion = models.PositiveIntegerField()
    archivo = models.FileField(
        upload_to="documentos/%Y/%m/", max_length=255, db_column="url_archivo_pdf"
    )
    palabras_clave = models.CharField(max_length=255, blank=True)
    vistas_contador = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PUBLICADO)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column="subido_por_usuario_id",
        related_name="documentos_subidos",
    )

    documento_vector = models.GeneratedField(
        expression=SearchVector("titulo", "resumen", "palabras_clave", config="spanish"),
        output_field=SearchVectorField(),
        db_persist=True,
    )

    autores = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="DocumentoAutor", related_name="documentos_autor"
    )
    tutores = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="DocumentoTutor", related_name="documentos_tutor"
    )

    class Meta:
        db_table = "documentos"
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        indexes = [
            models.Index(fields=["categoria"], name="idx_documentos_categoria"),
            models.Index(fields=["linea"], name="idx_documentos_linea"),
            GinIndex(fields=["documento_vector"], name="idx_documentos_fulltext"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(anio_publicacion__gte=1900)
                & models.Q(anio_publicacion__lte=ExtractYear(Now())),
                name="documentos_anio_publicacion_rango_check",
            ),
        ]

    def __str__(self):
        return self.titulo


class DocumentoAutor(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, db_column="documento_id")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="usuario_id"
    )

    class Meta:
        db_table = "documento_autores"
        verbose_name = "autor de documento"
        verbose_name_plural = "autores de documento"
        constraints = [
            models.UniqueConstraint(
                fields=["documento", "usuario"], name="documento_autores_unique"
            ),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.documento}"


class DocumentoTutor(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, db_column="documento_id")
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column="tutor_id"
    )

    class Meta:
        db_table = "documento_tutores"
        verbose_name = "tutor de documento"
        verbose_name_plural = "tutores de documento"
        constraints = [
            models.UniqueConstraint(fields=["documento", "tutor"], name="documento_tutores_unique"),
        ]

    def __str__(self):
        return f"{self.tutor} - {self.documento}"


class HistorialConsulta(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="usuario_id",
        related_name="historial_consultas",
    )
    documento = models.ForeignKey(
        Documento,
        on_delete=models.CASCADE,
        db_column="documento_id",
        related_name="historial_consultas",
    )
    fecha_visualizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "historial_consultas"
        verbose_name = "historial de consulta"
        verbose_name_plural = "historial de consultas"

    def __str__(self):
        return f"{self.usuario} vio {self.documento} ({self.fecha_visualizacion})"
