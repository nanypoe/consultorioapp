import customtkinter as ctk
from services.historial_service import HistorialService
from services.cita_service import CitaService
from datetime import datetime

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class HistorialView(ctk.CTkFrame):
    
    title = "Historial médico de Pacientes"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.historial_service = HistorialService()
        self.cita_service = CitaService()
        
        self.historiales_data = [] 
        self.selected_historial_id = None
        self.selected_row_labels = [] 
        
        self.citas_sin_historial_map = {} 

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Lista de historiales clínicos", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        ctk.CTkLabel(self.action_frame, text="Asociar Cita:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.combobox_cita = ctk.CTkComboBox(self.action_frame, values=["Cargando citas completadas..."])
        self.combobox_cita.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Diagnóstico:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_diagnostico = ctk.CTkEntry(self.action_frame)
        self.entry_diagnostico.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Notas de evolución:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_notas = ctk.CTkEntry(self.action_frame, height=50) 
        self.entry_notas.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        
        btn_crear = ctk.CTkButton(self.action_frame, text="Crear historial", command=self.action_crear)
        btn_crear.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=2, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=2, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.load_citas_pendientes()
        self.load_historiales()


    def load_citas_pendientes(self):
        """Carga las citas 'Completadas' sin registro de historial para el ComboBox de creación."""
        
        citas_db = self.historial_service.obtener_citas_sin_historial()
        
        nombres_citas = []
        self.citas_sin_historial_map = {}
        
        for c_id, p_nombre, p_apellido, d_nombre, d_apellido, fecha_hora, motivo in citas_db:
            
            fecha_str = fecha_hora.strftime('%Y-%m-%d %H:%M')
            nombre_completo = f"Cita {c_id}: {p_nombre} {p_apellido} con Dr. {d_nombre} ({fecha_str})"
            nombres_citas.append(nombre_completo)
            self.citas_sin_historial_map[nombre_completo] = c_id

        if nombres_citas:
            self.combobox_cita.configure(values=nombres_citas, state="normal")
            self.combobox_cita.set(nombres_citas[0]) 
            self.combobox_cita.cget("values")
        else:
            self.combobox_cita.configure(values=["No hay citas completadas sin historial"], state="disabled")
            self.combobox_cita.set("No hay citas completadas sin historial")

            
    def load_historiales(self):
        """Carga los historiales de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.historiales_data = self.historial_service.obtener_todos_historiales()
        self.selected_historial_id = None
        self.selected_row_labels = [] 

        if not self.historiales_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay historiales médicos registrados.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Fecha Reg.", "Paciente", "Doctor", "Diagnóstico", "Cita ID"]
        
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)
        
        
        for i, historial in enumerate(self.historiales_data):
            historial_id = historial[0]
            fecha_reg = historial[1].strftime('%Y-%m-%d %H:%M')
            diagnostico_corto = historial[2][:40] + '...' if len(historial[2]) > 40 else historial[2]
            paciente = f"{historial[4]} {historial[5]}"
            doctor = f"{historial[6]} {historial[7]}"
            cita_id = historial[8]
            
            display_data = [historial_id, fecha_reg, paciente, doctor, diagnostico_corto, cita_id]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            row_labels = []
            
            for col, data in enumerate(display_data): 
                text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, hid=historial_id, hdata=historial, r_labels=row_labels: self.select_historial(hid, hdata, r_labels))
                
                row_labels.append(label)


    def select_historial(self, historial_id, historial_data, current_row_labels):
        """Maneja la selección de un historial, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_historial_id = historial_id
        
        self.msg_label.configure(text=f"Historial ID {historial_id} seleccionado.", text_color="blue")
        
        self.clear_entries(keep_selection=True) 
        
        historial_detalles = self.historial_service.obtener_historial_por_id(historial_id)
        
        if historial_detalles:
            self.entry_diagnostico.insert(0, historial_detalles[2])
            self.entry_notas.insert(0, historial_detalles[3])
            
            self.combobox_cita.set(f"Cita ID: {historial_detalles[1]} (Solo actualización)")
            self.combobox_cita.configure(state="disabled")


    def action_crear(self):
        """Maneja la creación de un nuevo registro de historial."""
        try:
            cita_nombre = self.combobox_cita.get()
            diagnostico = self.entry_diagnostico.get()
            notas_evolucion = self.entry_notas.get()
            
            cita_id = self.citas_sin_historial_map.get(cita_nombre)
            
            if not all([cita_id, diagnostico, notas_evolucion]):
                self.msg_label.configure(text="Error: Complete el diagnóstico y las notas y seleccione una Cita válida.", text_color="red")
                return

            if self.historial_service.crear_historial(cita_id, diagnostico, notas_evolucion):
                self.msg_label.configure(text=f"Historial creado para Cita ID {cita_id}.", text_color="green")
                self.load_historiales() 
                self.load_citas_pendientes() 
                self.clear_entries()  
            else:
                self.msg_label.configure(text="Error al crear el historial (Probablemente ya exista uno para esta cita).", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_actualizar(self):
        """Maneja la actualización de un historial existente."""
        if not self.selected_historial_id:
            self.msg_label.configure(text="Error: Seleccione un historial primero.", text_color="red")
            return
            
        try:
            diagnostico = self.entry_diagnostico.get()
            notas_evolucion = self.entry_notas.get()
            
            if self.historial_service.actualizar_historial(self.selected_historial_id, diagnostico, notas_evolucion):
                self.msg_label.configure(text=f"Historial ID {self.selected_historial_id} actualizado.", text_color="green")
                self.load_historiales() 
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al actualizar el historial.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de un historial."""
        if not self.selected_historial_id:
            self.msg_label.configure(text="Error: Seleccione un historial para eliminar.", text_color="red")
            return

        if self.historial_service.eliminar_historial(self.selected_historial_id):
            self.msg_label.configure(text=f"Historial ID {self.selected_historial_id} eliminado.", text_color="orange")
            self.load_historiales()
            self.load_citas_pendientes() 
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al eliminar el historial.", text_color="red")


    def clear_entries(self, keep_selection=False):
        """Limpia todos los campos de entrada y la selección."""
        if not keep_selection and self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
            self.selected_row_labels = []
            self.selected_historial_id = None
            
        self.entry_diagnostico.delete(0, 'end')
        self.entry_notas.delete(0, 'end')
        
        self.combobox_cita.configure(state="normal")
        if self.combobox_cita.cget("values") and self.combobox_cita.cget("values")[0] != "No hay citas Completadas sin Historial":
            self.combobox_cita.set(self.combobox_cita.cget("values")[0])
        else:
            self.combobox_cita.set("No hay citas Completadas sin Historial")


    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView