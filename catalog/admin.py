from django.contrib import admin

from .models import (
    CategoriaDocumento,
    Documento,
    DocumentoAutor,
    DocumentoTutor,
    HistorialConsulta,
    LineaInvestigacion,
)


@admin.register(CategoriaDocumento)
class CategoriaDocumentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre"]


@admin.register(LineaInvestigacion)
class LineaInvestigacionAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre"]


class DocumentoAutorInline(admin.TabularInline):
    model = DocumentoAutor
    extra = 1


class DocumentoTutorInline(admin.TabularInline):
    model = DocumentoTutor
    extra = 1


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "categoria", "linea", "estado", "anio_publicacion", "vistas_contador"]
    list_filter = ["estado", "categoria", "linea"]
    search_fields = ["titulo", "resumen", "palabras_clave"]
    inlines = [DocumentoAutorInline, DocumentoTutorInline]
    readonly_fields = ["vistas_contador", "fecha_subida"]


@admin.register(HistorialConsulta)
class HistorialConsultaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "documento", "fecha_visualizacion"]
