import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from funcionarios.models import Subdireccion, Departamento, Unidad

def populate_org():
    print("Iniciando población de estructura organizacional...")
    
    # 1. Subdirecciones
    subdirecciones_data = [
        "Dirección Ejecutiva",
        "Subdirección de Planeamiento y Desarrollo Organizacional",
        "Subdirección de Gestión de Personas",
        "Subdirección de Administración y Finanzas",
        "Subdirección de Apoyo Técnico Pedagógico",
        "Subdirección de Infraestructura, Recursos y Comunicaciones"
    ]
    
    sub_map = {}
    for name in subdirecciones_data:
        sub, created = Subdireccion.objects.get_or_create(nombre=name)
        sub_map[name] = sub
        if created:
            print(f"Creada Subdirección: {name}")

    # 2. Departamentos
    depts_data = [
        ("Departamento de Gestión de Personas", "Subdirección de Gestión de Personas"),
        ("Departamento de Administración y Finanzas", "Subdirección de Administración y Finanzas"),
        ("Departamento Técnico Pedagógico", "Subdirección de Apoyo Técnico Pedagógico"),
        ("Departamento de Infraestructura y Recursos", "Subdirección de Infraestructura, Recursos y Comunicaciones")
    ]
    
    dept_map = {}
    for d_name, s_name in depts_data:
        dept, created = Departamento.objects.get_or_create(
            nombre=d_name,
            subdireccion=sub_map[s_name]
        )
        dept_map[d_name] = dept
        if created:
            print(f"Creado Departamento: {d_name}")

    # 3. Unidades
    unidades_data = [
        # SGP
        ("Unidad de Gestión de Personal", "Departamento de Gestión de Personas"),
        ("Unidad de Bienestar", "Departamento de Gestión de Personas"),
        # SAF
        ("Unidad de Finanzas", "Departamento de Administración y Finanzas"),
        ("Unidad de Tesorería", "Departamento de Administración y Finanzas"),
        ("Unidad de Abastecimiento", "Departamento de Administración y Finanzas"),
        ("Unidad de Servicios Generales", "Departamento de Administración y Finanzas"),
        ("Unidad de Informática", "Departamento de Administración y Finanzas")
    ]
    
    for u_name, d_name in unidades_data:
        u, created = Unidad.objects.get_or_create(
            nombre=u_name,
            departamento=dept_map[d_name]
        )
        if created:
            print(f"Creada Unidad: {u_name}")

    print("Población completada con éxito.")

if __name__ == "__main__":
    populate_org()
