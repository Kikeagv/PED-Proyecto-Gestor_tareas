# Gestor de Tareas con Dependencias

**Prototipo Fase 1 (30%) - Programación con Estructuras de Datos**

Un sistema de gestión de tareas que maneja dependencias entre ellas usando estructuras de datos tipo grafo y ordenamiento topológico.

## 🎯 Funcionalidades Implementadas

### Gestión de Tareas
- ✅ Crear nuevas tareas con nombre, descripción, prioridad y fecha límite
- ✅ Ver listado completo de todas las tareas
- ✅ Eliminar tareas existentes
- ✅ Marcar tareas como completadas
- ✅ Editar información básica de tareas

### Gestión de Dependencias
- ✅ Agregar dependencias entre tareas (Tarea A debe completarse antes que Tarea B)
- ✅ Detección automática de ciclos al agregar dependencias
- ✅ Visualización de dependencias en formato de lista

### Planificación Inteligente
- ✅ Calcular orden de ejecución válido mediante ordenamiento topológico (Algoritmo de Kahn)
- ✅ Identificar tareas ejecutables en el momento actual
- ✅ Mostrar "siguiente tarea recomendada" basada en prioridad y dependencias
- ✅ Plan diario de trabajo con gestión de cola (FIFO)

### Base de Datos
- ✅ Persistencia de datos con SQLite
- ✅ Tablas: `tareas`, `dependencias`
- ✅ Operaciones CRUD básicas
- ✅ Datos persisten entre sesiones

### Interfaz Gráfica
- ✅ Ventana principal intuitiva con Tkinter
- ✅ Panel de acciones principales
- ✅ Vista detallada de tareas
- ✅ Información de dependencias
- ✅ Estadísticas del proyecto

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.11+
- No requiere bibliotecas externas (usa solo estándar de Python)

### Instalación y Ejecución

1. **Clonar o descargar el proyecto**
   ```bash
   # Si estás en el directorio del proyecto
   cd /Users/enriqueagv/projects/desktop/ped1
   ```

### 🎯 Opciones de Interfaz

#### Opción 1: Interfaz Web (Recomendada para macOS 16)
Funciona en cualquier navegador web y es compatible con todas las versiones de macOS.

```bash
python3 start_web.py
```

Luego abre tu navegador en: **http://localhost:8080**

*Alternativamente:* `python3 web_interface_fixed.py` (versión corregida)

#### Opción 2: Interfaz de Línea de Comandos (CLI)
Perfecta para desarrolladores, funciona en cualquier sistema operativo.

```bash
python3 main_cli.py
```

#### Opción 3: Interfaz Gráfica Tkinter (Para macOS 26+)
La interfaz gráfica original (puede no funcionar en versiones antiguas de macOS).

```bash
python3 main.py
```

### 📊 Bases de Datos

Cada interfaz usa su propia base de datos:
- Web: `gestor_tareas_web.db`
- CLI: `gestor_tareas_cli.db`
- GUI: `gestor_tareas.db`

3. **Primera vez**
   - Se creará automáticamente el archivo de base de datos correspondiente
   - Este archivo contiene toda tu información de tareas y dependencias

## 🎮 Uso de la Aplicación

### 🌐 Interfaz Web
- **Navegador moderno**: Abre `http://localhost:8080` en tu navegador preferido
- **Panel Izquierdo**: Acciones principales (botones interactivos)
- **Panel Central**: Listado visual de todas las tareas
- **Panel Derecho**: Estadísticas del proyecto en tiempo real
- **Modales**: Formularios emergentes para crear tareas y agregar dependencias
- **Auto-refresh**: Actualización automática cada 30 segundos

### 💻 Interfaz CLI (Línea de Comandos)
- **Menu numérico**: Selecciona opciones del 0-10
- **Navegación por números**: Ingresa IDs de las tareas para operaciones específicas
- **Clear interface**: Pantalla limpia con colores y emojis para mejor legibilidad
- **Validaciones**: Verificación automática de entradas y errores
- **Progreso**: Indicadores visuales del avance del proyecto

### 🖥️ Interfaz GUI Tkinter
- **Panel Izquierdo**: Acciones disponibles
- **Panel Central**: Listado de todas las tareas
- **Panel Derecho**: Detalles de la tarea seleccionada

### Flu Básico de Trabajo

1. **Crear Tareas**: Usa "➕ Nueva Tarea"
2. **Establecer Dependencias**: Usa "🔗 Agregar Dependencia"
3. **Ver Orden Sugerido**: Usa "📊 Ver Orden de Ejecución"
4. **Ver Disponibles**: Usa "🎯 Tareas Ejecutables"
5. **Obtener Recomendación**: Usa "⭐ Siguiente Tarea"
6. **Marcar Completadas**: Usa "✓ Marcar Completada"

 Ejemplo de Flujo de Trabajo

```
1. Crear: "Investigar requisitos" (Prioridad 5)
2. Crear: "Diseñar arquitectura" (Prioridad 4)
3. Crear: "Implementar módulo" (Prioridad 3)
4. Agregar dependencia: "Investigar requisitos" → "Diseñar arquitectura"
5. Agregar dependencia: "Diseñar arquitectura" → "Implementar módulo"
6. Ver orden: ["Investigar requisitos", "Diseñar arquitectura", "Implementar módulo"]
7. Ejecutar: Solo "Investigar requisitos" está disponible
8. Completar: "Investigar requisitos"
9. Nuevo disponible: "Diseñar arquitectura"
```

## 🧪 Pruebas Realizadas

Todas las funcionalidades han sido verificadas:

- ✅ Creación y gestión de tareas
- ✅ Detección de ciclos en dependencias
- ✅ Ordenamiento topológico correcto
- ✅ Identificación de tareas ejecutables
- ✅ Base de datos funcional
- ✅ Interfaz gráfica operativa

## 📁 Estructura del Proyecto

```
gestor-tareas-deps/
├── src/
│   ├── models/           # Modelos de datos (Tarea, Grafo, PlanDiario)
│   ├── database/         # Gestor de base de datos SQLite
│   ├── controllers/      # Lógica principal (GestorProyecto)
│   └── views/            # Interfaz gráfica (Tkinter)
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias (solo Python estándar)
└── README.md           # Esta documentación
```

## 🛠️ Estructuras de Datos Implementadas

1. **Grafo Dirigido Acíclico (DAG)**
   - Representación: Lista de adyacencia
   - Algoritmo: Detección de ciclos (DFS)
   - Ordenamiento: Algoritmo de Kahn

2. **Cola (Queue)**
   - Uso: Plan diario de trabajo
   - Implementación: `collections.deque`

3. **Diccionario Hash**
   - Uso: Metadatos de tareas y búsqueda rápida
   - Complejidad: O(1) promedio

## 🎓 Aspectos Académicos

Este proyecto implementa conceptos de:
- **Programación con Estructuras de Datos**
- **Algoritmos de Grafos**
- **Ordenamiento Topológico**
- **Manejo de Base de Datos**
- **Desarrollo de Interfaces Gráficas**

## 📝 Notas para el profesor

- El prototipo implementa el 30% del proyecto completo
- Todos los componentes básicos funcionan correctamente
- Se verifican las operaciones fundamentales de las estructuras de datos
- El código está organizado siguiendo buenas prácticas de desarrollo

---

**Universidad Técnica Particular de Loja**
**Programación con Estructuras de Datos (PED941)**
**Proyecto Final - Fase 1**