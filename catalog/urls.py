from rest_framework.routers import DefaultRouter

from .views import CategoriaDocumentoViewSet, DocumentoViewSet, LineaInvestigacionViewSet

router = DefaultRouter()
router.register("categorias", CategoriaDocumentoViewSet, basename="categoria")
router.register("lineas", LineaInvestigacionViewSet, basename="linea")
router.register("documentos", DocumentoViewSet, basename="documento")

urlpatterns = router.urls
