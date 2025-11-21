import customtkinter as ctk
from services.cita_service import CitaService
from services.paciente_service import PacienteService
from services.doctores_service import DoctorService
from datetime import datetime
from tkcalendar import Calendar 
import tkinter as tk

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class CitaView(ctk.CTkFrame):
    
    title = "Gestión de citas"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.cita_service = CitaService()
        self.paciente_service = PacienteService()
        self.doctor_service = DoctorService()
        
        self.citas_data = [] 
        self.selected_cita_id = None
        self.selected_row_labels = [] 
        
        self.pacientes_map = {} 
        self.doctores_map = {}
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Lista de citas (por fecha)", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        self.create_combobox_row(self.action_frame, 0, "Paciente:", "combobox_paciente", 0, "Doctor:", "combobox_doctor", 2)
        
        ctk.CTkLabel(self.action_frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.entry_fecha = ctk.CTkEntry(self.action_frame, state="readonly", width=120) 
        self.entry_fecha.grid(row=1, column=1, padx=(10, 5), pady=5, sticky="w")
        
        self.btn_fecha_picker = ctk.CTkButton(self.action_frame, text="📅", width=30, command=self.open_datepicker)
        self.btn_fecha_picker.grid(row=1, column=1, padx=(140, 10), pady=5, sticky="w")
        
        ctk.CTkLabel(self.action_frame, text="Hora (HH:MM:SS):").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        self.entry_hora = ctk.CTkEntry(self.action_frame, state="readonly", width=120) 
        self.entry_hora.grid(row=1, column=3, padx=(10, 5), pady=5, sticky="w")
        
        self.btn_hora_picker = ctk.CTkButton(self.action_frame, text="⏱️", width=30, command=self.open_timepicker)
        self.btn_hora_picker.grid(row=1, column=3, padx=(140, 10), pady=5, sticky="w")

        ctk.CTkLabel(self.action_frame, text="Motivo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_motivo = ctk.CTkEntry(self.action_frame)
        self.entry_motivo.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew") 
        
        ctk.CTkLabel(self.action_frame, text="Estado:").grid(row=2, column=3, padx=10, pady=5, sticky="w") 
        self.combobox_estado = ctk.CTkComboBox(self.action_frame, values=["Pendiente", "Completada", "Cancelada"])
        self.combobox_estado.grid(row=2, column=3, padx=10, pady=5, sticky="e") 
        
        btn_crear = ctk.CTkButton(self.action_frame, text="Crear Cita", command=self.action_crear)
        btn_crear.grid(row=3, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=3, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=3, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=4, column=0, columnspan=4, pady=(0, 10))

        self.load_relations()
        self.load_citas()
        

    def create_combobox_row(self, container, row, label1, attr1, col1, label2, attr2, col2):
        """Función auxiliar para crear pares de etiquetas y ComboBoxes en una fila."""
        ctk.CTkLabel(container, text=label1).grid(row=row, column=col1, padx=10, pady=5, sticky="w")
        combo1 = ctk.CTkComboBox(container, values=["Cargando..."])
        combo1.grid(row=row, column=col1 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr1, combo1)
        
        ctk.CTkLabel(container, text=label2).grid(row=row, column=col2, padx=10, pady=5, sticky="w")
        combo2 = ctk.CTkComboBox(container, values=["Cargando..."])
        combo2.grid(row=row, column=col2 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr2, combo2)

    def open_datepicker(self):
        """Abre una ventana de calendario modal para seleccionar la fecha."""
        
        top = tk.Toplevel(self)
        top.title("Seleccionar Fecha")
        
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
        
    def open_timepicker(self):
        """Abre una ventana modal para seleccionar la hora."""
        
        top = tk.Toplevel(self)
        top.title("Seleccionar Hora")
        
        current_time_str = self.entry_hora.get()
        try:
            current_time = datetime.strptime(current_time_str, '%H:%M:%S').time()
        except ValueError:
            current_time = datetime.now().time()
            
        current_h = current_time.hour
        current_m = current_time.minute
        current_s = current_time.second
        
        
        time_frame = ctk.CTkFrame(top)
        time_frame.pack(padx=20, pady=20)
        
        ctk.CTkLabel(time_frame, text="Hora:").grid(row=0, column=0, padx=5, pady=5)
        var_h = tk.StringVar(value=f"{current_h:02d}")
        spin_h = tk.Spinbox(time_frame, from_=0, to=23, wrap=True, format="%02.0f",
                            width=4, textvariable=var_h, state="readonly")
        spin_h.grid(row=1, column=0, padx=5, pady=5)
        
        ctk.CTkLabel(time_frame, text="Minuto:").grid(row=0, column=1, padx=5, pady=5)
        var_m = tk.StringVar(value=f"{current_m:02d}")
        spin_m = tk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f",
                            width=4, textvariable=var_m, state="readonly")
        spin_m.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(time_frame, text="Segundo:").grid(row=0, column=2, padx=5, pady=5)
        var_s = tk.StringVar(value=f"{current_s:02d}")
        spin_s = tk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f",
                            width=4, textvariable=var_s, state="readonly")
        spin_s.grid(row=1, column=2, padx=5, pady=5)
        
        def set_time():
            h = var_h.get()
            m = var_m.get()
            s = var_s.get()
            selected_time = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
            
            self.entry_hora.configure(state="normal") 
            self.entry_hora.delete(0, 'end')
            self.entry_hora.insert(0, selected_time)
            self.entry_hora.configure(state="readonly") 
            top.destroy() 

        ctk.CTkButton(top, text="Aceptar", command=set_time).pack(pady=(0, 20))
        
        top.grab_set() 
        top.update_idletasks()
        width = top.winfo_width()
        height = top.winfo_height()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (width // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (height // 2)
        top.geometry(f'{width}x{height}+{x}+{y}')
        top.resizable(False, False)


    def load_relations(self):
        """Carga los pacientes y doctores para los ComboBoxes."""
        
        pacientes_db = self.paciente_service.obtener_todos_pacientes()
        nombres_pacientes = []
        self.pacientes_map = {}
        for p_id, nombre, apellido, _, _, _ in pacientes_db:
            nombre_completo = f"{nombre} {apellido} (ID: {p_id})"
            nombres_pacientes.append(nombre_completo)
            self.pacientes_map[nombre_completo] = p_id
            
        self.combobox_paciente.configure(values=nombres_pacientes)
        if nombres_pacientes:
            self.combobox_paciente.set(nombres_pacientes[0])
            
        doctores_db = self.doctor_service.obtener_todos_doctores()
        nombres_doctores = []
        self.doctores_map = {}
        for d_id, nombre, apellido, especialidad, _, _ in doctores_db: 
            nombre_completo = f"{nombre} {apellido} ({especialidad}, ID: {d_id})"
            nombres_doctores.append(nombre_completo)
            self.doctores_map[nombre_completo] = d_id
            
        self.combobox_doctor.configure(values=nombres_doctores)
        if nombres_doctores:
            self.combobox_doctor.set(nombres_doctores[0])
            
    
    def load_citas(self):
        """Carga las citas de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.citas_data = self.cita_service.obtener_todas_citas()
        self.selected_cita_id = None
        self.selected_row_labels = [] 

        if not self.citas_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay citas registradas.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Fecha/Hora", "Paciente", "Doctor", "Motivo", "Estado"]
        
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)

        for i, cita in enumerate(self.citas_data):
            cita_id = cita[0]
            fecha_hora = cita[1].strftime('%Y-%m-%d %H:%M')
            motivo = cita[2]
            estado = cita[3]
            paciente_nombre = f"{cita[4]} {cita[5]}"
            doctor_nombre = f"{cita[6]} {cita[7]}"
            
            display_data = [cita_id, fecha_hora, paciente_nombre, doctor_nombre, motivo, estado]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            row_labels = []
            
            for col, data in enumerate(display_data): 
                text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, cid=cita_id, cdata=cita, r_labels=row_labels: self.select_cita(cid, cdata, r_labels))
                
                row_labels.append(label)

    def select_cita(self, cita_id, cita_data, current_row_labels):
        """Maneja la selección de una cita, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_cita_id = cita_id
        
        self.msg_label.configure(text=f"Cita ID {cita_id} seleccionada.", text_color="blue")
        
        self.entry_fecha.configure(state="normal") 
        self.entry_hora.configure(state="normal") 
        
        self.clear_entries(keep_selection=True) 

        cita_detalles = self.cita_service.obtener_cita_por_id(cita_id)
        
        if cita_detalles:
            p_id_selected = cita_detalles[1]
            d_id_selected = cita_detalles[2]
            fecha_hora_dt = cita_detalles[3]
            motivo_selected = cita_detalles[4]
            estado_selected = cita_detalles[5]

            self.entry_fecha.insert(0, fecha_hora_dt.strftime('%Y-%m-%d'))
            self.entry_hora.insert(0, fecha_hora_dt.strftime('%H:%M:%S'))
            self.entry_motivo.insert(0, motivo_selected)
            self.combobox_estado.set(estado_selected)
            
            paciente_nombre_map = {v: k for k, v in self.pacientes_map.items()}
            doctor_nombre_map = {v: k for k, v in self.doctores_map.items()}
            
            if p_id_selected in paciente_nombre_map:
                self.combobox_paciente.set(paciente_nombre_map[p_id_selected])
            if d_id_selected in doctor_nombre_map:
                self.combobox_doctor.set(doctor_nombre_map[d_id_selected])
                
        self.entry_fecha.configure(state="readonly")
        self.entry_hora.configure(state="readonly")


    def action_crear(self):
        """Maneja la creación de una nueva cita."""
        try:
            paciente_nombre = self.combobox_paciente.get()
            doctor_nombre = self.combobox_doctor.get()
            fecha_str = self.entry_fecha.get()
            hora_str = self.entry_hora.get()
            motivo = self.entry_motivo.get()
            estado = self.combobox_estado.get()
            
            paciente_id = self.pacientes_map.get(paciente_nombre)
            doctor_id = self.doctores_map.get(doctor_nombre)
            fecha_hora = f"{fecha_str} {hora_str}"

            if not all([paciente_id, doctor_id, fecha_str, hora_str, motivo]):
                self.msg_label.configure(text="Error: Complete los campos de Paciente, Doctor, Fecha, Hora y Motivo.", text_color="red")
                return

            if self.cita_service.crear_cita(paciente_id, doctor_id, fecha_hora, motivo):
                self.msg_label.configure(text=f"Cita agendada para Paciente ID {paciente_id}.", text_color="green")
                self.load_citas() 
                self.clear_entries()  
            else:
                self.msg_label.configure(text="Error al crear la cita.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: Revise formato de Fecha/Hora. {e}", text_color="red")


    def action_actualizar(self):
        """Maneja la actualización de una cita existente."""
        if not self.selected_cita_id:
            self.msg_label.configure(text="Error: Seleccione una cita primero.", text_color="red")
            return
            
        try:
            paciente_nombre = self.combobox_paciente.get()
            doctor_nombre = self.combobox_doctor.get()
            fecha_str = self.entry_fecha.get()
            hora_str = self.entry_hora.get()
            motivo = self.entry_motivo.get()
            estado = self.combobox_estado.get()
            
            paciente_id = self.pacientes_map.get(paciente_nombre)
            doctor_id = self.doctores_map.get(doctor_nombre)
            fecha_hora = f"{fecha_str} {hora_str}"

            if self.cita_service.actualizar_cita(self.selected_cita_id, paciente_id, doctor_id, fecha_hora, motivo, estado):
                self.msg_label.configure(text=f"Cita ID {self.selected_cita_id} actualizada.", text_color="green")
                self.load_citas() 
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al actualizar la cita.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error en datos: Revise formato de Fecha/Hora. {e}", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de una cita."""
        if not self.selected_cita_id:
            self.msg_label.configure(text="Error: Seleccione una cita para eliminar.", text_color="red")
            return

        if self.cita_service.eliminar_cita(self.selected_cita_id):
            self.msg_label.configure(text=f"Cita ID {self.selected_cita_id} eliminada.", text_color="orange")
            self.load_citas()
            self.clear_entries()
        else:
            self.msg_label.configure(text="Error al eliminar la cita. (Verifique si tiene historial asociado).", text_color="red")


    def clear_entries(self, keep_selection=False):
        """Limpia todos los campos de entrada y la selección."""
        
        if not keep_selection and self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
            self.selected_row_labels = []
            self.selected_cita_id = None
            
        is_readonly_fecha = self.entry_fecha.cget("state") == "readonly"
        if is_readonly_fecha:
            self.entry_fecha.configure(state="normal")
            
        is_readonly_hora = self.entry_hora.cget("state") == "readonly"
        if is_readonly_hora:
            self.entry_hora.configure(state="normal")
            
        self.entry_fecha.delete(0, 'end')
        self.entry_hora.delete(0, 'end')
        self.entry_motivo.delete(0, 'end')
        
        if is_readonly_fecha:
            self.entry_fecha.configure(state="readonly")
        if is_readonly_hora:
            self.entry_hora.configure(state="readonly")
        
        if self.combobox_paciente.cget("values"):
            self.combobox_paciente.set(self.combobox_paciente.cget("values")[0])
        if self.combobox_doctor.cget("values"):
            self.combobox_doctor.set(self.combobox_doctor.cget("values")[0])
        self.combobox_estado.set("Pendiente")
        

    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView