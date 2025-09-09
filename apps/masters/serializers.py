from rest_framework import serializers
from .models import *


class Cie10Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cie10
        fields = ['id', 'name', 'code']