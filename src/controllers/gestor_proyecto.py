"""
Gestor de Proyecto
Controlador principal que coordina todas las operaciones
Sistema de Gestion de Tareas con Dependencias - Fase 2
Universidad Don Bosco - PED
"""

from typing import List, Optional, Tuple, Set
import logging

from models.tarea import Tarea
from models.grafo_tareas import GrafoTareas
from models.plan_diario import PlanDiario
from database.db_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GestorProyectoError(Exception):
    """Excepcion personalizada para errores del gestor"""
    pass


class GestorProyecto:
    """Controlador principal del sistema de gestion de tareas
    
    Implementa la logica de negocio utilizando:
    - Grafo Dirigido Aciclico (DAG) para dependencias
    - Cola (Queue) para el plan diario
    - Base de datos SQLite para persistencia
    """

    def __init__(self, db_path: str = "gestor_tareas.db"):
        """
        Inicializa el gestor de proyecto

        Args:
            db_path: Ruta de la base de datos
            
        Raises:
            GestorProyectoError: Si hay error al inicializar
        """
        try:
            self.db = DatabaseManager(db_path)
            self.grafo = GrafoTareas()
            self.plan_diario = PlanDiario()
            self.cargar_desde_db()
            logger.info(f"Gestor inicializado con base de datos: {db_path}")
        except Exception as e:
            logger.error(f"Error al inicializar gestor: {e}")
            raise GestorProyectoError(f"Error al inicializar: {e}")

    def cargar_desde_db(self) -> None:
        """Carga todas las tareas y dependencias desde la base de datos"""
        # Cargar tareas al grafo
        tareas = self.db.obtener_todas_tareas()
        for tarea in tareas:
            self.grafo.agregar_tarea(tarea.id)

        # Cargar dependencias
        dependencias = self.db.obtener_todas_dependencias()
        for origen, destino in dependencias:
            self.grafo.agregar_dependencia(origen, destino)

    # ===== OPERACIONES DE TAREAS =====

    def crear_tarea(self, nombre: str, descripcion: str = "",
                   prioridad: int = 3, fecha_limite=None,
                   estimacion_horas: float = 0.0) -> Tuple[bool, str, Optional[int]]:
        """
        Crea una nueva tarea

        Args:
            nombre: Nombre de la tarea
            descripcion: Descripción detallada
            prioridad: Prioridad de 1 a 5
            fecha_limite: Fecha límite (datetime o None)
            estimacion_horas: Horas estimadas

        Returns:
            Tupla (éxito, mensaje, id_tarea)
        """
        if not nombre or nombre.strip() == "":
            return False, "El nombre de la tarea no puede estar vacío", None

        if not 1 <= prioridad <= 5:
            return False, "La prioridad debe estar entre 1 y 5", None

        try:
            # Crear tarea
            tarea = Tarea(
                id=None,
                nombre=nombre.strip(),
                descripcion=descripcion.strip(),
                prioridad=prioridad,
                fecha_limite=fecha_limite,
                estimacion_horas=estimacion_horas
            )

            # Guardar en base de datos
            tarea_id = self.db.crear_tarea(tarea)
            tarea.id = tarea_id

            # Agregar al grafo
            self.grafo.agregar_tarea(tarea_id)

            return True, f"Tarea '{nombre}' creada exitosamente", tarea_id

        except Exception as e:
            return False, f"Error al crear tarea: {str(e)}", None

    def obtener_tarea(self, tarea_id: int) -> Optional[Tarea]:
        """
        Obtiene una tarea por su ID

        Args:
            tarea_id: ID de la tarea

        Returns:
            Objeto Tarea o None
        """
        return self.db.obtener_tarea(tarea_id)

    def obtener_todas_tareas(self) -> List[Tarea]:
        """
        Obtiene todas las tareas

        Returns:
            Lista de tareas
        """
        return self.db.obtener_todas_tareas()

    def actualizar_tarea(self, tarea: Tarea) -> Tuple[bool, str]:
        """
        Actualiza una tarea existente

        Args:
            tarea: Objeto Tarea con datos actualizados

        Returns:
            Tupla (éxito, mensaje)
        """
        if not tarea.nombre or tarea.nombre.strip() == "":
            return False, "El nombre no puede estar vacío"

        if not 1 <= tarea.prioridad <= 5:
            return False, "La prioridad debe estar entre 1 y 5"

        try:
            if self.db.actualizar_tarea(tarea):
                return True, "Tarea actualizada exitosamente"
            else:
                return False, "No se pudo actualizar la tarea"
        except Exception as e:
            return False, f"Error al actualizar: {str(e)}"

    def eliminar_tarea(self, tarea_id: int) -> Tuple[bool, str]:
        """
        Elimina una tarea

        Args:
            tarea_id: ID de la tarea a eliminar

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Eliminar del plan diario si está
            self.plan_diario.eliminar_tarea(tarea_id)

            # Eliminar del grafo
            self.grafo.eliminar_tarea(tarea_id)

            # Eliminar de la base de datos
            if self.db.eliminar_tarea(tarea_id):
                return True, "Tarea eliminada exitosamente"
            else:
                return False, "No se pudo eliminar la tarea"

        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"

    def marcar_completada(self, tarea_id: int) -> Tuple[bool, str, List[int]]:
        """
        Marca una tarea como completada

        Args:
            tarea_id: ID de la tarea

        Returns:
            Tupla (éxito, mensaje, lista de tareas desbloqueadas)
        """
        tarea = self.db.obtener_tarea(tarea_id)
        if not tarea:
            return False, "Tarea no encontrada", []

        # Cambiar estado
        tarea.completar()
        self.db.actualizar_tarea(tarea)

        # Eliminar del plan diario
        self.plan_diario.eliminar_tarea(tarea_id)

        # Obtener tareas desbloqueadas
        tareas_completadas = self._obtener_ids_completadas()
        tareas_desbloqueadas = []

        for dep_tarea_id in self.grafo.obtener_dependientes(tarea_id):
            deps = self.grafo.obtener_dependencias(dep_tarea_id)
            if all(dep in tareas_completadas for dep in deps):
                dep_tarea = self.db.obtener_tarea(dep_tarea_id)
                if dep_tarea and dep_tarea.estado != 'completada':
                    tareas_desbloqueadas.append(dep_tarea_id)

        mensaje = f"✓ Tarea completada"
        if tareas_desbloqueadas:
            mensaje += f". {len(tareas_desbloqueadas)} tarea(s) desbloqueada(s)"

        return True, mensaje, tareas_desbloqueadas

    # ===== OPERACIONES DE DEPENDENCIAS =====

    def agregar_dependencia(self, origen: int, destino: int) -> Tuple[bool, str]:
        """
        Agrega una dependencia entre dos tareas

        Args:
            origen: ID de la tarea prerequisito
            destino: ID de la tarea que depende

        Returns:
            Tupla (éxito, mensaje)
        """
        # Validar en el grafo (detecta ciclos)
        exito, mensaje = self.grafo.agregar_dependencia(origen, destino)

        if exito:
            # Guardar en base de datos
            if self.db.crear_dependencia(origen, destino):
                return True, mensaje
            else:
                # Revertir en el grafo
                self.grafo.eliminar_dependencia(origen, destino)
                return False, "Error al guardar en base de datos"

        return False, mensaje

    def eliminar_dependencia(self, origen: int, destino: int) -> Tuple[bool, str]:
        """
        Elimina una dependencia

        Args:
            origen: ID de la tarea origen
            destino: ID de la tarea destino

        Returns:
            Tupla (éxito, mensaje)
        """
        # Eliminar del grafo
        if self.grafo.eliminar_dependencia(origen, destino):
            # Eliminar de base de datos
            self.db.eliminar_dependencia(origen, destino)
            return True, "Dependencia eliminada"

        return False, "La dependencia no existe"

    def obtener_dependencias(self, tarea_id: int) -> List[Tarea]:
        """
        Obtiene las tareas de las que depende una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de objetos Tarea
        """
        ids_deps = self.grafo.obtener_dependencias(tarea_id)
        return [self.db.obtener_tarea(id) for id in ids_deps if self.db.obtener_tarea(id)]

    def obtener_dependientes(self, tarea_id: int) -> List[Tarea]:
        """
        Obtiene las tareas que dependen de una tarea

        Args:
            tarea_id: ID de la tarea

        Returns:
            Lista de objetos Tarea
        """
        ids_deps = self.grafo.obtener_dependientes(tarea_id)
        return [self.db.obtener_tarea(id) for id in ids_deps if self.db.obtener_tarea(id)]

    # ===== OPERACIONES DE PLANIFICACIÓN =====

    def calcular_orden_ejecucion(self) -> Optional[List[Tarea]]:
        """
        Calcula el orden de ejecución usando ordenamiento topológico

        Returns:
            Lista de tareas en orden válido, o None si hay ciclo
        """
        orden_ids = self.grafo.ordenamiento_topologico()

        if orden_ids is None:
            return None

        # Filtrar solo tareas pendientes o en progreso
        tareas_ordenadas = []
        for tarea_id in orden_ids:
            tarea = self.db.obtener_tarea(tarea_id)
            if tarea and tarea.estado != 'completada':
                tareas_ordenadas.append(tarea)

        return tareas_ordenadas

    def obtener_tareas_ejecutables(self) -> List[Tarea]:
        """
        Obtiene las tareas que pueden ejecutarse ahora

        Returns:
            Lista de tareas ejecutables ordenadas por prioridad
        """
        tareas_completadas = self._obtener_ids_completadas()
        ids_ejecutables = self.grafo.tareas_ejecutables(tareas_completadas)

        # Obtener objetos Tarea y filtrar completadas
        tareas = []
        for tarea_id in ids_ejecutables:
            tarea = self.db.obtener_tarea(tarea_id)
            if tarea and tarea.estado != 'completada':
                tareas.append(tarea)

        # Ordenar por prioridad descendente
        tareas.sort(key=lambda t: t.prioridad, reverse=True)

        return tareas

    def obtener_siguiente_tarea(self) -> Optional[Tarea]:
        """
        Obtiene la siguiente tarea recomendada

        Returns:
            Objeto Tarea o None si no hay tareas ejecutables
        """
        tareas_ejecutables = self.obtener_tareas_ejecutables()

        if tareas_ejecutables:
            return tareas_ejecutables[0]

        return None

    # ===== OPERACIONES DEL PLAN DIARIO =====

    def agregar_al_plan_diario(self, tarea_id: int) -> Tuple[bool, str]:
        """
        Agrega una tarea al plan diario

        Args:
            tarea_id: ID de la tarea

        Returns:
            Tupla (éxito, mensaje)
        """
        tarea = self.db.obtener_tarea(tarea_id)
        if not tarea:
            return False, "Tarea no encontrada"

        if tarea.estado == 'completada':
            return False, "No se pueden agregar tareas completadas al plan"

        # Verificar si es ejecutable
        tareas_completadas = self._obtener_ids_completadas()
        if tarea_id not in self.grafo.tareas_ejecutables(tareas_completadas):
            return False, "Esta tarea no es ejecutable aún (tiene dependencias pendientes)"

        self.plan_diario.agregar_tarea(tarea_id)
        return True, f"Tarea '{tarea.nombre}' agregada al plan diario"

    def obtener_plan_diario(self) -> List[Tarea]:
        """
        Obtiene todas las tareas del plan diario

        Returns:
            Lista de tareas en el plan
        """
        ids_plan = self.plan_diario.obtener_todas()
        return [self.db.obtener_tarea(id) for id in ids_plan if self.db.obtener_tarea(id)]

    def limpiar_plan_diario(self) -> None:
        """Limpia todas las tareas del plan diario"""
        self.plan_diario.limpiar()

    def eliminar_del_plan(self, tarea_id: int) -> bool:
        """
        Elimina una tarea del plan diario

        Args:
            tarea_id: ID de la tarea

        Returns:
            True si se eliminó, False si no estaba
        """
        return self.plan_diario.eliminar_tarea(tarea_id)

    # ===== ESTADÍSTICAS Y MÉTRICAS =====

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del proyecto

        Returns:
            Diccionario con estadísticas
        """
        stats = self.db.obtener_estadisticas()

        # Agregar tareas ejecutables
        stats['ejecutables'] = len(self.obtener_tareas_ejecutables())

        # Calcular porcentaje de avance
        if stats['total_tareas'] > 0:
            stats['porcentaje_completado'] = (stats['completadas'] / stats['total_tareas']) * 100
        else:
            stats['porcentaje_completado'] = 0

        return stats

    # ===== MÉTODOS AUXILIARES =====

    def _obtener_ids_completadas(self) -> Set[int]:
        """Obtiene el conjunto de IDs de tareas completadas"""
        tareas_completadas = self.db.obtener_tareas_por_estado('completada')
        return {tarea.id for tarea in tareas_completadas}

    def cerrar(self) -> None:
        """Cierra conexiones y libera recursos"""
        self.db.desconectar()