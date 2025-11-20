import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class PacienteService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_paciente(self, nombre, apellido, fecha_nacimiento, telefono, direccion):
        sql = """
        INSERT INTO Pacientes (nombre, apellido, fecha_nacimiento, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (nombre, apellido, fecha_nacimiento, telefono, direccion)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Paciente {nombre} {apellido} creado exitosamente.")
            return True
        else:
            print(f"Error al crear el paciente {nombre} {apellido}.")
            return False

    def obtener_todos_pacientes(self):
        sql = "SELECT id, nombre, apellido, fecha_nacimiento, telefono, direccion FROM Pacientes ORDER BY nombre, apellido"
        return self.db.ejecutar_consulta(sql)
    
    def obtener_paciente_por_id(self, paciente_id):
        sql = "SELECT id, nombre, apellido, fecha_nacimiento, telefono, direccion FROM Pacientes WHERE id = %s"
        return self.db.ejecutar_consulta(sql, params=(paciente_id,), fetch_one=True)
        
    def actualizar_paciente(self, paciente_id, nombre, apellido, fecha_nacimiento, telefono, direccion):
        sql = """
        UPDATE Pacientes 
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, telefono = %s, direccion = %s
        WHERE id = %s
        """
        params = (nombre, apellido, fecha_nacimiento, telefono, direccion, paciente_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Paciente ID {paciente_id} actualizado exitosamente.")
            return True
        else:
            print(f"Error al actualizar el paciente ID {paciente_id}.")
            return False
            
    def eliminar_paciente(self, paciente_id):
        sql = "DELETE FROM Pacientes WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(paciente_id,))
        
        if resultado:
            print(f"Paciente ID {paciente_id} eliminado exitosamente.")
            return True
        else:
            print(f"Error al eliminar el paciente ID {paciente_id}.")
            return False