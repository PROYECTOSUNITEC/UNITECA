from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UsuarioManager


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "roles"
        verbose_name = "rol"
        verbose_name_plural = "roles"

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Estado(models.TextChoices):
        ACTIVO = "activo", "Activo"
        SUSPENDIDO = "suspendido", "Suspendido"
        INACTIVO = "inactivo", "Inactivo"

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255, db_column="password_hash")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    roles = models.ManyToManyField(Rol, through="UsuarioRol", related_name="usuarios", blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    @property
    def is_active(self):
        return self.estado == self.Estado.ACTIVO

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}".strip()

    def get_short_name(self):
        return self.nombre

    def __str__(self):
        return self.get_full_name() or self.email


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column="usuario_id")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column="rol_id")

    class Meta:
        db_table = "usuario_roles"
        constraints = [
            models.UniqueConstraint(fields=["usuario", "rol"], name="usuario_roles_unique"),
        ]

    def __str__(self):
        return f"{self.usuario} -> {self.rol}"
