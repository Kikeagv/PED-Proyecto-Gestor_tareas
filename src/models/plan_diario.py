"""
Plan Diario
Gestiona la cola de tareas para el día actual
"""

from collections import deque
from typing import List, Optional
from datetime import date

class PlanDiario:
    """Cola para gestionar el plan de tareas diario"""

    def __init__(self):
        """Inicializa el plan diario"""
        self.cola: deque = deque()
        self.fecha = date.today()

    def agregar_tarea(self, tarea_id: int) -> None:
        """
        Agrega una tarea al plan diario

        Args:
            tarea_id: ID de la tarea a agregar
        """
        if tarea_id not in self.cola:
            self.cola.append(tarea_id)

    def siguiente_tarea(self) -> Optional[int]:
        """
        Obtiene y elimina la siguiente tarea del plan

        Returns:
            ID de la siguiente tarea, o None si está vacío
        """
        if self.cola:
            return self.cola.popleft()
        return None

    def ver_siguiente(self) -> Optional[int]:
        """
        Consulta la siguiente tarea sin eliminarla

        Returns:
            ID de la siguiente tarea, o None si está vacío
        """
        if self.cola:
            return self.cola[0]
        return None

    def esta_vacio(self) -> bool:
        """
        Verifica si el plan está vacío

        Returns:
            True si está vacío, False en caso contrario
        """
        return len(self.cola) == 0

    def obtener_todas(self) -> List[int]:
        """
        Obtiene todas las tareas del plan sin modificarlo

        Returns:
            Lista de IDs de tareas en el plan
        """
        return list(self.cola)

    def limpiar(self) -> None:
        """Limpia todas las tareas del plan"""
        self.cola.clear()

    def eliminar_tarea(self, tarea_id: int) -> bool:
        """
        Elimina una tarea específica del plan

        Args:
            tarea_id: ID de la tarea a eliminar

        Returns:
            True si se eliminó, False si no estaba en el plan
        """
        try:
            self.cola.remove(tarea_id)
            return True
        except ValueError:
            return False

    def mover_arriba(self, tarea_id: int) -> bool:
        """
        Mueve una tarea hacia arriba en la prioridad

        Args:
            tarea_id: ID de la tarea a mover

        Returns:
            True si se movió, False si no se pudo
        """
        try:
            idx = self.cola.index(tarea_id)
            if idx > 0:
                # Convertir a lista, intercambiar, volver a deque
                lista = list(self.cola)
                lista[idx], lista[idx-1] = lista[idx-1], lista[idx]
                self.cola = deque(lista)
                return True
            return False
        except ValueError:
            return False

    def mover_abajo(self, tarea_id: int) -> bool:
        """
        Mueve una tarea hacia abajo en la prioridad

        Args:
            tarea_id: ID de la tarea a mover

        Returns:
            True si se movió, False si no se pudo
        """
        try:
            idx = self.cola.index(tarea_id)
            if idx < len(self.cola) - 1:
                lista = list(self.cola)
                lista[idx], lista[idx+1] = lista[idx+1], lista[idx]
                self.cola = deque(lista)
                return True
            return False
        except ValueError:
            return False

    def __len__(self) -> int:
        """Retorna el número de tareas en el plan"""
        return len(self.cola)

    def __str__(self) -> str:
        """Representación en string del plan"""
        return f"Plan Diario ({self.fecha}): {list(self.cola)}"