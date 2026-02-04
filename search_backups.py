import json
import re

def search_backups():
    files = ['data_backup_v2_fixed.json', 'data_backup_fixed.json']
    keywords = ['subdireccion', 'departamento', 'unidad', 'area', 'subdirección']
    
    for filename in files:
        print(f"\n=== Searching in {filename} ===")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                models = set()
                found_items = []
                
                for item in data:
                    model = item.get('model', '')
                    models.add(model)
                    
                    # Search in fields
                    fields_str = str(item.get('fields', {})).lower()
                    if any(key in fields_str for key in keywords) or any(key in model.lower() for key in keywords):
                        found_items.append(item)
                
                print(f"Found {len(found_items)} items related to organizational structure.")
                print(f"Models present in backup: {list(models)}")
                
                # Print sample organizational items
                for item in found_items[:20]:
                    print(json.dumps(item, indent=2))
                    
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    search_backups()
