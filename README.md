# Proyecto Final Curso de Programación
## Sistema de Gestión de consultorio médico

Este proyecto es un Sistema de Gestión de Citas y Pacientes desarrollado en Python utilizando CustomTkinter para la interfaz gráfica y MySQL como backend.

## 🛠️ Tecnologías Utilizadas

* **GUI:** CustomTkinter
* **Base de Datos:** MySQL
* **Conector:** mysql-connector-python
* **Reportes:** Pandas (Excel), FPDF (PDF)

## 📦 Estructura del Proyecto

* `db/`: Módulos de conexión y configuración de la base de datos.
* `gui/`: Módulos de las vistas (ventanas) de la aplicación.
* `services/`: Módulos de la lógica de negocio (CRUD, Reportes, etc.).
* `main.py`: Punto de entrada de la aplicación.

## ⚙️ Configuración e instalación

### 1. Requisitos Previos

1.  **Python 3.x:** Asegúrese de tener Python instalado.
2.  **MySQL/MariaDB:** Debe tener un servidor de MySQL activo (ej. a través de XAMPP o WAMP).

### 2. Instalación de Dependencias

1.  Clone este repositorio: `git clone [URL_DEL_REPOSITORIO]`
2.  Navegue a la carpeta del proyecto.
3.  Cree y active un entorno virtual (recomendado).
4.  Instale las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuración de la Base de Datos

1.  Verifique el archivo `db/config.py` y ajuste las credenciales de conexión (`host`, `user`, `password`, `database`) si son diferentes a las predeterminadas.
2.  Ejecute el script de inicialización para crear las tablas:
    ```bash
    python setup_db.py
    ```

### 4. Ejecución

Ejecute la aplicación principal:

```bash
python main.py