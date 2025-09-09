# Cambia "your_app" al nombre de tu aplicación
import os
import django

# Asegúrate de que tu configuración de settings es la correcta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Ahora puedes importar tus modelos
from apps.patients.models import EPS, Etnia, Gender, MaritalStatus, IdentificationType

def add_to_database(items, model, field_name, field_codename):
    """
    Función recursiva para agregar elementos a la base de datos si no existen.
    
    :param items: lista de diccionarios con 'name' y 'codename' (o solo 'name' para algunos casos).
    :param model: modelo de la base de datos donde se almacenarán los elementos.
    :param field_name: nombre del campo del modelo para almacenar el nombre.
    :param field_codename: nombre del campo del modelo para almacenar el codename.
    """
    if not items:
        return  # Caso base de la recursión: lista vacía, se detiene

    item = items[0]  # Toma el primer elemento de la lista

    # Verifica si el 'codename' ya existe en la base de datos
    if field_codename:
        if not model.objects.filter(codename=item[field_codename]).exists():
            new_item = model(**{field_name: item['name'], field_codename: item['codename']})
            new_item.save()
            print(f"{item['name']} agregado correctamente con codename {item['codename']}.")
        else:
            print(f"{item['name']} ya existe en la base de datos.")
    else:
        # Solo agrega 'name', para aquellos casos que no tienen codename
        if not model.objects.filter(name=item['name']).exists():
            new_item = model(**{field_name: item['name']})
            new_item.save()
            print(f"{item['name']} agregado correctamente.")
        else:
            print(f"{item['name']} ya existe en la base de datos.")
    
    add_to_database(items[1:], model, field_name, field_codename)  # Llamada recursiva para el siguiente elemento


def fill_therapy_approaches():
    # Lista de enfoques terapéuticos con su codename
    eps_array = [
        {"name": "Nueva EPS", "codename": "nueva_eps"},
        {"name": "SURA", "codename": "sura"},
        {"name": "Sanitas", "codename": "sanitas"},
        {"name": "Coomeva", "codename": "coomeva"},
        {"name": "Compensar", "codename": "compensar"},
        {"name": "EPS Famisanar", "codename": "famisanar"},
        {"name": "Medimás", "codename": "medimas"},
        {"name": "Alianza Sanitas", "codename": "alianza_sanitas"},
        {"name": "Colpatria", "codename": "colpatria"},
        {"name": "Cafesalud", "codename": "cafesalud"},
        {"name": "EPS Sanitas", "codename": "sanitas_eps"},
        {"name": "Comfenalco", "codename": "comfenalco"},
        {"name": "Médico Coomeva", "codename": "medico_coomeva"},
        {"name": "Cruz Blanca", "codename": "cruz_blanca"},
        {"name": "Famisanar", "codename": "famisanar"},
        {"name": "Convida", "codename": "convida"},
        {"name": "Salud Total", "codename": "salud_total"},
        {"name": "EPS Inder", "codename": "eps_inder"},
        {"name": "Epsax", "codename": "epsax"},
        {"name": "Pijaosalud", "codename": "pijaosalud"},
        {"name": "Medimás EPS", "codename": "medimas_eps"},
        {"name": "EPS Sanitas", "codename": "eps_sanitas"},
        {"name": "Coosalud", "codename": "coosalud"},
        {"name": "Salud Vida", "codename": "salud_vida"},
        {"name": "EPS Mía", "codename": "eps_mia"},
        {"name": "Comfama", "codename": "comfama"},
        {"name": "Emssanar", "codename": "emssanar"},
        {"name": "Savia Salud", "codename": "savia_salud"},
        {"name": "Política Nacional de EPS", "codename": "politica_nacional_eps"},
        {"name": "Magisterio", "codename": "magisterio"},
        {"name": "Otra", "codename": "otra"},
    ]

    etnias_colombia = [
        {"name": "Caucásica", "codename": "caucasian"},
        {"name": "Afrocolombiana", "codename": "afrocolombian"},
        {"name": "Indígena", "codename": "indigenous"},
        {"name": "Mestiza", "codename": "mestizo"},
        {"name": "Raizal", "codename": "raizal"},
        {"name": "Palenquero", "codename": "palenquero"},
        {"name": "Ninguna", "codename": "none"}
    ]

    genders = [
        {"name": "Masculino", "codename": "M"},
        {"name": "Femenino", "codename": "F"},
        {"name": "No binario", "codename": "NB"},
        {"name": "Otro", "codename": "O"}
    ]

    marital_status = [
        {"name": "Soltero/a"},
        {"name": "Casado/a"},
        {"name": "Divorciado/a"},
        {"name": "Viudo/a"},
        {"name": "Unión libre"},
        {"name": "Separado/a"}
    ]

    identification_types = [
        {"name": "Cédula de ciudadanía", "abbreviation": "CC"},
        {"name": "Cédula de extranjería", "abbreviation": "CE"},
        {"name": "Pasaporte", "abbreviation": "PSP"},
        {"name": "Tarjeta de identidad", "abbreviation": "TI"},
        {"name": "NIT", "abbreviation": "NIT"}
    ]
        
        # Iterar sobre la lista y agregar cada enfoque
        
    add_to_database(eps_array, EPS, 'name', 'codename')
    add_to_database(etnias_colombia, Etnia, 'name', 'codename')
    add_to_database(genders, Gender, 'name', 'codename')
    add_to_database(marital_status, MaritalStatus, 'name', None)
    add_to_database(identification_types, IdentificationType, 'name', 'abbreviation')


if __name__ == "__main__":
    fill_therapy_approaches()
