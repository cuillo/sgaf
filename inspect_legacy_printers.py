import sqlite3

legacy_db_path = r"c:\Users\SLEP IQUIQUE\Desktop\Programas\SYSSSGG\db.sqlite3"

def inspect():
    try:
        conn = sqlite3.connect(legacy_db_path)
        cursor = conn.cursor()
        
        # Check table name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'printers%'")
        tables = cursor.fetchall()
        print("Tables:", tables)
        
        if tables:
            table_name = tables[0][0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"\nColumns for {table_name}:")
            for col in columns:
                print(col)
                
            # Get data count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nTotal records: {count}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
