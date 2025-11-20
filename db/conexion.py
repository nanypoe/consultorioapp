import pymysql
import traceback
from pymysql import Error

class ConexionDB:
    _DATABASE = { 
        'host': '127.0.0.1', 
        'database': 'consultorio_db', 
        'user': 'root', 
        'password': '',
        'port': 3306,
    }

    _instancia = None
    _conexion = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
        return cls._instancia

    def conectar(self):
        if self._conexion is None or not (hasattr(self._conexion, 'ping') and self._conexion.ping(reconnect=True)):
            print("Intentando conectar a la base de datos...")
            try:
                self._conexion = pymysql.connect(
                    host=self._DATABASE['host'],
                    user=self._DATABASE['user'],
                    password=self._DATABASE['password'],
                    database=self._DATABASE['database'],
                    port=self._DATABASE['port']
                )
                print("Conexión a MySQL establecida con éxito.")
                return True
            except Exception as e:
                print("==============================================")
                print("ERROR CRÍTICO DETECTADO DURANTE LA CONEXIÓN")
                print("==============================================")
                print(f"Error: {e}")
                traceback.print_exc()
                print("==============================================")
                self._conexion = None
                return False
        return True

    def desconectar(self):
        if self._conexion is not None:
            self._conexion.close()
            self._conexion = None
            print("Conexión a MySQL cerrada.")

    def obtener_conexion(self):
        if self.conectar():
            return self._conexion
        return None

    def ejecutar_consulta(self, sql_query, params=None, fetch_one=False):
        conn = self.obtener_conexion()
        if conn is None:
            return None

        is_write_op = sql_query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE'))
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, params or ())
                if is_write_op:
                    conn.commit() 
                    return True 
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except Error as e:
            print(f"Error en la ejecución de la consulta: {e}")
            if is_write_op and conn:
                conn.rollback() 
            return None