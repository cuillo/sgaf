import json

def search_utf16_backup():
    filename = 'data_backup_v2.json'
    print(f"\n=== Searching in {filename} (UTF-16) ===")
    try:
        with open(filename, 'r', encoding='utf-16') as f:
            data = json.load(f)
            # Find models starting with core or having org names
            org_items = []
            for item in data:
                model = item.get('model', '').lower()
                if any(x in model for x in ['subdireccion', 'departamento', 'unidad', 'area']):
                    org_items.append(item)
            
            print(f"Found {len(org_items)} items.")
            for item in org_items:
                print(json.dumps(item, indent=2))
                
            # Also check a few items to see what models exist
            print("\nSample models found:")
            print(list(set(item.get('model') for item in data[:50])))
            
    except Exception as e:
        print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    search_utf16_backup()
