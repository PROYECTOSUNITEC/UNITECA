from django.urls import path
from django.views.generic import RedirectView  # <--- Importa RedirectView
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Redirige la raíz '/' directamente a la página de login
    path('', RedirectView.as_view(url='/login/', permanent=False), name='index'),

    # Rutas de vistas HTML
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recovery/', RecoveryView.as_view(), name='recovery'),

    # Endpoints de la API de DRF
    path('api/accounts/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/accounts/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/accounts/password-reset/', PasswordResetAPIView.as_view(), name='api_recovery'),

    # Ruta HTML para el formulario de restablecer contraseña
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]