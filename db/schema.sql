CREATE DATABASE IF NOT EXISTS consultorio_db;
USE consultorio_db;

CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Secretario', 'Doctor') NOT NULL DEFAULT 'Secretario'
);

CREATE TABLE IF NOT EXISTS Pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    direccion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Doctores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    licencia_medica VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    doctor_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    motivo TEXT,
    estado ENUM('Pendiente', 'Confirmada', 'Completada', 'Cancelada') NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(id),
    FOREIGN KEY (doctor_id) REFERENCES Doctores(id)
);

INSERT INTO Usuarios (nombre_usuario, contrasena, nombre_completo, rol) 
VALUES ('admin', 'admin123', 'Administrador Principal', 'Administrador');

-- ACTUALIZANDO DB PARA MÁS TABLAS
USE consultorio_db;

CREATE TABLE IF NOT EXISTS Especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(100) UNIQUE NOT NULL
);

ALTER TABLE Doctores
ADD especialidad_id INT,
ADD FOREIGN KEY (especialidad_id) REFERENCES Especialidades(id);

CREATE TABLE IF NOT EXISTS Historial_Medico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cita_id INT NOT NULL UNIQUE, 
    diagnostico TEXT,
    notas_evolucion TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cita_id) REFERENCES Citas(id)
);

CREATE TABLE IF NOT EXISTS Servicios_Consultorio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    costo DECIMAL(10, 2) NOT NULL
);

INSERT INTO Especialidades (nombre_especialidad) VALUES ('Medicina General'), ('Pediatría'), ('Odontología'), ('Cardiología');

INSERT INTO Servicios_Consultorio (nombre_servicio, costo) VALUES ('Consulta Estándar', 50.00), ('Revisión Anual', 30.00), ('Extracción Dental', 120.00);