import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from funcionarios.models import Subdireccion, Departamento, Unidad

def reset_and_sync_org():
    print("Iniciando limpia y sincronización total desde SYSSSGG...")
    
    # 1. Limpieza total (Orden inverso por FKs)
    Unidad.objects.all().delete()
    Departamento.objects.all().delete()
    Subdireccion.objects.all().delete()
    print("Tablas organizacionales limpiadas.")

    # 2. Subdirecciones (ID, Nombre)
    subs_data = [
        (1, 'Subdirección de Administración y Finanzas'),
        (2, 'Subdirección de Infraestructura y Mantenimiento'),
        (3, 'Subdirección de Planificación y Control de Gestión'),
        (4, 'Subdirección de Gestión de Personas'),
        (5, 'Subdirección de Apoyo Técnico Pedagógico'),
        (6, 'Dirección Ejecutiva'),
    ]
    
    sub_map = {}
    for sid, name in subs_data:
        sub = Subdireccion.objects.create(id=sid, nombre=name)
        sub_map[sid] = sub
        print(f"Subdirección creada: {name} (ID: {sid})")

    # 3. Departamentos (ID, Nombre, Subid)
    depts_data = [
        (16, 'Mejora Continua', 5),
        (17, 'Acompañamiento Pedagógico', 5),
        (18, 'Monitoreo y Datos', 5),
        (19, 'Desarrollo Integral', 5),
        (20, 'Contabilidad y Finanzas', 1),
        (21, 'Compras y Logística', 1),
        (22, 'Coordinación de SSGG, Operaciones y Soporte TI', 1),
        (23, 'Gestión y Desarrollo de Personas', 4),
        (24, 'Remuneraciones', 4),
        (25, 'Infraestructura', 2),
        (26, 'Mantenimiento', 2),
        (27, 'Innovación Educativa', 5),
        (28, 'Auditoría y Aseguramiento de Calidad', 6),
        (29, 'Gabinete', 6),
        (30, 'Vinculación, Participación y Comunicaciones', 6),
        (31, 'Jurídico y Transparencia', 6),
    ]
    
    dept_map = {}
    for did, name, sid in depts_data:
        dept = Departamento.objects.create(id=did, nombre=name, subdireccion=sub_map[sid])
        dept_map[did] = dept
        print(f"Departamento creado: {name} (ID: {did})")

    # 4. Unidades (ID, Nombre, Deptid)
    unidades_data = [
        (1, 'Establecimientos Educacionales', 17),
        (2, 'Jardines Infantiles', 17),
        (3, 'Inclusión', 17),
        (4, 'Desarrollo Profesional Integral', 16),
        (5, 'Plataformas', 16),
        (6, 'Monitoreo de Información', 18),
        (7, 'Programas Educativos', 18),
        (8, 'Convivencia Escolar', 19),
        (9, 'Trayectoria', 19),
        (10, 'Servicios Generales', 22),
        (11, 'Operaciones', 22),
        (12, 'Soporte TI', 22),
        (13, 'Bodega y Logística', 21),
        (14, 'Compras', 21),
        (15, 'Inventario', 21),
        (16, 'Contabilidad y Conciliaciones', 20),
        (17, 'Control Presupuestario y Subvenciones', 20),
        (18, 'Tesorería', 20),
        (19, 'Rendiciones', 20),
        (20, 'Comunicaciones', 30),
    ]
    
    for uid, name, did in unidades_data:
        Unidad.objects.create(id=uid, nombre=name, departamento=dept_map[did])
        print(f"Unidad creada: {name} (ID: {uid})")

    print("\nSincronización total completada con éxito. La data ahora cuadra con SYSSSGG.")

if __name__ == "__main__":
    reset_and_sync_org()
