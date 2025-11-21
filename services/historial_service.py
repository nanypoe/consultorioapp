import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class HistorialService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_historial(self, cita_id, diagnostico, notas_evolucion):
        """
        Crea un nuevo registro de historial médico para una cita específica.
        (Renombrado de crear_registro a crear_historial para consistencia con la vista).
        """
        sql = """
        INSERT INTO Historial_Medico (cita_id, diagnostico, notas_evolucion)
        VALUES (%s, %s, %s)
        """
        params = (cita_id, diagnostico, notas_evolucion)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Registro de historial creado exitosamente para Cita ID {cita_id}.")
            return True
        else:
            print(f"Error al crear el registro para Cita ID {cita_id}. (Podría ya existir).")
            return False

    def obtener_citas_sin_historial(self):
        """
        Obtiene todas las citas marcadas como 'Completada' que aún no tienen 
        un registro en Historial_Medico. (Método Faltante)
        """
        sql = """
        SELECT 
            c.id, p.nombre, p.apellido, d.nombre, d.apellido, c.fecha_hora, c.motivo
        FROM 
            Citas c
        JOIN 
            Pacientes p ON c.paciente_id = p.id
        JOIN
            Doctores d ON c.doctor_id = d.id
        LEFT JOIN 
            Historial_Medico hm ON c.id = hm.cita_id
        WHERE 
            c.estado = 'Completada' 
            AND hm.id IS NULL
        ORDER BY c.fecha_hora ASC
        """
        return self.db.ejecutar_consulta(sql)
        
    def obtener_todos_historiales(self):
        """
        Obtiene todos los historiales con detalles de la cita, paciente y doctor.
        (Método Faltante)
        """
        sql = """
        SELECT 
            hm.id, hm.fecha_registro, hm.diagnostico, hm.notas_evolucion,
            p.nombre, p.apellido, 
            d.nombre, d.apellido,
            c.id AS cita_id
        FROM 
            Historial_Medico hm
        JOIN 
            Citas c ON hm.cita_id = c.id
        JOIN
            Pacientes p ON c.paciente_id = p.id
        JOIN
            Doctores d ON c.doctor_id = d.id
        ORDER BY hm.fecha_registro DESC
        """
        return self.db.ejecutar_consulta(sql)

    def obtener_historial_por_id(self, historial_id):
        """
        Retorna los detalles de un historial por su ID.
        (Método Faltante, usado en la vista)
        """
        sql = """
        SELECT 
            id, cita_id, diagnostico, notas_evolucion, fecha_registro
        FROM 
            Historial_Medico
        WHERE 
            id = %s
        """
        return self.db.ejecutar_consulta(sql, params=(historial_id,), fetch_one=True)
        
    def actualizar_historial(self, historial_id, diagnostico, notas_evolucion):
        """
        Actualiza el diagnóstico y las notas de un registro existente por su ID.
        (Renombrado y corregido para usar historial_id, no cita_id).
        """
        sql = """
        UPDATE Historial_Medico 
        SET diagnostico = %s, notas_evolucion = %s, fecha_registro = %s
        WHERE id = %s
        """
        params = (diagnostico, notas_evolucion, datetime.now(), historial_id) 
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Historial ID {historial_id} actualizado exitosamente.")
            return True
        else:
            print(f"Error al actualizar el historial ID {historial_id}.")
            return False
            
    def eliminar_historial(self, historial_id):
        """
        Elimina el registro de historial médico por su ID.
        (Renombrado y corregido para usar historial_id, no cita_id).
        """
        sql = "DELETE FROM Historial_Medico WHERE id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(historial_id,))
        
        if resultado:
            print(f"Historial ID {historial_id} eliminado exitosamente.")
            return True
        else:
            print(f"Error al eliminar el historial ID {historial_id}.")
            return False