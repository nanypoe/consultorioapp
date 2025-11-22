# Curso de programación | Proyecto final
## Sistema de gestión de consultorio médico

Este proyecto es un **Sistema de Gestión de Citas y Pacientes** desarrollado en Python, diseñado para modernizar y agilizar los procesos administrativos de un consultorio médico. Utiliza una arquitectura modular (MVC), **CustomTkinter** para una interfaz gráfica moderna y **MySQL** para una gestión de datos robusta.

---

## Tecnologías utilizadas

* **Lenguaje:** Python 3.10+
* **GUI:** CustomTkinter (Interfaz moderna y responsiva)
* **Base de Datos:** MySQL / MariaDB
* **Conector DB:** PyMySQL
* **Reportes:**
    * *Pandas / Openpyxl:* Generación de reportes en Excel.
    * *FPDF:* Generación de reportes en PDF.
* **Utilidades:** tkcalendar (Selector de fechas).

---

## Estructura del proyecto

La aplicación sigue una arquitectura modular estricta para facilitar el mantenimiento:

* `db/`: Contiene la lógica de conexión (Singleton) y configuración de la base de datos.
* `gui/`: Contiene todas las clases de la interfaz gráfica (Vistas/Ventanas).
* `services/`: Contiene la lógica de negocio y acceso a datos (CRUDs) separados por entidad.
* `reportes_generados/`: Carpeta donde se guardan automáticamente los archivos PDF y Excel creados.
* `main.py`: Punto de entrada principal de la aplicación.

---

## Configuración e instalación

### 1. Requisitos Previos
* **Python 3.x:** Asegúrese de tener Python instalado y agregado al PATH.
* **MySQL/MariaDB:** Debe tener un servidor de MySQL activo (ej. a través de XAMPP, WAMP o instalación nativa).

### 2. Instalación de Dependencias
1.  Clone este repositorio o descargue el código fuente.
2.  Navegue a la carpeta del proyecto en su terminal.
3.  **(Opcional pero recomendado)** Cree y active un entorno virtual:

    ```bash
    python -m venv .venv
    
    # En Windows:
    .venv\Scripts\activate
    
    # En Linux/Mac:
    source .venv/bin/activate
    ```

4.  Instale las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuración de la Base de Datos
1.  Asegúrese de que su servicio MySQL esté corriendo (Puerto 3306 por defecto).
2.  Importe el esquema de la base de datos utilizando su gestor favorito (phpMyAdmin, Workbench) o ejecute el script SQL proporcionado en `db/schema.sql`.
3.  Verifique el archivo `db/conexion.py` y ajuste las credenciales (`user`, `password`) si son diferentes a las predeterminadas (`root`/vacío).

### 4. Ejecución
Ejecute la aplicación principal desde la terminal:

```bash
python main.py
```

## Manual de Uso

### 1. Inicio de Sesión (Login)
Al iniciar la aplicación, se le solicitarán sus credenciales.

* **Usuario por defecto:** `admin`
* **Contraseña por defecto:** `admin123`

> **Nota:** El sistema valida su rol (**Administrador**, **Médico**, **Secretario**) para habilitar o restringir funciones.

### 2. Navegación (Menú Principal)
El menú principal es su centro de mando. Desde aquí puede acceder a todos los módulos:

* **Gestión de Pacientes:** Registrar, buscar y editar información de pacientes.
* **Gestión de Doctores:** Administrar el personal médico y sus especialidades.
* **Agendar Citas:** Módulo central para programar consultas.
* **Reportes:** Generación de documentos.
* **Gestión de Usuarios:** (Solo Administradores) Crear cuentas para el personal.
* **Catálogos:** (Solo Administradores) Gestionar lista de precios y servicios.

### 3. Gestión de Citas
1.  Vaya a **"Agendar Citas"**.
2.  Seleccione un **Paciente** y un **Doctor** de las listas desplegables.
3.  Use el selector de calendario para la fecha y el selector de tiempo para la hora.
4.  Escriba el motivo de la consulta.
5.  Haga clic en **"Crear Cita"**.
6.  *Para editar:* Haga clic en cualquier cita de la lista, modifique los datos y presione **"Actualizar"**.

### 4. Generación de Reportes
Vaya a la sección de **"Reportes del Sistema"**:

* **Listado de Pacientes (Excel):** Genera un archivo `.xlsx` con toda la base de datos de pacientes. Ideal para análisis externo.
* **Historial Médico (PDF):** Seleccione un paciente específico para generar un documento PDF detallado con todas sus consultas pasadas, diagnósticos y notas de evolución.
* **Citas Pendientes (PDF):** Genera un reporte operativo con todas las citas futuras o pendientes de atención.

### 5. Gestión de Historial Médico (Post-Consulta)
Una vez que una cita ha sido completada:

1.  Vaya al módulo de **Historial Médico**.
2.  Seleccione la cita completada en el desplegable.
3.  Ingrese el **Diagnóstico** y las **Notas de Evolución**.
4.  Guarde el registro. Esto vinculará permanentemente la información clínica a esa cita específica.
