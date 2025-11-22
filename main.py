import customtkinter as ctk
from gui.login_view import LoginView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Consultorio Médico")
        self.geometry("1000x700")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue") 
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self.switch_frame(LoginView)

    def switch_frame(self, frame_class):
        """Muestra una nueva ventana (frame) y oculta la actual."""
        
        
        new_frame = frame_class(self.container, self)
        
        if self.frames.get(frame_class) is not None:
             frame = self.frames[frame_class]
        else:
             frame = new_frame
             self.frames[frame_class] = frame

        for f in self.container.winfo_children():
            f.grid_forget()
            
        frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()