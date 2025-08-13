# from rest_framework import viewsets, status, permissions
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound
# from .models import MedicalRecord, MedicalEpisode
# from .serializers import (
#     MedicalRecordSerializer,
#     MedicalEpisodeSerializer,
#     PatientWithRecordsSerializer
# )
# from apps.patients.models import Patient


# class MedicalRecordViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MedicalRecordSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return MedicalRecord.objects.filter(
#             is_active=True,
#             patient__user=user
#         ).select_related('patient', 'episode', 'created_by')

#     def destroy(self, request, *args, **kwargs):
#         try:
#             record = self.get_object()

#             if not record.is_active:
#                 return Response(
#                     {"detail": "This medical record is already inactive."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             record.is_active = False
#             record.save()
#             return Response(
#                 {"detail": "Medical record was deactivated successfully."},
#                 status=status.HTTP_204_NO_CONTENT
#             )

#         except MedicalRecord.DoesNotExist:
#             raise NotFound(detail="Medical record not found.")

#         except Exception as e:
#             return Response(
#                 {"detail": f"Unexpected error: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class MedicalEpisodeViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MedicalEpisodeSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return MedicalEpisode.objects.filter(
#             is_active=True,
#             patient__user=user
#         ).prefetch_related('records')


# class PatientWithRecordsViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PatientWithRecordsSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Patient.objects.filter(
#             is_active=True,
#             user=user
#         ).prefetch_related('medical_records')
