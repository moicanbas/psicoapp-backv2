from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

schema_view = get_schema_view(
    openapi.Info(
        title="API Auth",
        default_version='v1',
        description="Documentación de autenticación con JWT y DRF",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/patients/', include('apps.patients.urls')),
    path('api/medical_records/', include('apps.medicalrecords.urls')),

    # Password reset views (puedes ajustar los paths si deseas)
    path('api/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
