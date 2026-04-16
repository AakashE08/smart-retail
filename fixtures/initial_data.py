import os
import sys
import subprocess
from datetime import datetime

def dump_mysql_data():
    print("Dumping MySQL data...")
    
    # MySQL connection details from your settings
    db_name = 'retail_management'
    db_user = 'root'
    db_password = 'aakash8805'
    
    # Create backup directory if it doesn't exist
    backup_dir = 'retail_management/fixtures/mysql_backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate timestamp for the backup file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'{backup_dir}/retail_management_{timestamp}.sql'
    
    # MySQL dump command
    dump_cmd = f'mysqldump -u {db_user} -p{db_password} {db_name} > {backup_file}'
    
    try:
        print(f"Creating backup: {backup_file}")
        subprocess.run(dump_cmd, shell=True, check=True)
        print("MySQL backup completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating MySQL backup: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    dump_mysql_data() 