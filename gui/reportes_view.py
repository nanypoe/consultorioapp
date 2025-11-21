import customtkinter as ctk
from services.reportes_service import ReportesService
import os
import webbrowser
from tkinter import filedialog
from services.paciente_service import PacienteService 

class ReportesView(ctk.CTkFrame):
    
    title = "Generador de Reportes del sistema"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.reportes_service = ReportesService()
        self.paciente_service = PacienteService()
        self.pacientes_map = {} 

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.report_container = ctk.CTkFrame(self)
        self.report_container.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.report_container.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(self.report_container, text="Reporte 1: Listado de Pacientes (Excel)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(5, 0), sticky="sw")
        
        self.frame_r1 = ctk.CTkFrame(self.report_container, border_width=2) 
        self.frame_r1.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_r1.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame_r1, text="Genera un archivo XLSX con todos los pacientes registrados.").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        btn_r1 = ctk.CTkButton(self.frame_r1, text="Generar Excel", command=lambda: self.generar_reporte(1))
        btn_r1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.report_container, text="Reporte 2/3: Historial Médico Detallado (PDF)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=(5, 0), sticky="sw")
        
        self.frame_r2 = ctk.CTkFrame(self.report_container, border_width=2) 
        self.frame_r2.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_r2.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self.frame_r2, text="Seleccione el Paciente para ver su Historial Médico completo:").grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.combobox_pacientes = ctk.CTkComboBox(self.frame_r2, values=["Cargando Pacientes..."])
        self.combobox_pacientes.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        btn_r2 = ctk.CTkButton(self.frame_r2, text="Generar PDF Historial", command=lambda: self.generar_reporte(2))
        btn_r2.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(self.report_container, text="Reporte 4: Citas Pendientes (PDF)", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=(5, 0), sticky="sw")
        
        self.frame_r4 = ctk.CTkFrame(self.report_container, border_width=2) 
        self.frame_r4.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_r4.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame_r4, text="Genera un listado de todas las citas cuyo estado es 'Pendiente'.").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        btn_r4 = ctk.CTkButton(self.frame_r4, text="Generar PDF Citas", command=lambda: self.generar_reporte(4))
        btn_r4.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.footer_frame.grid_columnconfigure((0, 1), weight=1) 
        
        self.msg_label = ctk.CTkLabel(self.footer_frame, text="", text_color="green", anchor="w")
        self.msg_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.footer_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        
        self.load_pacientes()


    def load_pacientes(self):
        """Carga los pacientes para el ComboBox del reporte parametrizado."""
        try:
            pacientes = self.paciente_service.obtener_todos_pacientes()
            nombres_pacientes = []
            self.pacientes_map = {}
            
            for p_id, nombre, apellido, _, _, _ in pacientes:
                nombre_completo = f"ID {p_id}: {nombre} {apellido}"
                nombres_pacientes.append(nombre_completo)
                self.pacientes_map[nombre_completo] = p_id

            if nombres_pacientes:
                self.combobox_pacientes.configure(values=nombres_pacientes, state="normal")
                self.combobox_pacientes.set(nombres_pacientes[0]) 
            else:
                self.combobox_pacientes.configure(values=["No hay pacientes registrados"], state="disabled")
                self.combobox_pacientes.set("No hay pacientes registrados")
                
        except Exception as e:
             self.msg_label.configure(text=f"Error cargando pacientes: {e}", text_color="red")


    def generar_reporte(self, tipo_reporte):
        """Función principal para generar cualquier reporte."""
        
        dir_seleccionado = filedialog.askdirectory(title="Seleccionar Carpeta para Guardar el Reporte")
        if not dir_seleccionado:
            self.msg_label.configure(text="Generación cancelada.", text_color="orange")
            return
            
        ruta_guardado = None
        
        if tipo_reporte == 1: 
            ruta_guardado = os.path.join(dir_seleccionado, "Listado_Pacientes_")
            success, resultado = self.reportes_service.generar_reporte_excel_pacientes(ruta_guardado)
            
        elif tipo_reporte == 2: 
            paciente_nombre_seleccionado = self.combobox_pacientes.get()
            paciente_id = self.pacientes_map.get(paciente_nombre_seleccionado)
            
            if not paciente_id:
                self.msg_label.configure(text="Error: Seleccione un paciente válido.", text_color="red")
                return

            ruta_guardado = os.path.join(dir_seleccionado, f"Historial_Paciente_{paciente_id}_")
            success, resultado = self.reportes_service.generar_reporte_pdf_historial_paciente(paciente_id, ruta_guardado)

        elif tipo_reporte == 4: 
            ruta_guardado = os.path.join(dir_seleccionado, "Citas_Pendientes_")
            success, resultado = self.reportes_service.generar_reporte_pdf_citas_pendientes(ruta_guardado)

        else:
            self.msg_label.configure(text="Reporte no implementado.", text_color="red")
            return

        
        if success:
            self.msg_label.configure(text=f"Reporte generado exitosamente: {resultado}", text_color="green")
            if os.path.isdir(dir_seleccionado):
                self.after(500, lambda: webbrowser.open(dir_seleccionado)) 
        else:
            self.msg_label.configure(text=f"Error al generar el reporte: {resultado}", text_color="red")
            

    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView