from django.db import DatabaseError
from django.test import TestCase

from accounts.models import Usuario

from .models import (
    CategoriaDocumento,
    Documento,
    DocumentoAutor,
    DocumentoTutor,
    HistorialConsulta,
    LineaInvestigacion,
)


class DocumentoTests(TestCase):
    def setUp(self):
        self.categoria = CategoriaDocumento.objects.create(nombre="Categoría de prueba")
        self.linea = LineaInvestigacion.objects.create(nombre="Línea de prueba")
        self.usuario = Usuario.objects.create_user(
            email="autor@example.com", nombre="Autor", apellido="Uno", password="s3cret!"
        )

    def _crear_documento(self):
        return Documento.objects.create(
            titulo="Sistema de gestión bibliotecaria",
            resumen="Resumen de prueba",
            categoria=self.categoria,
            linea=self.linea,
            anio_publicacion=2026,
            archivo="documentos/prueba.pdf",
            subido_por=self.usuario,
        )

    def test_documento_vector_se_genera_con_el_contenido(self):
        documento = self._crear_documento()
        documento.refresh_from_db()
        self.assertIn("sistem", str(documento.documento_vector))

    def test_historial_incrementa_vistas_via_trigger(self):
        documento = self._crear_documento()
        self.assertEqual(documento.vistas_contador, 0)
        HistorialConsulta.objects.create(usuario=self.usuario, documento=documento)
        documento.refresh_from_db()
        self.assertEqual(documento.vistas_contador, 1)

    def test_autor_no_puede_ser_tutor_de_su_propio_documento(self):
        documento = self._crear_documento()
        DocumentoAutor.objects.create(documento=documento, usuario=self.usuario)
        with self.assertRaises(DatabaseError):
            DocumentoTutor.objects.create(documento=documento, tutor=self.usuario)
