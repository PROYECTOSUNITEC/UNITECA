from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import LoginSerializer, RegisterSerializer

import re
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


import logging
logger = logging.getLogger(__name__)

# --- Vistas basadas en HTML (Templates) ---

class LoginView(TemplateView):
    template_name = 'accounts/login.html'

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

class RecoveryView(TemplateView):
    template_name = 'accounts/recovery.html'


# --- Vistas de la API (DRF) ---

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"detail": "Inicio de sesión exitoso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuario registrado exitosamente. Redirigiendo al inicio de sesión..."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()

class PasswordResetAPIView(APIView):
    def post(self, request):
        correoUsuario = request.data.get("email", "").strip()
        if not correoUsuario:
            return Response(
                {"error": "Por favor, ingresa un correo electrónico"}, 
                status=status.HTTP_400_BAD_REQUEST
            )        
        try:
            usuarioInstancia = User.objects.get(email=correoUsuario)
        except User.DoesNotExist:
            return Response(
                {"error": "El correo ingresado no pertenece a ningún usuario registrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generación de tokens seguros
        uidB64 = urlsafe_base64_encode(force_bytes(usuarioInstancia.pk))
        tokenSeguro = default_token_generator.make_token(usuarioInstancia)

        protocoloConexion = "https" if request.is_secure() else "http"
        hostServidor = request.get_host()
        enlaceRecuperacion = f"{protocoloConexion}://{hostServidor}/reset_password/{uidB64}/{tokenSeguro}/"

        # Envío del correo electrónico
        asuntoCorreo = "UNITECa - Restablecer Contraseña"
        cuerpoMensaje = (
            f"Saludos {usuarioInstancia.email},\n\n"
            f"Se ha solicitado un restablecimiento de contraseña para tu cuenta.\n"
            f"Por favor, haz clic en el siguiente enlace para ingresar tu nueva clave:\n\n"
            f"{enlaceRecuperacion}\n\n"
            f"El enlace expira en 15 minutos.\n\n"
            f"Si usted no solicitó este cambio, puede ignorar este mensaje de forma segura."
        )
        
        remitenteConfigurado = None  # Django usará automáticamente el EMAIL_HOST_USER

        try:
            send_mail(asuntoCorreo, cuerpoMensaje, remitenteConfigurado, [usuarioInstancia.email], fail_silently=False)
            return Response(
                {"detail": "Se ha enviado un enlace de recuperación a su correo institucional"}, 
                status=status.HTTP_200_OK
            )
        except Exception as errorEnvio:
            return Response(
                {"error": f"Error al enviar el correo. Por favor, intente más tarde"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetConfirmView(View):
    templateName = 'accounts/password_reset_confirm.html'

    def get(self, request, uidb64, token):
        userInstance = self.getUser(uidb64)
        
        # Validar si el token y el usuario son correctos antes de mostrar la página
        if userInstance is not None and default_token_generator.check_token(userInstance, token):
            return render(request, self.templateName, {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "El enlace de recuperación es inválido o ha expirado.")
            return redirect('login')

    def post(self, request, uidb64, token):
        userInstance = self.getUser(uidb64)
        
        if userInstance is not None and default_token_generator.check_token(userInstance, token):
            newPassword = request.POST.get('password')
            confirmPassword = request.POST.get('confirmPassword')

            if not newPassword or newPassword != confirmPassword:
                messages.error(request, "Las contraseñas no coinciden o están vacías.")
                return render(request, self.templateName, {'uidb64': uidb64, 'token': token})

            # Guardar la nueva contraseña encriptada
            userInstance.set_password(newPassword)
            userInstance.save()
            
            messages.success(request, "¡Contraseña actualizada con éxito! Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "El enlace de recuperación es inválido o ha expirado.")
            return redirect('login')

    def getUser(self, uidb64):
        try:
            decodedUid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=decodedUid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None