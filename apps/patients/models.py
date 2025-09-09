from django.db import models
from apps.users.models import User

# Abstract base model with logical deletion and timestamps


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True

# Master Tables


class IdentificationType(BaseModel):
    name = models.CharField(max_length=50, verbose_name="Name")
    abbreviation = models.CharField(max_length=10, verbose_name="Abbreviation")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Identification Type"
        verbose_name_plural = "Identification Types"
        ordering = ['name']


class Gender(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Name")
    codename = models.CharField(max_length=20, verbose_name="Codeame")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"
        ordering = ['name']


class EPS(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Name")
    codename = models.CharField(max_length=120, verbose_name="Codename")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "EPS"
        verbose_name_plural = "EPSs"
        ordering = ['name']


class Etnia(BaseModel):
    name = models.CharField(max_length=60, verbose_name="Name")
    codename = models.CharField(max_length=60, verbose_name="Codename")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etnia"
        verbose_name_plural = "Etnias"
        ordering = ['name']


class MaritalStatus(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marital Status"
        verbose_name_plural = "Marital Statuses"
        ordering = ['name']


class Tutor(BaseModel):
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=150)
    cellphone = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutors"
        ordering = ['name']

# Main model: Patient


class Patient(BaseModel):
    identification_type = models.ForeignKey(
        IdentificationType, on_delete=models.PROTECT, verbose_name="Identification Type")
    identification_number = models.CharField(
        max_length=20, unique=True, verbose_name="Identification Number")
    name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender = models.ForeignKey(
        Gender, on_delete=models.PROTECT, verbose_name="Gender")
    marital_status = models.ForeignKey(
        MaritalStatus, on_delete=models.PROTECT, verbose_name="Marital Status", null=True)
    birth_date = models.DateField(verbose_name="Birth Date")
    email = models.EmailField(null=True, blank=True)
    cellphone = models.CharField(max_length=25, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    tutor = models.ForeignKey(
        Tutor, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=200, blank=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.PROTECT, blank=True)
    eps = models.ForeignKey(EPS, on_delete=models.PROTECT, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.identification_number} - {self.name} {self.last_name} | user: {self.user}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-id']
