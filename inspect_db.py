import sqlite3
import json

def inspect_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables: {tables}")
    
    # Check for organizational tables
    org_tables = [t for t in tables if 'subdireccion' in t.lower() or 'departamento' in t.lower() or 'unidad' in t.lower()]
    print(f"Organizational tables: {org_tables}")
    
    for table in org_tables:
        print(f"\n--- Content of {table} ---")
        try:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error reading {table}: {e}")
            
    # Also check if there's any data in 'funcionarios_funcionario'
    if 'funcionarios_funcionario' in tables:
        print("\n--- Check funcionarios_funcionario for associations ---")
        cursor.execute("SELECT subdireccion_id, departamento_id, unidad_id FROM funcionarios_funcionario LIMIT 5")
        print(cursor.fetchall())

    conn.close()

if __name__ == "__main__":
    inspect_db()
