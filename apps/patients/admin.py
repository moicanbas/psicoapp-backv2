from django.contrib import admin
from .models import (
    IdentificationType, Gender, MaritalStatus, Patient, Tutor, EPS, Etnia
)
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(IdentificationType)
admin.site.register(Gender)
admin.site.register(MaritalStatus)
admin.site.register(Tutor)
admin.site.register(EPS)
admin.site.register(Etnia)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'identification_number', 'full_name', 'user', 'birth_date'
    )
    search_fields = (
        'identification_number', 'name', 'last_name',
        'email', 'cellphone', 'user__username', 'user__email'
    )
    ordering = ('-id',)
    
    list_filter = ('user', )
    
    def full_name(self, obj):
        return f"{obj.name} {obj.last_name}"
    full_name.short_description = 'Full Name'  # Nombre de la columna
    full_name.admin_order_field = 'name'  # Ordena por 'name'

