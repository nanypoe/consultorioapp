import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.conexion import ConexionDB

import pandas as pd
from fpdf import FPDF

class ReportesService:
    def __init__(self):
        self.db = ConexionDB()
        self.output_dir = "reportes_generados"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    
    def generar_reporte_excel_pacientes(self, ruta_guardado=None):
        """
        Reporte 1: Reporte Excel Simple - Listado de Pacientes.
        """
        print("Generando Reporte Excel de Pacientes...")
        
        sql = """
        SELECT 
            id, nombre, apellido, fecha_nacimiento, telefono, direccion 
        FROM 
            Pacientes 
        ORDER BY 
            apellido ASC
        """
        data = self.db.ejecutar_consulta(sql)
        
        if not data:
            print("No hay datos de pacientes para generar el reporte.")
            return False, "No hay datos de pacientes."

        columnas = [
            'ID', 'Nombre', 'Apellido', 'Fecha Nacimiento', 
            'Teléfono', 'Dirección' 
        ]
        df = pd.DataFrame(data, columns=columnas)
        
        # --- LÓGICA DE GUARDADO RESTAURADA ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if ruta_guardado is not None:
            # Completa la ruta con el timestamp y la extensión, usando la base pasada por la vista
            ruta_final = f"{ruta_guardado}{timestamp}.xlsx"
        else:
            # Si no se pasó ruta, usa la carpeta de reportes por defecto
            nombre_archivo = f"Listado_Pacientes_{timestamp}.xlsx"
            ruta_final = os.path.join(self.output_dir, nombre_archivo)
            
        try:
            # Guardar el archivo
            df.to_excel(ruta_final, index=False, sheet_name='Pacientes')
            print(f"Reporte Excel generado en: {ruta_final}")
            # Retornar éxito y la ruta final
            return True, ruta_final
        except Exception as e:
            print(f"Error al escribir el archivo Excel: {e}")
            # Retornar fallo y el mensaje de error
            return False, f"Error al guardar: {e}"
        # --- FIN LÓGICA DE GUARDADO RESTAURADA ---

# Reportes en PDF
    def generar_reporte_pdf_historial_paciente(self, paciente_id, ruta_guardado=None):
        """
        Reporte 2 y 3: Reporte Maestro-Detalle y con Parámetros (ID de Paciente).
        Muestra la información del paciente y luego el detalle de sus citas/historial.
        """
        print(f"Generando Reporte PDF de Historial para Paciente ID: {paciente_id}...")
        
        sql_paciente = "SELECT nombre, apellido, telefono FROM Pacientes WHERE id = %s"
        paciente_data = self.db.ejecutar_consulta(sql_paciente, params=(paciente_id,), fetch_one=True)
        
        if not paciente_data:
            return False, f"Paciente ID {paciente_id} no encontrado."

        sql_historial = """
        SELECT 
            c.fecha_hora, d.nombre, d.apellido, hm.diagnostico, hm.notas_evolucion
        FROM 
            Citas c
        JOIN 
            Historial_Medico hm ON c.id = hm.cita_id
        JOIN
            Doctores d ON c.doctor_id = d.id
        WHERE 
            c.paciente_id = %s
        ORDER BY 
            c.fecha_hora DESC
        """
        historial_data = self.db.ejecutar_consulta(sql_historial, params=(paciente_id,))

        pdf = FPDF('P', 'mm', 'A4') 
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Historial Médico Detallado del Paciente', 0, 1, 'C')
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 7, 'Paciente:', 0, 0, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 7, f"{paciente_data[0]} {paciente_data[1]} (ID: {paciente_id})", 0, 1, 'L')
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 7, 'Contacto:', 0, 0, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 7, f"Tel: {paciente_data[2]}", 0, 1, 'L')
        pdf.ln(5)

        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(30, 7, 'Fecha/Hora', 1, 0, 'C', 1)
        pdf.cell(40, 7, 'Doctor', 1, 0, 'C', 1)
        pdf.cell(100, 7, 'Diagnóstico y Notas', 1, 1, 'C', 1)
        
        pdf.set_font('Arial', '', 10)
        
        if not historial_data:
            pdf.cell(0, 7, 'No se encontraron registros de historial para este paciente.', 1, 1, 'C')
        else:
            for cita in historial_data:
                fecha_hora = cita[0].strftime('%Y-%m-%d %H:%M')
                doctor = f"Dr. {cita[1]} {cita[2]}"
                diagnostico = cita[3]
                notas = cita[4]
                
                pdf.cell(30, 6, fecha_hora, 1, 0, 'L')
                pdf.cell(40, 6, doctor, 1, 0, 'L')
                
                x_inicio = pdf.get_x()
                y_inicio = pdf.get_y()
                
                pdf.set_font('Arial', 'B', 9)
                pdf.set_x(x_inicio)
                pdf.multi_cell(100, 4, f"Diagnóstico: {diagnostico}", 0, 'L')
                
                pdf.set_font('Arial', '', 9)
                pdf.set_x(x_inicio)
                pdf.multi_cell(100, 4, f"Notas: {notas}", 0, 'L')
                
                y_fin = pdf.get_y()
                pdf.set_xy(x_inicio + 100, y_inicio)
                pdf.cell(0, y_fin - y_inicio, "", 1, 1, 'L') 
                pdf.set_xy(10, y_fin)
                
                
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Historial_Paciente_{paciente_id}_{timestamp}.pdf"
        
        if ruta_guardado is None:
            ruta_guardado = os.path.join(self.output_dir, nombre_archivo)
            
        try:
            pdf.output(ruta_guardado)
            print(f"Reporte PDF generado en: {ruta_guardado}")
            return True, ruta_guardado
        except Exception as e:
            print(f"Error al escribir el archivo PDF: {e}")
            return False, f"Error al guardar: {e}"

    def generar_reporte_pdf_citas_pendientes(self, ruta_guardado=None):
        """
        Reporte 4: Reporte Listado PDF - Citas con estado 'Pendiente'.
        """
        print("Generando Reporte PDF de Citas Pendientes...")
        
        sql = """
        SELECT 
            c.id, c.fecha_hora, p.nombre, p.apellido, d.nombre, d.apellido, c.motivo
        FROM 
            Citas c
        JOIN 
            Pacientes p ON c.paciente_id = p.id
        JOIN
            Doctores d ON c.doctor_id = d.id
        WHERE 
            c.estado = 'Pendiente'
        ORDER BY 
            c.fecha_hora ASC
        """
        citas_data = self.db.ejecutar_consulta(sql)
        
        pdf = FPDF('L', 'mm', 'A4') 
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Citas Pendientes de Consulta', 0, 1, 'C')
        pdf.ln(5)

        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 10)
        
        pdf.cell(15, 7, 'ID', 1, 0, 'C', 1)
        pdf.cell(30, 7, 'Fecha/Hora', 1, 0, 'C', 1)
        pdf.cell(60, 7, 'Paciente', 1, 0, 'C', 1)
        pdf.cell(60, 7, 'Doctor Asignado', 1, 0, 'C', 1)
        pdf.cell(105, 7, 'Motivo', 1, 1, 'C', 1)
        
        pdf.set_font('Arial', '', 10)
        
        if not citas_data:
            pdf.cell(0, 7, 'No hay citas pendientes actualmente.', 1, 1, 'C')
        else:
            for c_id, fecha_hora, p_nombre, p_apellido, d_nombre, d_apellido, motivo in citas_data:
                fecha_str = fecha_hora.strftime('%Y-%m-%d %H:%M')
                paciente = f"{p_nombre} {p_apellido}"
                doctor = f"Dr. {d_nombre} {d_apellido}"
                
                pdf.cell(15, 6, str(c_id), 1, 0, 'C')
                pdf.cell(30, 6, fecha_str, 1, 0, 'L')
                pdf.cell(60, 6, paciente, 1, 0, 'L')
                pdf.cell(60, 6, doctor, 1, 0, 'L')
                pdf.cell(105, 6, motivo, 1, 1, 'L')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Citas_Pendientes_{timestamp}.pdf"
        
        if ruta_guardado is None:
            ruta_guardado = os.path.join(self.output_dir, nombre_archivo)
            
        try:
            pdf.output(ruta_guardado)
            print(f"Reporte PDF generado en: {ruta_guardado}")
            return True, ruta_guardado
        except Exception as e:
            print(f"Error al escribir el archivo PDF: {e}")
            return False, f"Error al guardar: {e}"