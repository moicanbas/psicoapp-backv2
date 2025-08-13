from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from .tokens import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.middleware.csrf import get_token
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": "Ya existe un usuario con este correo o nombre de usuario. Verifica los campos."}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"detail": "El usuario ya existe o hay un conflicto con los datos."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "Ocurrió un error inesperado. Intenta nuevamente."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Credenciales inválidas."}, status=status.HTTP_400_BAD_REQUEST)

        # Tokens generados correctamente
        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        # Crear respuesta
        response = Response({"detail": "Login exitoso"},
                            status=status.HTTP_200_OK)

        # Cookies seguras y HttpOnly para JWT
        access_exp = timezone.now() + timedelta(minutes=1)
        refresh_exp = timezone.now() + timedelta(days=7)

        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=False,  # True si usas HTTPS
            samesite="Strict",
            expires=access_exp,
        )

        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=False,
            samesite="Strict",
            expires=refresh_exp,
        )

        # 🔹 Generar y setear CSRF token como cookie (NO HttpOnly)
        csrf_token = get_token(request)
        response.set_cookie(
            key="csrftoken",
            value=csrf_token,
            httponly=False,
            secure=False,  # True si usas HTTPS
            samesite="Strict",
        )

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response(
            {"detail": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)

        # Borrar cookies (se deben llamar igual que las usadas)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class CookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            raise AuthenticationFailed("No refresh token found")

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
        except Exception:
            raise AuthenticationFailed("Invalid or expired refresh token")

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,  # True en producción
            samesite="Lax",
            max_age=300,
        )
        return response


class SilentCookieTokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response(status=204)  # sin refresh token, pero no error

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
        except Exception:
            return Response(status=204)

        response = Response(status=204)
        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=300,
        )
        return response
