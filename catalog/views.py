from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import CategoriaDocumento, Documento, LineaInvestigacion
from .serializers import (
    CategoriaDocumentoSerializer,
    DocumentoSerializer,
    LineaInvestigacionSerializer,
)


class CategoriaDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoriaDocumento.objects.all()
    serializer_class = CategoriaDocumentoSerializer


class LineaInvestigacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LineaInvestigacion.objects.all()
    serializer_class = LineaInvestigacionSerializer


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    parser_classes = [MultiPartParser, FormParser]
