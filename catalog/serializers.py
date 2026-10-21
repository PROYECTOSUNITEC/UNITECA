from rest_framework import serializers

from .models import CategoriaDocumento, Documento, LineaInvestigacion


class CategoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaDocumento
        fields = ["id", "nombre", "descripcion"]


class LineaInvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaInvestigacion
        fields = ["id", "nombre", "descripcion"]


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = [
            "id",
            "titulo",
            "resumen",
            "categoria",
            "linea",
            "institucion",
            "anio_publicacion",
            "archivo",
            "palabras_clave",
            "vistas_contador",
            "estado",
            "fecha_subida",
            "subido_por",
        ]
        read_only_fields = ["vistas_contador", "fecha_subida"]
