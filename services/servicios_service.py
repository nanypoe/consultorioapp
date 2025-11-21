import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class ServiciosService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_servicio(self, nombre_servicio, descripcion, costo):
        """
        Crea un nuevo servicio en el catálogo.
        """
        sql = """
        INSERT INTO Servicios_Consultorio (nombre_servicio, descripcion, costo)
        VALUES (%s, %s, %s)
        """
        try:
            costo_decimal = float(costo)
        except ValueError:
            print("Error: El costo debe ser un valor numérico.")
            return False
            
        params = (nombre_servicio, descripcion, costo_decimal)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Servicio '{nombre_servicio}' creado exitosamente.")
            return True
        else:
            print(f"Error al crear el servicio '{nombre_servicio}'.")
            return False

    def obtener_todos_servicios(self):
        """
        Retorna todos los servicios, incluyendo su costo.
        """
        sql = "SELECT id, nombre_servicio, descripcion, costo FROM Servicios_Consultorio ORDER BY nombre_servicio ASC"
        return self.db.ejecutar_consulta(sql)
    
    def obtener_servicio_por_id(self, servicio_id):
        """
        Retorna un servicio específico por su ID.
        """
        sql = "SELECT id, nombre_servicio, descripcion, costo FROM Servicios_Consultorio WHERE id = %s"
        return self.db.ejecutar_consulta(sql, params=(servicio_id,), fetch_one=True)
        
    def actualizar_servicio(self, servicio_id, nombre_servicio, descripcion, costo):
        """
        Actualiza los datos de un servicio existente.
        """
        sql = """
        UPDATE Servicios_Consultorio 
        SET nombre_servicio = %s, descripcion = %s, costo = %s
        WHERE id = %s
        """
        try:
            costo_decimal = float(costo)
        except ValueError:
            print("Error: El costo debe ser un valor numérico.")
            return False
            
        params = (nombre_servicio, descripcion, costo_decimal, servicio_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Servicio ID {servicio_id} actualizado exitosamente.")
            return True
        else:
            print(f"Error al actualizar el servicio ID {servicio_id}.")
            return False
            
    def eliminar_servicio(self, servicio_id):
        """
        Elimina un servicio por su ID.
        """
        sql = "DELETE FROM Servicios_Consultorio WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(servicio_id,))
        
        if resultado:
            print(f"Servicio ID {servicio_id} eliminado exitosamente.")
            return True
        else:
            print(f"Error al eliminar el servicio ID {servicio_id}.")
            return False