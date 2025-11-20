import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

class HistorialMedicoService:
    def __init__(self):
        self.db = ConexionDB()

    def crear_registro(self, cita_id, diagnostico, notas_evolucion):
        """
        Crea un nuevo registro de historial médico para una cita específica.
        Nota: El campo cita_id es UNIQUE.
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

    def obtener_registro_por_cita(self, cita_id):
        """
        Retorna el registro de historial médico para una cita específica.
        Incluye detalles del paciente y doctor para contexto.
        """
        sql = """
        SELECT 
            hm.id, hm.diagnostico, hm.notas_evolucion, hm.fecha_registro,
            c.id, c.fecha_hora, 
            p.nombre, p.apellido, 
            d.nombre, d.apellido
        FROM 
            Historial_Medico hm
        JOIN 
            Citas c ON hm.cita_id = c.id
        JOIN
            Pacientes p ON c.paciente_id = p.id
        JOIN
            Doctores d ON c.doctor_id = d.id
        WHERE 
            hm.cita_id = %s
        """
        return self.db.ejecutar_consulta(sql, params=(cita_id,), fetch_one=True)
        
    def actualizar_registro(self, cita_id, diagnostico, notas_evolucion):
        """Actualiza el diagnóstico y las notas de un registro existente."""
        sql = """
        UPDATE Historial_Medico 
        SET diagnostico = %s, notas_evolucion = %s, fecha_registro = CURRENT_TIMESTAMP
        WHERE cita_id = %s
        """
        params = (diagnostico, notas_evolucion, cita_id)
        
        resultado = self.db.ejecutar_consulta(sql, params=params)
        
        if resultado:
            print(f"Historial para Cita ID {cita_id} actualizado exitosamente.")
            return True
        else:
            print(f"Error al actualizar el historial para Cita ID {cita_id}.")
            return False
            
    def eliminar_registro_por_cita(self, cita_id):
        """Elimina el registro de historial médico asociado a una cita específica."""
        sql = "DELETE FROM Historial_Medico WHERE cita_id = %s"
        
        resultado = self.db.ejecutar_consulta(sql, params=(cita_id,))
        
        if resultado:
            print(f"Historial para Cita ID {cita_id} eliminado exitosamente.")
            return True
        else:
            print(f"Error al eliminar el historial para Cita ID {cita_id}.")
            return False