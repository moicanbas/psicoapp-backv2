from django.contrib import admin
from .models import (
    IdentificationType, Gender, MaritalStatus, Patient, Tutor, EPS, Etnia
)

admin.site.register(IdentificationType)
admin.site.register(Gender)
admin.site.register(MaritalStatus)
admin.site.register(Patient)
admin.site.register(Tutor)
admin.site.register(EPS)
admin.site.register(Etnia)