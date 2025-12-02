#!/usr/bin/env python3
"""
Interfaz Web Moderna - Gestor de Tareas con Dependencias
Sistema completo con UI profesional para Fase 2
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
import sqlite3
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.gestor_proyecto import GestorProyecto

_gestor_instance = None

def get_gestor():
    """Get or create the global gestor instance"""
    global _gestor_instance
    if _gestor_instance is None:
        _gestor_instance = GestorProyecto('gestor_tareas_web.db')
    return _gestor_instance


class ModernWebHandler(BaseHTTPRequestHandler):
    """Handler HTTP para la interfaz web moderna"""

    def __init__(self, *args, **kwargs):
        if not hasattr(ModernWebHandler, '_gestor_initialized'):
            ModernWebHandler._gestor_initialized = True
            get_gestor()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Maneja solicitudes GET"""
        try:
            if self.path == '/' or self.path == '/index.html':
                self.serve_html()
            elif self.path.startswith('/api/'):
                self.handle_api_get()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_POST(self):
        """Maneja solicitudes POST"""
        try:
            if self.path.startswith('/api/'):
                self.handle_api_post()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_DELETE(self):
        """Maneja solicitudes DELETE"""
        try:
            if self.path.startswith('/api/'):
                self.handle_api_delete()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_PUT(self):
        """Maneja solicitudes PUT"""
        try:
            if self.path.startswith('/api/'):
                self.handle_api_put()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_html(self):
        """Sirve la pagina HTML principal con UI moderna"""
        html_content = self.get_modern_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def get_modern_html(self):
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestor de Tareas con Dependencias - UDB</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #818cf8;
            --secondary: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1e293b;
            --dark-light: #334155;
            --gray: #64748b;
            --gray-light: #94a3b8;
            --light: #f1f5f9;
            --white: #ffffff;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius: 12px;
            --radius-lg: 16px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: var(--dark);
        }

        .app-container {
            min-height: 100vh;
            background: var(--light);
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%);
            color: white;
            padding: 1.5rem 2rem;
            box-shadow: var(--shadow-lg);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 48px;
            height: 48px;
            background: rgba(255,255,255,0.2);
            border-radius: var(--radius);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }

        .logo h1 {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .logo span {
            font-size: 0.85rem;
            opacity: 0.85;
            font-weight: 400;
        }

        .header-actions {
            display: flex;
            gap: 12px;
        }

        /* Main Layout */
        .main-layout {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 280px 1fr 320px;
            gap: 1.5rem;
        }

        @media (max-width: 1200px) {
            .main-layout {
                grid-template-columns: 1fr;
            }
        }

        /* Cards */
        .card {
            background: var(--white);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            box-shadow: var(--shadow-lg);
        }

        .card-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--light);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .card-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .card-body {
            padding: 1.5rem;
        }

        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 0.75rem 1.25rem;
            font-size: 0.9rem;
            font-weight: 500;
            border: none;
            border-radius: var(--radius);
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            white-space: nowrap;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, var(--secondary) 0%, #059669 100%);
            color: white;
        }

        .btn-secondary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }

        .btn-warning {
            background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
            color: white;
        }

        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        }

        .btn-outline {
            background: transparent;
            border: 2px solid var(--gray-light);
            color: var(--gray);
        }

        .btn-outline:hover {
            border-color: var(--primary);
            color: var(--primary);
            background: rgba(99, 102, 241, 0.05);
        }

        .btn-block {
            width: 100%;
        }

        .btn-sm {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }

        .btn-icon {
            width: 36px;
            height: 36px;
            padding: 0;
            border-radius: 8px;
        }

        /* Action Menu */
        .action-menu {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .action-btn {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 1rem;
            background: var(--light);
            border: none;
            border-radius: var(--radius);
            cursor: pointer;
            transition: all 0.2s;
            text-align: left;
            font-size: 0.95rem;
            color: var(--dark);
        }

        .action-btn:hover {
            background: var(--primary);
            color: white;
            transform: translateX(4px);
        }

        .action-btn .icon {
            width: 36px;
            height: 36px;
            background: var(--white);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            transition: all 0.2s;
        }

        .action-btn:hover .icon {
            background: rgba(255,255,255,0.2);
        }

        /* Task List */
        .task-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 600px;
            overflow-y: auto;
        }

        .task-list::-webkit-scrollbar {
            width: 6px;
        }

        .task-list::-webkit-scrollbar-track {
            background: var(--light);
            border-radius: 3px;
        }

        .task-list::-webkit-scrollbar-thumb {
            background: var(--gray-light);
            border-radius: 3px;
        }

        .task-item {
            background: var(--white);
            border: 1px solid var(--light);
            border-radius: var(--radius);
            padding: 1rem 1.25rem;
            transition: all 0.2s;
            cursor: pointer;
            position: relative;
        }

        .task-item:hover {
            border-color: var(--primary-light);
            box-shadow: var(--shadow);
            transform: translateY(-2px);
        }

        .task-item.selected {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .task-item.completed {
            opacity: 0.7;
            background: var(--light);
        }

        .task-item.completed .task-name {
            text-decoration: line-through;
            color: var(--gray);
        }

        .task-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 8px;
        }

        .task-name {
            font-weight: 600;
            color: var(--dark);
            font-size: 1rem;
        }

        .task-description {
            font-size: 0.85rem;
            color: var(--gray);
            margin-bottom: 12px;
            line-height: 1.5;
        }

        .task-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }

        .task-actions {
            display: flex;
            gap: 4px;
            opacity: 0;
            transition: opacity 0.2s;
        }

        .task-item:hover .task-actions {
            opacity: 1;
        }

        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
        }

        .badge-priority-5, .badge-priority-4 {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
        }

        .badge-priority-3 {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
        }

        .badge-priority-2, .badge-priority-1 {
            background: rgba(16, 185, 129, 0.1);
            color: var(--secondary);
        }

        .badge-status-pendiente {
            background: rgba(100, 116, 139, 0.1);
            color: var(--gray);
        }

        .badge-status-en_progreso {
            background: rgba(99, 102, 241, 0.1);
            color: var(--primary);
        }

        .badge-status-completada {
            background: rgba(16, 185, 129, 0.1);
            color: var(--secondary);
        }

        /* Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }

        .stat-card {
            background: linear-gradient(135deg, var(--light) 0%, var(--white) 100%);
            padding: 1rem;
            border-radius: var(--radius);
            text-align: center;
            border: 1px solid var(--light);
        }

        .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1;
            margin-bottom: 4px;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Progress */
        .progress-container {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--light);
        }

        .progress-bar {
            width: 100%;
            height: 12px;
            background: var(--light);
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 6px;
            transition: width 0.5s ease;
        }

        .progress-text {
            text-align: center;
            font-weight: 600;
            color: var(--primary);
        }

        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal {
            background: var(--white);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            width: 100%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            animation: modalSlideIn 0.3s ease;
        }

        @keyframes modalSlideIn {
            from {
                opacity: 0;
                transform: translateY(-20px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .modal-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--light);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .modal-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--dark);
        }

        .modal-close {
            width: 36px;
            height: 36px;
            border: none;
            background: var(--light);
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.25rem;
            color: var(--gray);
            transition: all 0.2s;
        }

        .modal-close:hover {
            background: var(--danger);
            color: white;
        }

        .modal-body {
            padding: 1.5rem;
        }

        .modal-footer {
            padding: 1rem 1.5rem;
            border-top: 1px solid var(--light);
            display: flex;
            justify-content: flex-end;
            gap: 12px;
        }

        /* Forms */
        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-label {
            display: block;
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--dark);
            margin-bottom: 6px;
        }

        .form-input, .form-select, .form-textarea {
            width: 100%;
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            border: 2px solid var(--light);
            border-radius: var(--radius);
            transition: all 0.2s;
            font-family: inherit;
        }

        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .form-textarea {
            resize: vertical;
            min-height: 100px;
        }

        /* Alerts */
        .alert-container {
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .alert {
            padding: 1rem 1.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow-lg);
            display: flex;
            align-items: center;
            gap: 12px;
            animation: alertSlideIn 0.3s ease;
            min-width: 300px;
        }

        @keyframes alertSlideIn {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .alert-success {
            background: var(--secondary);
            color: white;
        }

        .alert-error {
            background: var(--danger);
            color: white;
        }

        .alert-info {
            background: var(--primary);
            color: white;
        }

        /* Dependency Graph */
        .dependency-item {
            display: flex;
            align-items: center;
            padding: 0.75rem;
            background: var(--light);
            border-radius: var(--radius);
            margin-bottom: 8px;
            gap: 12px;
        }

        .dependency-arrow {
            color: var(--primary);
            font-size: 1.25rem;
        }

        .dependency-task {
            flex: 1;
            font-size: 0.9rem;
        }

        /* Filter Tabs */
        .filter-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .filter-tab {
            padding: 0.5rem 1rem;
            border: none;
            background: var(--light);
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--gray);
        }

        .filter-tab:hover {
            background: var(--primary-light);
            color: white;
        }

        .filter-tab.active {
            background: var(--primary);
            color: white;
        }

        /* Search */
        .search-box {
            position: relative;
            margin-bottom: 1rem;
        }

        .search-input {
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.75rem;
            border: 2px solid var(--light);
            border-radius: var(--radius);
            font-size: 0.95rem;
            transition: all 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray-light);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--gray);
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .empty-state-text {
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Tooltip */
        .tooltip {
            position: relative;
        }

        .tooltip::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            padding: 6px 12px;
            background: var(--dark);
            color: white;
            font-size: 0.75rem;
            border-radius: 6px;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s;
        }

        .tooltip:hover::after {
            opacity: 1;
        }

        /* Loading */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--light);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Info Panel */
        .info-panel {
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
            color: white;
            padding: 1.5rem;
            border-radius: var(--radius);
            margin-bottom: 1rem;
        }

        .info-panel h3 {
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }

        .info-panel p {
            font-size: 0.85rem;
            opacity: 0.9;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem;
            background: var(--dark);
            color: white;
            margin-top: 2rem;
        }

        .footer p {
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">📋</div>
                    <div>
                        <h1>Gestor de Tareas</h1>
                        <span>Sistema de Dependencias con Grafos</span>
                    </div>
                </div>
                <div class="header-actions">
                    <button class="btn btn-primary" onclick="openModal('createTaskModal')">
                        <span>+</span> Nueva Tarea
                    </button>
                </div>
            </div>
        </header>

        <main class="main-layout">
            <!-- Sidebar - Acciones -->
            <aside>
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>🎯</span> Acciones
                        </h2>
                    </div>
                    <div class="card-body">
                        <div class="action-menu">
                            <button class="action-btn" onclick="openModal('createTaskModal')">
                                <span class="icon">➕</span>
                                <span>Crear Tarea</span>
                            </button>
                            <button class="action-btn" onclick="openModal('dependencyModal')">
                                <span class="icon">🔗</span>
                                <span>Agregar Dependencia</span>
                            </button>
                            <button class="action-btn" onclick="viewExecutionOrder()">
                                <span class="icon">📊</span>
                                <span>Orden de Ejecucion</span>
                            </button>
                            <button class="action-btn" onclick="viewExecutableTasks()">
                                <span class="icon">🎯</span>
                                <span>Tareas Ejecutables</span>
                            </button>
                            <button class="action-btn" onclick="viewNextTask()">
                                <span class="icon">⭐</span>
                                <span>Siguiente Tarea</span>
                            </button>
                            <button class="action-btn" onclick="openModal('viewDependenciesModal')">
                                <span class="icon">🕸️</span>
                                <span>Ver Dependencias</span>
                            </button>
                            <button class="action-btn" onclick="refreshData()">
                                <span class="icon">🔄</span>
                                <span>Actualizar</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="info-panel" style="margin-top: 1rem;">
                    <h3>💡 Estructuras de Datos</h3>
                    <p>Este sistema utiliza <strong>Grafos Dirigidos Aciclicos (DAG)</strong> para dependencias y <strong>Colas (Queue)</strong> para el plan diario.</p>
                </div>
            </aside>

            <!-- Main Content - Lista de Tareas -->
            <section>
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>📋</span> Mis Tareas
                        </h2>
                        <span id="taskCount" class="badge badge-status-pendiente">0 tareas</span>
                    </div>
                    <div class="card-body">
                        <div class="search-box">
                            <span class="search-icon">🔍</span>
                            <input type="text" class="search-input" id="searchInput" placeholder="Buscar tareas..." oninput="filterTasks()">
                        </div>
                        
                        <div class="filter-tabs">
                            <button class="filter-tab active" data-filter="all" onclick="setFilter('all')">Todas</button>
                            <button class="filter-tab" data-filter="pendiente" onclick="setFilter('pendiente')">Pendientes</button>
                            <button class="filter-tab" data-filter="en_progreso" onclick="setFilter('en_progreso')">En Progreso</button>
                            <button class="filter-tab" data-filter="completada" onclick="setFilter('completada')">Completadas</button>
                        </div>

                        <div id="taskList" class="task-list">
                            <div class="loading"><div class="spinner"></div></div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Sidebar - Estadisticas -->
            <aside>
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>📈</span> Estadisticas
                        </h2>
                    </div>
                    <div class="card-body">
                        <div id="statsContainer">
                            <div class="loading"><div class="spinner"></div></div>
                        </div>
                    </div>
                </div>

                <div class="card" style="margin-top: 1rem;">
                    <div class="card-header">
                        <h2 class="card-title">
                            <span>📅</span> Plan Diario
                        </h2>
                    </div>
                    <div class="card-body">
                        <div id="dailyPlan">
                            <p style="color: var(--gray); font-size: 0.9rem;">Agrega tareas ejecutables al plan diario.</p>
                        </div>
                    </div>
                </div>
            </aside>
        </main>

        <footer class="footer">
            <p>Universidad Don Bosco - Programacion con Estructuras de Datos</p>
            <p>Sistema de Gestion de Tareas con Dependencias - Fase 2</p>
        </footer>
    </div>

    <!-- Alert Container -->
    <div id="alertContainer" class="alert-container"></div>

    <!-- Modal: Crear Tarea -->
    <div id="createTaskModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">➕ Crear Nueva Tarea</h3>
                <button class="modal-close" onclick="closeModal('createTaskModal')">&times;</button>
            </div>
            <form id="createTaskForm" onsubmit="createTask(event)">
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Nombre de la tarea *</label>
                        <input type="text" class="form-input" id="taskName" required placeholder="Ej: Disenar base de datos">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Descripcion</label>
                        <textarea class="form-textarea" id="taskDescription" placeholder="Describe la tarea..."></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Prioridad</label>
                        <select class="form-select" id="taskPriority">
                            <option value="1">1 - Muy Baja</option>
                            <option value="2">2 - Baja</option>
                            <option value="3" selected>3 - Media</option>
                            <option value="4">4 - Alta</option>
                            <option value="5">5 - Muy Alta</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Fecha limite (opcional)</label>
                        <input type="date" class="form-input" id="taskDeadline">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline" onclick="closeModal('createTaskModal')">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Crear Tarea</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal: Editar Tarea -->
    <div id="editTaskModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">✏️ Editar Tarea</h3>
                <button class="modal-close" onclick="closeModal('editTaskModal')">&times;</button>
            </div>
            <form id="editTaskForm" onsubmit="updateTask(event)">
                <div class="modal-body">
                    <input type="hidden" id="editTaskId">
                    <div class="form-group">
                        <label class="form-label">Nombre de la tarea *</label>
                        <input type="text" class="form-input" id="editTaskName" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Descripcion</label>
                        <textarea class="form-textarea" id="editTaskDescription"></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Estado</label>
                        <select class="form-select" id="editTaskStatus">
                            <option value="pendiente">Pendiente</option>
                            <option value="en_progreso">En Progreso</option>
                            <option value="completada">Completada</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Prioridad</label>
                        <select class="form-select" id="editTaskPriority">
                            <option value="1">1 - Muy Baja</option>
                            <option value="2">2 - Baja</option>
                            <option value="3">3 - Media</option>
                            <option value="4">4 - Alta</option>
                            <option value="5">5 - Muy Alta</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline" onclick="closeModal('editTaskModal')">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Guardar Cambios</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal: Agregar Dependencia -->
    <div id="dependencyModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">🔗 Agregar Dependencia</h3>
                <button class="modal-close" onclick="closeModal('dependencyModal')">&times;</button>
            </div>
            <form id="dependencyForm" onsubmit="addDependency(event)">
                <div class="modal-body">
                    <p style="color: var(--gray); margin-bottom: 1rem; font-size: 0.9rem;">
                        Define que una tarea debe completarse antes de otra. El sistema detectara automaticamente ciclos invalidos.
                    </p>
                    <div class="form-group">
                        <label class="form-label">Tarea Prerequisito (debe completarse primero)</label>
                        <select class="form-select" id="depPrerequisite" required>
                            <option value="">Selecciona una tarea...</option>
                        </select>
                    </div>
                    <div style="text-align: center; color: var(--primary); font-size: 1.5rem; margin: 0.5rem 0;">
                        ⬇️
                    </div>
                    <div class="form-group">
                        <label class="form-label">Tarea Dependiente (se desbloquea despues)</label>
                        <select class="form-select" id="depDependent" required>
                            <option value="">Selecciona una tarea...</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline" onclick="closeModal('dependencyModal')">Cancelar</button>
                    <button type="submit" class="btn btn-secondary">Agregar Dependencia</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal: Ver Dependencias -->
    <div id="viewDependenciesModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">🕸️ Grafo de Dependencias</h3>
                <button class="modal-close" onclick="closeModal('viewDependenciesModal')">&times;</button>
            </div>
            <div class="modal-body">
                <div id="dependenciesList">
                    <div class="loading"><div class="spinner"></div></div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline" onclick="closeModal('viewDependenciesModal')">Cerrar</button>
            </div>
        </div>
    </div>

    <!-- Modal: Resultado de Orden -->
    <div id="resultModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title" id="resultModalTitle">Resultado</h3>
                <button class="modal-close" onclick="closeModal('resultModal')">&times;</button>
            </div>
            <div class="modal-body">
                <div id="resultModalContent"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" onclick="closeModal('resultModal')">Entendido</button>
            </div>
        </div>
    </div>

    <!-- Modal: Confirmar Eliminacion -->
    <div id="deleteConfirmModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">⚠️ Confirmar Eliminacion</h3>
                <button class="modal-close" onclick="closeModal('deleteConfirmModal')">&times;</button>
            </div>
            <div class="modal-body">
                <p>¿Estas seguro de que deseas eliminar esta tarea? Esta accion no se puede deshacer.</p>
                <p id="deleteTaskName" style="font-weight: 600; margin-top: 1rem; color: var(--danger);"></p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline" onclick="closeModal('deleteConfirmModal')">Cancelar</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteBtn">Eliminar</button>
            </div>
        </div>
    </div>

    <script>
        // Estado global de la aplicacion
        let tasks = [];
        let currentFilter = 'all';
        let taskToDelete = null;

        // Funciones de utilidad
        function showAlert(message, type = 'success') {
            const container = document.getElementById('alertContainer');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.innerHTML = `<span>${type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ'}</span> ${message}`;
            container.appendChild(alert);
            
            setTimeout(() => {
                alert.style.animation = 'alertSlideIn 0.3s ease reverse';
                setTimeout(() => alert.remove(), 300);
            }, 4000);
        }

        function openModal(modalId) {
            document.getElementById(modalId).classList.add('active');
            
            if (modalId === 'dependencyModal') {
                populateDependencySelects();
            } else if (modalId === 'viewDependenciesModal') {
                loadDependencies();
            }
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        // API calls
        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const options = {
                    method: method,
                    headers: { 'Content-Type': 'application/json' }
                };
                if (data && method !== 'GET') {
                    options.body = JSON.stringify(data);
                }
                const response = await fetch('/api/' + endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                showAlert('Error de conexion con el servidor', 'error');
                return null;
            }
        }

        // Cargar datos
        async function loadTasks() {
            const response = await apiCall('tasks');
            if (response && response.success) {
                tasks = response.data;
                renderTasks();
                updateTaskCount();
            }
        }

        async function loadStatistics() {
            const response = await apiCall('statistics');
            if (response && response.success) {
                renderStatistics(response.data);
            }
        }

        async function loadDailyPlan() {
            const response = await apiCall('daily-plan');
            if (response && response.success) {
                renderDailyPlan(response.data);
            }
        }

        function refreshData() {
            loadTasks();
            loadStatistics();
            loadDailyPlan();
            showAlert('Datos actualizados', 'info');
        }

        // Renderizado
        function renderTasks() {
            const container = document.getElementById('taskList');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            let filteredTasks = tasks.filter(task => {
                const matchesFilter = currentFilter === 'all' || task.estado === currentFilter;
                const matchesSearch = task.nombre.toLowerCase().includes(searchTerm) || 
                                     (task.descripcion && task.descripcion.toLowerCase().includes(searchTerm));
                return matchesFilter && matchesSearch;
            });

            filteredTasks.sort((a, b) => b.prioridad - a.prioridad);

            if (filteredTasks.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <p class="empty-state-text">No hay tareas ${currentFilter !== 'all' ? 'con este filtro' : 'registradas'}</p>
                        <button class="btn btn-primary" onclick="openModal('createTaskModal')">Crear Primera Tarea</button>
                    </div>
                `;
                return;
            }

            container.innerHTML = filteredTasks.map(task => `
                <div class="task-item ${task.estado === 'completada' ? 'completed' : ''}" onclick="selectTask(${task.id})">
                    <div class="task-header">
                        <span class="task-name">${escapeHtml(task.nombre)}</span>
                        <div class="task-actions">
                            ${task.estado !== 'completada' ? `
                                <button class="btn btn-icon btn-secondary tooltip" data-tooltip="Completar" onclick="event.stopPropagation(); completeTask(${task.id})">✓</button>
                            ` : ''}
                            <button class="btn btn-icon btn-outline tooltip" data-tooltip="Editar" onclick="event.stopPropagation(); openEditModal(${task.id})">✏️</button>
                            <button class="btn btn-icon btn-danger tooltip" data-tooltip="Eliminar" onclick="event.stopPropagation(); confirmDelete(${task.id})">🗑️</button>
                        </div>
                    </div>
                    ${task.descripcion ? `<p class="task-description">${escapeHtml(task.descripcion)}</p>` : ''}
                    <div class="task-meta">
                        <span class="badge badge-status-${task.estado}">${formatStatus(task.estado)}</span>
                        <span class="badge badge-priority-${task.prioridad}">⭐ ${task.prioridad}</span>
                        ${task.fecha_limite ? `<span class="badge badge-status-pendiente">📅 ${formatDate(task.fecha_limite)}</span>` : ''}
                    </div>
                </div>
            `).join('');
        }

        function renderStatistics(stats) {
            const container = document.getElementById('statsContainer');
            container.innerHTML = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_tareas}</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.completadas}</div>
                        <div class="stat-label">Completadas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.pendientes}</div>
                        <div class="stat-label">Pendientes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.ejecutables}</div>
                        <div class="stat-label">Ejecutables</div>
                    </div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${stats.porcentaje_completado}%"></div>
                    </div>
                    <div class="progress-text">${stats.porcentaje_completado.toFixed(1)}% Completado</div>
                </div>
            `;
        }

        function renderDailyPlan(planTasks) {
            const container = document.getElementById('dailyPlan');
            if (!planTasks || planTasks.length === 0) {
                container.innerHTML = '<p style="color: var(--gray); font-size: 0.9rem;">No hay tareas en el plan diario.</p>';
                return;
            }
            container.innerHTML = planTasks.map((task, index) => `
                <div class="dependency-item">
                    <span>${index + 1}.</span>
                    <span class="dependency-task">${escapeHtml(task.nombre)}</span>
                </div>
            `).join('');
        }

        // Acciones de tareas
        async function createTask(event) {
            event.preventDefault();
            const data = {
                nombre: document.getElementById('taskName').value,
                descripcion: document.getElementById('taskDescription').value,
                prioridad: parseInt(document.getElementById('taskPriority').value),
                fecha_limite: document.getElementById('taskDeadline').value || null
            };
            
            const response = await apiCall('tasks', 'POST', data);
            if (response && response.success) {
                showAlert('Tarea creada exitosamente');
                closeModal('createTaskModal');
                document.getElementById('createTaskForm').reset();
                refreshData();
            } else {
                showAlert(response?.error || 'Error al crear tarea', 'error');
            }
        }

        async function completeTask(taskId) {
            const response = await apiCall(`tasks/${taskId}/complete`, 'POST');
            if (response && response.success) {
                showAlert(response.message);
                refreshData();
            } else {
                showAlert(response?.error || 'Error al completar tarea', 'error');
            }
        }

        function openEditModal(taskId) {
            const task = tasks.find(t => t.id === taskId);
            if (!task) return;
            
            document.getElementById('editTaskId').value = task.id;
            document.getElementById('editTaskName').value = task.nombre;
            document.getElementById('editTaskDescription').value = task.descripcion || '';
            document.getElementById('editTaskStatus').value = task.estado;
            document.getElementById('editTaskPriority').value = task.prioridad;
            
            openModal('editTaskModal');
        }

        async function updateTask(event) {
            event.preventDefault();
            const taskId = document.getElementById('editTaskId').value;
            const data = {
                nombre: document.getElementById('editTaskName').value,
                descripcion: document.getElementById('editTaskDescription').value,
                estado: document.getElementById('editTaskStatus').value,
                prioridad: parseInt(document.getElementById('editTaskPriority').value)
            };
            
            const response = await apiCall(`tasks/${taskId}`, 'PUT', data);
            if (response && response.success) {
                showAlert('Tarea actualizada exitosamente');
                closeModal('editTaskModal');
                refreshData();
            } else {
                showAlert(response?.error || 'Error al actualizar tarea', 'error');
            }
        }

        function confirmDelete(taskId) {
            const task = tasks.find(t => t.id === taskId);
            if (!task) return;
            
            taskToDelete = taskId;
            document.getElementById('deleteTaskName').textContent = task.nombre;
            document.getElementById('confirmDeleteBtn').onclick = () => deleteTask(taskId);
            openModal('deleteConfirmModal');
        }

        async function deleteTask(taskId) {
            const response = await apiCall(`tasks/${taskId}`, 'DELETE');
            if (response && response.success) {
                showAlert('Tarea eliminada');
                closeModal('deleteConfirmModal');
                refreshData();
            } else {
                showAlert(response?.error || 'Error al eliminar tarea', 'error');
            }
        }

        // Dependencias
        function populateDependencySelects() {
            const pendingTasks = tasks.filter(t => t.estado !== 'completada');
            const options = pendingTasks.map(t => `<option value="${t.id}">${escapeHtml(t.nombre)}</option>`).join('');
            document.getElementById('depPrerequisite').innerHTML = '<option value="">Selecciona una tarea...</option>' + options;
            document.getElementById('depDependent').innerHTML = '<option value="">Selecciona una tarea...</option>' + options;
        }

        async function addDependency(event) {
            event.preventDefault();
            const origen = parseInt(document.getElementById('depPrerequisite').value);
            const destino = parseInt(document.getElementById('depDependent').value);
            
            if (origen === destino) {
                showAlert('Una tarea no puede depender de si misma', 'error');
                return;
            }
            
            const response = await apiCall('dependencies', 'POST', { origen, destino });
            if (response && response.success) {
                showAlert('Dependencia agregada exitosamente');
                closeModal('dependencyModal');
                refreshData();
            } else {
                showAlert(response?.error || 'Error al agregar dependencia', 'error');
            }
        }

        async function loadDependencies() {
            const container = document.getElementById('dependenciesList');
            const response = await apiCall('dependencies');
            
            if (response && response.success) {
                if (response.data.length === 0) {
                    container.innerHTML = '<p style="color: var(--gray); text-align: center;">No hay dependencias definidas.</p>';
                    return;
                }
                
                container.innerHTML = response.data.map(dep => `
                    <div class="dependency-item">
                        <span class="dependency-task">${escapeHtml(dep.origen_nombre)}</span>
                        <span class="dependency-arrow">➔</span>
                        <span class="dependency-task">${escapeHtml(dep.destino_nombre)}</span>
                        <button class="btn btn-icon btn-danger btn-sm" onclick="removeDependency(${dep.origen}, ${dep.destino})">🗑️</button>
                    </div>
                `).join('');
            }
        }

        async function removeDependency(origen, destino) {
            const response = await apiCall(`dependencies/${origen}/${destino}`, 'DELETE');
            if (response && response.success) {
                showAlert('Dependencia eliminada');
                loadDependencies();
                refreshData();
            } else {
                showAlert(response?.error || 'Error al eliminar dependencia', 'error');
            }
        }

        // Visualizaciones
        async function viewExecutionOrder() {
            const response = await apiCall('execution-order');
            if (response && response.success) {
                showResultModal('📊 Orden de Ejecucion (Ordenamiento Topologico)', response.data);
            }
        }

        async function viewExecutableTasks() {
            const response = await apiCall('executable-tasks');
            if (response && response.success) {
                showResultModal('🎯 Tareas Ejecutables Ahora', response.data);
            }
        }

        async function viewNextTask() {
            const response = await apiCall('next-task');
            if (response && response.success) {
                if (response.data) {
                    showResultModal('⭐ Siguiente Tarea Recomendada', [response.data]);
                } else {
                    showResultModal('⭐ Siguiente Tarea', [], 'No hay tareas ejecutables disponibles.');
                }
            }
        }

        function showResultModal(title, tasksList, emptyMessage = null) {
            document.getElementById('resultModalTitle').textContent = title;
            const content = document.getElementById('resultModalContent');
            
            if (!tasksList || tasksList.length === 0) {
                content.innerHTML = `<p style="color: var(--gray); text-align: center;">${emptyMessage || 'No hay tareas disponibles.'}</p>`;
            } else {
                content.innerHTML = tasksList.map((task, index) => `
                    <div class="dependency-item">
                        <span style="font-weight: 600; color: var(--primary);">${index + 1}.</span>
                        <span class="dependency-task">
                            <strong>${escapeHtml(task.nombre)}</strong>
                            <span class="badge badge-priority-${task.prioridad}" style="margin-left: 8px;">⭐ ${task.prioridad}</span>
                        </span>
                    </div>
                `).join('');
            }
            
            openModal('resultModal');
        }

        // Filtros
        function setFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-tab').forEach(tab => {
                tab.classList.toggle('active', tab.dataset.filter === filter);
            });
            renderTasks();
        }

        function filterTasks() {
            renderTasks();
        }

        function updateTaskCount() {
            const count = tasks.length;
            document.getElementById('taskCount').textContent = `${count} tarea${count !== 1 ? 's' : ''}`;
        }

        function selectTask(taskId) {
            document.querySelectorAll('.task-item').forEach(item => item.classList.remove('selected'));
            event.currentTarget.classList.add('selected');
        }

        // Utilidades
        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function formatStatus(status) {
            const statusMap = {
                'pendiente': 'Pendiente',
                'en_progreso': 'En Progreso',
                'completada': 'Completada'
            };
            return statusMap[status] || status;
        }

        function formatDate(dateStr) {
            if (!dateStr) return '';
            return new Date(dateStr).toLocaleDateString('es-ES');
        }

        // Cerrar modales al hacer clic fuera
        document.querySelectorAll('.modal-overlay').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });

        // Inicializacion
        document.addEventListener('DOMContentLoaded', () => {
            refreshData();
            setInterval(() => {
                loadTasks();
                loadStatistics();
            }, 60000);
        });
    </script>
</body>
</html>'''

    def handle_api_get(self):
        """Maneja API GET requests"""
        path = self.path.split('/api/')[1].split('?')[0]
        path_parts = path.split('/')
        endpoint = path_parts[0]
        
        response = {'success': False, 'error': 'Endpoint no encontrado'}
        
        try:
            gestor = get_gestor()
            
            if endpoint == 'tasks':
                tasks = gestor.obtener_todas_tareas()
                response = {'success': True, 'data': [t.to_dict() for t in tasks]}
            
            elif endpoint == 'statistics':
                stats = gestor.obtener_estadisticas()
                response = {'success': True, 'data': stats}
            
            elif endpoint == 'execution-order':
                orden = gestor.calcular_orden_ejecucion()
                response = {'success': True, 'data': [t.to_dict() for t in orden] if orden else []}
            
            elif endpoint == 'executable-tasks':
                ejecutables = gestor.obtener_tareas_ejecutables()
                response = {'success': True, 'data': [t.to_dict() for t in ejecutables]}
            
            elif endpoint == 'next-task':
                siguiente = gestor.obtener_siguiente_tarea()
                response = {'success': True, 'data': siguiente.to_dict() if siguiente else None}
            
            elif endpoint == 'daily-plan':
                plan = gestor.obtener_plan_diario()
                response = {'success': True, 'data': [t.to_dict() for t in plan]}
            
            elif endpoint == 'dependencies':
                deps = gestor.db.obtener_todas_dependencias()
                dep_list = []
                for origen, destino in deps:
                    tarea_origen = gestor.obtener_tarea(origen)
                    tarea_destino = gestor.obtener_tarea(destino)
                    if tarea_origen and tarea_destino:
                        dep_list.append({
                            'origen': origen,
                            'destino': destino,
                            'origen_nombre': tarea_origen.nombre,
                            'destino_nombre': tarea_destino.nombre
                        })
                response = {'success': True, 'data': dep_list}
                
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def handle_api_post(self):
        """Maneja API POST requests"""
        path = self.path.split('/api/')[1]
        path_parts = path.split('/')
        endpoint = path_parts[0]
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        response = {'success': False, 'error': 'Operacion no soportada'}
        
        try:
            gestor = get_gestor()
            
            if endpoint == 'tasks':
                nombre = data.get('nombre', '').strip()
                if not nombre:
                    response = {'success': False, 'error': 'El nombre es requerido'}
                else:
                    exito, mensaje, tarea_id = gestor.crear_tarea(
                        nombre=nombre,
                        descripcion=data.get('descripcion', ''),
                        prioridad=data.get('prioridad', 3)
                    )
                    response = {
                        'success': exito,
                        'message': mensaje,
                        'data': {'id': tarea_id} if exito else None,
                        'error': mensaje if not exito else None
                    }
            
            elif endpoint == 'dependencies':
                origen = data.get('origen')
                destino = data.get('destino')
                if not origen or not destino:
                    response = {'success': False, 'error': 'Origen y destino son requeridos'}
                else:
                    exito, mensaje = gestor.agregar_dependencia(origen, destino)
                    response = {
                        'success': exito,
                        'message': mensaje,
                        'error': mensaje if not exito else None
                    }
            
            elif len(path_parts) >= 3 and path_parts[2] == 'complete':
                task_id = int(path_parts[1])
                exito, mensaje, desbloqueadas = gestor.marcar_completada(task_id)
                response = {
                    'success': exito,
                    'message': mensaje,
                    'data': {'desbloqueadas': desbloqueadas},
                    'error': mensaje if not exito else None
                }
                
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def handle_api_put(self):
        """Maneja API PUT requests"""
        path = self.path.split('/api/')[1]
        path_parts = path.split('/')
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        response = {'success': False, 'error': 'Operacion no soportada'}
        
        try:
            gestor = get_gestor()
            
            if path_parts[0] == 'tasks' and len(path_parts) > 1:
                task_id = int(path_parts[1])
                tarea = gestor.obtener_tarea(task_id)
                
                if not tarea:
                    response = {'success': False, 'error': 'Tarea no encontrada'}
                else:
                    if 'nombre' in data:
                        tarea.nombre = data['nombre']
                    if 'descripcion' in data:
                        tarea.descripcion = data['descripcion']
                    if 'estado' in data:
                        tarea.estado = data['estado']
                    if 'prioridad' in data:
                        tarea.prioridad = data['prioridad']
                    
                    exito, mensaje = gestor.actualizar_tarea(tarea)
                    response = {
                        'success': exito,
                        'message': mensaje,
                        'error': mensaje if not exito else None
                    }
                    
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def handle_api_delete(self):
        """Maneja API DELETE requests"""
        path = self.path.split('/api/')[1]
        path_parts = path.split('/')
        
        response = {'success': False, 'error': 'Operacion no soportada'}
        
        try:
            gestor = get_gestor()
            
            if path_parts[0] == 'tasks' and len(path_parts) > 1:
                task_id = int(path_parts[1])
                exito, mensaje = gestor.eliminar_tarea(task_id)
                response = {
                    'success': exito,
                    'message': mensaje,
                    'error': mensaje if not exito else None
                }
            
            elif path_parts[0] == 'dependencies' and len(path_parts) >= 3:
                origen = int(path_parts[1])
                destino = int(path_parts[2])
                exito, mensaje = gestor.eliminar_dependencia(origen, destino)
                response = {
                    'success': exito,
                    'message': mensaje,
                    'error': mensaje if not exito else None
                }
                
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def send_json(self, data):
        """Envia una respuesta JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        json_str = json.dumps(data, ensure_ascii=False, default=str)
        self.wfile.write(json_str.encode('utf-8'))

    def send_404(self):
        """Envia un error 404"""
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': False, 'error': 'Not found'}).encode())

    def send_error_response(self, error_msg):
        """Envia una respuesta de error"""
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': False, 'error': error_msg}).encode())

    def log_message(self, format, *args):
        """Reduce logs"""
        pass


def main():
    """Inicia el servidor web"""
    port = 8080
    server_address = ('', port)
    
    print("\n" + "="*60)
    print("   🚀 GESTOR DE TAREAS CON DEPENDENCIAS - WEB UI")
    print("   📚 Universidad Don Bosco - PED Fase 2")
    print("="*60)
    print(f"\n   🌐 Servidor corriendo en: http://localhost:{port}")
    print("   📱 Abre esta URL en tu navegador")
    print("\n   ⏹️  Presiona Ctrl+C para detener el servidor")
    print("="*60 + "\n")
    
    try:
        httpd = HTTPServer(server_address, ModernWebHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        global _gestor_instance
        if _gestor_instance:
            _gestor_instance.cerrar()


if __name__ == "__main__":
    main()
