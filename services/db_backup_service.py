import os
import subprocess
from datetime import datetime

from db.config import DB_CONFIG 

class DBBackupService:
    def __init__(self):
        self.backup_dir = "db_backups"
        self.MYSQL_BIN_PATH = "/opt/lampp/bin/" 
        
        print(f"Configuración de XAMPP: {self.MYSQL_BIN_PATH}")

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
    def _build_command_base(self, executable, db_name, extra_args=None):
        """Construye la lista de comandos base para mysql/mysqldump."""
        command = [
            os.path.join(self.MYSQL_BIN_PATH, executable),
            f'-h{DB_CONFIG["host"]}',
            f'-u{DB_CONFIG["user"]}',
        ]
        
        password = DB_CONFIG['password']
        if password:
            command.append(f'-p{password}')
            
        if extra_args:
            command.extend(extra_args)
            
        command.append(db_name)
        return command

    def crear_respaldo(self):
        """Genera un archivo .sql de respaldo de la base de datos usando mysqldump."""
        db_name = DB_CONFIG['database']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.backup_dir, f"{db_name}_backup_{timestamp}.sql")
        
        mysqldump_executable = os.path.join(self.MYSQL_BIN_PATH, 'mysqldump')
        
        print(f"--- INICIO DE RESPALDO DE BD ---")
        print(f"Base de datos: '{db_name}'")
        
        extra_args = ['--single-transaction']
        command = self._build_command_base('mysqldump', db_name, extra_args)
        # Ocultamos la contraseña en el log por seguridad
        command_log = ' '.join(command).replace(DB_CONFIG.get('password', ''), '******')
        print(f"Comando a ejecutar: {command_log}")

        try:
            with open(file_path, 'w') as f:
                print("Iniciando subprocess.run para mysqldump con timeout de 300s...")
                result = subprocess.run(
                    command, 
                    stdout=f, 
                    stderr=subprocess.PIPE, 
                    check=True, 
                    text=True, 
                    close_fds=True, 
                    timeout=300
                )
            
            print(f"--- RESPALDO CREADO EXITOSAMENTE ---")
            return True, file_path
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al ejecutar mysqldump (Código: {e.returncode}):\n{e.stderr.strip()}"
            print(f"ERROR: subprocess.CalledProcessError detectado.")
            print(error_msg)
            return False, error_msg
        except FileNotFoundError:
            print(f"ERROR: FileNotFoundError detectado.")
            return False, f"Error: '{mysqldump_executable}' no encontrado. Verifique la ruta de XAMPP."
        except subprocess.TimeoutExpired:
            error_msg = "Error de respaldo: El proceso mysqldump excedió el tiempo límite (300s). Posiblemente un bloqueo."
            print(f"ERROR: subprocess.TimeoutExpired detectado.")
            return False, error_msg
        except Exception as e:
            error_msg = f"Ocurrió un error inesperado durante el respaldo: {e}"
            print(f"ERROR: Excepción inesperada: {e}")
            return False, error_msg

    def restaurar_respaldo(self, file_path):
        """Restaura la base de datos a partir de un archivo .sql usando el comando mysql."""
        db_name = DB_CONFIG['database']
        mysql_executable = os.path.join(self.MYSQL_BIN_PATH, 'mysql')

        print(f"--- INICIO DE RESTAURACIÓN DE BD ---")
        print(f"Base de datos: '{db_name}'")
        print(f"Archivo de respaldo: {file_path}")

        if not os.path.exists(file_path):
            print(f"ERROR: Archivo de respaldo no encontrado: {file_path}")
            return False, f"Archivo de respaldo no encontrado: {file_path}"
        
        command = self._build_command_base('mysql', db_name)
        command_log = ' '.join(command).replace(DB_CONFIG.get('password', ''), '******')
        print(f"Comando a ejecutar: {command_log}")
        
        try:
            with open(file_path, 'r') as f:
                print("Iniciando subprocess.run para mysql con timeout de 300s...")
                
                # MODIFICACIÓN CLAVE: Capturamos STDOUT para evitar deadlocks
                result = subprocess.run(
                    command, 
                    stdin=f, 
                    stdout=subprocess.PIPE, # <-- CAPTURA DE SALIDA ESTÁNDAR
                    stderr=subprocess.PIPE, 
                    check=True, 
                    text=True, 
                    close_fds=True,
                    timeout=300
                )
            
            # Imprimimos cualquier salida para diagnóstico, incluso si fue exitosa
            if result.stdout:
                print(f"SALIDA STDOUT (EXITOSA): \n{result.stdout.strip()}")

            print(f"--- RESTAURACIÓN FINALIZADA EXITOSAMENTE ---")
            return True, f"Base de datos restaurada desde {file_path}"
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Error al ejecutar el comando mysql (Código: {e.returncode}):\n{e.stderr.strip()}"
            print(f"ERROR: subprocess.CalledProcessError detectado.")
            print(error_msg)
            return False, error_msg
        except FileNotFoundError:
            print(f"ERROR: FileNotFoundError detectado.")
            return False, f"Error: '{mysql_executable}' no encontrado. Verifique la ruta de XAMPP."
        except subprocess.TimeoutExpired:
            error_msg = "Error de restauración: El proceso mysql excedió el tiempo límite (300s). Esto indica un bloqueo grave en la ejecución de la consulta."
            print(f"ERROR: subprocess.TimeoutExpired detectado.")
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Ocurrió un error inesperado durante la restauración: {e}"
            print(f"ERROR: Excepción inesperada: {e}")
            return False, error_msg