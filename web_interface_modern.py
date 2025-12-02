#!/usr/bin/env python3
"""
Interfaz Web Moderna - Gestor de Tareas con Dependencias
Sistema completo con UI profesional para Fase 2
Universidad Don Bosco - PED
"""

import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.gestor_proyecto import GestorProyecto

_gestor_instance = None

def get_gestor():
    global _gestor_instance
    if _gestor_instance is None:
        _gestor_instance = GestorProyecto('gestor_tareas_web.db')
    return _gestor_instance


class ModernWebHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        if not hasattr(ModernWebHandler, '_gestor_initialized'):
            ModernWebHandler._gestor_initialized = True
            get_gestor()
        super().__init__(*args, **kwargs)

    def do_GET(self):
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
        try:
            if self.path.startswith('/api/'):
                self.handle_api_post()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_DELETE(self):
        try:
            if self.path.startswith('/api/'):
                self.handle_api_delete()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_PUT(self):
        try:
            if self.path.startswith('/api/'):
                self.handle_api_put()
            else:
                self.send_404()
        except Exception as e:
            self.send_error_response(str(e))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serve_html(self):
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
    <title>Gestor de Tareas | UDB</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,700&family=Public+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0d0d0d;
            --bg-secondary: #161616;
            --bg-tertiary: #1f1f1f;
            --bg-card: #1a1a1a;
            --bg-hover: #252525;
            
            --text-primary: #e8e6e3;
            --text-secondary: #a8a5a0;
            --text-muted: #6b6965;
            
            --accent: #e85d04;
            --accent-light: #f48c06;
            --accent-glow: rgba(232, 93, 4, 0.15);
            
            --success: #2ec4b6;
            --warning: #ffbe0b;
            --danger: #e63946;
            
            --border: #2a2a2a;
            --border-light: #333;
            
            --font-display: 'Fraunces', Georgia, serif;
            --font-body: 'Public Sans', -apple-system, sans-serif;
            
            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
            
            --shadow: 0 4px 20px rgba(0,0,0,0.4);
            --shadow-glow: 0 0 30px var(--accent-glow);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            font-size: 16px;
        }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated background */
        .bg-pattern {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -1;
            background: 
                radial-gradient(ellipse at 20% 20%, rgba(232, 93, 4, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(46, 196, 182, 0.05) 0%, transparent 50%),
                linear-gradient(180deg, var(--bg-primary) 0%, #0a0a0a 100%);
        }

        .bg-grid {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: -1;
            background-image: 
                linear-gradient(var(--border) 1px, transparent 1px),
                linear-gradient(90deg, var(--border) 1px, transparent 1px);
            background-size: 60px 60px;
            opacity: 0.3;
            mask-image: radial-gradient(ellipse at center, black 0%, transparent 70%);
        }

        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px var(--accent-glow); }
            50% { box-shadow: 0 0 20px var(--accent-glow), 0 0 30px var(--accent-glow); }
        }

        .animate-in {
            animation: fadeInUp 0.5s ease-out forwards;
        }

        .stagger-1 { animation-delay: 0.1s; opacity: 0; }
        .stagger-2 { animation-delay: 0.2s; opacity: 0; }
        .stagger-3 { animation-delay: 0.3s; opacity: 0; }
        .stagger-4 { animation-delay: 0.4s; opacity: 0; }

        /* Header */
        .header {
            padding: 2rem 3rem;
            border-bottom: 1px solid var(--border);
            background: rgba(13, 13, 13, 0.8);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: baseline;
            gap: 1rem;
        }

        .logo h1 {
            font-family: var(--font-display);
            font-size: 1.75rem;
            font-weight: 500;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .logo h1 span {
            color: var(--accent);
        }

        .logo-tag {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        /* Main Layout */
        .main-layout {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem 3rem;
            display: grid;
            grid-template-columns: 280px 1fr 340px;
            gap: 2rem;
        }

        @media (max-width: 1200px) {
            .main-layout {
                grid-template-columns: 1fr;
                padding: 1.5rem;
            }
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: var(--border-light);
        }

        .card-header {
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .card-title {
            font-family: var(--font-display);
            font-size: 1.1rem;
            font-weight: 500;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .card-title-icon {
            width: 8px;
            height: 8px;
            background: var(--accent);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .card-body {
            padding: 1.5rem;
        }

        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            font-family: var(--font-body);
            font-size: 0.875rem;
            font-weight: 500;
            border: 1px solid transparent;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }

        .btn-primary {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        .btn-primary:hover {
            background: var(--accent-light);
            box-shadow: var(--shadow-glow);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: transparent;
            color: var(--text-primary);
            border-color: var(--border-light);
        }

        .btn-secondary:hover {
            background: var(--bg-hover);
            border-color: var(--text-muted);
        }

        .btn-ghost {
            background: transparent;
            color: var(--text-secondary);
            border: none;
            padding: 0.5rem;
        }

        .btn-ghost:hover {
            color: var(--text-primary);
            background: var(--bg-hover);
        }

        .btn-danger {
            background: transparent;
            color: var(--danger);
            border-color: var(--danger);
        }

        .btn-danger:hover {
            background: var(--danger);
            color: white;
        }

        .btn-success {
            background: var(--success);
            color: var(--bg-primary);
            border-color: var(--success);
        }

        .btn-block {
            width: 100%;
        }

        /* Action Menu */
        .action-menu {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .action-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
            font-family: var(--font-body);
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .action-item:hover {
            background: var(--bg-hover);
            border-color: var(--border);
            color: var(--text-primary);
        }

        .action-item:hover .action-icon {
            color: var(--accent);
        }

        .action-icon {
            font-size: 1.1rem;
            transition: color 0.2s;
        }

        /* Task List */
        .task-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 65vh;
            overflow-y: auto;
            padding-right: 0.5rem;
        }

        .task-list::-webkit-scrollbar {
            width: 4px;
        }

        .task-list::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        .task-list::-webkit-scrollbar-thumb {
            background: var(--border-light);
            border-radius: 2px;
        }

        .task-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem 1.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            animation: slideIn 0.3s ease-out forwards;
        }

        .task-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--accent);
            border-radius: var(--radius-md) 0 0 var(--radius-md);
            opacity: 0;
            transition: opacity 0.2s;
        }

        .task-item:hover {
            border-color: var(--border-light);
            background: var(--bg-tertiary);
        }

        .task-item:hover::before {
            opacity: 1;
        }

        .task-item.completed {
            opacity: 0.5;
        }

        .task-item.completed .task-name {
            text-decoration: line-through;
            color: var(--text-muted);
        }

        .task-item.blocked {
            border-color: var(--danger);
            border-style: dashed;
        }

        .task-item.blocked::before {
            background: var(--danger);
            opacity: 0.5;
        }

        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }

        .task-name {
            font-weight: 500;
            color: var(--text-primary);
            font-size: 0.95rem;
        }

        .task-description {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
            line-height: 1.5;
        }

        .task-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
        }

        .task-actions {
            display: flex;
            gap: 0.25rem;
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
            gap: 0.25rem;
            padding: 0.25rem 0.6rem;
            border-radius: 100px;
            font-size: 0.7rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .badge-priority {
            background: rgba(232, 93, 4, 0.15);
            color: var(--accent-light);
        }

        .badge-priority.high {
            background: rgba(230, 57, 70, 0.15);
            color: var(--danger);
        }

        .badge-priority.low {
            background: rgba(46, 196, 182, 0.15);
            color: var(--success);
        }

        .badge-status {
            background: var(--bg-tertiary);
            color: var(--text-muted);
        }

        .badge-status.active {
            background: rgba(46, 196, 182, 0.15);
            color: var(--success);
        }

        .badge-blocked {
            background: rgba(230, 57, 70, 0.15);
            color: var(--danger);
        }

        /* Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }

        .stat-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1rem;
            text-align: center;
            transition: all 0.2s;
        }

        .stat-item:hover {
            border-color: var(--accent);
        }

        .stat-value {
            font-family: var(--font-display);
            font-size: 2rem;
            font-weight: 500;
            color: var(--text-primary);
            line-height: 1;
        }

        .stat-label {
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 0.5rem;
        }

        /* Progress */
        .progress-section {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
        }

        .progress-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }

        .progress-label {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .progress-value {
            font-family: var(--font-display);
            font-size: 0.9rem;
            color: var(--accent);
        }

        .progress-bar {
            height: 6px;
            background: var(--bg-tertiary);
            border-radius: 3px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--accent-light));
            border-radius: 3px;
            transition: width 0.5s ease;
        }

        /* Dependency Graph */
        .graph-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            min-height: 300px;
            position: relative;
            overflow: auto;
        }

        .graph-empty {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 200px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .graph-node {
            position: absolute;
            background: var(--bg-card);
            border: 2px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 0.75rem 1rem;
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-primary);
            cursor: pointer;
            transition: all 0.2s;
            max-width: 150px;
            text-align: center;
            z-index: 2;
        }

        .graph-node:hover {
            border-color: var(--accent);
            transform: scale(1.05);
            z-index: 3;
        }

        .graph-node.completed {
            border-color: var(--success);
            background: rgba(46, 196, 182, 0.1);
        }

        .graph-node.blocked {
            border-color: var(--danger);
            border-style: dashed;
        }

        .graph-node.executable {
            border-color: var(--accent);
            animation: glow 2s infinite;
        }

        .graph-svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .graph-edge {
            stroke: var(--border-light);
            stroke-width: 2;
            fill: none;
            marker-end: url(#arrowhead);
        }

        /* Search & Filters */
        .search-section {
            margin-bottom: 1rem;
        }

        .search-input {
            width: 100%;
            padding: 0.75rem 1rem;
            padding-left: 2.5rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            font-family: var(--font-body);
            font-size: 0.9rem;
            color: var(--text-primary);
            transition: all 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .search-input::placeholder {
            color: var(--text-muted);
        }

        .search-wrapper {
            position: relative;
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .filter-tabs {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .filter-tab {
            padding: 0.5rem 1rem;
            background: transparent;
            border: 1px solid var(--border);
            border-radius: 100px;
            font-family: var(--font-body);
            font-size: 0.8rem;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
        }

        .filter-tab:hover {
            border-color: var(--text-muted);
            color: var(--text-secondary);
        }

        .filter-tab.active {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }

        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
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
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 480px;
            max-height: 90vh;
            overflow-y: auto;
            animation: fadeInUp 0.3s ease-out;
        }

        .modal-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .modal-title {
            font-family: var(--font-display);
            font-size: 1.25rem;
            font-weight: 500;
        }

        .modal-close {
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-secondary);
            border: none;
            border-radius: var(--radius-sm);
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 1.25rem;
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
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: flex-end;
            gap: 0.75rem;
        }

        /* Forms */
        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .form-input, .form-select, .form-textarea {
            width: 100%;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            font-family: var(--font-body);
            font-size: 0.9rem;
            color: var(--text-primary);
            transition: all 0.2s;
        }

        .form-input:focus, .form-select:focus, .form-textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .form-textarea {
            resize: vertical;
            min-height: 100px;
        }

        .form-select {
            cursor: pointer;
        }

        /* Alerts */
        .toast-container {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .toast {
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            animation: slideIn 0.3s ease-out;
            min-width: 280px;
        }

        .toast-success {
            border-color: var(--success);
        }

        .toast-success .toast-icon {
            color: var(--success);
        }

        .toast-error {
            border-color: var(--danger);
        }

        .toast-error .toast-icon {
            color: var(--danger);
        }

        .toast-icon {
            font-size: 1.1rem;
        }

        .toast-message {
            font-size: 0.9rem;
            color: var(--text-primary);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
        }

        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.3;
        }

        .empty-state-text {
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }

        /* Dependency Visualization */
        .dep-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 0.5rem;
        }

        .dep-arrow {
            color: var(--accent);
            font-size: 1.25rem;
        }

        .dep-task {
            flex: 1;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .dep-task.source {
            color: var(--text-primary);
        }

        /* Info Panel */
        .info-panel {
            background: linear-gradient(135deg, rgba(232, 93, 4, 0.1) 0%, transparent 100%);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            margin-top: 1rem;
        }

        .info-panel h4 {
            font-family: var(--font-display);
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }

        .info-panel p {
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.6;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
        }

        .footer p {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .footer strong {
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    <div class="bg-grid"></div>

    <header class="header">
        <div class="header-content">
            <div class="logo">
                <h1>Task<span>Flow</span></h1>
                <span class="logo-tag">Dependency Manager</span>
            </div>
            <button class="btn btn-primary" onclick="openModal('createTaskModal')">
                + Nueva Tarea
            </button>
        </div>
    </header>

    <main class="main-layout">
        <!-- Sidebar Actions -->
        <aside class="animate-in stagger-1">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-title-icon"></span>
                        Acciones
                    </h2>
                </div>
                <div class="card-body">
                    <div class="action-menu">
                        <button class="action-item" onclick="openModal('createTaskModal')">
                            <span class="action-icon">+</span>
                            <span>Crear Tarea</span>
                        </button>
                        <button class="action-item" onclick="openModal('dependencyModal')">
                            <span class="action-icon">&#8594;</span>
                            <span>Nueva Dependencia</span>
                        </button>
                        <button class="action-item" onclick="viewExecutionOrder()">
                            <span class="action-icon">&#9776;</span>
                            <span>Orden Topologico</span>
                        </button>
                        <button class="action-item" onclick="viewExecutableTasks()">
                            <span class="action-icon">&#10003;</span>
                            <span>Tareas Disponibles</span>
                        </button>
                        <button class="action-item" onclick="viewNextTask()">
                            <span class="action-icon">&#9733;</span>
                            <span>Siguiente Tarea</span>
                        </button>
                        <button class="action-item" onclick="refreshData()">
                            <span class="action-icon">&#8635;</span>
                            <span>Actualizar</span>
                        </button>
                    </div>

                    <div class="info-panel">
                        <h4>Estructuras de Datos</h4>
                        <p>Grafo Dirigido Aciclico (DAG) para dependencias. Ordenamiento topologico con algoritmo de Kahn. Cola FIFO para plan diario.</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <section class="animate-in stagger-2">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-title-icon"></span>
                        Tareas
                    </h2>
                    <span id="taskCount" class="badge badge-status">0</span>
                </div>
                <div class="card-body">
                    <div class="search-section">
                        <div class="search-wrapper">
                            <span class="search-icon">&#128269;</span>
                            <input type="text" class="search-input" id="searchInput" placeholder="Buscar tareas..." oninput="filterTasks()">
                        </div>
                    </div>
                    
                    <div class="filter-tabs">
                        <button class="filter-tab active" data-filter="all" onclick="setFilter('all')">Todas</button>
                        <button class="filter-tab" data-filter="pendiente" onclick="setFilter('pendiente')">Pendientes</button>
                        <button class="filter-tab" data-filter="en_progreso" onclick="setFilter('en_progreso')">En Progreso</button>
                        <button class="filter-tab" data-filter="completada" onclick="setFilter('completada')">Completadas</button>
                        <button class="filter-tab" data-filter="blocked" onclick="setFilter('blocked')">Bloqueadas</button>
                    </div>

                    <div id="taskList" class="task-list">
                        <div class="empty-state">
                            <div class="empty-state-icon">&#128203;</div>
                            <p class="empty-state-text">Cargando tareas...</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dependency Graph -->
            <div class="card" style="margin-top: 1.5rem;">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-title-icon"></span>
                        Grafo de Dependencias
                    </h2>
                </div>
                <div class="card-body">
                    <div id="graphContainer" class="graph-container">
                        <svg class="graph-svg" id="graphSvg">
                            <defs>
                                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                                    <polygon points="0 0, 10 3.5, 0 7" fill="#e85d04" />
                                </marker>
                            </defs>
                        </svg>
                        <div class="graph-empty">
                            <p>Agrega tareas y dependencias para visualizar el grafo</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Sidebar Stats -->
        <aside class="animate-in stagger-3">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-title-icon"></span>
                        Estadisticas
                    </h2>
                </div>
                <div class="card-body">
                    <div id="statsContainer">
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value">-</div>
                                <div class="stat-label">Total</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">-</div>
                                <div class="stat-label">Completadas</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">-</div>
                                <div class="stat-label">Pendientes</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">-</div>
                                <div class="stat-label">Ejecutables</div>
                            </div>
                        </div>
                        <div class="progress-section">
                            <div class="progress-header">
                                <span class="progress-label">Progreso</span>
                                <span class="progress-value" id="progressValue">0%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dependencies List -->
            <div class="card" style="margin-top: 1.5rem;">
                <div class="card-header">
                    <h2 class="card-title">
                        <span class="card-title-icon"></span>
                        Dependencias
                    </h2>
                </div>
                <div class="card-body">
                    <div id="dependenciesList" style="max-height: 300px; overflow-y: auto;">
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Sin dependencias</p>
                    </div>
                </div>
            </div>
        </aside>
    </main>

    <footer class="footer">
        <p><strong>Universidad Don Bosco</strong> &mdash; Programacion con Estructuras de Datos</p>
        <p>Sistema de Gestion de Tareas con Dependencias &mdash; Fase 2</p>
    </footer>

    <!-- Toast Container -->
    <div id="toastContainer" class="toast-container"></div>

    <!-- Modals -->
    <!-- Create Task Modal -->
    <div id="createTaskModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Nueva Tarea</h3>
                <button class="modal-close" onclick="closeModal('createTaskModal')">&times;</button>
            </div>
            <form id="createTaskForm" onsubmit="createTask(event)">
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Nombre *</label>
                        <input type="text" class="form-input" id="taskName" required placeholder="Nombre de la tarea">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Descripcion</label>
                        <textarea class="form-textarea" id="taskDescription" placeholder="Descripcion opcional..."></textarea>
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
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('createTaskModal')">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Crear</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Edit Task Modal -->
    <div id="editTaskModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Editar Tarea</h3>
                <button class="modal-close" onclick="closeModal('editTaskModal')">&times;</button>
            </div>
            <form id="editTaskForm" onsubmit="updateTask(event)">
                <div class="modal-body">
                    <input type="hidden" id="editTaskId">
                    <div class="form-group">
                        <label class="form-label">Nombre *</label>
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
                    <button type="button" class="btn btn-secondary" onclick="closeModal('editTaskModal')">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Guardar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Dependency Modal -->
    <div id="dependencyModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Nueva Dependencia</h3>
                <button class="modal-close" onclick="closeModal('dependencyModal')">&times;</button>
            </div>
            <form id="dependencyForm" onsubmit="addDependency(event)">
                <div class="modal-body">
                    <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1.5rem;">
                        La tarea dependiente no podra completarse hasta que la tarea prerequisito este completada.
                    </p>
                    <div class="form-group">
                        <label class="form-label">Tarea Prerequisito (debe completarse primero)</label>
                        <select class="form-select" id="depPrerequisite" required>
                            <option value="">Seleccionar...</option>
                        </select>
                    </div>
                    <div style="text-align: center; color: var(--accent); font-size: 1.5rem; margin: 0.5rem 0;">
                        &#8595;
                    </div>
                    <div class="form-group">
                        <label class="form-label">Tarea Dependiente (se desbloquea despues)</label>
                        <select class="form-select" id="depDependent" required>
                            <option value="">Seleccionar...</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('dependencyModal')">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Agregar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Result Modal -->
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
                <button type="button" class="btn btn-primary" onclick="closeModal('resultModal')">Cerrar</button>
            </div>
        </div>
    </div>

    <!-- Delete Confirm Modal -->
    <div id="deleteModal" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 class="modal-title">Eliminar Tarea</h3>
                <button class="modal-close" onclick="closeModal('deleteModal')">&times;</button>
            </div>
            <div class="modal-body">
                <p style="color: var(--text-secondary);">Esta accion no se puede deshacer.</p>
                <p id="deleteTaskName" style="font-weight: 600; color: var(--danger); margin-top: 1rem;"></p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" onclick="closeModal('deleteModal')">Cancelar</button>
                <button type="button" class="btn btn-danger" id="confirmDeleteBtn">Eliminar</button>
            </div>
        </div>
    </div>

    <script>
        // State
        let tasks = [];
        let dependencies = [];
        let executableTaskIds = new Set();
        let currentFilter = 'all';

        // Toast notifications
        function showToast(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <span class="toast-icon">${type === 'success' ? '&#10003;' : '&#10007;'}</span>
                <span class="toast-message">${message}</span>
            `;
            container.appendChild(toast);
            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        // Modal functions
        function openModal(modalId) {
            document.getElementById(modalId).classList.add('active');
            if (modalId === 'dependencyModal') {
                populateDependencySelects();
            }
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        // API
        async function apiCall(endpoint, method = 'GET', data = null) {
            try {
                const options = { method, headers: { 'Content-Type': 'application/json' } };
                if (data && method !== 'GET') options.body = JSON.stringify(data);
                const response = await fetch('/api/' + endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                showToast('Error de conexion', 'error');
                return null;
            }
        }

        // Data loading
        async function loadTasks() {
            const response = await apiCall('tasks');
            if (response?.success) {
                tasks = response.data;
                renderTasks();
                updateTaskCount();
            }
        }

        async function loadStatistics() {
            const response = await apiCall('statistics');
            if (response?.success) {
                renderStatistics(response.data);
            }
        }

        async function loadDependencies() {
            const response = await apiCall('dependencies');
            if (response?.success) {
                dependencies = response.data;
                renderDependencies();
                renderGraph();
            }
        }

        async function loadExecutableTasks() {
            const response = await apiCall('executable-tasks');
            if (response?.success) {
                executableTaskIds = new Set(response.data.map(t => t.id));
            }
        }

        async function refreshData() {
            await Promise.all([loadTasks(), loadStatistics(), loadDependencies(), loadExecutableTasks()]);
            renderTasks();
            renderGraph();
            showToast('Datos actualizados');
        }

        // Check if task can be completed (all dependencies completed)
        function canCompleteTask(taskId) {
            const taskDeps = dependencies.filter(d => d.destino === taskId);
            for (const dep of taskDeps) {
                const prereq = tasks.find(t => t.id === dep.origen);
                if (prereq && prereq.estado !== 'completada') {
                    return false;
                }
            }
            return true;
        }

        function getBlockingTasks(taskId) {
            const blocking = [];
            const taskDeps = dependencies.filter(d => d.destino === taskId);
            for (const dep of taskDeps) {
                const prereq = tasks.find(t => t.id === dep.origen);
                if (prereq && prereq.estado !== 'completada') {
                    blocking.push(prereq.nombre);
                }
            }
            return blocking;
        }

        // Rendering
        function renderTasks() {
            const container = document.getElementById('taskList');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            let filtered = tasks.filter(task => {
                const matchesSearch = task.nombre.toLowerCase().includes(searchTerm) || 
                                     (task.descripcion?.toLowerCase().includes(searchTerm));
                if (!matchesSearch) return false;
                
                if (currentFilter === 'all') return true;
                if (currentFilter === 'blocked') {
                    return task.estado !== 'completada' && !canCompleteTask(task.id);
                }
                return task.estado === currentFilter;
            });

            filtered.sort((a, b) => b.prioridad - a.prioridad);

            if (filtered.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">&#128203;</div>
                        <p class="empty-state-text">No hay tareas</p>
                        <button class="btn btn-primary" onclick="openModal('createTaskModal')">Crear tarea</button>
                    </div>
                `;
                return;
            }

            container.innerHTML = filtered.map((task, index) => {
                const isBlocked = task.estado !== 'completada' && !canCompleteTask(task.id);
                const blockingTasks = isBlocked ? getBlockingTasks(task.id) : [];
                const isExecutable = executableTaskIds.has(task.id);
                
                let priorityClass = '';
                if (task.prioridad >= 4) priorityClass = 'high';
                else if (task.prioridad <= 2) priorityClass = 'low';

                return `
                    <div class="task-item ${task.estado === 'completada' ? 'completed' : ''} ${isBlocked ? 'blocked' : ''}" 
                         style="animation-delay: ${index * 0.05}s">
                        <div class="task-header">
                            <span class="task-name">${escapeHtml(task.nombre)}</span>
                            <div class="task-actions">
                                ${task.estado !== 'completada' ? `
                                    <button class="btn btn-ghost" onclick="event.stopPropagation(); tryCompleteTask(${task.id})" title="Completar">&#10003;</button>
                                ` : ''}
                                <button class="btn btn-ghost" onclick="event.stopPropagation(); openEditModal(${task.id})" title="Editar">&#9998;</button>
                                <button class="btn btn-ghost" onclick="event.stopPropagation(); confirmDelete(${task.id})" title="Eliminar">&#128465;</button>
                            </div>
                        </div>
                        ${task.descripcion ? `<p class="task-description">${escapeHtml(task.descripcion)}</p>` : ''}
                        <div class="task-meta">
                            <span class="badge badge-priority ${priorityClass}">P${task.prioridad}</span>
                            <span class="badge badge-status ${task.estado === 'completada' ? 'active' : ''}">${formatStatus(task.estado)}</span>
                            ${isBlocked ? `<span class="badge badge-blocked" title="Bloqueada por: ${blockingTasks.join(', ')}">Bloqueada</span>` : ''}
                            ${isExecutable && task.estado !== 'completada' ? `<span class="badge badge-status active">Ejecutable</span>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function renderStatistics(stats) {
            const container = document.getElementById('statsContainer');
            container.innerHTML = `
                <div class="stats-grid">
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
                <div class="progress-section">
                    <div class="progress-header">
                        <span class="progress-label">Progreso</span>
                        <span class="progress-value">${stats.porcentaje_completado.toFixed(0)}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${stats.porcentaje_completado}%"></div>
                    </div>
                </div>
            `;
        }

        function renderDependencies() {
            const container = document.getElementById('dependenciesList');
            if (dependencies.length === 0) {
                container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem;">Sin dependencias definidas</p>';
                return;
            }
            container.innerHTML = dependencies.map(dep => `
                <div class="dep-item">
                    <span class="dep-task source">${escapeHtml(dep.origen_nombre)}</span>
                    <span class="dep-arrow">&#8594;</span>
                    <span class="dep-task">${escapeHtml(dep.destino_nombre)}</span>
                    <button class="btn btn-ghost" onclick="removeDependency(${dep.origen}, ${dep.destino})" title="Eliminar">&#10007;</button>
                </div>
            `).join('');
        }

        function renderGraph() {
            const container = document.getElementById('graphContainer');
            const svg = document.getElementById('graphSvg');
            
            // Clear existing nodes (keep svg)
            container.querySelectorAll('.graph-node').forEach(n => n.remove());
            svg.innerHTML = `<defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#e85d04" />
                </marker>
            </defs>`;

            if (tasks.length === 0) {
                container.querySelector('.graph-empty').style.display = 'flex';
                return;
            }
            container.querySelector('.graph-empty').style.display = 'none';

            // Calculate positions using simple layout
            const nodePositions = {};
            const containerWidth = container.clientWidth - 40;
            const containerHeight = Math.max(300, tasks.length * 50);
            container.style.height = containerHeight + 'px';

            // Group tasks by dependency level
            const levels = {};
            const taskLevels = {};
            
            // Calculate level for each task (0 = no dependencies)
            function getLevel(taskId, visited = new Set()) {
                if (visited.has(taskId)) return 0;
                visited.add(taskId);
                
                const deps = dependencies.filter(d => d.destino === taskId);
                if (deps.length === 0) return 0;
                
                let maxLevel = 0;
                for (const dep of deps) {
                    maxLevel = Math.max(maxLevel, getLevel(dep.origen, visited) + 1);
                }
                return maxLevel;
            }

            tasks.forEach(task => {
                const level = getLevel(task.id);
                taskLevels[task.id] = level;
                if (!levels[level]) levels[level] = [];
                levels[level].push(task);
            });

            const maxLevel = Math.max(...Object.keys(levels).map(Number), 0);
            const levelWidth = containerWidth / (maxLevel + 1);

            // Position nodes
            Object.entries(levels).forEach(([level, levelTasks]) => {
                const x = parseInt(level) * levelWidth + 20;
                const yStep = (containerHeight - 40) / (levelTasks.length + 1);
                
                levelTasks.forEach((task, idx) => {
                    nodePositions[task.id] = {
                        x: x,
                        y: (idx + 1) * yStep
                    };
                });
            });

            // Draw edges first
            dependencies.forEach(dep => {
                const from = nodePositions[dep.origen];
                const to = nodePositions[dep.destino];
                if (from && to) {
                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    const midX = (from.x + to.x) / 2;
                    path.setAttribute('d', `M ${from.x + 75} ${from.y + 20} Q ${midX} ${from.y + 20}, ${midX} ${(from.y + to.y) / 2 + 20} T ${to.x} ${to.y + 20}`);
                    path.setAttribute('class', 'graph-edge');
                    svg.appendChild(path);
                }
            });

            // Draw nodes
            tasks.forEach(task => {
                const pos = nodePositions[task.id];
                if (!pos) return;

                const isBlocked = task.estado !== 'completada' && !canCompleteTask(task.id);
                const isExecutable = executableTaskIds.has(task.id) && task.estado !== 'completada';

                const node = document.createElement('div');
                node.className = `graph-node ${task.estado === 'completada' ? 'completed' : ''} ${isBlocked ? 'blocked' : ''} ${isExecutable ? 'executable' : ''}`;
                node.style.left = pos.x + 'px';
                node.style.top = pos.y + 'px';
                node.textContent = task.nombre.length > 20 ? task.nombre.substring(0, 17) + '...' : task.nombre;
                node.title = task.nombre;
                node.onclick = () => openEditModal(task.id);
                container.appendChild(node);
            });
        }

        // Task actions
        async function createTask(event) {
            event.preventDefault();
            const data = {
                nombre: document.getElementById('taskName').value,
                descripcion: document.getElementById('taskDescription').value,
                prioridad: parseInt(document.getElementById('taskPriority').value)
            };
            
            const response = await apiCall('tasks', 'POST', data);
            if (response?.success) {
                showToast('Tarea creada');
                closeModal('createTaskModal');
                document.getElementById('createTaskForm').reset();
                refreshData();
            } else {
                showToast(response?.error || 'Error al crear', 'error');
            }
        }

        async function tryCompleteTask(taskId) {
            const task = tasks.find(t => t.id === taskId);
            if (!task) return;

            // Check dependencies
            if (!canCompleteTask(taskId)) {
                const blocking = getBlockingTasks(taskId);
                showToast(`No se puede completar. Primero completa: ${blocking.join(', ')}`, 'error');
                return;
            }

            const response = await apiCall(`tasks/${taskId}/complete`, 'POST');
            if (response?.success) {
                showToast(response.message);
                refreshData();
            } else {
                showToast(response?.error || 'Error', 'error');
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
            if (response?.success) {
                showToast('Tarea actualizada');
                closeModal('editTaskModal');
                refreshData();
            } else {
                showToast(response?.error || 'Error', 'error');
            }
        }

        function confirmDelete(taskId) {
            const task = tasks.find(t => t.id === taskId);
            if (!task) return;
            
            document.getElementById('deleteTaskName').textContent = task.nombre;
            document.getElementById('confirmDeleteBtn').onclick = () => deleteTask(taskId);
            openModal('deleteModal');
        }

        async function deleteTask(taskId) {
            const response = await apiCall(`tasks/${taskId}`, 'DELETE');
            if (response?.success) {
                showToast('Tarea eliminada');
                closeModal('deleteModal');
                refreshData();
            } else {
                showToast(response?.error || 'Error', 'error');
            }
        }

        // Dependencies
        function populateDependencySelects() {
            const pending = tasks.filter(t => t.estado !== 'completada');
            const options = pending.map(t => `<option value="${t.id}">${escapeHtml(t.nombre)}</option>`).join('');
            document.getElementById('depPrerequisite').innerHTML = '<option value="">Seleccionar...</option>' + options;
            document.getElementById('depDependent').innerHTML = '<option value="">Seleccionar...</option>' + options;
        }

        async function addDependency(event) {
            event.preventDefault();
            const origen = parseInt(document.getElementById('depPrerequisite').value);
            const destino = parseInt(document.getElementById('depDependent').value);
            
            if (origen === destino) {
                showToast('Una tarea no puede depender de si misma', 'error');
                return;
            }
            
            const response = await apiCall('dependencies', 'POST', { origen, destino });
            if (response?.success) {
                showToast('Dependencia agregada');
                closeModal('dependencyModal');
                refreshData();
            } else {
                showToast(response?.error || 'Error', 'error');
            }
        }

        async function removeDependency(origen, destino) {
            const response = await apiCall(`dependencies/${origen}/${destino}`, 'DELETE');
            if (response?.success) {
                showToast('Dependencia eliminada');
                refreshData();
            } else {
                showToast(response?.error || 'Error', 'error');
            }
        }

        // Views
        async function viewExecutionOrder() {
            const response = await apiCall('execution-order');
            if (response?.success) {
                showResultModal('Orden Topologico', response.data, 
                    'Este es el orden valido de ejecucion basado en las dependencias (Algoritmo de Kahn).');
            }
        }

        async function viewExecutableTasks() {
            const response = await apiCall('executable-tasks');
            if (response?.success) {
                showResultModal('Tareas Ejecutables', response.data,
                    'Estas tareas pueden completarse ahora (todas sus dependencias estan completas).');
            }
        }

        async function viewNextTask() {
            const response = await apiCall('next-task');
            if (response?.success) {
                if (response.data) {
                    showResultModal('Siguiente Tarea Recomendada', [response.data],
                        'Basado en prioridad y dependencias.');
                } else {
                    showResultModal('Siguiente Tarea', [],
                        'No hay tareas ejecutables disponibles.');
                }
            }
        }

        function showResultModal(title, tasksList, description) {
            document.getElementById('resultModalTitle').textContent = title;
            const content = document.getElementById('resultModalContent');
            
            let html = description ? `<p style="color: var(--text-muted); margin-bottom: 1rem; font-size: 0.85rem;">${description}</p>` : '';
            
            if (!tasksList || tasksList.length === 0) {
                html += '<p style="color: var(--text-muted); text-align: center;">No hay tareas</p>';
            } else {
                html += tasksList.map((task, idx) => `
                    <div class="dep-item">
                        <span style="color: var(--accent); font-weight: 600;">${idx + 1}.</span>
                        <span class="dep-task source">${escapeHtml(task.nombre)}</span>
                        <span class="badge badge-priority">P${task.prioridad}</span>
                    </div>
                `).join('');
            }
            
            content.innerHTML = html;
            openModal('resultModal');
        }

        // Filters
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
            document.getElementById('taskCount').textContent = tasks.length;
        }

        // Utils
        function escapeHtml(text) {
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function formatStatus(status) {
            const map = { 'pendiente': 'Pendiente', 'en_progreso': 'En Progreso', 'completada': 'Completada' };
            return map[status] || status;
        }

        // Close modals on outside click
        document.querySelectorAll('.modal-overlay').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.classList.remove('active');
            });
        });

        // Window resize handler for graph
        window.addEventListener('resize', () => {
            if (tasks.length > 0) renderGraph();
        });

        // Init
        document.addEventListener('DOMContentLoaded', () => {
            refreshData();
            setInterval(refreshData, 60000);
        });
    </script>
</body>
</html>'''

    def handle_api_get(self):
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
                    t_origen = gestor.obtener_tarea(origen)
                    t_destino = gestor.obtener_tarea(destino)
                    if t_origen and t_destino:
                        dep_list.append({
                            'origen': origen,
                            'destino': destino,
                            'origen_nombre': t_origen.nombre,
                            'destino_nombre': t_destino.nombre
                        })
                response = {'success': True, 'data': dep_list}
                
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def handle_api_post(self):
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
            
            # Check for complete endpoint first
            if len(path_parts) >= 3 and path_parts[0] == 'tasks' and path_parts[2] == 'complete':
                task_id = int(path_parts[1])
                
                # Verify dependencies are completed before allowing completion
                tarea = gestor.obtener_tarea(task_id)
                if not tarea:
                    response = {'success': False, 'error': 'Tarea no encontrada'}
                else:
                    # Check if all dependencies are completed
                    deps = gestor.obtener_dependencias(task_id)
                    blocking = [d.nombre for d in deps if d.estado != 'completada']
                    
                    if blocking:
                        response = {
                            'success': False,
                            'error': f'No se puede completar. Primero completa: {", ".join(blocking)}'
                        }
                    else:
                        exito, mensaje, desbloqueadas = gestor.marcar_completada(task_id)
                        response = {
                            'success': exito,
                            'message': mensaje,
                            'data': {'desbloqueadas': desbloqueadas},
                            'error': mensaje if not exito else None
                        }
            
            elif endpoint == 'tasks':
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
                
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.send_json(response)

    def handle_api_put(self):
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
                    # If trying to set status to completed, check dependencies
                    if data.get('estado') == 'completada' and tarea.estado != 'completada':
                        deps = gestor.obtener_dependencias(task_id)
                        blocking = [d.nombre for d in deps if d.estado != 'completada']
                        if blocking:
                            response = {
                                'success': False,
                                'error': f'No se puede completar. Primero completa: {", ".join(blocking)}'
                            }
                            self.send_json(response)
                            return
                    
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
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode('utf-8'))

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': False, 'error': 'Not found'}).encode())

    def send_error_response(self, error_msg):
        self.send_response(500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': False, 'error': error_msg}).encode())

    def log_message(self, format, *args):
        pass


def main():
    port = 8080
    server_address = ('', port)
    
    print("\n" + "="*60)
    print("   TASKFLOW - Gestor de Tareas con Dependencias")
    print("   Universidad Don Bosco - PED Fase 2")
    print("="*60)
    print(f"\n   Servidor: http://localhost:{port}")
    print("   Ctrl+C para detener")
    print("="*60 + "\n")
    
    try:
        httpd = HTTPServer(server_address, ModernWebHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n   Servidor detenido")
        global _gestor_instance
        if _gestor_instance:
            _gestor_instance.cerrar()


if __name__ == "__main__":
    main()
