from django.db import models

from apps.patients.models import BaseModel

class Cie10(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=155)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "diagnosis"
        verbose_name_plural = "diagnosis"
        ordering = ['code']
    