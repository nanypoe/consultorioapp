import customtkinter as ctk
from gui.login_view import LoginView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Gestión de Consultorio - Login")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.current_frame = None
        self.user_session = None 
        
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        self.switch_frame(LoginView)

    def switch_frame(self, frame_class, **kwargs):
        
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        new_frame = frame_class(master=self, app=self, **kwargs)
        self.current_frame = new_frame
        
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        if hasattr(new_frame, 'title'):
            self.title(new_frame.title)

    def logout(self):
        
        self.user_session = None
        self.title("Sistema de Gestión de Consultorio - Login")
        self.switch_frame(LoginView)


if __name__ == "__main__":
    app = App()
    app.mainloop()