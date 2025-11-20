import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class CitaService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_cita(self, paciente_id, doctor_id, fecha_hora, motivo):
        """Inserta una nueva cita en la base de datos."""
        sql = """
        INSERT INTO Citas (paciente_id, doctor_id, fecha_hora, motivo, estado)
        VALUES (%s, %s, %s, %s, 'Pendiente')
        """
        params = (paciente_id, doctor_id, fecha_hora, motivo)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Cita creada para Paciente ID {paciente_id} con Doctor ID {doctor_id}.")
            return True
        else:
            print(f"Error al crear la cita.")
            return False

    def obtener_todas_citas(self):
        """Retorna todas las citas con los nombres completos del paciente y doctor."""
        sql = """
        SELECT 
            c.id, 
            c.fecha_hora, 
            c.motivo, 
            c.estado, 
            p.nombre, p.apellido,   -- Datos del Paciente
            d.nombre, d.apellido    -- Datos del Doctor
        FROM 
            Citas c
        JOIN 
            Pacientes p ON c.paciente_id = p.id
        JOIN 
            Doctores d ON c.doctor_id = d.id
        ORDER BY 
            c.fecha_hora DESC
        """
        return self.db.ejecutar_consulta(sql)
    
    def obtener_cita_por_id(self, cita_id):
        """Retorna una cita específica por su ID."""
        sql = """
        SELECT 
            c.id, c.paciente_id, c.doctor_id, c.fecha_hora, c.motivo, c.estado 
        FROM Citas c
        WHERE id = %s
        """
        return self.db.ejecutar_consulta(sql, params=(cita_id,), fetch_one=True)
        
    def actualizar_cita(self, cita_id, paciente_id, doctor_id, fecha_hora, motivo, estado):
        """Actualiza los datos de una cita existente."""
        sql = """
        UPDATE Citas 
        SET paciente_id = %s, doctor_id = %s, fecha_hora = %s, motivo = %s, estado = %s
        WHERE id = %s
        """
        params = (paciente_id, doctor_id, fecha_hora, motivo, estado, cita_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Cita ID {cita_id} actualizada exitosamente.")
            return True
        else:
            print(f"Error al actualizar la cita ID {cita_id}.")
            return False
            
    def eliminar_cita(self, cita_id):
        """Elimina una cita por su ID."""
        sql = "DELETE FROM Citas WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(cita_id,))
        
        if resultado:
            print(f"Cita ID {cita_id} eliminada exitosamente.")
            return True
        else:
            print(f"Error al eliminar la cita ID {cita_id}.")
            return False