from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Patient, IdentificationType, Gender, MaritalStatus, EPS, Etnia
from .serializers import (
    PatientSerializer, 
    IdentificationTypeSerializer, 
    GenderSerializer, 
    MaritalStatusSerializer, 
    EtniaSerializer, 
    EPSSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer

    def get_queryset(self):
        user = self.request.user
        return Patient.objects.filter(is_active=True, user=user)

    def destroy(self, request, *args, **kwargs):
        try:
            patient = self.get_object()

            if not patient.is_active:
                return Response(
                    {"detail": "Patient is already inactive."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            patient.is_active = False
            patient.save()
            return Response(
                {"detail": "Patient was deactivated successfully."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Patient.DoesNotExist:
            raise NotFound(detail="Patient not found.")

        except Exception as e:
            return Response(
                {"detail": f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IdentificationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = IdentificationType.objects.filter(is_active=True)
    serializer_class = IdentificationTypeSerializer


class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Gender.objects.filter(is_active=True)
    serializer_class = GenderSerializer


class MaritalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = MaritalStatus.objects.filter(is_active=True)
    serializer_class = MaritalStatusSerializer


class EPSViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EPS.objects.filter(is_active=True)
    serializer_class = EPSSerializer


class EtniaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Etnia.objects.filter(is_active=True)
    serializer_class = EtniaSerializer
