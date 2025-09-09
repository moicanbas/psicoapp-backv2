from django.core.management.base import BaseCommand
import os
import django
from apps.masters.models import Cie10

# Asegúrate de que tu configuración de settings es la correcta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


class Command(BaseCommand):
    help = 'Llena la base de datos con los diagnósticos CIE-10 en la tabla Cie10'

    def handle(self, *args, **kwargs):
        disorders_cie10 = [
            # Trastornos del estado de ánimo (F30–F39)
            ('Trastorno Depresivo Mayor', 'F32'),
            ('Trastorno Bipolar I', 'F31.0'),
            ('Trastorno Bipolar II', 'F31.8'),
            ('Trastorno Ciclotímico', 'F34.0'),

            # Trastornos de ansiedad (F40–F41)
            ('Trastorno de Ansiedad Generalizada', 'F41.1'),
            ('Trastorno de Pánico', 'F41.0'),
            ('Trastorno de Ansiedad Social (Fobia Social)', 'F40.1'),
            ('Fobia Específica', 'F40.2'),
            ('Trastorno Obsesivo-Compulsivo', 'F42'),
            ('Trastorno de Estrés Postraumático', 'F43.1'),
            ('Trastorno de Ansiedad por Separación', 'F93.0'),

            # Trastornos de la conducta y control de impulsos
            ('Trastorno Disruptivo, del Control de los Impulsos y de la Conducta', 'F91'),
            ('Trastorno de la Conducta', 'F91.1'),
            ('Trastornos de la Conducta Alimentaria', 'F50'),

            # Trastornos depresivos persistentes
            ('Distimia', 'F34.1'),

            # Trastornos psicóticos (F20–F29)
            ('Esquizofrenia', 'F20'),
            ('Trastorno Psicótico Breve', 'F23.0'),
            ('Trastorno Esquizoafectivo / Esquizofreniforme', 'F25'),
            ('Trastorno Psicótico Inducido por Sustancias', 'F19.5'),
            ('Trastorno Psicótico debido a una Condición Médica', 'F06.2'),

            # Trastornos de la personalidad (F60–F61)
            ('Trastorno de la Personalidad Antisocial', 'F60.2'),
            ('Trastorno de la Personalidad Narcisista', 'F60.8'),
            ('Trastorno de la Personalidad Histriónica', 'F60.4'),
            ('Trastorno de la Personalidad Paranoide', 'F60.0'),
            ('Trastorno de la Personalidad Esquizoide', 'F60.1'),
            ('Trastorno de la Personalidad Esquizotípica', 'F21'),
            ('Trastorno de la Personalidad Dependiente', 'F60.7'),
            ('Trastorno de la Personalidad Evitativa (Ansiosa)', 'F60.6'),
            ('Trastorno de la Personalidad Obsesivo-Compulsiva', 'F60.5'),

            # Trastornos disociativos (F44)
            ('Trastorno de Identidad Disociativa', 'F44.81'),
            ('Amnesia Disociativa', 'F44.0'),
            ('Trastorno Disociativo de la Personalidad', 'F44.81'),
            ('Trastorno de Despersonalización', 'F48.1'),

            # Trastornos somatomorfos (F45–F48)
            ('Trastorno de Conversión', 'F44.4'),
            ('Trastorno Somatomorfo', 'F45.9'),
            ('Trastorno Facticio', 'F68.1'),
            ('Trastorno de Somatización', 'F45.0'),

            # Trastornos del sueño (F51, G47)
            ('Insomnio', 'F51.0'),
            ('Apnea del Sueño', 'G47.3'),
            ('Narcolepsia', 'G47.4'),
            ('Parasomnias', 'F51.3'),
            ('Trastorno del Sueño REM', 'G47.52'),
            ('Trastorno del Sueño No REM', 'F51.9'),

            # Trastornos relacionados con sustancias (F10–F19)
            ('Trastorno por Consumo de Alcohol', 'F10.2'),
            ('Trastorno por Consumo de Sustancias', 'F19.2'),
            ('Dependencia de Sustancias', 'F19.2'),
            ('Trastorno por Consumo de Cannabis', 'F12.2'),
            ('Trastorno por Consumo de Estimulantes', 'F15.2'),
            ('Trastorno por Consumo de Opioides', 'F11.2'),

            # Trastornos de la conducta alimentaria
            ('Anorexia Nerviosa', 'F50.0'),
            ('Bulimia Nerviosa', 'F50.2'),
            ('Trastorno por Atracones', 'F50.8'),

            # Trastornos neurocognitivos (Demencias, F00–F03, G30–G31)
            ('Trastorno Neurocognitivo Mayor (Demencia)', 'F03'),
            ('Enfermedad de Alzheimer', 'F00'),
            ('Demencia Vascular', 'F01'),
            ('Trastorno Neurocognitivo debido a la Enfermedad de Parkinson', 'F02.3'),

            # Trastornos del desarrollo (F80–F89, F70–F79)
            ('Trastorno del Espectro Autista', 'F84.0'),
            ('Síndrome de Asperger', 'F84.5'),
            ('Trastorno del Lenguaje', 'F80'),
            ('Trastorno del Aprendizaje (Específicos)', 'F81'),
            ('Trastorno de Déficit de Atención e Hiperactividad', 'F90.0'),
            ('Trastorno del Desarrollo Intelectual (Retraso mental)', 'F70'),
            ('Trastorno de la Coordinación Motora', 'F82'),

            # Trastornos de la sexualidad y género
            ('Trastorno de la Conducta Sexual', 'F52.9'),
            ('Trastorno de la Identidad de Género', 'F64'),
            ('Disfunción Sexual', 'F52'),

            # Trastornos de la conducta disruptiva
            ('Trastorno de Oposición Desafiante', 'F91.3'),
            ('Trastorno Disruptivo', 'F91'),

            # Otros trastornos
            ('Trastorno de la Conducta Desafiante', 'F91.3'),
            ('Trastorno de Ansiedad por Separación', 'F93.0'),
            ('Trastorno del Comportamiento de Control de Impulsos', 'F63'),
            ('Trastorno de la Personalidad Esquizoide', 'F60.1'),
        ]

        for name, code in disorders_cie10:
            Cie10.objects.get_or_create(name=name, code=code)

        self.stdout.write(self.style.SUCCESS('✅ Datos CIE-10 cargados correctamente en la base de datos.'))
