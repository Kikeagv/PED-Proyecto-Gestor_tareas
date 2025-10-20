"""
Database Manager
Maneja todas las operaciones de base de datos
"""

import sqlite3
import os
from typing import List, Optional, Tuple
from datetime import datetime
from models.tarea import Tarea

class DatabaseManager:
    """Gestor de base de datos SQLite"""

    def __init__(self, db_path: str = "gestor_tareas.db"):
        """
        Inicializa el gestor de base de datos

        Args:
            db_path: Ruta del archivo de base de datos
        """
        self.db_path = db_path
        self.conexion: Optional[sqlite3.Connection] = None
        self.inicializar_db()

    def inicializar_db(self) -> None:
        """Crea las tablas si no existen"""
        self.conectar()

        # Leer y ejecutar el schema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                self.conexion.executescript(schema_sql)
                self.conexion.commit()
        except FileNotFoundError:
            # Si no existe el archivo, crear las tablas directamente
            self.crear_tablas_directamente()

    def crear_tablas_directamente(self) -> None:
        """Crea las tablas directamente sin archivo SQL"""
        cursor = self.conexion.cursor()

        # Tabla tareas
        cursor.execute('''
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
            )
        ''')

        # Tabla dependencias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dependencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea_origen INTEGER NOT NULL,
                tarea_destino INTEGER NOT NULL,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tarea_origen) REFERENCES tareas(id) ON DELETE CASCADE,
                FOREIGN KEY (tarea_destino) REFERENCES tareas(id) ON DELETE CASCADE,
                CONSTRAINT unica_dependencia UNIQUE(tarea_origen, tarea_destino),
                CONSTRAINT no_auto_dependencia CHECK (tarea_origen != tarea_destino)
            )
        ''')

        # Índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_estado ON tareas(estado)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_prioridad ON tareas(prioridad)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dependencias_origen ON dependencias(tarea_origen)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dependencias_destino ON dependencias(tarea_destino)')

        self.conexion.commit()

    def conectar(self) -> None:
        """Establece conexión con la base de datos"""
        if self.conexion is None:
            self.conexion = sqlite3.connect(self.db_path)
            self.conexion.row_factory = sqlite3.Row
            # Habilitar claves foráneas
            self.conexion.execute("PRAGMA foreign_keys = ON")

    def desconectar(self) -> None:
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            self.conexion = None

    # ===== OPERACIONES CRUD PARA TAREAS =====

    def crear_tarea(self, tarea: Tarea) -> int:
        """
        Crea una nueva tarea en la base de datos

        Args:
            tarea: Objeto Tarea a crear

        Returns:
            ID de la tarea creada
        """
        cursor = self.conexion.cursor()

        cursor.execute('''
            INSERT INTO tareas (nombre, descripcion, estado, prioridad,
                              fecha_limite, estimacion_horas)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            tarea.nombre,
            tarea.descripcion,
            tarea.estado,
            tarea.prioridad,
            tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
            tarea.estimacion_horas
        ))

        self.conexion.commit()
        return cursor.lastrowid

    def obtener_tarea(self, tarea_id: int) -> Optional[Tarea]:
        """
        Obtiene una tarea por su ID

        Args:
            tarea_id: ID de la tarea

        Returns:
            Objeto Tarea o None si no existe
        """
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM tareas WHERE id = ?', (tarea_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_tarea(row)
        return None

    def obtener_todas_tareas(self) -> List[Tarea]:
        """
        Obtiene todas las tareas

        Returns:
            Lista de objetos Tarea
        """
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM tareas ORDER BY id')
        rows = cursor.fetchall()

        return [self._row_to_tarea(row) for row in rows]

    def obtener_tareas_por_estado(self, estado: str) -> List[Tarea]:
        """
        Obtiene tareas filtradas por estado

        Args:
            estado: Estado a filtrar

        Returns:
            Lista de tareas con ese estado
        """
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM tareas WHERE estado = ? ORDER BY prioridad DESC', (estado,))
        rows = cursor.fetchall()

        return [self._row_to_tarea(row) for row in rows]

    def actualizar_tarea(self, tarea: Tarea) -> bool:
        """
        Actualiza una tarea existente

        Args:
            tarea: Objeto Tarea con datos actualizados

        Returns:
            True si se actualizó, False en caso contrario
        """
        cursor = self.conexion.cursor()

        cursor.execute('''
            UPDATE tareas
            SET nombre = ?, descripcion = ?, estado = ?, prioridad = ?,
                fecha_limite = ?, estimacion_horas = ?
            WHERE id = ?
        ''', (
            tarea.nombre,
            tarea.descripcion,
            tarea.estado,
            tarea.prioridad,
            tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
            tarea.estimacion_horas,
            tarea.id
        ))

        self.conexion.commit()
        return cursor.rowcount > 0

    def eliminar_tarea(self, tarea_id: int) -> bool:
        """
        Elimina una tarea

        Args:
            tarea_id: ID de la tarea a eliminar

        Returns:
            True si se eliminó, False en caso contrario
        """
        cursor = self.conexion.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
        self.conexion.commit()
        return cursor.rowcount > 0

    # ===== OPERACIONES PARA DEPENDENCIAS =====

    def crear_dependencia(self, origen: int, destino: int) -> bool:
        """
        Crea una dependencia entre dos tareas

        Args:
            origen: ID de la tarea origen (prerequisito)
            destino: ID de la tarea destino (dependiente)

        Returns:
            True si se creó, False en caso contrario
        """
        try:
            cursor = self.conexion.cursor()
            cursor.execute('''
                INSERT INTO dependencias (tarea_origen, tarea_destino)
                VALUES (?, ?)
            ''', (origen, destino))
            self.conexion.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_dependencias(self, tarea_id: int) -> List[int]:
        """
        Obtiene las tareas de las que depende una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de IDs de tareas prerequisito
        """
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT tarea_origen FROM dependencias WHERE tarea_destino = ?
        ''', (tarea_id,))

        return [row[0] for row in cursor.fetchall()]

    def obtener_dependientes(self, tarea_id: int) -> List[int]:
        """
        Obtiene las tareas que dependen de una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de IDs de tareas dependientes
        """
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT tarea_destino FROM dependencias WHERE tarea_origen = ?
        ''', (tarea_id,))

        return [row[0] for row in cursor.fetchall()]

    def obtener_todas_dependencias(self) -> List[Tuple[int, int]]:
        """
        Obtiene todas las dependencias

        Returns:
            Lista de tuplas (origen, destino)
        """
        cursor = self.conexion.cursor()
        cursor.execute('SELECT tarea_origen, tarea_destino FROM dependencias')
        return [(row[0], row[1]) for row in cursor.fetchall()]

    def eliminar_dependencia(self, origen: int, destino: int) -> bool:
        """
        Elimina una dependencia

        Args:
            origen: ID de la tarea origen
            destino: ID de la tarea destino

        Returns:
            True si se eliminó, False en caso contrario
        """
        cursor = self.conexion.cursor()
        cursor.execute('''
            DELETE FROM dependencias
            WHERE tarea_origen = ? AND tarea_destino = ?
        ''', (origen, destino))
        self.conexion.commit()
        return cursor.rowcount > 0

    # ===== MÉTODOS AUXILIARES =====

    def _row_to_tarea(self, row: sqlite3.Row) -> Tarea:
        """Convierte una fila de BD a objeto Tarea"""
        tarea = Tarea(
            id=row['id'],
            nombre=row['nombre'],
            descripcion=row['descripcion'] or '',
            estado=row['estado'],
            prioridad=row['prioridad'],
            estimacion_horas=row['estimacion_horas'] or 0.0
        )

        if row['fecha_creacion']:
            tarea.fecha_creacion = datetime.fromisoformat(row['fecha_creacion'])

        if row['fecha_limite']:
            tarea.fecha_limite = datetime.fromisoformat(row['fecha_limite'])

        return tarea

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del proyecto

        Returns:
            Diccionario con estadísticas
        """
        cursor = self.conexion.cursor()

        # Total de tareas
        cursor.execute('SELECT COUNT(*) FROM tareas')
        total = cursor.fetchone()[0]

        # Tareas por estado
        cursor.execute('SELECT estado, COUNT(*) FROM tareas GROUP BY estado')
        por_estado = {row[0]: row[1] for row in cursor.fetchall()}

        # Total de dependencias
        cursor.execute('SELECT COUNT(*) FROM dependencias')
        total_deps = cursor.fetchone()[0]

        return {
            'total_tareas': total,
            'pendientes': por_estado.get('pendiente', 0),
            'en_progreso': por_estado.get('en_progreso', 0),
            'completadas': por_estado.get('completada', 0),
            'total_dependencias': total_deps
        }