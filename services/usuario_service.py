import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class UsuarioService:
    def __init__(self):
        self.db = ConexionDB()

    def autenticar_usuario(self, nombre_usuario, contrasena):
        sql = "SELECT id, nombre_completo, rol, contrasena FROM Usuarios WHERE nombre_usuario = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(nombre_usuario,), fetch_one=True)
        
        if resultado:
            id_usuario, nombre_completo, rol, contrasena_db = resultado
            
            if contrasena == contrasena_db:
                print(f"Login exitoso para {nombre_usuario} ({rol})")
                return (id_usuario, nombre_completo, rol)
            else:
                print(f"Fallo de autenticación: Contraseña incorrecta para {nombre_usuario}.")
                return False
        else:
            print(f"Fallo de autenticación: Usuario '{nombre_usuario}' no encontrado.")
            return False

    def crear_usuario(self, nombre_usuario, contrasena, nombre_completo, rol):
        sql = """
        INSERT INTO Usuarios (nombre_usuario, contrasena, nombre_completo, rol)
        VALUES (%s, %s, %s, %s)
        """
        
        params = (nombre_usuario, contrasena, nombre_completo, rol)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Usuario '{nombre_usuario}' creado exitosamente.")
            return True
        else:
            print(f"Error al crear el usuario '{nombre_usuario}'.")
            return False
            
    def obtener_todos_usuarios(self):
        sql = "SELECT id, nombre_usuario, nombre_completo, rol FROM Usuarios"
        return self.db.ejecutar_consulta(sql)