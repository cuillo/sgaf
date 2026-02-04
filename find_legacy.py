import sqlite3

def find_legacy_data():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    print("--- FULL TABLE LIST ---")
    for t in tables:
        print(t)
        
    # Search for legacy organizational tables
    legacy_patterns = ['core', 'legacy', 'old', 'sys']
    possible_tables = []
    for t in tables:
        if any(p in t.lower() for p in legacy_patterns):
            possible_tables.append(t)
            
    print("\n--- POSSIBLE LEGACY TABLES ---")
    print(possible_tables)
    
    for t in possible_tables:
        print(f"\n--- Content of {t} (first 10) ---")
        try:
            cursor.execute(f"SELECT * FROM {t} LIMIT 10")
            print(cursor.fetchall())
        except:
            pass
            
    conn.close()

if __name__ == "__main__":
    find_legacy_data()
