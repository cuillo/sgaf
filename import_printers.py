import sqlite3
import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from impresoras.models import Printer

legacy_db_path = r"c:\Users\SLEP IQUIQUE\Desktop\Programas\SYSSSGG\db.sqlite3"

def import_data():
    if not os.path.exists(legacy_db_path):
        print(f"Error: Database not found at {legacy_db_path}")
        return

    conn = sqlite3.connect(legacy_db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("Importing printers...")
    cursor.execute("SELECT * FROM printers_printer")
    rows = cursor.fetchall()

    for row in rows:
        try:
            # Check if printer already exists by IP or Name
            if Printer.objects.filter(ip_address=row['ip_address']).exists():
                print(f"Skipping {row['name']} ({row['ip_address']}) - Already exists")
                continue

            printer = Printer(
                name=row['name'],
                location=row['location'],
                floor=row['floor'],
                ip_address=row['ip_address'],
                type=row['type'],
                community=row['community'],
                snmp_port=row['snmp_port'],
                enabled=bool(row['enabled']),
                notes=row['notes'],
                # Last status fields
                last_check=row['last_check'],
                last_ok=bool(row['last_ok']) if row['last_ok'] is not None else None,
                last_message=row['last_message'],
                last_black=row['last_black'],
                last_cyan=row['last_cyan'],
                last_magenta=row['last_magenta'],
                last_yellow=row['last_yellow'],
                serial_number=row['serial_number'],
                last_connected=bool(row['last_connected']) if row['last_connected'] is not None else None,
                last_woke=bool(row['last_woke']) if row['last_woke'] is not None else None,
            )
            
            # Handle JSON field for errors
            if row['last_errors']:
                try:
                    printer.last_errors = json.loads(row['last_errors'])
                except:
                    printer.last_errors = []
            
            printer.save()
            print(f"Imported {printer.name}")

        except Exception as e:
            print(f"Error importing {row['name']}: {e}")

    conn.close()
    print("Done.")

if __name__ == "__main__":
    import_data()
