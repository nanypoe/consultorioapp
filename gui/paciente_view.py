import customtkinter as ctk
from services.paciente_service import PacienteService
from datetime import datetime
from tkcalendar import Calendar 
import tkinter as tk 

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class PacienteView(ctk.CTkFrame):
    
    title = "Gestión de pacientes"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.paciente_service = PacienteService()
        self.pacientes_data = []
        self.selected_paciente_id = None
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
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Lista de pacientes", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        self.create_entry_row(self.action_frame, 0, "Nombre:", "entry_nombre", 0, "Apellido:", "entry_apellido", 2)
        
        ctk.CTkLabel(self.action_frame, text="F. Nacimiento (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.entry_fecha = ctk.CTkEntry(self.action_frame, state="readonly", width=120) 
        self.entry_fecha.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="w")
        
        self.btn_fecha_picker = ctk.CTkButton(self.action_frame, text="📅", width=30, command=self.open_datepicker)
        self.btn_fecha_picker.grid(row=1, column=1, padx=(140, 10), pady=5, sticky="w")
        
        ctk.CTkLabel(self.action_frame, text="Teléfono:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_telefono = ctk.CTkEntry(self.action_frame)
        self.entry_telefono.grid(row=1, column=3, padx=10, pady=5, sticky="ew")        
        
        ctk.CTkLabel(self.action_frame, text="Dirección:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_direccion = ctk.CTkEntry(self.action_frame, width=500)
        self.entry_direccion.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")

        btn_crear = ctk.CTkButton(self.action_frame, text="Crear Nuevo", command=self.action_crear)
        btn_crear.grid(row=3, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=3, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=3, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=4, column=0, columnspan=4, pady=(0, 10))

        self.load_pacientes()

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

    def open_datepicker(self):
        """Abre una ventana de calendario modal para seleccionar la fecha."""
        
        top = tk.Toplevel(self)
        top.title("Seleccionar fecha")
        try:
            current_date = datetime.strptime(self.entry_fecha.get(), '%Y-%m-%d')
        except ValueError:
            current_date = datetime.now()

        cal = Calendar(top, 
                       selectmode='day',
                       date_pattern='y-mm-dd',
                       year=current_date.year,
                       month=current_date.month,
                       day=current_date.day)
        
        cal.pack(padx=20, pady=20)

        def set_date():
            selected_date = cal.get_date()
            self.entry_fecha.configure(state="normal") 
            self.entry_fecha.delete(0, 'end')
            self.entry_fecha.insert(0, selected_date)
            self.entry_fecha.configure(state="readonly") 
            top.destroy() 

        ctk.CTkButton(top, text="Aceptar", command=set_date).pack(pady=(0, 20))
        
        top.grab_set() 
        
        top.update_idletasks()
        width = top.winfo_width()
        height = top.winfo_height()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        top.geometry(f'{width}x{height}+{x}+{y}')
        top.resizable(False, False)

    def load_pacientes(self):
        """Carga los pacientes de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.pacientes_data = self.paciente_service.obtener_todos_pacientes()
        self.selected_paciente_id = None
        self.selected_row_labels = [] 

        if not self.pacientes_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay pacientes registrados.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Nombre", "Apellido", "F. Nacimiento", "Teléfono", "Dirección"]
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)

        for i, paciente in enumerate(self.pacientes_data):
            paciente_id = paciente[0]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            
            row_labels = []

            for col, data in enumerate(paciente):
                if col == 3 and isinstance(data, datetime):
                    text = data.strftime('%Y-%m-%d')
                else:
                    text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, pid=paciente_id, pdata=paciente, r_labels=row_labels: self.select_paciente(pid, pdata, r_labels))
                
                row_labels.append(label)


    def select_paciente(self, paciente_id, paciente_data, current_row_labels):
        """Maneja la selección de un paciente, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_paciente_id = paciente_id
        
        self.msg_label.configure(text=f"Paciente ID {paciente_id} seleccionado.", text_color="blue")
        
        self.entry_fecha.configure(state="normal") 

        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        self.entry_fecha.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        
        self.entry_nombre.insert(0, paciente_data[1])
        self.entry_apellido.insert(0, paciente_data[2])
        
        fecha_nacimiento = paciente_data[3].strftime('%Y-%m-%d') if isinstance(paciente_data[3], datetime) else str(paciente_data[3])
        self.entry_fecha.insert(0, fecha_nacimiento)
        
        self.entry_telefono.insert(0, paciente_data[4])
        self.entry_direccion.insert(0, paciente_data[5])
        
        self.entry_fecha.configure(state="readonly")


    def action_crear(self):
        """Maneja la creación de un nuevo paciente."""
        try:
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            fecha = self.entry_fecha.get()
            telefono = self.entry_telefono.get()
            direccion = self.entry_direccion.get()
            
            if not all([nombre, apellido, fecha, telefono]):
                self.msg_label.configure(text="Error: Faltan campos obligatorios.", text_color="red")
                return

            if self.paciente_service.crear_paciente(nombre, apellido, fecha, telefono, direccion):
                self.msg_label.configure(text=f"Paciente {nombre} {apellido} creado.", text_color="green")
                self.load_pacientes() 
                self.clear_entries()  
            else:
                self.msg_label.configure(text="Error al crear el paciente.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_actualizar(self):
        """Maneja la actualización de un paciente existente."""
        if not self.selected_paciente_id:
            self.msg_label.configure(text="Error: Seleccione un paciente primero.", text_color="red")
            return
            
        try:
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            fecha = self.entry_fecha.get()
            telefono = self.entry_telefono.get()
            direccion = self.entry_direccion.get()

            if self.paciente_service.actualizar_paciente(self.selected_paciente_id, nombre, apellido, fecha, telefono, direccion):
                self.msg_label.configure(text=f"Paciente ID {self.selected_paciente_id} actualizado.", text_color="green")
                self.load_pacientes() 
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al actualizar el paciente.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: {e}", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de un paciente."""
        if not self.selected_paciente_id:
            self.msg_label.configure(text="Error: Seleccione un paciente para eliminar.", text_color="red")
            return

        if self.paciente_service.eliminar_paciente(self.selected_paciente_id):
            self.msg_label.configure(text=f"🗑️ Paciente ID {self.selected_paciente_id} eliminado.", text_color="orange")
            self.load_pacientes()
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al eliminar el paciente. (Verifique si tiene citas asociadas).", text_color="red")


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
        self.entry_fecha.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        self.selected_paciente_id = None

        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
        
        self.entry_fecha.configure(state="normal") 
        self.entry_fecha.delete(0, 'end')
        self.entry_fecha.configure(state="readonly") 
        
        self.entry_telefono.delete(0, 'end')
        self.entry_direccion.delete(0, 'end')
        self.selected_paciente_id = None
        

    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView