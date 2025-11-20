import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class EspecialidadService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_especialidad(self, nombre):
        """Inserta una nueva especialidad."""
        sql = "INSERT INTO Especialidades (nombre_especialidad) VALUES (%s)"
        params = (nombre,)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Especialidad '{nombre}' creada exitosamente.")
            return True
        else:
            print(f"Error al crear la especialidad '{nombre}'.")
            return False

    def obtener_todas_especialidades(self):
        """Retorna todas las especialidades (ID y Nombre)."""
        sql = "SELECT id, nombre_especialidad FROM Especialidades ORDER BY nombre_especialidad"
        
        return self.db.ejecutar_consulta(sql)
        
    def obtener_especialidad_por_id(self, especialidad_id):
        """Retorna una especialidad específica por su ID."""
        sql = "SELECT id, nombre_especialidad FROM Especialidades WHERE id = %s"
        return self.db.ejecutar_consulta(sql, params=(especialidad_id,), fetch_one=True)
        
    def actualizar_especialidad(self, especialidad_id, nuevo_nombre):
        """Actualiza el nombre de una especialidad existente."""
        sql = "UPDATE Especialidades SET nombre_especialidad = %s WHERE id = %s"
        params = (nuevo_nombre, especialidad_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Especialidad ID {especialidad_id} actualizada a '{nuevo_nombre}'.")
            return True
        else:
            print(f"Error al actualizar la especialidad ID {especialidad_id}.")
            return False
            
    def eliminar_especialidad(self, especialidad_id):
        """Elimina una especialidad por su ID."""
        sql = "DELETE FROM Especialidades WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(especialidad_id,))
        
        if resultado:
            print(f"Especialidad ID {especialidad_id} eliminada exitosamente.")
            return True
        else:
            print(f"Error al eliminar la especialidad ID {especialidad_id}. (Podría tener Doctores asociados).")
            return False
