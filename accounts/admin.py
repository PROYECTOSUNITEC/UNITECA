from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Rol, Usuario, UsuarioRol


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    ordering = ["email"]
    list_display = ["email", "nombre", "apellido", "estado", "is_staff"]
    list_filter = ["estado", "is_staff", "is_superuser"]
    search_fields = ["email", "nombre", "apellido"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Datos personales", {"fields": ("nombre", "apellido", "estado")}),
        ("Permisos", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nombre", "apellido", "password1", "password2"),
            },
        ),
    )


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre"]


@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ["usuario", "rol"]
