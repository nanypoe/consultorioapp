import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class DoctorService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_doctor(self, nombre, apellido, especialidad_id, licencia_medica):
        """Inserta un nuevo doctor en la base de datos."""
        sql = """
        INSERT INTO Doctores (nombre, apellido, especialidad_id, licencia_medica)
        VALUES (%s, %s, %s, %s)
        """
        params = (nombre, apellido, especialidad_id, licencia_medica)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Doctor {nombre} {apellido} creado exitosamente con Especialidad ID: {especialidad_id}.")
            return True
        else:
            print(f"Error al crear el doctor {nombre} {apellido}.")
            return False

    def obtener_todos_doctores(self):
        """Retorna todos los doctores con el nombre de su especialidad."""
        sql = """
        SELECT 
            d.id, d.nombre, d.apellido, e.nombre_especialidad, d.licencia_medica, d.especialidad_id
        FROM 
            Doctores d
        JOIN 
            Especialidades e ON d.especialidad_id = e.id
        ORDER BY 
            d.apellido, d.nombre
        """
        return self.db.ejecutar_consulta(sql)
    
    def obtener_doctor_por_id(self, doctor_id):
        """Retorna un doctor específico por su ID con el nombre de especialidad."""
        sql = """
        SELECT 
            d.id, d.nombre, d.apellido, e.nombre_especialidad, d.licencia_medica, d.especialidad_id
        FROM 
            Doctores d
        JOIN 
            Especialidades e ON d.especialidad_id = e.id
        WHERE 
            d.id = %s
        """
        return self.db.ejecutar_consulta(sql, params=(doctor_id,), fetch_one=True)
        
    def actualizar_doctor(self, doctor_id, nombre, apellido, especialidad_id, licencia_medica):
        """Actualiza los datos de un doctor existente, incluyendo la especialidad_id."""
        sql = """
        UPDATE Doctores 
        SET nombre = %s, apellido = %s, especialidad_id = %s, licencia_medica = %s
        WHERE id = %s
        """
        params = (nombre, apellido, especialidad_id, licencia_medica, doctor_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Doctor ID {doctor_id} actualizado exitosamente.")
            return True
        else:
            print(f"Error al actualizar el doctor ID {doctor_id}.")
            return False
            
    def eliminar_doctor(self, doctor_id):
        """Elimina un doctor por su ID."""
        sql = "DELETE FROM Doctores WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(doctor_id,))
        
        if resultado:
            print(f"Doctor ID {doctor_id} eliminado exitosamente.")
            return True
        else:
            print(f"Error al eliminar el doctor ID {doctor_id}.")
            return False
