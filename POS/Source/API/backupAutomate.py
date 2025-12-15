import os
import subprocess
import datetime
import shutil

class MySQLBackup:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.backup_dir = os.path.join(current_dir, "..", "..", "Backups")
        self.db_name = "pos"
        self.db_user = "root"
        
    def create_backup(self):
        try:
            self.backup_dir = os.path.abspath(self.backup_dir)
            os.makedirs(self.backup_dir, exist_ok=True)
            
            mysqldump = self._find_mysqldump()
            if not mysqldump:
                return False, "MySQL mysqldump not found."
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"{self.db_name}_backup_{timestamp}.sql")
            
            # Remove if exists
            if os.path.exists(backup_file):
                os.remove(backup_file)
            
            cmd = [
                mysqldump,
                f"--user={self.db_user}",
                "--host=localhost",
                self.db_name
            ]
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                process = subprocess.Popen(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True
                )
                stderr = process.communicate()
            
            if process.returncode == 0 and os.path.exists(backup_file):
                file_size = os.path.getsize(backup_file)
                if file_size > 0:
                    return True, f"Backup created: {backup_file}"
                else:
                    os.remove(backup_file)
                    return False, "Empty backup file"
            else:
                error = stderr if stderr else "Unknown error"
                return False, f"Backup failed: {error}"
                
        except Exception as e:
            return False, f"Backup error: {str(e)}"
    
    def _find_mysqldump(self):
        # Check PATH first
        found = shutil.which("mysqldump")
        if found:
            return found
        
        # Check XAMPP location
        xampp_path = r"C:\xampp\mysql\bin\mysqldump.exe"
        if os.path.exists(xampp_path):
            return xampp_path
        
        return None
