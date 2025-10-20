"""
Grafo de Tareas
Implementa el grafo dirigido acíclico para modelar dependencias
"""

from collections import defaultdict, deque
from typing import List, Dict, Set, Optional, Tuple

class GrafoTareas:
    """Grafo dirigido para representar dependencias entre tareas"""

    def __init__(self):
        """Inicializa el grafo con lista de adyacencia"""
        self.lista_adyacencia: Dict[int, List[int]] = defaultdict(list)
        self.grados_entrada: Dict[int, int] = defaultdict(int)
        self.tareas_ids: Set[int] = set()

    def agregar_tarea(self, tarea_id: int) -> None:
        """
        Agrega una tarea (nodo) al grafo

        Args:
            tarea_id: ID de la tarea a agregar
        """
        if tarea_id not in self.tareas_ids:
            self.tareas_ids.add(tarea_id)
            if tarea_id not in self.lista_adyacencia:
                self.lista_adyacencia[tarea_id] = []
            if tarea_id not in self.grados_entrada:
                self.grados_entrada[tarea_id] = 0

    def agregar_dependencia(self, origen: int, destino: int) -> Tuple[bool, str]:
        """
        Agrega una dependencia entre dos tareas

        Args:
            origen: ID de la tarea prerequisito
            destino: ID de la tarea que depende de origen

        Returns:
            Tupla (éxito, mensaje)
        """
        # Validar que ambas tareas existan
        if origen not in self.tareas_ids:
            return False, f"La tarea {origen} no existe"
        if destino not in self.tareas_ids:
            return False, f"La tarea {destino} no existe"

        # Validar auto-dependencia
        if origen == destino:
            return False, "Una tarea no puede depender de sí misma"

        # Verificar si la dependencia ya existe
        if destino in self.lista_adyacencia[origen]:
            return False, "Esta dependencia ya existe"

        # Agregar temporalmente y verificar ciclos
        self.lista_adyacencia[origen].append(destino)
        self.grados_entrada[destino] += 1

        if self.detectar_ciclo():
            # Revertir cambios
            self.lista_adyacencia[origen].remove(destino)
            self.grados_entrada[destino] -= 1
            return False, "Esta dependencia crearía un ciclo"

        return True, "Dependencia agregada exitosamente"

    def eliminar_dependencia(self, origen: int, destino: int) -> bool:
        """
        Elimina una dependencia entre dos tareas

        Args:
            origen: ID de la tarea origen
            destino: ID de la tarea destino

        Returns:
            True si se eliminó, False si no existía
        """
        if destino in self.lista_adyacencia[origen]:
            self.lista_adyacencia[origen].remove(destino)
            self.grados_entrada[destino] -= 1
            return True
        return False

    def eliminar_tarea(self, tarea_id: int) -> None:
        """
        Elimina una tarea del grafo

        Args:
            tarea_id: ID de la tarea a eliminar
        """
        if tarea_id not in self.tareas_ids:
            return

        # Eliminar aristas salientes
        for destino in self.lista_adyacencia[tarea_id]:
            self.grados_entrada[destino] -= 1
        del self.lista_adyacencia[tarea_id]

        # Eliminar aristas entrantes
        for origen in self.tareas_ids:
            if origen != tarea_id and tarea_id in self.lista_adyacencia[origen]:
                self.lista_adyacencia[origen].remove(tarea_id)

        del self.grados_entrada[tarea_id]
        self.tareas_ids.remove(tarea_id)

    def detectar_ciclo(self) -> bool:
        """
        Detecta si existe un ciclo en el grafo usando DFS

        Returns:
            True si existe ciclo, False en caso contrario
        """
        visitado = set()
        en_recursion = set()

        def dfs(nodo: int) -> bool:
            visitado.add(nodo)
            en_recursion.add(nodo)

            for vecino in self.lista_adyacencia[nodo]:
                if vecino not in visitado:
                    if dfs(vecino):
                        return True
                elif vecino in en_recursion:
                    return True

            en_recursion.remove(nodo)
            return False

        for nodo in self.tareas_ids:
            if nodo not in visitado:
                if dfs(nodo):
                    return True

        return False

    def ordenamiento_topologico(self) -> Optional[List[int]]:
        """
        Calcula el ordenamiento topológico usando el algoritmo de Kahn

        Returns:
            Lista de IDs de tareas en orden válido, o None si hay ciclo
        """
        # Copiar grados de entrada
        grados = self.grados_entrada.copy()

        # Cola con nodos sin dependencias
        cola = deque([nodo for nodo in self.tareas_ids if grados[nodo] == 0])
        resultado = []

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo)

            # Reducir grado de entrada de vecinos
            for vecino in self.lista_adyacencia[nodo]:
                grados[vecino] -= 1
                if grados[vecino] == 0:
                    cola.append(vecino)

        # Si no se procesaron todos los nodos, hay ciclo
        if len(resultado) != len(self.tareas_ids):
            return None

        return resultado

    def tareas_ejecutables(self, tareas_completadas: Set[int]) -> List[int]:
        """
        Obtiene las tareas que pueden ejecutarse (sin dependencias pendientes)

        Args:
            tareas_completadas: Conjunto de IDs de tareas ya completadas

        Returns:
            Lista de IDs de tareas ejecutables
        """
        ejecutables = []

        for tarea_id in self.tareas_ids:
            if tarea_id in tareas_completadas:
                continue

            # Verificar si todas las dependencias están completadas
            dependencias_completas = True
            for origen in self.tareas_ids:
                if tarea_id in self.lista_adyacencia[origen]:
                    if origen not in tareas_completadas:
                        dependencias_completas = False
                        break

            if dependencias_completas:
                ejecutables.append(tarea_id)

        return ejecutables

    def obtener_dependencias(self, tarea_id: int) -> List[int]:
        """
        Obtiene las tareas de las cuales depende una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de IDs de tareas prerequisito
        """
        dependencias = []
        for origen in self.tareas_ids:
            if tarea_id in self.lista_adyacencia[origen]:
                dependencias.append(origen)
        return dependencias

    def obtener_dependientes(self, tarea_id: int) -> List[int]:
        """
        Obtiene las tareas que dependen de una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de IDs de tareas dependientes
        """
        return self.lista_adyacencia[tarea_id].copy()

    def __str__(self) -> str:
        """Representación en string del grafo"""
        resultado = "Grafo de Dependencias:\n"
        for origen in sorted(self.tareas_ids):
            destinos = self.lista_adyacencia[origen]
            resultado += f"  Tarea {origen} -> {destinos}\n"
        return resultado