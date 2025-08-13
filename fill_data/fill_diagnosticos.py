import django
import os

# Configuración para usar Django sin tener que ejecutarlo como un servidor
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Cambia a tu archivo de configuración
django.setup()

from your_app.models import TherapyApproach  # Cambia "your_app" al nombre de tu aplicación

def fill_therapy_approaches():
    # Lista de enfoques terapéuticos con su codename
    approaches = [
        ('Psicoanalista/Psicodinámico', 'PST/PD'),  
        ('Humanista/Existencial', 'HUM/EXIST'),    
        ('Sistémico/Familiar', 'SYS/FAM'),         
        ('Enfoque Integrativo', 'INT'),            
        ('Terapia Cognitiva de la Realidad', 'RCT'), 
        ('Terapia Cognitiva Conductual', 'RCT'), 
        ('Otro', 'otro'),
    ]

    # Iterar sobre la lista y agregar cada enfoque
    for name, codename in approaches:
        if not TherapyApproach.objects.filter(codename=codename).exists():  # Verificar si ya existe
            approach = TherapyApproach(name=name, codename=codename)
            approach.save()
            print(f"Enfoque {name} agregado correctamente con codename {codename}.")
        else:
            print(f"El enfoque {name} ya existe en la base de datos.")

if __name__ == "__main__":
    fill_therapy_approaches()
