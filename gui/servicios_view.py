import customtkinter as ctk
from services.servicios_service import ServiciosService

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class ServiciosView(ctk.CTkFrame):
    
    title = "Catálogo de servicios y costos"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.servicios_service = ServiciosService()
        
        self.servicios_data = [] 
        self.selected_servicio_id = None
        self.selected_row_labels = [] 
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Servicios del consultorio", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        ctk.CTkLabel(self.action_frame, text="Nombre del servicio:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(self.action_frame)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Costo (USD):").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_costo = ctk.CTkEntry(self.action_frame)
        self.entry_costo.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Descripción:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_descripcion = ctk.CTkEntry(self.action_frame, height=50) 
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        
        btn_crear = ctk.CTkButton(self.action_frame, text="Crear Servicio", command=self.action_crear)
        btn_crear.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=2, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=2, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.load_servicios()


    def load_servicios(self):
        """Carga los servicios de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.servicios_data = self.servicios_service.obtener_todos_servicios()
        self.selected_servicio_id = None
        self.selected_row_labels = [] 

        if not self.servicios_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay servicios registrados.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Servicio", "Descripción", "Costo"]
        
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)
        
        for i, servicio in enumerate(self.servicios_data):
            servicio_id = servicio[0]
            nombre = servicio[1]
            
            descripcion = servicio[2] if servicio[2] is not None else ""
            
            descripcion_corta = descripcion[:50] + '...' if len(descripcion) > 50 else descripcion
            
            costo_formateado = f"${servicio[3]:.2f}"
            
            display_data = [servicio_id, nombre, descripcion_corta, costo_formateado]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            row_labels = []
            
            for col, data in enumerate(display_data): 
                text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, sid=servicio_id, sdata=servicio, r_labels=row_labels: self.select_servicio(sid, sdata, r_labels))
                
                row_labels.append(label)


    def select_servicio(self, servicio_id, servicio_data, current_row_labels):
        """Maneja la selección de un servicio, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_servicio_id = servicio_id
        
        self.msg_label.configure(text=f"Servicio ID {servicio_id} seleccionado.", text_color="blue")
        
        self.clear_entries(keep_selection=True) 
        
        nombre_a_insertar = servicio_data[1] if servicio_data[1] is not None else ""
        descripcion_a_insertar = servicio_data[2] if servicio_data[2] is not None else ""
        costo_a_insertar = str(servicio_data[3]) if servicio_data[3] is not None else ""
        
        self.entry_nombre.insert(0, nombre_a_insertar)
        self.entry_descripcion.insert(0, descripcion_a_insertar)
        self.entry_costo.insert(0, costo_a_insertar) 


    def action_crear(self):
        """Maneja la creación de un nuevo servicio."""
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        costo = self.entry_costo.get()
            
        if not all([nombre, costo]):
            self.msg_label.configure(text="Error: Nombre y Costo son obligatorios.", text_color="red")
            return

        if self.servicios_service.crear_servicio(nombre, descripcion, costo):
            self.msg_label.configure(text=f"Servicio '{nombre}' creado.", text_color="green")
            self.load_servicios() 
            self.clear_entries()  
        else:
            self.msg_label.configure(text="Error al crear el servicio. Revise el formato del Costo.", text_color="red")
                
    
    def action_actualizar(self):
        """Maneja la actualización de un servicio existente."""
        if not self.selected_servicio_id:
            self.msg_label.configure(text="Error: Seleccione un servicio primero.", text_color="red")
            return
            
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        costo = self.entry_costo.get()

        if self.servicios_service.actualizar_servicio(self.selected_servicio_id, nombre, descripcion, costo):
            self.msg_label.configure(text=f"Servicio ID {self.selected_servicio_id} actualizado.", text_color="green")
            self.load_servicios() 
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al actualizar el servicio. Revise el formato del Costo.", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de un servicio."""
        if not self.selected_servicio_id:
            self.msg_label.configure(text="Error: Seleccione un servicio para eliminar.", text_color="red")
            return

        if self.servicios_service.eliminar_servicio(self.selected_servicio_id):
            self.msg_label.configure(text=f"Servicio ID {self.selected_servicio_id} eliminado.", text_color="orange")
            self.load_servicios()
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al eliminar el servicio.", text_color="red")


    def clear_entries(self, keep_selection=False):
        """Limpia todos los campos de entrada y la selección."""
        if not keep_selection and self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
            self.selected_row_labels = []
            self.selected_servicio_id = None
            
        self.entry_nombre.delete(0, 'end')
        self.entry_descripcion.delete(0, 'end')
        self.entry_costo.delete(0, 'end')


    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView