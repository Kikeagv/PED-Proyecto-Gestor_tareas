"""
Modelo de Tarea
Representa una tarea individual en el sistema
"""

from datetime import datetime
from typing import Optional, List

class Tarea:
    """Clase que representa una tarea en el proyecto"""

    def __init__(self, id: Optional[int], nombre: str, descripcion: str = "",
                 estado: str = "pendiente", prioridad: int = 3,
                 fecha_limite: Optional[datetime] = None,
                 estimacion_horas: float = 0.0):
        """
        Inicializa una nueva tarea

        Args:
            id: Identificador único de la tarea (None para nuevas tareas)
            nombre: Nombre de la tarea
            descripcion: Descripción detallada
            estado: Estado actual ('pendiente', 'en_progreso', 'completada')
            prioridad: Prioridad de 1 (baja) a 5 (alta)
            fecha_limite: Fecha límite para completar la tarea
            estimacion_horas: Tiempo estimado en horas
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.prioridad = prioridad
        self.fecha_creacion = datetime.now()
        self.fecha_limite = fecha_limite
        self.estimacion_horas = estimacion_horas
        self.dependencias: List[int] = []  # IDs de tareas prerequisito

    def __str__(self) -> str:
        """Representación en string de la tarea"""
        return f"[{self.id}] {self.nombre} - {self.estado} (Prioridad: {self.prioridad})"

    def __repr__(self) -> str:
        return self.__str__()

    def completar(self) -> None:
        """Marca la tarea como completada"""
        self.estado = "completada"

    def iniciar(self) -> None:
        """Marca la tarea como en progreso"""
        self.estado = "en_progreso"

    def to_dict(self) -> dict:
        """Convierte la tarea a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'estimacion_horas': self.estimacion_horas
        }

    @staticmethod
    def from_dict(data: dict) -> 'Tarea':
        """Crea una tarea desde un diccionario"""
        tarea = Tarea(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            descripcion=data.get('descripcion', ''),
            estado=data.get('estado', 'pendiente'),
            prioridad=data.get('prioridad', 3),
            estimacion_horas=data.get('estimacion_horas', 0.0)
        )

        if data.get('fecha_limite'):
            tarea.fecha_limite = datetime.fromisoformat(data['fecha_limite'])

        if data.get('fecha_creacion'):
            tarea.fecha_creacion = datetime.fromisoformat(data['fecha_creacion'])

        return tarea