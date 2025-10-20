#!/usr/bin/env python3
"""
Interfaz Web Simple
Alternativa que funciona en cualquier navegador
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.gestor_proyecto import GestorProyecto

class GestorTareasWebHandler(BaseHTTPRequestHandler):
    """Handler HTTP para la interfaz web"""

    def __init__(self, *args, **kwargs):
        # Inicializar el gestor de proyectos (se crea una instancia global)
        if not hasattr(GestorTareasWebHandler, 'gestor'):
            GestorTareasWebHandler.gestor = GestorProyecto('gestor_tareas_web.db')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Maneja solicitudes GET"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            self.send_404()

    def do_POST(self):
        """Maneja solicitudes POST"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_404()

    def serve_html(self):
        """Sirve la página HTML principal"""
        html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Tareas con Dependencias</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .main-content {
            display: grid;
            grid-template-columns: 300px 1fr 300px;
            gap: 20px;
            margin-bottom: 30px;
        }

        .panel {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .panel h2 {
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin: 5px 0;
            width: 100%;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        }

        .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }

        .form-group input,
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }

        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }

        .task-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .task-item {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            transition: transform 0.2s;
        }

        .task-item:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .task-item.completed {
            border-left-color: #28a745;
            opacity: 0.8;
        }

        .task-item h4 {
            margin-bottom: 8px;
            color: #333;
        }

        .task-item .meta {
            font-size: 12px;
            color: #666;
            display: flex;
            gap: 15px;
        }

        .priority-high {
            color: #dc3545;
            font-weight: bold;
        }

        .priority-medium {
            color: #ffc107;
            font-weight: bold;
        }

        .priority-low {
            color: #28a745;
            font-weight: bold;
        }

        .status-badge {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .status-pending {
            background: #fff3cd;
            color: #856404;
        }

        .status-progress {
            background: #cce7ff;
            color: #004085;
        }

        .status-completed {
            background: #d4edda;
            color: #155724;
        }

        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }

        .stat-item {
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }

        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }

        .modal-content {
            background-color: white;
            margin: 10% auto;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }

        .close:hover {
            color: black;
        }

        .alert {
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            display: none;
        }

        .alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .alert-error {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .hidden {
            display: none !important;
        }

        footer {
            text-align: center;
            padding: 20px;
            background: #333;
            color: white;
            border-radius: 10px;
            margin-top: 30px;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 Gestor de Tareas con Dependencias</h1>
            <p>Versión Web - Compatible con cualquier macOS</p>
        </header>

        <div class="main-content">
            <!-- Panel Izquierdo - Acciones -->
            <div class="panel">
                <h2>🎯 Acciones</h2>

                <button class="btn" onclick="showCreateTask()">➕ Nueva Tarea</button>
                <button class="btn btn-secondary" onclick="showAddDependency()">🔗 Agregar Dependencia</button>
                <button class="btn btn-secondary" onclick="viewExecutionOrder()">📊 Orden de Ejecución</button>
                <button class="btn btn-secondary" onclick="viewExecutableTasks()">🎯 Tareas Ejecutables</button>
                <button class="btn btn-secondary" onclick="viewNextTask()">⭐ Siguiente Tarea</button>
                <button class="btn btn-danger" onclick="showCompleteTask()">✅ Marcar Completada</button>
                <button class="btn" onclick="viewDailyPlan()">📅 Plan Diario</button>
                <button class="btn" onclick="refreshData()">🔄 Actualizar</button>
            </div>

            <!-- Panel Central - Tareas -->
            <div class="panel">
                <h2>📋 Todas las Tareas</h2>
                <div id="taskList" class="task-list">
                    <p>Cargando tareas...</p>
                </div>
            </div>

            <!-- Panel Derecho - Estadísticas -->
            <div class="panel">
                <h2>📈 Estadísticas</h2>
                <div id="statistics">
                    <p>Cargando estadísticas...</p>
                </div>
            </div>
        </div>

        <!-- Alertas -->
        <div id="alertSuccess" class="alert alert-success"></div>
        <div id="alertError" class="alert alert-error"></div>

        <!-- Modal para crear tarea -->
        <div id="createTaskModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('createTaskModal')">&times;</span>
                <h2>➕ Crear Nueva Tarea</h2>
                <form id="createTaskForm">
                    <div class="form-group">
                        <label for="taskName">Nombre: *</label>
                        <input type="text" id="taskName" required>
                    </div>
                    <div class="form-group">
                        <label for="taskDescription">Descripción:</label>
                        <textarea id="taskDescription" rows="3"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="taskPriority">Prioridad (1-5):</label>
                        <select id="taskPriority">
                            <option value="1">1 - Baja</option>
                            <option value="2">2 - Baja</option>
                            <option value="3" selected>3 - Media</option>
                            <option value="4">4 - Alta</option>
                            <option value="5">5 - Muy Alta</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">Crear Tarea</button>
                </form>
            </div>
        </div>

        <!-- Modal para agregar dependencia -->
        <div id="addDependencyModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('addDependencyModal')">&times;</span>
                <h2>🔗 Agregar Dependencia</h2>
                <form id="addDependencyForm">
                    <div class="form-group">
                        <label for="taskPrerequisite">Tarea Prerequisito: *</label>
                        <select id="taskPrerequisite" required>
                            <option value="">Seleccione...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="taskDependent">Tarea Dependiente: *</label>
                        <select id="taskDependent" required>
                            <option value="">Seleccione...</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">Agregar Dependencia</button>
                </form>
            </div>
        </div>

        <!-- Modal para marcar completada -->
        <div id="completeTaskModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('completeTaskModal')">&times;</span>
                <h2>✅ Marcar Tarea como Completada</h2>
                <form id="completeTaskForm">
                    <div class="form-group">
                        <label for="taskToComplete">Tarea: *</label>
                        <select id="taskToComplete" required>
                            <option value="">Seleccione...</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">Marcar como Completada</button>
                </form>
            </div>
        </div>

        <footer>
            <p>© Gestor de T con Dependencias - Universidad Técnica Particular de Loja</p>
        </footer>
    </div>

    <script>
        // Variables globales
        let tasks = [];

        // Funciones generales
        function showAlert(message, type = 'success') {
            const alertElement = document.getElementById('alert' + (type === 'success' ? 'Success' : 'Error'));
            alertElement.textContent = message;
            alertElement.style.display = 'block';

            setTimeout(() => {
                alertElement.style.display = 'none';
            }, 3000);
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        function showModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
        }

        // API Calls
        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const options = {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    }
                };

                if (data && method !== 'GET') {
                    options.body = JSON.stringify(data);
                }

                const response = await fetch('/api/' + endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                showAlert('Error de conexión con el servidor', 'error');
                return null;
            }
        }

        // Funciones de la aplicación
        function refreshData() {
            loadTasks();
            loadStatistics();
        }

        async function loadTasks() {
            const response = await apiCall('tasks');
            if (response && response.success) {
                tasks = response.data;
                displayTasks(response.data);
            }
        }

        function displayTasks(tasksData) {
            const taskList = document.getElementById('taskList');

            if (tasksData.length === 0) {
                taskList.innerHTML = '<p>No hay tareas registradas.</p>';
                return;
            }

            tasksData.sort((a, b) => b.prioridad - a.prioridad);

            let html = '';
            tasksData.forEach(task => {
                const priorityClass = task.prioridad >= 4 ? 'priority-high' : 'priority-low';
                const statusClass = 'status-' + task.estado.replace('_', '');
                const completedClass = task.estado === 'completada' ? 'completed' : '';

                const fechaLimite = task.fecha_limite ?
                    new Date(task.fecha_limite).toLocaleDateString('es-ES') : '';

                html += `
                    <div class="task-item ${completedClass}">
                        <h4>${task.nombre}</h4>
                        ${task.descripcion ? `<p>${task.descripcion}</p>` : ''}
                        <div class="meta">
                            <span class="${statusClass} status-badge">${task.estado.replace('_', '')}</span>
                            <span class="${priorityClass}">⭐ ${task.prioridad}</span>
                            ${fechaLimite ? `<span>📅 ${fechaLimite}</span>` : ''}
                        </div>
                    </div>
                `;
            });

            taskList.innerHTML = html;
        }

        async function loadStatistics() {
            const response = await apiCall('statistics');
            if (response && response.success) {
                displayStatistics(response.data);
            }
        }

        function displayStatistics(stats) {
            const statsElement = document.getElementById('statistics');

            const html = `
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">${stats.total_tareas}</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.completadas}</div>
                        <div class="stat-label">Completadas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.pendientes}</div>
                        <div class="stat-label">Pendientes</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.ejecutables}</div>
                        <div class="stat-label">Ejecutables</div>
                    </div>
                </div>
                <div style="margin-top: 15px; text-align: center;">
                    <div>P</div>
                    <div style="font-size: 18px; color: #667eea; font-weight: bold;">${stats.porcentaje_completado.toFixed(1)}%</div>
                </div>
            `;

            statsElement.innerHTML = html;
        }

        function showCreateTask() {
            showModal('createTaskModal');
        }

        document.getElementById('createTaskForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const data = {
                nombre: document.getElementById('taskName').value,
                descripcion: document.getElementById('taskDescription').value,
                prioridad: parseInt(document.getElementById('taskPriority').value)
            };

            const response = await apiCall('tasks', 'POST', data);
            if (response && response.success) {
                showAlert('Tarea creada exitosamente');
                closeModal('createTaskModal');
                document.getElementById('createTaskForm').reset();
                refreshData();
            } else {
                showAlert(response.error || 'Error al crear tarea', 'error');
            }
        });

        function showAddDependency() {
            if (tasks.length < 2) {
                showAlert('Se necesitan al menos 2 tareas para crear dependencias', 'error');
                return;
            }

            const prerequisiteSelect = document.getElementById('taskPrerequisite');
            const dependentSelect = document.getElementById('taskDependent');

            let options = '';
            tasks.forEach(task => {
                options += `<option value="${task.id}">${task.nombre}</option>`;
            });

            prerequisiteSelect.innerHTML = '<option value="">Seleccione...</option>' + options;
            dependentSelect.innerHTML = '<option value="">Seleccione...</option>' + options;

            showModal('addDependencyModal');
        }

        document.getElementById('addDependencyForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const origen = parseInt(document.getElementById('taskPrerequisite').value);
            const destino = parseInt(document.getElementById('taskDependent').value);

            if (origen === destino) {
                showAlert('Una tarea no puede depender de sí misma', 'error');
                return;
            }

            const response = await apiCall('dependencies', 'POST', { origen, destino });
            if (response && response.success) {
                showAlert('Dependencia agregada exitosamente');
                closeModal('addDependencyModal');
                refreshData();
            } else {
                showAlert(response.error || 'Error al agregar dependencia', 'error');
            }
        });

        function showCompleteTask() {
            const pendientes = tasks.filter(task => task.estado !== 'completada');

            if (pendientes.length === 0) {
                showAlert('No hay tareas pendientes por completar', 'error');
                return;
            }

            const selectElement = document.getElementById('taskToComplete');
            let options = '';

            pendientes.forEach(task => {
                options += `<option value="${task.id}">${task.nombre}</option>`;
            });

            selectElement.innerHTML = '<option value="">Seleccione...</option>' + options;
            showModal('completeTaskModal');
        }

        document.getElementById('completeTaskForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const taskId = parseInt(document.getElementById('taskToComplete').value);
            const response = await apiCall(`tasks/${taskId}/complete`, 'POST');

            if (response && response.success) {
                showAlert(response.message);
                closeModal('completeTaskModal');
                refreshData();
            } else {
                showAlert(response.error || 'Error al completar tarea', 'error');
            }
        });

        async function viewExecutionOrder() {
            const response = await apiCall('execution-order');

            if (response && response.success) {
                if (response.data && response.data.length > 0) {
                    let orderText = 'ORDEN DE EJECUCIÓN VÁLIDO:\n\n';
                    response.data.forEach((task, index) => {
                        const priorityIcon = task.prioridad >= 4 ? '🔥' : task.prioridad >= 3 ? '⭐' : '📋';
                        orderText += `${index + 1}. ${priorityIcon} ${task.nombre} (Prioridad: ${task.prioridad})\n`;
                    });
                    alert(orderText);
                } else {
                    alert('No hay tareas pendientes o hay ciclos en las dependencias.');
                }
            }
        }

        async function viewExecutableTasks() {
            const response = await apiCall('executable-tasks');

            if (response && response.success) {
                if (response.data && response.data.length > 0) {
                    let text = `TAREAS EJECUTABLES AHORA (${response.data.length}):\n\n`;
                    response.data.forEach((task, index) => {
                        const priorityIcon = task.prioridad >= 4 ? '🔥' : task.prioridad >= 3 ? '⭐' : '📋';
                        text += `${index + 1}. ${priorityIcon} ${task.nombre} (Prioridad: ${task.prioridad})\n`;
                    });
                    alert(text);
                } else {
                    alert('No hay tareas ejecutables en este momento.\n\nRevisa las dependencias pendientes.');
                }
            }
        }

        async function viewNextTask() {
            const response = await apiCall('next-task');

            if (response && response.success) {
                if (response.data) {
                    const task = response.data;
                    const fechaLimite = task.fecha_limite ?
                        `\nLímite: ${new Date(task.fecha_limite).toLocaleDateString('es-ES')}` : '';
                    alert(`SIGUIENTE TAREA RECOMENDADA:\n\n🎯 ${task.nombre}${fechaLimite}\n⭐ Prioridad: ${task.prioridad}/5`);
                } else {
                    alert('No hay tareas disponibles para ejecutar.\n\nRevisa el estado de tus dependencias.');
                }
            }
        }

        async function viewDailyPlan() {
            const response = await apiCall('daily-plan');

            if (response && response.success) {
                if (response.data && response.data.length > 0) {
                    let text = `PLAN DIARIO (${response.data.length} tareas):\n\n`;
                    response.data.forEach((task, index) => {
                        text += `${index + 1}. ${task.nombre}\n`;
                    });
                    alert(text);
                } else {
                    alert('No hay tareas en el plan diario.\n\n puedes agregar tareas ejecutables al plan diario.');
                }
            }
        }

        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {
            refreshData();

            // Auto-refresh cada 30 segundos
            setInterval(refreshData, 30000);
        });

        // Cerrarmodales al hacer clic fuera
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }
    </script>
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def handle_api_get(self):
        """Maneja API GET requests"""
        path_parts = self.path.split('/api/')[1].split('/')
        endpoint = path_parts[0]

        response = {'success': False}

        try:
            if endpoint == 'tasks':
                tasks = self.gestor.obtener_todas_tareas()
                response = {
                    'success': True,
                    'data': [task.to_dict() for task in tasks]
                }
            elif endpoint == 'statistics':
                stats = self.gestor.obtener_estadisticas()
                response = {'success': True, 'data': stats}
            elif endpoint == 'execution-order':
                orden = self.gestor.calcular_orden_ejecucion()
                response = {
                    'success': True,
                    'data': [task.to_dict() for task in orden] if orden else []
                }
            elif endpoint == 'executable-tasks':
                ejecutables = self.gestor.obtener_tareas_ejecutables()
                response = {
                    'success': True,
                    'data': [task.to_dict() for task in ejecutables]
                }
            elif endpoint == 'next-task':
                siguiente = self.gestor.obtener_siguiente_tarea()
                response = {
                    'success': True,
                    'data': siguiente.to_dict() if siguiente else None
                }
            elif endpoint == 'daily-plan':
                plan = self.gestor.obtener_plan_diario()
                response = {
                    'success': True,
                    'data': [task.to_dict() for task in plan]
                }
        except Exception as e:
            response = {'success': False, 'error': str(e)}

        self.send_json(response)

    def handle_api_post(self):
        """Maneja API POST requests"""
        path_parts = self.path.split('/api/')[1].split('/')
        endpoint = path_parts[0]

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}

        response = {'success': False}

        try:
            if endpoint == 'tasks':
                exito, mensaje, tarea_id = self.gestor.crear_tarea(
                    data.get('nombre', ''),
                    data.get('descripcion', ''),
                    data.get('prioridad', 3)
                )
                response = {
                    'success': exito,
                    'message': mensaje,
                    'data': {'tarea_id': tarea_id} if exito else None,
                    'error': mensaje if not exito else None
                }
            elif endpoint == 'dependencies':
                origen = data.get('origen')
                destino = data.get('destino')
                exito, mensaje = self.gestor.agregar_dependencia(origen, destino)
                response = {
                    'success': exito,
                    'message': mensaje,
                    'error': mensaje if not exito else None
                }
            elif endpoint.startswith('tasks/') and 'complete' in path_parts:
                task_id = int(path_parts[1])
                exito, mensaje, tareas_desbloqueadas = self.gestor.marcar_completada(task_id)
                response = {
                    'success': exito,
                    'message': mensaje,
                    'error': mensaje if not exito else None,
                    'data': {'tareas_desbloqueadas': tareas_desbloqueadas}
                }
        except Exception as e:
            response = {'success': False, 'error': str(e)}

        self.send_json(response)

    def send_json(self, data):
        """Envía una respuesta JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        self.wfile.write(json_str.encode('utf-8'))

    def send_404(self):
        """Envía un error 404"""
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Page not found')

    def log_message(self, format, *args):
        """Override para reducir logs"""
        pass


def main():
    """Inicia el servidor web"""
    port = 8080
    server_address = ('', port)

    print("🌐 Iniciando Gestor de Tareas Web...")
    print(f"📍 El servidor está corriendo en: http://localhost:{port}")
    print("📱 Abre tu navegador web y accede a la URL arriba")
    print("⏹️  Presiona Ctrl+C para detener el servidor")

    try:
        httpd = HTTPServer(server_address, GestorTareasWebHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        # Cerrar la conexión del gestor
        if hasattr(GestorTareasWebHandler, 'gestor'):
            GestorTareasWebHandler.gestor.cerrar()

if __name__ == "__main__":
    main()