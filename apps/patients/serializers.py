from rest_framework import serializers
from .models import *
from datetime import date


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'name', 'cellphone', 'relationship']


class EtniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etnia
        fields = ['id', 'name']


class EPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = EPS
        fields = ['id', 'name']


class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = ['id', 'name', 'abbreviation']


class PatientSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer(required=False, allow_null=True)
    identification_type = serializers.PrimaryKeyRelatedField(
        queryset=IdentificationType.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )
    eps = serializers.PrimaryKeyRelatedField(
        queryset=EPS.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )
    etnia = serializers.PrimaryKeyRelatedField(
        queryset=Etnia.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'last_name',
            'email', 'birth_date', 'gender', 'tutor', 'address', 'religion',
            'identification_number', 'identification_type', 'marital_status', 'cellphone', 'address',
            'etnia', 'eps','profession'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_active']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.tutor:
            rep['tutor'] = TutorSerializer(instance.tutor).data
        if instance.identification_type:
            rep['identification_type'] = IdentificationTypeSerializer(
                instance.identification_type).data
        if instance.etnia:
            rep['etnia'] = EtniaSerializer(
                instance.etnia).data
        if instance.marital_status:
            rep['marital_status'] = MaritalStatusSerializer(
                instance.marital_status).data
        if instance.gender:
            rep['gender'] = GenderSerializer(
                instance.gender).data
        if instance.eps:
            rep['etnia'] = EPSSerializer(
                instance.etnia).data

        return rep

    def validate(self, attrs):
        birth_date = attrs.get("birth_date")
        tutor_data = self.initial_data.get("tutor")

        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - \
                ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18 and not tutor_data:
                raise serializers.ValidationError(
                    "El tutor es obligatorio para menores de edad.")

        return attrs

    def get_or_create_tutor(self, tutor_data):
        cellphone = tutor_data.get('cellphone')
        relationship = tutor_data.get('relationship')
        if cellphone:
            tutor, _ = Tutor.objects.get_or_create(
                cellphone=cellphone,
                relationship=relationship,
                defaults={'name': tutor_data.get('name')}
            )
            return tutor
        return None

    def create(self, validated_data):
        tutor_data = validated_data.pop('tutor', None)
        if tutor_data:
            validated_data['tutor'] = self.get_or_create_tutor(tutor_data)

        # Asignar el usuario autenticado
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        tutor_data = validated_data.pop('tutor', None)
        if tutor_data:
            if instance.tutor:
                for attr, value in tutor_data.items():
                    setattr(instance.tutor, attr, value)
                instance.tutor.save()
            else:
                validated_data['tutor'] = self.get_or_create_tutor(tutor_data)
        return super().update(instance, validated_data)


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id', 'name']
