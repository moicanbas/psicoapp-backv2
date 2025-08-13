# from django.db import models
# from apps.patients.models import Patient, BaseModel
# from django.conf import settings

# class TherapyApproach(models.Model):
#     name = models.CharField(max_length=100)
#     codename = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return f"{self.name} ({self.codename})"

#     class Meta:
#         verbose_name = "Therapy Approach"
#         verbose_name_plural = "Therapy Approaches"

# class PsychologicalDisorder(models.Model):
#     name = models.CharField(max_length=255)
#     cie_code = models.CharField(max_length=10, unique=True)

#     def __str__(self):
#         return f"{self.name} ({self.cie_code})"

#     class Meta:
#         verbose_name = "Psychological Disorder"
#         verbose_name_plural = "Psychological Disorders"

# class MedicalEpisode(BaseModel):
#     patient = models.ForeignKey(
#         Patient, on_delete=models.CASCADE, related_name="episodes")

#     def __str__(self):
#         return f"Episode for {self.patient.full_name} - {self.created_at.strftime('%Y-%m-%d')}"

# class Treatment(BaseModel):
#     name = models.CharField(max_length=100, unique=True)
#     codename = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return f"{self.name} ({self.codename})"

#     class Meta:
#         verbose_name = "Treatment"
#         verbose_name_plural = "Treatments"

# class MedicalRecord(BaseModel):
#     FOLLOW_UP = 'follow_up'
#     NEW_DIAGNOSIS = 'new_diagnosis'

#     TYPE_OF_VISIT_CHOICES = [
#         (FOLLOW_UP, 'Follow-up'),
#         (NEW_DIAGNOSIS, 'New Diagnosis'),
#     ]

#     patient = models.ForeignKey(
#         Patient, on_delete=models.CASCADE, related_name="medical_records")
#     episode = models.ForeignKey(
#         MedicalEpisode, on_delete=models.SET_NULL, null=True, related_name="records")

#     # Existing fields
#     reason_for_visit = models.TextField()
#     initial_reaction = models.TextField(blank=True)
#     history_of_present_illness = models.TextField(
#         verbose_name="History of Present Illness", 
#         help_text="Describe the current symptoms and course of the patient's illness."
#     )
#     psychological_disorder = models.ForeignKey(PsychologicalDisorder, on_delete=models.CASCADE)
#     physical_exam = models.TextField(blank=True)
#     therapy_approach = models.ForeignKey(TherapyApproach, on_delete=models.CASCADE)
#     type_of_visit = models.CharField(
#         max_length=20, choices=TYPE_OF_VISIT_CHOICES, default=NEW_DIAGNOSIS)
    
#     # New fields based on the list
#     family_nucleus = models.TextField(verbose_name="Current Family Nucleus", blank=True)
#     personal_and_family_history = models.TextField(verbose_name="Personal and Family History", blank=True)
#     daily_activities = models.TextField(verbose_name="Daily Activities", blank=True)
#     visual_contact = models.TextField(verbose_name="Visual Contact", blank=True)
#     verbal_contact = models.TextField(verbose_name="Verbal Contact", blank=True)
#     orientation = models.TextField(verbose_name="Orientation", blank=True)
#     attention = models.TextField(verbose_name="Attention", blank=True)
#     present_thoughts_ideas = models.TextField(verbose_name="Present Thoughts/Types of Ideas", blank=True)
#     tendencies = models.TextField(verbose_name="Tendencies", blank=True)
#     memory = models.TextField(verbose_name="Memory", blank=True)
#     language = models.TextField(verbose_name="Language", blank=True)
#     affect = models.TextField(verbose_name="Affect", blank=True)
#     behavior = models.TextField(verbose_name="Behavior", blank=True)
#     sensoperception = models.TextField(verbose_name="Sensoperception", blank=True)
#     religious_beliefs = models.TextField(verbose_name="Religious Beliefs", blank=True)
#     couple_interaction = models.TextField(verbose_name="Couple Interaction", blank=True)
#     support_network = models.TextField(verbose_name="Support Network", blank=True)
#     insight = models.TextField(verbose_name="Insight", blank=True)
#     social_interaction = models.TextField(verbose_name="Social Interaction", blank=True)
#     family_interaction = models.TextField(verbose_name="Family Interaction", blank=True)
#     laboral_interaction = models.TextField(verbose_name="Laboral Interaction", blank=True)
#     couple_interaction2 = models.TextField(verbose_name="Couple Interaction (2)", blank=True)  # Duplicated field renamed
#     analysis_and_intervention = models.TextField(verbose_name="Analysis and Intervention", blank=True)
#     diagnostic_impression = models.TextField(verbose_name="Diagnostic Impression", blank=True)
#     treatment = models.ForeignKey(
#         Treatment, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_records"
#     )
#     treatment_exist = models.BooleanField(default=False)
#     treatment_current = models.BooleanField(default=False)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.patient.full_name} - {self.created_at.strftime('%Y-%m-%d')} ({self.type_of_visit})"

#     class Meta:
#         ordering = ['-created_at']

# acompañante
# Ocupación 
# Estado civil 
# Eps 
# Edad
# Religión 
# Sexo 
# Etnia 
# Parentesco