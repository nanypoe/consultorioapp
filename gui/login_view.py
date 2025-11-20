import customtkinter as ctk
from services.usuario_service import UsuarioService 

class LoginView(ctk.CTkFrame):
    
    title = "Acceso al Sistema"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.usuario_service = UsuarioService()

        self.grid_rowconfigure((0, 4), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        
        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=1, pady=(20, 40), sticky="n")

        ctk.CTkLabel(self, text="Usuario:").grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Nombre de usuario", width=300)
        self.entry_usuario.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(self, text="Contraseña:").grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.entry_contrasena = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=300)
        self.entry_contrasena.grid(row=4, column=1, padx=10, pady=(0, 20), sticky="ew")
        
        self.label_mensaje = ctk.CTkLabel(self, text="", text_color="red")
        self.label_mensaje.grid(row=5, column=1, pady=(0, 10))

        self.btn_login = ctk.CTkButton(self, text="Iniciar Sesión", command=self.handle_login, width=300)
        self.btn_login.grid(row=6, column=1, padx=10, pady=(10, 30), sticky="ew")

        self.entry_usuario.insert(0, "admin")
        self.entry_contrasena.insert(0, "admin123")


    def handle_login(self):
        """
        Maneja la lógica del botón Iniciar Sesión.
        """
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        
        session_data = self.usuario_service.autenticar_usuario(usuario, contrasena)

        if session_data:
            self.app.user_session = session_data 
            self.label_mensaje.configure(text="Acceso concedido...", text_color="green")
            
            from gui.menu_view import MenuView 
            
            self.app.after(500, lambda: self.app.switch_frame(MenuView))
            
        else:
            self.label_mensaje.configure(text="Usuario o contraseña incorrectos.", text_color="red")
            self.entry_contrasena.delete(0, 'end')