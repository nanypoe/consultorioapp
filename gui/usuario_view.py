import customtkinter as ctk
from services.usuario_service import UsuarioService
from db.conexion import ConexionDB

HEADER_BG = "#7F7F7F" 
ROW_BG_ODD = "#B3B3B3" 
ROW_BG_EVEN = "#999999" 
ROW_BG_SELECTED = "#4682B4"

class UsuarioView(ctk.CTkFrame):
    
    title = "Gestión de usuarios"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.usuario_service = UsuarioService()
        
        self.usuarios_data = [] 
        self.selected_usuario_id = None
        self.selected_row_labels = [] 
        
        self.ROLES = self.get_enum_roles()

        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=0) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.list_container = ctk.CTkFrame(self)
        self.list_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_container, label_text="Lista de Usuarios", label_font=ctk.CTkFont(size=14, weight="bold"))
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 
        
        
        self.create_entry_row(self.action_frame, 0, "Usuario:", "entry_nombre_usuario", 0, "Contraseña:", "entry_contrasena", 2, is_password=True)
        
        ctk.CTkLabel(self.action_frame, text="Nombre Completo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre_completo = ctk.CTkEntry(self.action_frame)
        self.entry_nombre_completo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.action_frame, text="Rol:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.combobox_rol = ctk.CTkComboBox(self.action_frame, values=self.ROLES)
        self.combobox_rol.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        btn_crear = ctk.CTkButton(self.action_frame, text="Crear Nuevo", command=self.action_crear)
        btn_crear.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        btn_actualizar = ctk.CTkButton(self.action_frame, text="Actualizar (Datos/Rol)", command=self.action_actualizar, fg_color="#FF8C00", hover_color="#B87333")
        btn_actualizar.grid(row=2, column=1, padx=10, pady=15, sticky="ew")

        btn_eliminar = ctk.CTkButton(self.action_frame, text="Eliminar", command=self.action_eliminar, fg_color="red", hover_color="#800000")
        btn_eliminar.grid(row=2, column=2, padx=10, pady=15, sticky="ew")
        
        btn_volver = ctk.CTkButton(self.action_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=2, column=3, padx=10, pady=15, sticky="ew")
        
        self.msg_label = ctk.CTkLabel(self.action_frame, text="", text_color="green")
        self.msg_label.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.load_usuarios()

    def get_enum_roles(self):
        """Intenta obtener los valores del ENUM de la columna 'rol' de la tabla 'Usuarios'."""
        try:
            db = ConexionDB()
            sql = "SELECT COLUMN_TYPE FROM information_schema.COLUMNS WHERE TABLE_NAME = 'Usuarios' AND COLUMN_NAME = 'rol' AND TABLE_SCHEMA = 'consultorio_db'"
            result = db.ejecutar_consulta(sql, fetch_one=True)
            
            if result:
                enum_str = result[0].split('(')[1].split(')')[0]
                roles = [role.strip("'") for role in enum_str.split(',')]
                return roles
            else:
                return ['Administrador', 'Secretario', 'Doctor']
        except Exception as e:
            print(f"Error al obtener roles ENUM: {e}")
            return ['Administrador', 'Secretario', 'Doctor']

    def create_entry_row(self, container, row, label1, attr1, col1, label2, attr2, col2, is_password=False):
        """Función auxiliar para crear pares de etiquetas y entradas en una fila."""
        ctk.CTkLabel(container, text=label1).grid(row=row, column=col1, padx=10, pady=5, sticky="w")
        entry1 = ctk.CTkEntry(container)
        entry1.grid(row=row, column=col1 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr1, entry1) 
        
        ctk.CTkLabel(container, text=label2).grid(row=row, column=col2, padx=10, pady=5, sticky="w")
        if is_password:
            entry2 = ctk.CTkEntry(container, show="*") 
        else:
            entry2 = ctk.CTkEntry(container)
            
        entry2.grid(row=row, column=col2 + 1, padx=10, pady=5, sticky="ew")
        setattr(self, attr2, entry2)

    def load_usuarios(self):
        """Carga los usuarios de la DB y actualiza la lista visual."""
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        self.usuarios_data = self.usuario_service.obtener_todos_usuarios()
        self.selected_usuario_id = None
        self.selected_row_labels = [] 

        if not self.usuarios_data:
            ctk.CTkLabel(self.scroll_frame, text="No hay usuarios registrados.").grid(row=0, column=0, padx=10, pady=10)
            return

        headers = ["ID", "Usuario", "Nombre Completo", "Rol"]
        
        for col, header in enumerate(headers):
             ctk.CTkLabel(self.scroll_frame, text=header, font=ctk.CTkFont(weight="bold"), 
                          fg_color=HEADER_BG, corner_radius=5, anchor="w"
                          ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
             self.scroll_frame.grid_columnconfigure(col, weight=1)

        for i, usuario in enumerate(self.usuarios_data):
            usuario_id = usuario[0]
            
            row_bg_color = ROW_BG_EVEN if i % 2 == 0 else ROW_BG_ODD
            row_labels = []
            
            for col, data in enumerate(usuario): 
                text = str(data)
                    
                label = ctk.CTkLabel(self.scroll_frame, text=text, width=70, anchor="w",
                                     fg_color=row_bg_color, corner_radius=0)
                
                label.grid(row=i + 1, column=col, padx=1, pady=1, sticky="ew") 
               
                label.bind("<Button-1>", lambda event, uid=usuario_id, udata=usuario, r_labels=row_labels: self.select_usuario(uid, udata, r_labels))
                
                row_labels.append(label)


    def select_usuario(self, usuario_id, usuario_data, current_row_labels):
        """Maneja la selección de un usuario, llena el formulario y resalta la fila."""
        
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
        
        for label in current_row_labels:
            label.configure(fg_color=ROW_BG_SELECTED)
            
        self.selected_row_labels = current_row_labels
        self.selected_usuario_id = usuario_id
        
        self.msg_label.configure(text=f"Usuario ID {usuario_id} seleccionado: {usuario_data[1]}", text_color="blue")
        
        self.entry_nombre_usuario.delete(0, 'end')
        self.entry_contrasena.delete(0, 'end')
        self.entry_nombre_completo.delete(0, 'end')

        self.entry_nombre_usuario.insert(0, usuario_data[1])
        self.entry_contrasena.insert(0, "") 
        self.entry_nombre_completo.insert(0, usuario_data[2])
        
        self.combobox_rol.set(usuario_data[3]) 


    def action_crear(self):
        """Maneja la creación de un nuevo usuario."""
        try:
            nombre_usuario = self.entry_nombre_usuario.get()
            contrasena = self.entry_contrasena.get()
            nombre_completo = self.entry_nombre_completo.get()
            rol = self.combobox_rol.get()
            
            if not all([nombre_usuario, contrasena, nombre_completo, rol]):
                self.msg_label.configure(text="Error: Faltan campos obligatorios.", text_color="red")
                return

            if self.usuario_service.crear_usuario(nombre_usuario, contrasena, nombre_completo, rol):
                self.msg_label.configure(text=f"Usuario {nombre_usuario} creado.", text_color="green")
                self.load_usuarios() 
                self.clear_entries()  
            else:
                self.msg_label.configure(text="Error al crear el usuario (¿Ya existe el nombre de usuario?).", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error al crear: {e}", text_color="red")


    def action_actualizar(self):
        """Maneja la actualización de un usuario existente (solo Nombre, Rol)."""
        if not self.selected_usuario_id:
            self.msg_label.configure(text="Error: Seleccione un usuario primero.", text_color="red")
            return
            
        nombre_completo = self.entry_nombre_completo.get()
        rol = self.combobox_rol.get()
        contrasena_nueva = self.entry_contrasena.get() 
        
        if not all([nombre_completo, rol]):
            self.msg_label.configure(text="Error: El nombre completo y el rol son obligatorios.", text_color="red")
            return

        try:
            db = ConexionDB()
            
            if contrasena_nueva:
                sql = "UPDATE Usuarios SET nombre_completo = %s, rol = %s, contrasena = %s WHERE id = %s"
                params = (nombre_completo, rol, contrasena_nueva, self.selected_usuario_id)
            else:
                sql = "UPDATE Usuarios SET nombre_completo = %s, rol = %s WHERE id = %s"
                params = (nombre_completo, rol, self.selected_usuario_id)

            resultado = db.ejecutar_consulta(sql, params=params)
                
            if resultado:
                msg = f"Usuario ID {self.selected_usuario_id} actualizado."
                if contrasena_nueva:
                     msg += " (Contraseña cambiada)"
                self.msg_label.configure(text=msg, text_color="green")
                self.load_usuarios() 
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al actualizar el usuario.", text_color="red")
                
        except Exception as e:
            self.msg_label.configure(text=f"Error al actualizar: {e}", text_color="red")


    def action_eliminar(self):
        """Maneja la eliminación de un usuario."""
        if not self.selected_usuario_id:
            self.msg_label.configure(text="Error: Seleccione un usuario para eliminar.", text_color="red")
            return

        try:
            db = ConexionDB()
            sql = "DELETE FROM Usuarios WHERE id = %s"
            resultado = db.ejecutar_consulta(sql, params=(self.selected_usuario_id,))
            
            if resultado:
                self.msg_label.configure(text=f"Usuario ID {self.selected_usuario_id} eliminado.", text_color="orange")
                self.load_usuarios()
                self.clear_entries()
            else:
                self.msg_label.configure(text="Error al eliminar el usuario.", text_color="red")
        except Exception as e:
            self.msg_label.configure(text=f"Error al eliminar: {e}", text_color="red")


    def clear_entries(self):
        """Limpia todos los campos de entrada y la selección."""
        if self.selected_row_labels:
            for label in self.selected_row_labels:
                row_index = label.grid_info()['row']
                row_bg_color = ROW_BG_EVEN if (row_index - 1) % 2 == 0 else ROW_BG_ODD
                label.configure(fg_color=row_bg_color)
            self.selected_row_labels = []
            
        self.entry_nombre_usuario.delete(0, 'end')
        self.entry_contrasena.delete(0, 'end')
        self.entry_nombre_completo.delete(0, 'end')
        
        if self.ROLES:
            self.combobox_rol.set(self.ROLES[0])
            
        self.selected_usuario_id = None
        

    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView