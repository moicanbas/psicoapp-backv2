from rest_framework import viewsets, status, permissions
from .serializers import Cie10Serializer
from .models import Cie10


class Cie10ViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cie10.objects.filter(is_active=True)
    serializer_class = Cie10Serializer
