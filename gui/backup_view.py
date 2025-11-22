import customtkinter as ctk
from services.db_backup_service import DBBackupService
from tkinter import filedialog
import os
from tkinter import messagebox 
import threading 

class BackupView(ctk.CTkFrame):
    
    title = "Respaldo y restauración (BD)"

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.backup_service = DBBackupService()
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 

        ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=20, sticky="n")

        self.action_container = ctk.CTkFrame(self)
        self.action_container.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")
        self.action_container.grid_columnconfigure((0, 1), weight=1)
        self.action_container.grid_rowconfigure((0, 1), weight=1) 

        # Título de Respaldo
        ctk.CTkLabel(self.action_container, text="Crear respaldo (.sql)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=(5, 0), sticky="sw")
        
        # Frame de Respaldo
        self.frame_backup = ctk.CTkFrame(self.action_container, border_width=2) 
        self.frame_backup.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_backup.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame_backup, text="Guarda el estado actual de la base de datos en un archivo .sql.\nArchivos guardados en: db_backups/").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        btn_backup = ctk.CTkButton(self.frame_backup, text="Generar respaldo ahora", command=self.action_backup)
        btn_backup.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Título de Restauración
        ctk.CTkLabel(self.action_container, text="Restaurar BD (Precaución)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=(5, 0), sticky="sw")
        
        # Frame de Restauración
        self.frame_restore = ctk.CTkFrame(self.action_container, border_width=2) 
        self.frame_restore.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_restore.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame_restore, text="ADVERTENCIA: La restauración SOBREESCRIBIRÁ la base de datos actual con los datos del archivo .sql seleccionado. Use con precaución.", text_color="red").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        btn_restore = ctk.CTkButton(self.frame_restore, text="Seleccionar archivo y restaurar", command=self.action_restore, fg_color="red", hover_color="#800000")
        btn_restore.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.footer_frame.grid_columnconfigure(0, weight=1) 
        
        self.msg_label = ctk.CTkLabel(self.footer_frame, text="", text_color="green", anchor="w")
        self.msg_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # NUEVO: Barra de progreso en modo indeterminado
        self.progress_bar = ctk.CTkProgressBar(self.footer_frame, orientation="horizontal", mode="indeterminate")
        # Cambiamos la fila a 1 y movemos el botón Volver a la fila 2
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.progress_bar.set(0) # Inicialmente invisible
        
        btn_volver = ctk.CTkButton(self.footer_frame, text="Volver al Menú", command=lambda: self.app.switch_frame(self.get_menu_view()))
        btn_volver.grid(row=2, column=0, padx=10, pady=(5, 15), sticky="e") # Fila ajustada a 2


    def _update_status(self, success, message, is_backup=False):
        """Helper para actualizar la GUI y detener la barra de progreso de forma segura."""
        
        # Detener y ocultar la barra de progreso
        self.progress_bar.stop()
        self.progress_bar.set(0) 

        if success:
            text = f"Respaldo creado: {message}" if is_backup else f"Restauración exitosa. Reinicie la aplicación para asegurar la conexión. {message}"
            color = "green"
        else:
            text = f"Error de respaldo: {message}" if is_backup else f"Error de Restauración: {message}"
            color = "red"
            
        self.msg_label.configure(text=text, text_color=color)

    def action_backup(self):
        """Ejecuta la creación del respaldo."""
        self.msg_label.configure(text="Generando respaldo...", text_color="blue")
        self.progress_bar.start() # Iniciar barra
        self.update_idletasks() 

        success, message = self.backup_service.crear_respaldo()
        
        # Llamamos al helper para finalizar el proceso
        self._update_status(success, message, is_backup=True)

    def action_restore(self):
        """
        Ejecuta la restauración, pidiendo confirmación al usuario. Delega el trabajo pesado a un hilo.
        """
        
        file_path = filedialog.askopenfilename(
            defaultextension=".sql",
            filetypes=[("Archivos SQL", "*.sql")],
            title="Seleccionar Archivo de Respaldo (.sql)"
        )
        
        if not file_path:
            self.msg_label.configure(text="Restauración cancelada.", text_color="orange")
            return
            
        confirmar = messagebox.askokcancel(
            title="Confirmar Restauración",
            message=f"¿Está SEGURO que desea restaurar la base de datos con el archivo:\n{os.path.basename(file_path)}?\n\n¡TODOS LOS DATOS ACTUALES SE PERDERÁN!",
            icon="warning"
        )
        
        if not confirmar: 
            self.msg_label.configure(text="Restauración cancelada por el usuario.", text_color="orange")
            return

        self.msg_label.configure(text="Iniciando restauración... Esto puede tardar varios segundos.", text_color="blue")
        self.progress_bar.start() # Iniciar barra en modo indeterminado
        self.update_idletasks() 

        # Crear y ejecutar el hilo para la restauración
        restore_thread = threading.Thread(target=self._run_restore, args=(file_path,), daemon=True)
        restore_thread.start()

    def _run_restore(self, file_path):
        """
        Método ejecutado en un hilo separado para no bloquear la GUI.
        """
        
        success, message = self.backup_service.restaurar_respaldo(file_path)
        
        # NECESARIO: Usar self.app.after(0, ...) para garantizar que la actualización de la GUI
        # (incluyendo detener la barra de progreso) se ejecute en el hilo principal.
        self.app.after(0, lambda: self._update_status(success, message, is_backup=False))
            
            
    def get_menu_view(self):
        """Retorna la clase MenuView para la navegación."""
        from gui.menu_view import MenuView
        return MenuView