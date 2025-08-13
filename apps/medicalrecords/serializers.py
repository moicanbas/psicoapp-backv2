from rest_framework import serializers
from .models import MedicalRecord, MedicalEpisode
from apps.patients.models import Patient
from django.utils import timezone


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        exclude = ['created_by', 'is_active']
        read_only_fields = ['episode']

    def validate(self, data):
        patient = data['patient']
        now = timezone.now()
        requested_type = data.get('type_of_visit')
        recent_record = MedicalRecord.objects.filter(
            patient=patient,
            is_active=True
        ).order_by('-created_at').first()

        # 🔍 No registros anteriores
        if not recent_record:
            if requested_type != MedicalRecord.NEW_DIAGNOSIS:
                raise serializers.ValidationError(
                    {"type_of_visit": "First medical record must be 'new_diagnosis'."}
                )
            data['episode'] = MedicalEpisode.objects.create(patient=patient)
            return data

        # 🕒 Verificamos tiempo desde el último
        days_since_last = (now - recent_record.created_at).days

        if days_since_last > 90:
            # Han pasado más de 3 meses → debe ser nueva
            if requested_type != MedicalRecord.NEW_DIAGNOSIS:
                raise serializers.ValidationError({
                    "type_of_visit": "More than 3 months since last record. This must be a 'new_diagnosis'."
                })
            data['episode'] = MedicalEpisode.objects.create(patient=patient)
        else:
            # Dentro de 3 meses → debe ser seguimiento
            if requested_type != MedicalRecord.FOLLOW_UP:
                raise serializers.ValidationError({
                    "type_of_visit": "A recent medical record exists. This must be a 'follow_up'."
                })
            data['episode'] = recent_record.episode

        # 🔁 Validación de duplicados exactos
        fields_to_check = [
            'reason_for_visit', 'personal_history', 'family_history',
            'physical_exam', 'diagnosis', 'treatment_plan',
            'prescriptions', 'recommendations'
        ]
        is_duplicate = all(
            getattr(recent_record, field) == data.get(field)
            for field in fields_to_check
        )
        if is_duplicate:
            raise serializers.ValidationError(
                "Duplicate medical record not allowed.")

        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class MedicalEpisodeSerializer(serializers.ModelSerializer):
    records = MedicalRecordSerializer(
        many=True, read_only=True, source='records')

    class Meta:
        model = MedicalEpisode
        fields = ['id', 'patient', 'created_at', 'records']


class PatientWithRecordsSerializer(serializers.ModelSerializer):
    medical_records = MedicalRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name',
                  'identification_number', 'medical_records']
