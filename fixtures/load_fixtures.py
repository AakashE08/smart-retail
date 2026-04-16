import os
import sys
import subprocess
from datetime import datetime

def restore_mysql_data(backup_file=None):
    print("Restoring MySQL data...")
    
    # MySQL connection details from your settings
    db_name = 'retail_management'
    db_user = 'root'
    db_password = 'aakash8805'
    
    # If no backup file specified, use the most recent one
    if backup_file is None:
        backup_dir = 'retail_management/fixtures/mysql_backups'
        if not os.path.exists(backup_dir):
            print("No backup directory found!")
            return
        
        # Get the most recent backup file
        backup_files = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
        if not backup_files:
            print("No backup files found!")
            return
        
        backup_files.sort(reverse=True)
        backup_file = os.path.join(backup_dir, backup_files[0])
    
    # MySQL restore command
    restore_cmd = f'mysql -u {db_user} -p{db_password} {db_name} < {backup_file}'
    
    try:
        print(f"Restoring from backup: {backup_file}")
        subprocess.run(restore_cmd, shell=True, check=True)
        print("MySQL restore completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error restoring MySQL backup: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    # To restore from a specific backup file, pass it as an argument
    # restore_mysql_data('path/to/backup.sql')
    restore_mysql_data() 