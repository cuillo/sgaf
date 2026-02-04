import sqlite3
import os

legacy_db_path = r"c:\Users\SLEP IQUIQUE\Desktop\Programas\SYSSSGG\db.sqlite3"

def extract_org_data():
    if not os.path.exists(legacy_db_path):
        print(f"Error: Database not found at {legacy_db_path}")
        return
    
    conn = sqlite3.connect(legacy_db_path)
    cursor = conn.cursor()
    
    # 1. Subdirecciones
    print("--- SUBDIRECCIONES ---")
    cursor.execute("SELECT id, nombre FROM funcionarios_subdireccion")
    subdirecciones = cursor.fetchall()
    for row in subdirecciones:
        print(row)
        
    # 2. Departamentos
    print("\n--- DEPARTAMENTOS ---")
    cursor.execute("SELECT id, nombre, subdireccion_id FROM funcionarios_departamento")
    departamentos = cursor.fetchall()
    for row in departamentos:
        print(row)
        
    # 3. Unidades
    print("\n--- UNIDADES ---")
    cursor.execute("SELECT id, nombre, departamento_id FROM funcionarios_unidad")
    unidades = cursor.fetchall()
    for row in unidades:
        print(row)
        
    conn.close()

if __name__ == "__main__":
    extract_org_data()
