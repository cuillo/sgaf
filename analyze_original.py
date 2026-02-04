import json

def list_all_models_in_original_backup():
    filename = 'data_backup.json'
    print(f"\n=== Analyzing {filename} (Unicode) ===")
    try:
        with open(filename, 'r', encoding='utf-16') as f:
            data = json.load(f)
            models = {}
            for item in data:
                m = item.get('model')
                models[m] = models.get(m, 0) + 1
            
            print("Models found in backup:")
            for m, count in sorted(models.items()):
                print(f"- {m}: {count} items")
                
            # Specifically look for anything with "sub", "dep", "uni"
            print("\nOrganizational Items Found:")
            for item in data:
                m = item.get('model').lower()
                if any(x in m for x in ['sub', 'dep', 'uni']):
                    print(json.dumps(item, indent=2))
                    
    except Exception as e:
        print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    list_all_models_in_original_backup()
