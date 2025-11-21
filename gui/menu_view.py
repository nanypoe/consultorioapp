import customtkinter as ctk
from gui.paciente_view import PacienteView
from gui.doctor_view import DoctorView
from gui.cita_view import CitaView
from gui.usuario_view import UsuarioView
from gui.historial_view import HistorialView
from gui.servicios_view import ServiciosView
from gui.reportes_view import ReportesView

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
        
        
        self.crear_boton(button_container, "Gestión de pacientes", 0, 0, self.open_pacientes, "Manejar pacientes")
        self.crear_boton(button_container, "Gestión de doctores", 0, 1, self.open_doctores, "Manejar doctores")
        self.crear_boton(button_container, "Agendar citas", 1, 0, self.open_citas, "Manejar citas")
        self.crear_boton(button_container, "Reportes del sistema", 1, 1, self.open_reportes, "Generar reportes")
        self.crear_boton(button_container, "Historial del paciente", 2, 1, self.open_historiales, "Ver y gestionar historiales médicos")
        self.crear_boton(button_container, "Servicios y costos", 3, 0, self.open_servicios, "Ver y gestionar servicios y costos")

        if rol == 'Administrador':
            self.crear_boton(button_container, "Gestión de usuarios", 2, 0, self.open_usuarios, "Manejar usuarios y roles")

        ctk.CTkButton(self, text="Cerrar Sesión", command=self.app.logout, fg_color="red", hover_color="#800000").grid(row=3, column=0, pady=(0, 20), sticky="s")


    def crear_boton(self, container, texto, fila, columna, comando, tooltip):
        """Función auxiliar para crear y posicionar botones de navegación."""
        btn = ctk.CTkButton(container, text=texto, command=comando, width=250, height=40)
        btn.grid(row=fila, column=columna, padx=20, pady=20, sticky="ew")


    def open_pacientes(self):
        self.app.switch_frame(PacienteView)

    def open_doctores(self):
        self.app.switch_frame(DoctorView)

    def open_citas(self):
        self.app.switch_frame(CitaView)
        
    def open_reportes(self):
        self.app.switch_frame(ReportesView)

    def open_usuarios(self):
        self.app.switch_frame(UsuarioView)
    
    def open_historiales(self):
        self.app.switch_frame(HistorialView)

    def open_servicios(self):
        self.app.switch_frame(ServiciosView)