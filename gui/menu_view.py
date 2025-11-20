import customtkinter as ctk

class MenuView(ctk.CTkFrame):
    
    title = "Menú Principal"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        
        _, nombre_completo, rol = self.app.user_session
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 5))
        ctk.CTkLabel(self, text=f"Bienvenido(a), {nombre_completo} ({rol})", font=ctk.CTkFont(size=16)).grid(row=1, column=0, pady=(0, 5))
        
        button_container = ctk.CTkFrame(self)
        button_container.grid(row=2, column=0, padx=50, pady=(20, 50), sticky="n")
        
        button_container.grid_columnconfigure((0, 1), weight=1)
        
        
        self.crear_boton(button_container, "Gestión de Pacientes", 0, 0, self.open_pacientes, "Manejar pacientes")
        self.crear_boton(button_container, "Gestión de Doctores", 0, 1, self.open_doctores, "Manejar doctores")
        self.crear_boton(button_container, "Agendar Citas", 1, 0, self.open_citas, "Manejar citas")
        self.crear_boton(button_container, "Reportes del Sistema", 1, 1, self.open_reportes, "Generar reportes")

        if rol == 'Administrador':
            self.crear_boton(button_container, "Gestión de Usuarios", 2, 0, self.open_usuarios, "Manejar usuarios y roles")
            self.crear_boton(button_container, "Catálogos (Especialidades)", 2, 1, self.open_catalogos, "Manejar especialidades")

        ctk.CTkButton(self, text="Cerrar Sesión", command=self.app.logout, fg_color="red", hover_color="#800000").grid(row=3, column=0, pady=(0, 20), sticky="s")


    def crear_boton(self, container, texto, fila, columna, comando, tooltip):
        """Función auxiliar para crear y posicionar botones de navegación."""
        btn = ctk.CTkButton(container, text=texto, command=comando, width=250, height=40)
        btn.grid(row=fila, column=columna, padx=20, pady=20, sticky="ew")


    def open_pacientes(self):
        print("Navegando a Gestión de Pacientes...")

    def open_doctores(self):
        print("Navegando a Gestión de Doctores...")

    def open_citas(self):
        print("Navegando a Gestión de Citas...")
        
    def open_reportes(self):
        print("Navegando a Reportes...")

    def open_usuarios(self):
        print("Navegando a Gestión de Usuarios...")

    def open_catalogos(self):
        print("Navegando a Catálogos (Especialidades)...")