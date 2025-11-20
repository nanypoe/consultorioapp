from gui.app import App
from db.conexion import ConexionDB 

if __name__ == "__main__":
    app = App()
    app.mainloop()
    ConexionDB().desconectar()