from django.test import TestCase

from .models import Rol, Usuario


class UsuarioManagerTests(TestCase):
    def test_create_user_hashes_password_and_defaults_to_active(self):
        user = Usuario.objects.create_user(
            email="user@example.com", nombre="Ana", apellido="Pérez", password="s3cret!"
        )
        self.assertTrue(user.check_password("s3cret!"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_estado_suspendido_desactiva_al_usuario(self):
        user = Usuario.objects.create_user(
            email="user2@example.com", nombre="Ana", apellido="Pérez", password="s3cret!"
        )
        user.estado = Usuario.Estado.SUSPENDIDO
        user.save()
        self.assertFalse(user.is_active)

    def test_create_superuser_sets_staff_and_superuser(self):
        admin = Usuario.objects.create_superuser(
            email="admin@example.com", nombre="Admin", apellido="Uniteca", password="s3cret!"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class RolTests(TestCase):
    def test_str_returns_nombre(self):
        rol = Rol.objects.create(nombre="Bibliotecario")
        self.assertEqual(str(rol), "Bibliotecario")
