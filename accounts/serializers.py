from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Como USERNAME_FIELD es 'email', authenticate recibe email como username
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError("Credenciales inválidas o cuenta no registrada.")
        
        # Como tu is_active es un @property basado en el estado, authenticate ya evalúa 
        # si puede retornar el usuario dependiendo de si está activo o no.
            
        data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'email', 'password']

    def create(self, validated_data):
        # Utiliza tu UsuarioManager personalizado (objects.create_user)
        user = User.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            password=validated_data['password']
        )
        return user