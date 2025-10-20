# UNIVERSIDAD TÉCNICA PARTICULAR DE LOJA
## INGENIERÍA EN CIENCIAS DE LA COMPUTACIÓN

### PROGRAMACIÓN CON ESTRUCTURAS DE DATOS
### PROYECTO FINAL - FASE 1

**Asignatura:** Programación con Estructuras de Datos (PED941)

**Docente:** [Nombre del docente]

**Ciclo:** 02-2025

---

### INTEGRANTES DEL EQUIPO

| Fotografía | Nombre Completo | Carné |
|------------|----------------|-------|
| [Foto] | [Apellido1, Nombre1] | [Carné1] |
| [Foto] | [Apellido2, Nombre2] | [Carné2] |
| [Foto] | [Apellido3, Nombre3] | [Carné3] |
| [Foto] | [Apellido4, Nombre4] | [Carné4] |

**Fecha de entrega:** 12 de octubre de 2025

---

## ÍNDICE

1. Introducción
2. Explicación detallada de la lógica para resolver el problema
   - 2.1. Situación problemática elegida
   - 2.2. Estructuras de Datos seleccionadas y su forma de aplicación
   - 2.3. Procesos por registrar - Diagramas UML
   - 2.4. Proceso de servicio - Resultados esperados
3. Herramientas de desarrollo
4. Fuentes de consulta

---

## 1. INTRODUCCIÓN

La gestión efectiva de proyectos y tareas es fundamental en el desarrollo de software y en cualquier ámbito profesional que requiera planificación y organización. Uno de los mayores desafíos en la administración de proyectos complejos es manejar las dependencias entre tareas, es decir, identificar qué actividades deben completarse antes de iniciar otras.

El presente documento describe la Fase 1 del desarrollo de un **Gestor de Tareas con Dependencias**, un sistema informático diseñado para ayudar a usuarios individuales o equipos de trabajo a organizar, planificar y ejecutar tareas de manera eficiente, considerando las relaciones de precedencia entre ellas.

Este sistema implementa algoritmos avanzados basados en estructuras de datos tipo grafo para modelar las dependencias entre tareas y aplicar el ordenamiento topológico, permitiendo determinar un orden de ejecución válido. Adicionalmente, utiliza estructuras de cola para gestionar el plan de trabajo diario, optimizando la productividad del usuario.

El proyecto se desarrollará utilizando el lenguaje de programación Python, aprovechando su versatilidad y las bibliotecas disponibles para el desarrollo de interfaces gráficas y manejo de bases de datos.

---

## 2. EXPLICACIÓN DETALLADA DE LA LÓGICA PARA RESOLVER EL PROBLEMA

### 2.1. Situación problemática elegida

En el contexto profesional y académico actual, las personas frecuentemente enfrentan múltiples tareas que deben ejecutarse en un orden específico debido a dependencias lógicas o técnicas. Por ejemplo:

- En desarrollo de software: no se puede ejecutar pruebas unitarias sin antes haber escrito el código.
- En construcción: no se pueden instalar ventanas sin antes haber levantado las paredes.
- En investigación: no se puede analizar datos sin antes haberlos recolectado.

**Problemática identificada:**

Los gestores de tareas tradicionales (listas simples, calendarios) no consideran las dependencias entre actividades, lo que genera:

1. **Planificación ineficiente:** El usuario puede intentar realizar tareas sin haber completado sus prerequisitos.
2. **Pérdida de tiempo:** Falta de claridad sobre cuál es la siguiente tarea ejecutable.
3. **Riesgo de errores:** Ejecutar tareas fuera de orden puede causar problemas o retrabajos.
4. **Falta de visualización:** Dificultad para identificar cuellos de botella o el camino crítico del proyecto.

**Solución propuesta:**

Desarrollar un sistema que modele las tareas y sus dependencias como un grafo dirigido acíclico (DAG), permitiendo:
- Crear tareas con sus respectivas dependencias
- Calcular automáticamente un orden de ejecución válido mediante ordenamiento topológico
- Identificar en tiempo real cuáles son las tareas ejecutables (sin dependencias pendientes)
- Gestionar un plan diario de trabajo mediante una cola de prioridad
- Almacenar toda la información en una base de datos para persistencia

### 2.2. Estructuras de Datos seleccionadas y su forma de aplicación

El sistema implementa las siguientes estructuras de datos abstractas (TAD):

#### **2.2.1. Grafo Dirigido Acíclico (DAG) - Lista de Adyacencia**

**Justificación:**
Un grafo es la estructura natural para modelar relaciones de dependencia. Cada tarea es un nodo, y cada dependencia es una arista dirigida desde la tarea prerequisito hacia la tarea dependiente.

**Implementación:**
- **Representación:** Lista de adyacencia utilizando diccionarios de Python
  ```
  grafo = {
    'Tarea_A': ['Tarea_B', 'Tarea_C'],  # A debe completarse antes que B y C
    'Tarea_B': ['Tarea_D'],
    'Tarea_C': ['Tarea_D'],
    'Tarea_D': []
  }
  ```

**Operaciones principales:**
- **Agregar nodo (tarea):** O(1)
- **Agregar arista (dependencia):** O(1)
- **Eliminar nodo:** O(V + E) donde V=vértices, E=aristas
- **Detectar ciclos:** Algoritmo DFS modificado - O(V + E)
- **Ordenamiento topológico:** Algoritmo de Kahn o DFS - O(V + E)

**Ventajas de lista de adyacencia:**
- Eficiente en memoria para grafos dispersos (pocas dependencias por tarea)
- Rápida iteración sobre vecinos de un nodo
- Fácil implementación en Python con diccionarios

#### **2.2.2. Ordenamiento Topológico**

**Algoritmo de Kahn (Seleccionado):**

1. Calcular el grado de entrada (in-degree) de cada nodo
2. Inicializar cola con todos los nodos de grado 0 (sin dependencias)
3. Mientras la cola no esté vacía:
   - Extraer un nodo de la cola
   - Agregarlo al resultado ordenado
   - Reducir en 1 el grado de entrada de sus vecinos
   - Si algún vecino llega a grado 0, agregarlo a la cola
4. Si se procesaron todos los nodos, el orden es válido; si no, existe un ciclo

**Complejidad:** O(V + E)

**Aplicación en el sistema:**
- Generar un orden de ejecución sugerido para todas las tareas del proyecto
- Validar que no existan dependencias circulares
- Identificar múltiples órdenes válidos cuando existan tareas independientes

#### **2.2.3. Cola (Queue) para Plan Diario**

**Justificación:**
Una cola FIFO permite organizar las tareas ejecutables del día en orden de prioridad o urgencia.

**Implementación:**
- Utilizar `collections.deque` de Python para operaciones eficientes O(1) en ambos extremos

**Operaciones:**
- **Enqueue (agregar tarea al plan):** O(1)
- **Dequeue (obtener siguiente tarea):** O(1)
- **Peek (consultar siguiente sin extraer):** O(1)
- **Is_empty:** O(1)

**Aplicación:**
- Mantener la lista de tareas a realizar en el día actual
- Permitir reorganización mediante eliminación e inserción
- Mostrar de forma clara "cuál es la siguiente tarea a ejecutar"

#### **2.2.4. Diccionario Hash para Metadatos de Tareas**

**Estructura:**
```python
tareas = {
  'id_tarea': {
    'nombre': str,
    'descripcion': str,
    'estado': str,  # 'pendiente', 'en_progreso', 'completada'
    'prioridad': int,  # 1-5
    'fecha_creacion': datetime,
    'fecha_limite': datetime,
    'estimacion_horas': float,
    'dependencias': [ids],  # lista de IDs de tareas prerequisito
    'tags': [str]
  }
}
```

**Complejidad de búsqueda:** O(1) promedio

### 2.3. Procesos por registrar - Diagramas UML

#### **2.3.1. Diagrama de Casos de Uso**

```
                    Sistema Gestor de Tareas
                           
         +------------------------------------------+
         |                                          |
         |   [Gestionar Tareas]                     |
         |     - Crear tarea                        |
         |     - Editar tarea                       |
    Usuario     - Eliminar tarea                     |
         |     - Marcar como completada             |
         |                                          |
         |   [Gestionar Dependencias]               |
         |     - Agregar dependencia                |
         |     - Eliminar dependencia               |
         |     - Visualizar dependencias            |
         |                                          |
         |   [Planificación]                        |
         |     - Calcular orden topológico          |
         |     - Ver tareas ejecutables             |
         |     - Generar plan diario                |
         |     - Obtener siguiente tarea            |
         |                                          |
         |   [Visualización]                        |
         |     - Ver grafo de dependencias          |
         |     - Ver estadísticas del proyecto      |
         |     - Exportar plan                      |
         |                                          |
         +------------------------------------------+
```

#### **2.3.2. Diagrama de Clases**

```
+------------------+
|     Tarea        |
+------------------+
| - id: int        |
| - nombre: str    |
| - descripcion: str|
| - estado: str    |
| - prioridad: int |
| - fecha_creacion |
| - fecha_limite   |
| - estimacion: float|
+------------------+
| + crear()        |
| + editar()       |
| + completar()    |
| + obtener_info() |
+------------------+
         |
         | 1
         |
         | *
+------------------+
|  GrafoTareas     |
+------------------+
| - lista_adyacencia: dict|
| - grados_entrada: dict |
+------------------+
| + agregar_tarea()|
| + agregar_dependencia()|
| + eliminar_tarea()|
| + detectar_ciclo()|
| + ordenamiento_topologico()|
| + tareas_ejecutables()|
| + obtener_vecinos()|
+------------------+
         |
         |
+------------------+
|   PlanDiario     |
+------------------+
| - cola: deque    |
| - fecha: date    |
+------------------+
| + agregar_tarea()|
| + siguiente_tarea()|
| + ver_siguiente()|
| + reordenar()    |
| + esta_vacio()   |
+------------------+
         |
         |
+------------------+
|  GestorProyecto  |
+------------------+
| - grafo: GrafoTareas|
| - tareas: dict   |
| - plan: PlanDiario|
| - bd: BaseDatos  |
+------------------+
| + crear_tarea()  |
| + obtener_orden_ejecucion()|
| + actualizar_estado()|
| + calcular_metricas()|
| + guardar_proyecto()|
| + cargar_proyecto()|
+------------------+
         |
         |
+------------------+
|   BaseDatos      |
+------------------+
| - conexion: Connection|
+------------------+
| + guardar_tarea()|
| + obtener_tarea()|
| + guardar_dependencia()|
| + obtener_dependencias()|
| + actualizar()   |
| + eliminar()     |
+------------------+
```

#### **2.3.3. Diagrama de Secuencia - Crear Tarea con Dependencias**

```
Usuario    Interfaz    GestorProyecto    GrafoTareas    BaseDatos
  |           |              |                |             |
  |--Ingresar datos-->       |                |             |
  |           |              |                |             |
  |           |--Crear tarea()-->             |             |
  |           |              |                |             |
  |           |              |--Validar datos()            |
  |           |              |                |             |
  |           |              |--Agregar nodo()-->          |
  |           |              |                |             |
  |           |              |--Agregar dependencias()-->  |
  |           |              |                |             |
  |           |              |                |--Detectar ciclo()|
  |           |              |                |             |
  |           |              |                |<--Resultado--|
  |           |              |                |             |
  |           |              |--Guardar en BD()----------->|
  |           |              |                |             |
  |           |              |                |<--Confirmar--|
  |           |              |<--Tarea creada--|            |
  |           |<--Confirmar--|                |             |
  |<--Mostrar mensaje exitoso|                |             |
```

#### **2.3.4. Diagrama de Actividades - Calcular Siguiente Tarea Ejecutable**

```
(Inicio)
   |
   v
[Obtener todas las tareas pendientes]
   |
   v
[Calcular grado de entrada de cada tarea]
   |
   v
[Filtrar tareas con grado = 0]
   |
   v
<¿Existen tareas ejecutables?>
   |         \
   | Sí      \ No
   v          v
[Ordenar por prioridad]  [Mostrar mensaje: "No hay tareas disponibles"]
   |                                |
   v                                v
[Agregar a cola del plan diario]  (Fin)
   |
   v
[Retornar primera tarea de la cola]
   |
   v
[Mostrar al usuario]
   |
   v
(Fin)
```

### 2.4. Proceso de servicio - Resultados esperados

#### **2.4.1. Funcionalidades del Sistema al 30% (Prototipo Fase 1)**

**Módulo de Gestión de Tareas:**
- Crear nueva tarea con: nombre, descripción, prioridad, fecha límite
- Visualizar listado de todas las tareas
- Editar información básica de tareas
- Marcar tareas como completadas

**Módulo de Dependencias:**
- Agregar dependencias entre tareas (Tarea A debe completarse antes que Tarea B)
- Validación automática de ciclos al agregar dependencias
- Visualización de dependencias en formato de lista

**Módulo de Planificación:**
- Calcular y mostrar un orden de ejecución válido (ordenamiento topológico)
- Identificar tareas ejecutables en el momento actual
- Mostrar "siguiente tarea recomendada" basada en dependencias y prioridad

**Base de Datos:**
- Tablas: `tareas`, `dependencias`
- Operaciones CRUD básicas implementadas
- Persistencia de datos entre sesiones

#### **2.4.2. Resultados que el Sistema Devolverá al Usuario**

1. **Orden de Ejecución Válido:**
   - Lista ordenada de tareas respetando todas las dependencias
   - Ejemplo: ["Investigar requisitos", "Diseñar arquitectura", "Implementar módulo A", "Implementar módulo B", "Pruebas integración", "Despliegue"]

2. **Tareas Ejecutables Actuales:**
   - Lista de tareas que pueden iniciarse inmediatamente
   - Ejemplo: ["Diseñar logo", "Configurar repositorio", "Preparar presentación"]
   - Cada tarea muestra: nombre, prioridad, tiempo estimado, fecha límite

3. **Siguiente Tarea Recomendada:**
   - La tarea más prioritaria entre las ejecutables
   - Mensaje claro: "Tu próxima tarea es: [Nombre de tarea]"

4. **Alertas y Validaciones:**
   - "⚠️ No se puede agregar esta dependencia: crearía un ciclo"
   - "✓ Dependencia agregada exitosamente"
   - "✓ Tarea completada. X tareas desbloqueadas"

5. **Visualización del Grafo:**
   - Representación visual simple de tareas y sus conexiones
   - Nodos coloreados según estado: verde (completada), amarillo (en progreso), gris (pendiente)

6. **Métricas Básicas:**
   - Total de tareas en el proyecto
   - Tareas completadas / pendientes / ejecutables
   - Porcentaje de avance del proyecto

#### **2.4.3. Beneficios para el Usuario**

- **Claridad:** Saber siempre qué hacer a continuación
- **Eficiencia:** No perder tiempo decidiendo prioridades
- **Prevención de errores:** Imposible ejecutar tareas sin prerequisitos
- **Motivación:** Visualización clara del progreso
- **Organización:** Estructura lógica del trabajo

---

## 3. HERRAMIENTAS DE DESARROLLO

### 3.1. Lenguaje de Programación

**Python 3.11+**

**Justificación:**
- Sintaxis clara y legible
- Amplio soporte para estructuras de datos mediante módulos estándar (`collections`, `heapq`)
- Excelentes bibliotecas para interfaces gráficas y bases de datos
- Facilita el desarrollo rápido de prototipos

### 3.2. Framework de Interfaz Gráfica

**Tkinter** (biblioteca estándar de Python)

**Alternativa considerada:** PyQt5

**Justificación Tkinter:**
- Incluida en Python (no requiere instalación adicional)
- Suficiente para las necesidades del prototipo
- Documentación extensa y comunidad activa

### 3.3. Sistema Gestor de Base de Datos

**SQLite**

**Justificación:**
- Base de datos embebida (no requiere servidor)
- Perfecta para aplicaciones de escritorio monousuario
- Integración nativa con Python mediante módulo `sqlite3`
- Suficientemente potente para el volumen de datos esperado
- Facilita la portabilidad del proyecto

**Esquema de Base de Datos:**

```sql
-- Tabla de tareas
CREATE TABLE tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    prioridad INTEGER DEFAULT 3,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_limite DATETIME,
    estimacion_horas REAL,
    CONSTRAINT chk_prioridad CHECK (prioridad BETWEEN 1 AND 5),
    CONSTRAINT chk_estado CHECK (estado IN ('pendiente', 'en_progreso', 'completada'))
);

-- Tabla de dependencias (aristas del grafo)
CREATE TABLE dependencias (
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
CREATE INDEX idx_estado ON tareas(estado);
CREATE INDEX idx_dependencias_origen ON dependencias(tarea_origen);
CREATE INDEX idx_dependencias_destino ON dependencias(tarea_destino);
```

### 3.4. Bibliotecas Adicionales

**Para el prototipo (30%):**
- `tkinter` - Interfaz gráfica
- `sqlite3` - Base de datos (incluido en Python)
- `collections.deque` - Implementación eficiente de cola

**Para la Fase 2 (funcionalidades adicionales):**
- `matplotlib` - Visualización del grafo y diagramas de Gantt
- `networkx` - Algoritmos avanzados de grafos y visualización
- `datetime` - Manejo de fechas y plazos

### 3.5. Herramienta de Control de Versiones

**GitHub**

**Repositorio:** [Se proporcionará enlace]

**Estructura del proyecto:**
```
gestor-tareas-deps/
│
├── src/
│   ├── models/
│   │   ├── tarea.py
│   │   ├── grafo_tareas.py
│   │   └── plan_diario.py
│   ├── database/
│   │   ├── db_manager.py
│   │   └── schema.sql
│   ├── controllers/
│   │   └── gestor_proyecto.py
│   └── views/
│       ├── main_window.py
│       └── componentes/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── main.py
```

### 3.6. Entorno de Desarrollo

- **IDE:** Visual Studio Code / PyCharm Community
- **Sistema Operativo:** Multiplataforma (Windows/Linux/MacOS)
- **Gestión de dependencias:** pip + requirements.txt

---

## 4. FUENTES DE CONSULTA

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. https://mitpress.mit.edu/

Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). *Data Structures and Algorithms in Python*. John Wiley & Sons.

Kahn, A. B. (1962). Topological sorting of large networks. *Communications of the ACM*, 5(11), 558-562. https://doi.org/10.1145/368996.369025

Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media.

Python Software Foundation. (2024). *Python Documentation*. https://docs.python.org/3/

Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional.

SQLite Development Team. (2024). *SQLite Documentation*. https://www.sqlite.org/docs.html

Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual*. CreateSpace.

---

**Nota:** Este documento será actualizado conforme se implementen las funcionalidades del prototipo. El código fuente del avance al 30% estará disponible en el repositorio de GitHub especificado, con credenciales de acceso proporcionadas al docente.

# Código Completo del Prototipo - Fase 1
## Gestor de Tareas con Dependencias

Aquí está el código completo organizado en módulos:

## Estructura del Proyecto

```
gestor-tareas-deps/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tarea.py
│   │   ├── grafo_tareas.py
│   │   └── plan_diario.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py
│   │   └── schema.sql
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── gestor_proyecto.py
│   └── views/
│       ├── __init__.py
│       └── main_window.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 1. `main.py` (Punto de entrada)

```python
"""
Gestor de Tareas con Dependencias
Punto de entrada principal de la aplicación
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from views.main_window import AplicacionGestorTareas

def main():
    """Función principal que inicia la aplicación"""
    try:
        app = AplicacionGestorTareas()
        app.iniciar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

---

## 2. `src/models/tarea.py`

```python
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
```

---

## 3. `src/models/grafo_tareas.py`

```python
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
```

---

## 4. `src/models/plan_diario.py`

```python
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
```

---

## 5. `src/database/schema.sql`

```sql
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
```

---

## 6. `src/database/db_manager.py`

```python
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

        ```python
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
```

---

## 7. `src/controllers/gestor_proyecto.py`

```python
"""
Gestor de Proyecto
Controlador principal que coordina todas las operaciones
"""

from typing import List, Optional, Tuple, Set
from models.tarea import Tarea
from models.grafo_tareas import GrafoTareas
from models.plan_diario import PlanDiario
from database.db_manager import DatabaseManager

class GestorProyecto:
    """Controlador principal del sistema de gestión de tareas"""
    
    def __init__(self, db_path: str = "gestor_tareas.db"):
        """
        Inicializa el gestor de proyecto
        
        Args:
            db_path: Ruta de la base de datos
        """
        self.db = DatabaseManager(db_path)
        self.grafo = GrafoTareas()
        self.plan_diario = PlanDiario()
        self.cargar_desde_db()
    
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
```

---

## 8. `src/views/main_window.py`

```python
"""
Interfaz Gráfica Principal
Ventana principal usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from typing import Optional
from controllers.gestor_proyecto import GestorProyecto
from models.tarea import Tarea

class AplicacionGestorTareas:
    """Aplicación principal con interfaz gráfica"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.gestor = GestorProyecto()
        self.root = tk.Tk()
        self.configurar_ventana()
        self.crear_widgets()
        self.actualizar_vistas()
    
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("Gestor de Tareas con Dependencias")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # ===== FRAME PRINCIPAL =====
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # ===== TÍTULO =====
        titulo = tk.Label(main_frame, text="📋 Gestor de Tareas con Dependencias", 
                         font=('Arial', 20, 'bold'), fg='#2c3e50')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # ===== PANEL IZQUIERDO - ACCIONES =====
        panel_izq = ttk.LabelFrame(main_frame, text="Acciones", padding="10")
        panel_izq.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Botones de acciones
        ttk.Button(panel_izq, text="➕ Nueva Tarea", 
                  command=self.crear_tarea_dialog, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="🔗 Agregar Dependencia", 
                  command=self.agregar_dependencia_dialog, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="✓ Marcar Completada", 
                  command=self.marcar_completada_dialog, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="📊 Ver Orden de Ejecución", 
                  command=self.mostrar_orden_ejecucion, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="🎯 Tareas Ejecutables", 
                  command=self.mostrar_tareas_ejecutables, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="⭐ Siguiente Tarea", 
                  command=self.mostrar_siguiente_tarea, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Separator(panel_izq, orient=tk.HORIZONTAL).pack(pady=10, fill=tk.X)
        
        ttk.Button(panel_izq, text="📅 Ver Plan Diario", 
                  command=self.mostrar_plan_diario, width=20).pack(pady=5, fill=tk.X)
        
        ttk.Button(panel_izq, text="🔄 Actualizar Vista", 
                  command=self.actualizar_vistas, width=20).pack(pady=5, fill=tk.X)
        
        # Estadísticas
        ttk.Separator(panel_izq, orient=tk.HORIZONTAL).pack(pady=10, fill=tk.X)
        
        stats_frame = ttk.LabelFrame(panel_izq, text="Estadísticas", padding="5")
        stats_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.stats_labels = {}
        stats_items = [
            ('total', 'Total tareas:'),
            ('completadas', 'Completadas:'),
            ('pendientes', 'Pendientes:'),
            ('ejecutables', 'Ejecutables:'),
            ('porcentaje', 'Progreso:')
        ]
        
        for key, text in stats_items:
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=text, font=('Arial', 9)).pack(side=tk.LEFT)
            label = ttk.Label(frame, text="0", font=('Arial', 9, 'bold'))
            label.pack(side=tk.RIGHT)
            self.stats_labels[key] = label
        
        # ===== PANEL CENTRAL - LISTA DE TAREAS =====
        panel_central = ttk.LabelFrame(main_frame, text="Todas las Tareas", padding="10")
        panel_central.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        panel_central.columnconfigure(0, weight=1)
        panel_central.rowconfigure(0, weight=1)
        
        # Treeview para tareas
        tree_frame = ttk.Frame(panel_central)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Treeview
        self.tree_tareas = ttk.Treeview(tree_frame, 
                                        columns=('ID', 'Nombre', 'Estado', 'Prioridad', 'Deps'),
                                        show='headings',
                                        yscrollcommand=vsb.set,
                                        xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree_tareas.yview)
        hsb.config(command=self.tree_tareas.xview)
        
        # Configurar columnas
        self.tree_tareas.heading('ID', text='ID')
        self.tree_tareas.heading('Nombre', text='Nombre')
        self.tree_tareas.heading('Estado', text='Estado')
        self.tree_tareas.heading('Prioridad', text='Prioridad')
        self.tree_tareas.heading('Deps', text='Dependencias')
        
        self.tree_tareas.column('ID', width=50, anchor=tk.CENTER)
        self.tree_tareas.column('Nombre', width=250)
        self.tree_tareas.column('Estado', width=100, anchor=tk.CENTER)
        self.tree_tareas.column('Prioridad', width=80, anchor=tk.CENTER)
        self.tree_tareas.column('Deps', width=100, anchor=tk.CENTER)
        
        self.tree_tareas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de acciones sobre tarea seleccionada
        btn_frame = ttk.Frame(panel_central)
        btn_frame.grid(row=1, column=0, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Ver Detalles", 
                  command=self.ver_detalles_tarea).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Editar", 
                  command=self.editar_tarea).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Eliminar", 
                  command=self.eliminar_tarea).pack(side=tk.LEFT, padx=2)
        
        # ===== PANEL DERECHO - INFORMACIÓN =====
        panel_der = ttk.LabelFrame(main_frame, text="Información", padding="10")
        panel_der.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        panel_der.columnconfigure(0, weight=1)
        panel_der.rowconfigure(0, weight=1)
        
        # Text widget para información
        text_frame = ttk.Frame(panel_der)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        vsb_info = ttk.Scrollbar(text_frame, orient="vertical")
        vsb_info.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.text_info = tk.Text(text_frame, wrap=tk.WORD, width=30, height=20,
                                 yscrollcommand=vsb_info.set, font=('Arial', 10))
        self.text_info.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb_info.config(command=self.text_info.yview)
        
        # Mensaje inicial
        self.text_info.insert('1.0', "👋 Bienvenido al Gestor de Tareas\n\n"
                                    "Usa los botones de la izquierda para:\n"
                                    "• Crear nuevas tareas\n"
                                    "• Agregar dependencias\n"
                                    "• Ver orden de ejecución\n"
                                    "• Consultar tareas ejecutables\n\n"
                                    "Selecciona una tarea para ver sus detalles.")
        self.text_info.config(state=tk.DISABLED)
    
    # ===== MÉTODOS DE ACTUALIZACIÓN =====
    
    def actualizar_vistas(self):
        """Actualiza todas las vistas"""
        self.actualizar_lista_tareas()
        self.actualizar_estadisticas()
    
    def actualizar_lista_tareas(self):
        """Actualiza el Treeview de tareas"""
        # Limpiar
        for item in self.tree_tareas.get_children():
            self.tree_tareas.delete(item)
        
        # Cargar tareas
        tareas = self.gestor.obtener_todas_tareas()
        
        for tarea in tareas:
            # Contar dependencias
            deps = self.gestor.obtener_dependencias(tarea.id)
            num_deps = len(deps)
            
            # Determinar tag para color
            tag = tarea.estado
            
            self.tree_tareas.insert('', tk.END, 
                                   values=(tarea.id, tarea.nombre, tarea.estado, 
                                          tarea.prioridad, num_deps),
                                   tags=(tag,))
        
        # Configurar colores
        self.tree_tareas.tag_configure('completada', background='#d4edda')
        self.tree_tareas.tag_configure('en_progreso', background='#fff3cd')
        self.tree_tareas.tag_configure('pendiente', background='#f8f9fa')
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas"""
        stats = self.gestor.obtener_estadisticas()
        
        self.stats_labels['total'].config(text=str(stats['total_tareas']))
        self.stats_labels['completadas'].config(text=str(stats['completadas']))
        self.stats_labels['pendientes'].config(text=str(stats['pendientes']))
        self.stats_labels['ejecutables'].config(text=str(stats['ejecutables']))
        self.stats_labels['porcentaje'].config(
            text=f"{stats['porcentaje_completado']:.1f}%"
        )
    
    def actualizar_info(self, texto: str):
        """
        Actualiza el panel de información
        
        Args:
            texto: Texto a mostrar
        """
        self.text_info.config(state=tk.NORMAL)
        self.text_info.delete('1.0', tk.END)
        self.text_info.insert('1.0', texto)
        self.text_info.config(state=tk.DISABLED)
    
    # ===== DIÁLOGOS Y OPERACIONES =====
    
    def crear_tarea_dialog(self):
        """Diálogo para crear una nueva tarea"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Tarea")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        frame = ttk.Frame(dialog, padding="20")
        frame

        ```python
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        ttk.Label(frame, text="Nombre:*", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.grid(row=0, column=1, pady=5, padx=5)
        entry_nombre.focus()
        
        ttk.Label(frame, text="Descripción:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        text_desc = tk.Text(frame, width=30, height=5)
        text_desc.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(frame, text="Prioridad (1-5):", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        var_prioridad = tk.IntVar(value=3)
        spinbox_prioridad = ttk.Spinbox(frame, from_=1, to=5, textvariable=var_prioridad, width=10)
        spinbox_prioridad.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(frame, text="Estimación (horas):", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        entry_horas = ttk.Entry(frame, width=10)
        entry_horas.insert(0, "0")
        entry_horas.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def guardar():
            nombre = entry_nombre.get().strip()
            descripcion = text_desc.get('1.0', tk.END).strip()
            prioridad = var_prioridad.get()
            
            try:
                estimacion = float(entry_horas.get())
            except ValueError:
                estimacion = 0.0
            
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre es obligatorio", parent=dialog)
                return
            
            exito, mensaje, tarea_id = self.gestor.crear_tarea(
                nombre, descripcion, prioridad, None, estimacion
            )
            
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=dialog)
                self.actualizar_vistas()
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=dialog)
        
        ttk.Button(btn_frame, text="Guardar", command=guardar, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # Enter para guardar
        dialog.bind('<Return>', lambda e: guardar())
    
    def agregar_dependencia_dialog(self):
        """Diálogo para agregar una dependencia"""
        tareas = self.gestor.obtener_todas_tareas()
        
        if len(tareas) < 2:
            messagebox.showinfo("Información", 
                               "Necesitas al menos 2 tareas para crear una dependencia")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Dependencia")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Instrucciones
        ttk.Label(frame, text="Selecciona las tareas:", 
                 font=('Arial', 11, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Tarea origen (prerequisito)
        ttk.Label(frame, text="Tarea prerequisito:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        tareas_dict_origen = {f"[{t.id}] {t.nombre}": t.id for t in tareas}
        var_origen = tk.StringVar()
        combo_origen = ttk.Combobox(frame, textvariable=var_origen, 
                                    values=list(tareas_dict_origen.keys()), 
                                    state='readonly', width=35)
        combo_origen.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(frame, text="⬇ debe completarse antes que ⬇", 
                 font=('Arial', 9, 'italic'), foreground='gray').grid(
            row=2, column=0, columnspan=2, pady=5)
        
        # Tarea destino (dependiente)
        ttk.Label(frame, text="Tarea dependiente:", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        
        tareas_dict_destino = {f"[{t.id}] {t.nombre}": t.id for t in tareas}
        var_destino = tk.StringVar()
        combo_destino = ttk.Combobox(frame, textvariable=var_destino,
                                     values=list(tareas_dict_destino.keys()),
                                     state='readonly', width=35)
        combo_destino.grid(row=3, column=1, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def guardar():
            if not var_origen.get() or not var_destino.get():
                messagebox.showwarning("Advertencia", 
                                      "Debes seleccionar ambas tareas", parent=dialog)
                return
            
            origen_id = tareas_dict_origen[var_origen.get()]
            destino_id = tareas_dict_destino[var_destino.get()]
            
            exito, mensaje = self.gestor.agregar_dependencia(origen_id, destino_id)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=dialog)
                self.actualizar_vistas()
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"⚠️ {mensaje}", parent=dialog)
        
        ttk.Button(btn_frame, text="Agregar", command=guardar, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def marcar_completada_dialog(self):
        """Marca una tarea como completada"""
        tareas_pendientes = [t for t in self.gestor.obtener_todas_tareas() 
                            if t.estado != 'completada']
        
        if not tareas_pendientes:
            messagebox.showinfo("Información", "No hay tareas pendientes")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Marcar como Completada")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Selecciona la tarea completada:", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 15))
        
        tareas_dict = {f"[{t.id}] {t.nombre} - {t.estado}": t.id for t in tareas_pendientes}
        var_tarea = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var_tarea,
                            values=list(tareas_dict.keys()),
                            state='readonly', width=45)
        combo.pack(pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        def completar():
            if not var_tarea.get():
                messagebox.showwarning("Advertencia", 
                                      "Debes seleccionar una tarea", parent=dialog)
                return
            
            tarea_id = tareas_dict[var_tarea.get()]
            exito, mensaje, desbloqueadas = self.gestor.marcar_completada(tarea_id)
            
            if exito:
                msg_completo = mensaje
                if desbloqueadas:
                    tareas_desb = [self.gestor.obtener_tarea(id) for id in desbloqueadas]
                    nombres = [t.nombre for t in tareas_desb if t]
                    msg_completo += f"\n\nTareas desbloqueadas:\n• " + "\n• ".join(nombres)
                
                messagebox.showinfo("Éxito", msg_completo, parent=dialog)
                self.actualizar_vistas()
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=dialog)
        
        ttk.Button(btn_frame, text="✓ Completar", command=completar, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def mostrar_orden_ejecucion(self):
        """Muestra el orden de ejecución sugerido"""
        orden = self.gestor.calcular_orden_ejecucion()
        
        if orden is None:
            self.actualizar_info("❌ ERROR: Se detectó un ciclo en las dependencias.\n\n"
                               "Esto significa que existe una dependencia circular que hace "
                               "imposible completar el proyecto.\n\n"
                               "Por favor, revisa y elimina las dependencias circulares.")
            messagebox.showerror("Error", 
                               "Se detectó un ciclo en las dependencias. "
                               "No es posible calcular un orden válido.")
            return
        
        if not orden:
            self.actualizar_info("✓ ¡Todas las tareas están completadas!\n\n"
                               "No hay tareas pendientes en el proyecto.")
            return
        
        texto = "📊 ORDEN DE EJECUCIÓN SUGERIDO\n"
        texto += "=" * 40 + "\n\n"
        texto += "Este es un orden válido para ejecutar todas las tareas\n"
        texto += "respetando sus dependencias:\n\n"
        
        for i, tarea in enumerate(orden, 1):
            # Obtener dependencias
            deps = self.gestor.obtener_dependencias(tarea.id)
            deps_str = ", ".join([f"#{d.id}" for d in deps]) if deps else "Ninguna"
            
            texto += f"{i}. [{tarea.id}] {tarea.nombre}\n"
            texto += f"   Estado: {tarea.estado} | Prioridad: {tarea.prioridad}\n"
            texto += f"   Depende de: {deps_str}\n\n"
        
        self.actualizar_info(texto)
    
    def mostrar_tareas_ejecutables(self):
        """Muestra las tareas que pueden ejecutarse ahora"""
        ejecutables = self.gestor.obtener_tareas_ejecutables()
        
        if not ejecutables:
            self.actualizar_info("ℹ️ NO HAY TAREAS EJECUTABLES\n\n"
                               "Esto puede significar:\n"
                               "• Todas las tareas están completadas\n"
                               "• Todas las tareas pendientes tienen dependencias sin completar\n\n"
                               "Revisa el estado de las tareas y sus dependencias.")
            return
        
        texto = "🎯 TAREAS EJECUTABLES AHORA\n"
        texto += "=" * 40 + "\n\n"
        texto += "Estas tareas pueden iniciarse inmediatamente\n"
        texto += "(no tienen dependencias pendientes):\n\n"
        
        for i, tarea in enumerate(ejecutables, 1):
            texto += f"{i}. [{tarea.id}] {tarea.nombre}\n"
            texto += f"   Prioridad: {tarea.prioridad}/5\n"
            texto += f"   Estado: {tarea.estado}\n"
            if tarea.estimacion_horas > 0:
                texto += f"   Estimación: {tarea.estimacion_horas}h\n"
            texto += "\n"
        
        self.actualizar_info(texto)
    
    def mostrar_siguiente_tarea(self):
        """Muestra la siguiente tarea recomendada"""
        siguiente = self.gestor.obtener_siguiente_tarea()
        
        if not siguiente:
            self.actualizar_info("ℹ️ NO HAY SIGUIENTE TAREA\n\n"
                               "• Todas las tareas están completadas, o\n"
                               "• No hay tareas ejecutables en este momento\n\n"
                               "¡Buen trabajo! 🎉")
            messagebox.showinfo("Información", 
                               "No hay tareas disponibles para ejecutar en este momento.")
            return
        
        # Obtener información adicional
        deps = self.gestor.obtener_dependencias(siguiente.id)
        dependientes = self.gestor.obtener_dependientes(siguiente.id)
        
        texto = "⭐ TU PRÓXIMA TAREA ES:\n"
        texto += "=" * 40 + "\n\n"
        texto += f"📌 {siguiente.nombre}\n\n"
        texto += f"ID: {siguiente.id}\n"
        texto += f"Prioridad: {siguiente.prioridad}/5 {'⭐' * siguiente.prioridad}\n"
        texto += f"Estado: {siguiente.estado}\n"
        
        if siguiente.estimacion_horas > 0:
            texto += f"Tiempo estimado: {siguiente.estimacion_horas} horas\n"
        
        if siguiente.descripcion:
            texto += f"\nDescripción:\n{siguiente.descripcion}\n"
        
        if deps:
            texto += f"\n✓ Dependencias completadas:\n"
            for dep in deps:
                texto += f"  • [{dep.id}] {dep.nombre}\n"
        
        if dependientes:
            texto += f"\n🔓 Al completar esta tarea se desbloquearán:\n"
            for dep in dependientes:
                texto += f"  • [{dep.id}] {dep.nombre}\n"
        
        texto += "\n" + "=" * 40 + "\n"
        texto += "💡 Consejo: Enfócate en esta tarea para\n   maximizar tu progreso."
        
        self.actualizar_info(texto)
        
        # Preguntar si quiere agregarla al plan diario
        respuesta = messagebox.askyesno("Plan Diario", 
                                        f"¿Deseas agregar esta tarea\nal plan diario?\n\n{siguiente.nombre}",
                                        parent=self.root)
        if respuesta:
            exito, mensaje = self.gestor.agregar_al_plan_diario(siguiente.id)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showwarning("Advertencia", mensaje)
    
    def mostrar_plan_diario(self):
        """Muestra el plan diario"""
        plan = self.gestor.obtener_plan_diario()
        
        if not plan:
            self.actualizar_info("📅 PLAN DIARIO VACÍO\n\n"
                               "No hay tareas en el plan diario.\n\n"
                               "Usa el botón 'Siguiente Tarea' para obtener\n"
                               "recomendaciones y agregarlas al plan.")
            return
        
        texto = "📅 PLAN DIARIO\n"
        texto += "=" * 40 + "\n\n"
        texto += f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n"
        texto += f"Total de tareas: {len(plan)}\n\n"
        
        for i, tarea in enumerate(plan, 1):
            texto += f"{i}. [{tarea.id}] {tarea.nombre}\n"
            texto += f"   Prioridad: {tarea.prioridad}/5\n"
            if tarea.estimacion_horas > 0:
                texto += f"   Estimación: {tarea.estimacion_horas}h\n"
            texto += "\n"
        
        self.actualizar_info(texto)
    
    def ver_detalles_tarea(self):
        """Muestra los detalles de la tarea seleccionada"""
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una tarea primero")
            return
        
        item = self.tree_tareas.item(seleccion[0])
        tarea_id = item['values'][0]
        
        tarea = self.gestor.obtener_tarea(tarea_id)
        if not tarea:
            messagebox.showerror("Error", "No se pudo cargar la tarea")
            return
        
        # Obtener dependencias
        deps = self.gestor.obtener_dependencias(tarea.id)
        dependientes = self.gestor.obtener_dependientes(tarea.id)
        
        texto = f"📋 DETALLES DE LA TAREA\n"
        texto += "=" * 40 + "\n\n"
        texto += f"Nombre: {tarea.nombre}\n"
        texto += f"ID: {tarea.id}\n"
        texto += f"Estado: {tarea.estado}\n"
        texto += f"Prioridad: {tarea.prioridad}/5\n"
        
        if tarea.estimacion_horas > 0:
            texto += f"Estimación: {tarea.estimacion_horas} horas\n"
        
        if tarea.fecha_creacion:
            texto += f"Creada: {tarea.fecha_creacion.strftime('%d/%m/%Y %H:%M')}\n"
        
        if tarea.fecha_limite:
            texto += f"Fecha límite: {tarea.fecha_limite.strftime('%d/%m/%Y')}\n"
        
        if tarea.descripcion:
            texto += f"\nDescripción:\n{tarea.descripcion}\n"
        
        if deps:
            texto += f"\n📥 Depende de ({len(deps)}):\n"
            for dep in deps:
                estado_icon = "✓" if dep.estado == "completada" else "○"
                texto += f"  {estado_icon} [{dep.id}] {dep.nombre}\n"
        else:
            texto += f"\n📥 Sin dependencias (puede iniciarse ahora)\n"
        
        if dependientes:
            texto += f"\n📤 Bloquea a ({len(dependientes)}):\n"
            for dep in dependientes:
                texto += f"  • [{dep.id}] {dep.nombre}\n"
        
        self.actualizar_info(texto)
    
    def editar_tarea(self):
        """Edita la tarea seleccionada"""
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una tarea primero")
            return
        
        item = self.tree_tareas.item(seleccion[0])
        tarea_id = item['values'][0]
        
        tarea = self.gestor.obtener_tarea(tarea_id)
        if not tarea:
            messagebox.showerror("Error", "No se pudo cargar la tarea")
            return
        
        # Diálogo de edición
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar Tarea #{tarea.id}")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos
        ttk.Label(frame, text="Nombre:*", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40)
        entry_nombre.insert(0, tarea.nombre)
        entry_nombre.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(frame, text="Descripción:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        text_desc = tk.Text(frame, width=30, height=5)
        text_desc.insert('1.0', tarea.descripcion)
        text_desc.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(frame, text="Estado:", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        var_estado = tk.StringVar(value=tarea.estado)
        combo_estado = ttk.Combobox(frame, textvariable=var_estado,
                                    values=['pendiente', 'en_progreso', 'completada'],
                                    state='readonly', width=15)
        combo_estado.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(frame, text="Prioridad (1-5):", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        var_prioridad = tk.IntVar(value=tarea.prioridad)
        spinbox_prioridad = ttk.Spinbox(frame, from_=1, to=5, textvariable=var_prioridad, width=10)
        spinbox_prioridad.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(frame, text="Estimación (horas):", font=('Arial', 10)).grid(
            row=4, column=0, sticky=tk.W, pady=5)
        entry_horas = ttk.Entry(frame, width=10)
        entry_horas.insert(0, str(tarea.estimacion_horas))
        entry_horas.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def guardar():
            tarea.nombre = entry_nombre.get().strip()
            tarea.descripcion = text_desc.get('1.0', tk.END).strip()
            tarea.estado = var_estado.get()
            tarea.prioridad = var_prioridad.get()
            
            try:
                tarea.estimacion_horas = float(entry_horas.get())
            except ValueError:
                tarea.estimacion_horas = 0.0
            
            exito, mensaje = self.gestor.actualizar_tarea(tarea)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje, parent=dialog)
                self.actualizar_vistas()
                dialog.destroy()
            else:
                messagebox.showerror("Error", mensaje, parent=dialog)
        
        ttk.Button(btn_frame, text="Guardar", command=guardar, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def eliminar_tarea(self):
        """Elimina la tarea seleccionada"""
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showinfo("Información", "Selecciona una tarea primero")
            return
        
        item = self.tree_tareas.item(seleccion[0])
        tarea_id = item['values'][0]
        tarea_nombre = item['values'][1]
        
        # Confirmar
        respuesta = messagebox.askyesno("Confirmar eliminación",
                                       f"¿Estás seguro de eliminar la tarea?\n\n"
                                       f"[{tarea_id}] {tarea_nombre}\n\n"
                                       f"Esta acción también eliminará todas\n"
                                       f"sus dependencias asociadas.",
                                       icon='warning')
        
        if respuesta:
            exito, mensaje = self.gestor.eliminar_tarea(tarea_id)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_vistas()
                self.actualizar_info("Tarea eliminada exitosamente")
            else:
                messagebox.showerror("Error", mensaje)
    
    # ===== MÉTODOS DE CONTROL =====
    
    def iniciar(self):
        """Inicia el loop principal de la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.root.mainloop()
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación"""
        respuesta = messagebox.askyesno("Salir", 
                                        "¿Estás seguro de que deseas salir?")
        if respuesta:
            self.gestor.cerrar()
            self.root.destroy()
```

---

## 9. `requirements.txt`

```txt
# Gestor de Tareas con Dependencias
# Python 3.11+

# No se requieren bibliotecas externas para el prototipo Fase 1
# Tkinter viene incluido con Python

# Para Fase 2 (opcional):
# matplotlib>=3.7.0
# networkx>=3.0
```

---

## 10. `README.md`

```markdown
# Gestor de Tareas con Dependencias

Sistema de gestión de tareas que modela dependencias usando grafos dirigidos acíclicos (DAG) y calcula ordenamientos topológicos para optimizar la planificación.

## Características - Fase 1 (30%)

### Funcionalidades Implementadas

✅ **Gestión de Tareas**
- Crear tareas con nombre, descripción, prioridad (1-5), estimación de horas
- Editar información de tareas existentes
- Eliminar tareas
- Marcar tareas como completadas

✅ **Gestión de Dependencias**
- Agregar dependencias entre tareas (Tarea A debe completarse antes que B)
- Detección automática de ciclos (previene dependencias circulares)
- Eliminar dependencias
- Visualizar dependencias de cada tarea

✅ **Planificación Inteligente**
- Cálculo de orden de ejecución válido (Ordenamiento Topológico - Algoritmo de Kahn)
- Identificación de tareas ejecutables (sin dependencias pendientes)
- Recomendación de "siguiente tarea" basada en prioridad y dependencias
- Gestión de plan diario con cola FIFO

✅ **Persistencia de Datos**
- Base de datos SQLite
- Operaciones CRUD completas
- Integridad referencial
- Índices para optimización

✅ **Interfaz Gráfica**
- Interfaz amigable con Tkinter
- Visualización de todas las tareas
- Panel de información contextual
- Estadísticas en tiempo real

## Requisitos del Sistema

- Python 3.11 o superior
- Tkinter (incluido con Python)
- SQLite3 (incluido con Python)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone [URL_DEL_REPOSITORIO]
cd gestor-tareas-deps
```

### 2. Verificar instalación de Python

```bash
python --version
# Debe mostrar Python 3.11 o superior
```

### 3. No se requiere instalación de dependencias adicionales
Todas las bibliotecas necesarias vienen incluidas con Python.

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Operaciones Básicas

#### Crear una Tarea
1. Click en "➕ Nueva Tarea"
2. Ingresar nombre (obligatorio)
3. Opcional: descripción, prioridad, estimación
4. Click en "Guardar"

#### Agregar Dependencia
1. Click en "🔗 Agregar Dependencia"
2. Seleccionar tarea prerequisito
3. Seleccionar tarea dependiente
4. Click en "Agregar"
5. El sistema validará que no se creen ciclos

#### Ver Orden de Ejecución
1. Click en "📊 Ver Orden de Ejecución"
2. El sistema mostrará todas las tareas en un orden válido
3. Si

```markdown
3. Si hay un ciclo, mostrará un error

#### Obtener Siguiente Tarea
1. Click en "⭐ Siguiente Tarea"
2. El sistema recomendará la tarea más prioritaria que puede ejecutarse
3. Opción de agregarla al plan diario

#### Marcar Tarea como Completada
1. Click en "✓ Marcar Completada"
2. Seleccionar la tarea de la lista
3. El sistema mostrará qué tareas se desbloquean

## Estructura del Proyecto

```
gestor-tareas-deps/
│
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias (vacío en Fase 1)
├── README.md                        # Este archivo
│
└── src/
    ├── __init__.py
    │
    ├── models/                      # Modelos de datos
    │   ├── __init__.py
    │   ├── tarea.py                 # Clase Tarea
    │   ├── grafo_tareas.py          # Grafo (DAG) + ordenamiento topológico
    │   └── plan_diario.py           # Cola para plan diario
    │
    ├── database/                    # Capa de persistencia
    │   ├── __init__.py
    │   ├── db_manager.py            # Gestor de base de datos
    │   └── schema.sql               # Esquema de BD
    │
    ├── controllers/                 # Lógica de negocio
    │   ├── __init__.py
    │   └── gestor_proyecto.py       # Controlador principal
    │
    └── views/                       # Interfaz gráfica
        ├── __init__.py
        └── main_window.py           # Ventana principal (Tkinter)
```

## Estructuras de Datos Implementadas

### 1. Grafo Dirigido Acíclico (DAG)
- **Representación:** Lista de adyacencia con diccionarios
- **Complejidad espacial:** O(V + E)
- **Operaciones:**
  - Agregar nodo: O(1)
  - Agregar arista: O(1)
  - Detectar ciclo (DFS): O(V + E)
  - Ordenamiento topológico (Kahn): O(V + E)

### 2. Cola (Queue)
- **Implementación:** `collections.deque`
- **Operaciones:**
  - Enqueue: O(1)
  - Dequeue: O(1)
  - Peek: O(1)

### 3. Diccionario Hash
- **Uso:** Almacenamiento de metadatos de tareas
- **Complejidad:** O(1) promedio para búsqueda

## Base de Datos

### Esquema

**Tabla: tareas**
```sql
- id: INTEGER PRIMARY KEY
- nombre: VARCHAR(200) NOT NULL
- descripcion: TEXT
- estado: VARCHAR(20) -- 'pendiente', 'en_progreso', 'completada'
- prioridad: INTEGER (1-5)
- fecha_creacion: DATETIME
- fecha_limite: DATETIME
- estimacion_horas: REAL
```

**Tabla: dependencias**
```sql
- id: INTEGER PRIMARY KEY
- tarea_origen: INTEGER (FK -> tareas.id)
- tarea_destino: INTEGER (FK -> tareas.id)
- fecha_creacion: DATETIME
```

### Constraints
- No auto-dependencias
- Dependencias únicas
- Claves foráneas con CASCADE DELETE
- Check constraints para validación

## Algoritmos Clave

### Ordenamiento Topológico (Algoritmo de Kahn)

```python
def ordenamiento_topologico():
    1. Calcular grado de entrada de cada nodo
    2. Inicializar cola con nodos de grado 0
    3. Mientras la cola no esté vacía:
       a. Extraer nodo
       b. Agregarlo al resultado
       c. Reducir grado de sus vecinos
       d. Si vecino llega a grado 0, agregarlo a cola
    4. Si procesamos todos los nodos: orden válido
       Si no: existe ciclo
```

**Complejidad:** O(V + E) donde V = tareas, E = dependencias

### Detección de Ciclos (DFS)

```python
def detectar_ciclo():
    Para cada nodo no visitado:
        DFS con conjunto de nodos en recursión
        Si encontramos nodo en recursión: ciclo detectado
```

**Complejidad:** O(V + E)

## Ejemplos de Uso

### Caso 1: Proyecto de Software

```
Tareas:
1. Análisis de requisitos
2. Diseño de arquitectura
3. Implementar módulo A
4. Implementar módulo B
5. Pruebas de integración
6. Despliegue

Dependencias:
1 -> 2  (Análisis antes que Diseño)
2 -> 3  (Diseño antes que Módulo A)
2 -> 4  (Diseño antes que Módulo B)
3 -> 5  (Módulo A antes que Pruebas)
4 -> 5  (Módulo B antes que Pruebas)
5 -> 6  (Pruebas antes que Despliegue)

Orden válido: 1, 2, 3, 4, 5, 6
Otro orden válido: 1, 2, 4, 3, 5, 6
```

### Caso 2: Preparación de Evento

```
Tareas:
1. Definir presupuesto
2. Reservar local
3. Contratar catering
4. Diseñar invitaciones
5. Enviar invitaciones
6. Confirmar asistentes

Dependencias:
1 -> 2  (Presupuesto antes que Local)
1 -> 3  (Presupuesto antes que Catering)
1 -> 4  (Presupuesto antes que Invitaciones)
4 -> 5  (Diseñar antes que Enviar)
5 -> 6  (Enviar antes que Confirmar)

Tareas ejecutables inicialmente: 1
Después de completar 1: 2, 3, 4
```

## Características Adicionales Implementadas

### Validaciones
- ✅ Nombres de tarea no vacíos
- ✅ Prioridad entre 1 y 5
- ✅ No auto-dependencias
- ✅ Detección de ciclos
- ✅ No duplicar dependencias

### Estadísticas
- Total de tareas
- Tareas por estado (pendiente, en progreso, completada)
- Tareas ejecutables
- Porcentaje de avance
- Total de dependencias

### Interfaz
- Colores por estado (verde=completada, amarillo=en progreso, gris=pendiente)
- Panel de información contextual
- Mensajes informativos y de error
- Confirmaciones para acciones destructivas

## Limitaciones de la Fase 1

- ❌ Sin visualización gráfica del grafo
- ❌ Sin cálculo de camino crítico
- ❌ Sin diagramas de Gantt
- ❌ Sin análisis de fechas límite
- ❌ Sin exportación de datos
- ❌ Sin múltiples proyectos
- ❌ Sin colaboración multi-usuario

*Estas características se implementarán en la Fase 2*

## Solución de Problemas

### Error: "No module named 'tkinter'"

**En Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**En macOS:**
```bash
brew install python-tk
```

### Error: "Database is locked"

Cierra todas las instancias de la aplicación y vuelve a intentar.

### La aplicación no inicia

1. Verifica la versión de Python: `python --version`
2. Verifica que estés en el directorio correcto
3. Ejecuta: `python main.py`

### Ciclo detectado al agregar dependencia

Esto es correcto. El sistema previene dependencias circulares.
Ejemplo de ciclo:
- A depende de B
- B depende de C
- C depende de A ❌

## Pruebas Sugeridas

### Prueba 1: Flujo Básico
1. Crear 3 tareas: A, B, C
2. Agregar dependencia: A -> B
3. Agregar dependencia: B -> C
4. Ver orden de ejecución (debe ser: A, B, C)
5. Marcar A como completada
6. Verificar que B sea ejecutable
7. Marcar B como completada
8. Verificar que C sea ejecutable

### Prueba 2: Detección de Ciclos
1. Crear tareas: X, Y, Z
2. Agregar: X -> Y
3. Agregar: Y -> Z
4. Intentar agregar: Z -> X (debe fallar con mensaje de ciclo)

### Prueba 3: Orden Topológico Complejo
1. Crear 6 tareas con dependencias tipo DAG
2. Verificar que el orden respete todas las dependencias
3. Completar tareas en orden y verificar desbloqueos

### Prueba 4: Tareas Independientes
1. Crear 3 tareas sin dependencias
2. Verificar que todas sean ejecutables
3. El orden de ejecución puede variar

## Contribución al Proyecto

### Para Fase 2, se planea agregar:

**Funcionalidades de Estimaciones:**
- Cálculo de tiempo total del proyecto
- Identificación del camino crítico (Critical Path Method)
- Análisis de holguras

**Visualización:**
- Grafo visual con NetworkX y Matplotlib
- Diagrama de Gantt básico
- Línea de tiempo

**Mejoras de Planificación:**
- Fechas límite con alertas
- Recursos asignados a tareas
- Múltiples proyectos

## Autores

- [Nombre Estudiante 1] - [Carné]
- [Nombre Estudiante 2] - [Carné]
- [Nombre Estudiante 3] - [Carné]
- [Nombre Estudiante 4] - [Carné]

## Licencia

Proyecto académico - Universidad Técnica Particular de Loja
Programación con Estructuras de Datos (PED941)
Ciclo 02-2025

## Referencias

- Cormen, T. H., et al. (2022). Introduction to Algorithms (4th ed.)
- Algoritmo de Kahn para ordenamiento topológico
- Documentación oficial de Python: https://docs.python.org/3/
- SQLite Documentation: https://www.sqlite.org/docs.html

## Contacto

Para preguntas sobre el proyecto, contactar al docente de la asignatura.

---

**Versión:** 1.0 (Fase 1 - Prototipo 30%)  
**Fecha:** Octubre 2025  
**Estado:** ✅ Funcional
```

---

## 11. Archivo adicional: `src/__init__.py` y otros `__init__.py`

Para cada carpeta dentro de `src`, crear un archivo `__init__.py` vacío o con:

```python
"""
Módulo [nombre del paquete]
"""
```

---

## Instrucciones de Ejecución

### 1. Crear la estructura de carpetas

```bash
mkdir -p gestor-tareas-deps/src/models
mkdir -p gestor-tareas-deps/src/database
mkdir -p gestor-tareas-deps/src/controllers
mkdir -p gestor-tareas-deps/src/views
```

### 2. Crear todos los archivos

Copiar cada código en su archivo correspondiente según la estructura indicada.

### 3. Crear archivos `__init__.py` vacíos

```bash
touch gestor-tareas-deps/src/__init__.py
touch gestor-tareas-deps/src/models/__init__.py
touch gestor-tareas-deps/src/database/__init__.py
touch gestor-tareas-deps/src/controllers/__init__.py
touch gestor-tareas-deps/src/views/__init__.py
```

### 4. Ejecutar la aplicación

```bash
cd gestor-tareas-deps
python main.py
```

### 5. Verificación

Al ejecutar, deberías ver:
- Ventana principal con interfaz gráfica
- Panel de acciones a la izquierda
- Lista de tareas en el centro
- Panel de información a la derecha
- Base de datos `gestor_tareas.db` creada automáticamente

---

## Características Implementadas (30% del proyecto)

✅ **CRUD de Tareas** - Crear, Leer, Actualizar, Eliminar  
✅ **Gestión de Dependencias** - Agregar/Eliminar con validación de ciclos  
✅ **Grafo DAG** - Lista de adyacencia con algoritmos de grafos  
✅ **Ordenamiento Topológico** - Algoritmo de Kahn implementado  
✅ **Detección de Ciclos** - DFS para prevenir dependencias circulares  
✅ **Tareas Ejecutables** - Identificación automática  
✅ **Siguiente Tarea** - Recomendación basada en prioridad  
✅ **Plan Diario** - Cola FIFO para organización  
✅ **Base de Datos SQLite** - Persistencia completa  
✅ **Interfaz Gráfica Tkinter** - Amigable e intuitiva  
✅ **Estadísticas** - Métricas en tiempo real  

---

Este código está listo para ejecutarse y cumple con todos los requisitos de la Fase 1 del proyecto. La implementación usa las estructuras de datos especificadas (grafo, cola) y proporciona todas las funcionalidades solicitadas al 30% del proyecto completo.

