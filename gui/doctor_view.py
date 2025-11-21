import customtkinter as ctk
from services.doctores_service import DoctorService
from services.especialidades_service import EspecialidadService
from datetime import datetime

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class DoctorView(ctk.CTkFrame):
    
    title = "Gestión de doctores"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.doctor_service = DoctorService()
        self.especialidad_service = EspecialidadService()
        
        self.doctores_data = [] 
        self.selected_doctor_id = None
        self.selected_row_labels = [] 
        
        self.especialidades_map = {} 

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Lista de doctores", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        self.create_entry_row(self.action_frame, 0, "Nombre:", "entry_nombre", 0, "Apellido:", "entry_apellido", 2)
        
        ctk.CTkLabel(self.action_frame, text="Especialidad:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combobox_especialidad = ctk.CTkComboBox(self.action_frame, values=["Cargando..."])
        self.combobox_especialidad.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Licencia Médica:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_licencia = ctk.CTkEntry(self.action_frame)
        self.entry_licencia.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        btn_crear = ctk.CTkButton(self.action_frame, text="Crear Nuevo", command=self.action_crear)
        btn_crear.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=2, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=2, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.load_especialidades()
        self.load_doctores()
        

    def create_entry_row(self, container, row, label1, attr1, col1, label2, attr2, col2):
        """Función auxiliar para crear pares de etiquetas y entradas en una fila."""
        ctk.CTkLabel(container, text=label1).grid(row=row, column=col1, padx=10, pady=5, sticky="w")
        entry1 = ctk.CTkEntry(container)
        entry1.grid(row=row, column=col1 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr1, entry1) 
        
        ctk.CTkLabel(container, text=label2).grid(row=row, column=col2, padx=10, pady=5, sticky="w")
        entry2 = ctk.CTkEntry(container)
        entry2.grid(row=row, column=col2 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr2, entry2)

    def load_especialidades(self):
        """Carga las especialidades de la DB para el ComboBox."""
        especialidades_db = self.especialidad_service.obtener_todas_especialidades()
        
        nombres_especialidades = []
        self.especialidades_map = {}
        
        for e_id, e_nombre in especialidades_db:
            nombres_especialidades.append(e_nombre)
            self.especialidades_map[e_nombre] = e_id

        if nombres_especialidades:
            self.combobox_especialidad.configure(values=nombres_especialidades)
            self.combobox_especialidad.set(nombres_especialidades[0]) 
        else:
            self.combobox_especialidad.configure(values=["Sin Especialidades"])
            self.combobox_especialidad.set("Sin Especialidades")
            
    def load_doctores(self):
        """Carga los doctores de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.doctores_data = self.doctor_service.obtener_todos_doctores()
        self.selected_doctor_id = None
        self.selected_row_labels = [] 

        if not self.doctores_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay doctores registrados.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Nombre", "Apellido", "Especialidad", "Licencia"]
        
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)

        for i, doctor in enumerate(self.doctores_data):
            doctor_id = doctor[0]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            row_labels = []
            
            for col, data in enumerate(doctor[:5]): 
                text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, did=doctor_id, ddata=doctor, r_labels=row_labels: self.select_doctor(did, ddata, r_labels))
                
                row_labels.append(label)


    def select_doctor(self, doctor_id, doctor_data, current_row_labels):
        """Maneja la selección de un doctor, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_doctor_id = doctor_id
        
        self.msg_label.configure(text=f"Doctor ID {doctor_id} seleccionado.", text_color="blue")
        
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_licencia.delete(0, 'end')

        self.entry_nombre.insert(0, doctor_data[1])
        self.entry_apellido.insert(0, doctor_data[2])
        self.entry_licencia.insert(0, doctor_data[4])
        
        self.combobox_especialidad.set(doctor_data[3]) 


    def action_crear(self):
        """Maneja la creación de un nuevo doctor."""
        try:
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            licencia = self.entry_licencia.get()
            especialidad_nombre = self.combobox_especialidad.get()
            
            especialidad_id = self.especialidades_map.get(especialidad_nombre)
            
            if not all([nombre, apellido, licencia, especialidad_id]):
                self.msg_label.configure(text="Error: Faltan campos obligatorios o la especialidad no existe.", text_color="red")
                return

            if self.doctor_service.crear_doctor(nombre, apellido, especialidad_id, licencia):
                self.msg_label.configure(text=f"Doctor {nombre} {apellido} creado.", text_color="green")
                self.load_doctores() 
                self.clear_entries()  
            else:
                self.msg_label.configure(text="Error al crear el doctor.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_actualizar(self):
        """Maneja la actualización de un doctor existente."""
        if not self.selected_doctor_id:
            self.msg_label.configure(text="Error: Seleccione un doctor primero.", text_color="red")
            return
            
        try:
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            licencia = self.entry_licencia.get()
            especialidad_nombre = self.combobox_especialidad.get()
            
            especialidad_id = self.especialidades_map.get(especialidad_nombre)
            
            if self.doctor_service.actualizar_doctor(self.selected_doctor_id, nombre, apellido, especialidad_id, licencia):
                self.msg_label.configure(text=f"Doctor ID {self.selected_doctor_id} actualizado.", text_color="green")
                self.load_doctores() 
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al actualizar el doctor.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de un doctor."""
        if not self.selected_doctor_id:
            self.msg_label.configure(text="Error: Seleccione un doctor para eliminar.", text_color="red")
            return

        if self.doctor_service.eliminar_doctor(self.selected_doctor_id):
            self.msg_label.configure(text=f"Doctor ID {self.selected_doctor_id} eliminado.", text_color="orange")
            self.load_doctores()
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al eliminar el doctor. (Verifique si tiene citas asociadas).", text_color="red")


    def clear_entries(self):
        """Limpia todos los campos de entrada y la selección."""
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
            self.selected_row_labels = []
            
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_licencia.delete(0, 'end')
        
        if self.combobox_especialidad.cget("values"):
            self.combobox_especialidad.set(self.combobox_especialidad.cget("values")[0])
            
        self.selected_doctor_id = None
        

    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView