-- Schema para la base de datos del Gestor de Tareas

-- Tabla de tareas
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    prioridad INTEGER DEFAULT 3,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_limite DATETIME,
    estimacion_horas REAL DEFAULT 0.0,
    CONSTRAINT chk_prioridad CHECK (prioridad BETWEEN 1 AND 5),
    CONSTRAINT chk_estado CHECK (estado IN ('pendiente', 'en_progreso', 'completada'))
);

-- Tabla de dependencias (aristas del grafo)
CREATE TABLE IF NOT EXISTS dependencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarea_origen INTEGER NOT NULL,
    tarea_destino INTEGER NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tarea_origen) REFERENCES tareas(id) ON DELETE CASCADE,
    FOREIGN KEY (tarea_destino) REFERENCES tareas(id) ON DELETE CASCADE,
    CONSTRAINT unica_dependencia UNIQUE(tarea_origen, tarea_destino),
    CONSTRAINT no_auto_dependencia CHECK (tarea_origen != tarea_destino)
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_estado ON tareas(estado);
CREATE INDEX IF NOT EXISTS idx_prioridad ON tareas(prioridad);
CREATE INDEX IF NOT EXISTS idx_dependencias_origen ON dependencias(tarea_origen);
CREATE INDEX IF NOT EXISTS idx_dependencias_destino ON dependencias(tarea_destino);