#!/usr/bin/env python3
"""
Script para agregar datos de ejemplo de un proyecto de desarrollo de software
"""

import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.gestor_proyecto import GestorProyecto

def crear_proyecto_ejemplo(db_path):
    """Crea un proyecto de desarrollo de software completo"""
    print(f"🏗️  Creando proyecto de ejemplo en {db_path}...")

    gestor = GestorProyecto(db_path)

    # Fase de Inicio y Planificación
    print("\n📋 Creando tareas de la Fase de Inicio...")

    # Tareas de planificación
    analisis_id = gestor.crear_tarea(
        "Análisis de Requisitos",
        "Levantar y documentar todos los requisitos funcionales y no funcionales del sistema",
        5
    )[2]

    investigacion_id = gestor.crear_tarea(
        "Investigación de Tecnologías",
        "Investigar y evaluar diferentes tecnologías, frameworks y herramientas para el proyecto",
        5
    )[2]

    diseño_arq_id = gestor.crear_tarea(
        "Diseño de Arquitectura",
        "Diseñar la arquitectura general del sistema, patrones de diseño y componentes principales",
        5
    )[2]

    # Tareas de configuración
    setup_id = gestor.crear_tarea(
        "Configuración del Entorno",
        "Configurar entorno de desarrollo, control de versiones y herramientas de trabajo",
        4
    )[2]

    bd_id = gestor.crear_tarea(
        "Diseño de Base de Datos",
        "Diseñar el esquema de base de datos, relaciones normalización",
        5
    )[2]

    api_id = gestor.crear_tarea(
        "Diseño de API REST",
        "Definir endpoints, formatos de request/response y documentación de API",
        4
    )[2]

    # Fase de Desarrollo - Backend
    print("\n💻 Creando tareas de Desarrollo Backend...")

    # Autenticación y Seguridad
    auth_model_id = gestor.crear_tarea(
        "Modelo de Autenticación",
        "Implementar sistema de registro, login y gestión de usuarios con JWT",
        5
    )[2]

    auth_controller_id = gestor.crear_tarea(
        "Controlador de Autenticación",
        "Crear endpoints para registro, login, logout y gestión de sesión",
        5
    )[2]

    # Gestión de Usuarios y Roles
    user_model_id = gestor.crear_tarea(
        "Modelo de Usuarios y Roles",
        "Crear entidades de usuario, perfil y roles con permisos",
        4
    )[2]

    user_controller_id = gestor.crear_tarea(
        "CRUD de Usuarios",
        "Implementar endpoints completos para gestión de usuarios",
        4
    )[2]

    # Lógica de Negocio Principal
    service_core_id = gestor.crear_tarea(
        "Servicios de Negocio",
        "Implementar la lógica de negocio principal del sistema",
        5
    )[2]

    validations_id = gestor.crear_tarea(
        "Validaciones y Reglas",
        "Implementar validaciones de datos y reglas de negocio",
        4
    )[2]

    # Integraciones
    email_id = gestor.crear_tarea(
        "Servicio de Correo Electrónico",
        "Implementar envío de correos transaccionales y notificaciones",
        3
    )[2]

    storage_id = gestor.crear_tarea(
        "Servicio de Almacenamiento",
        "Implementar manejo de archivos, imágenes y documentos",
        3
    )[2]

    # Fase de Desarrollo - Frontend
    print("\n🎨 Creando tareas de Desarrollo Frontend...")

    setup_frontend_id = gestor.crear_tarea(
        "Setup del Proyecto Frontend",
        "Configurar React/Vue, webpack, babel y dependencias iniciales",
        5
    )[2]

    routing_id = gestor.crear_tarea(
        "Configuración de Rutas",
        "Implementar sistema de routing de la aplicación",
        4
    )[2]

    state_management_id = gestor.crear_tarea(
        "Gestión de Estado",
        "Configurar Redux/Vuex para gestión de estado global",
        4
    )[2]

    components_base_id = gestor.crear_tarea(
        "Componentes Base",
        "Crear componentes reutilizables (Header, Footer, Buttons, etc)",
        4
    )[2]

    auth_ui_id = gestor.crear_tarea(
        "Interfaz de Autenticación",
        "Crear formularios de login, registro y gestión de perfil",
        5
    )[2]

    dashboard_id = gestor.crear_tarea(
        "Dashboard Principal",
        "Crear vista principal del sistema con métricas y navegación",
        5
    )[2]

    # Formularios CRUD
    user_forms_id = gestor.crear_tarea(
        "Formularios de CRUD de Usuarios",
        "Crear interfaces para gestión completa de usuarios",
        4
    )[2]

    # Fase de Testing
    print("\n🧪 Creando tareas de Testing...")

    unit_backend_id = gestor.crear_tarea(
        "Tests Unitarios Backend",
        "Crear pruebas unitarias para servicios y controladores",
        4
    )[2]

    integration_backend_id = gestor.crear_tarea(
        "Tests de Integración Backend",
        "Crear pruebas de integración entre componentes backend",
        4
    )[2]

    unit_frontend_id = gestor.crear_tarea(
        "Tests Unitarios Frontend",
        "Crear pruebas unitarias para componentes y utilidades",
        3
    )[2]

    e2e_id = gestor.crear_tarea(
        "Tests End-to-End",
        "Crear pruebas automatizadas de flujos completos del sistema",
        4
    )[2]

    # Fase de Despliegue
    print("\n🚀 Creando tareas de Despliegue...")

    docker_id = gestor.crear_tarea(
        "Containerización con Docker",
        "Crear Dockerfiles y docker-compose para la aplicación",
        5
    )[2]

    ci_cd_id = gestor.crear_tarea(
        "Configuración CI/CD",
        "Configurar pipelines automáticos de integración y despliegue",
        4
    )[2]

    deploy_staging_id = gestor.crear_tarea(
        "Despliegue en Staging",
        "Configurar y desplegar ambiente de pruebas",
        4
    )[2]

    deploy_production_id = gestor.crear_tarea(
        "Despliegue en Producción",
        "Despliegue final del sistema en ambiente productivo",
        5
    )[2]

    monitoring_id = gestor.crear_tarea(
        "Configuración de Monitoreo",
        "Implementar logging, métricas y alertas del sistema",
        3
    )[2]

    # Fase de Documentación y Capacitación
    print("\n📚 Creando tareas de Documentación...")

    api_docs_id = gestor.crear_tarea(
        "Documentación de API",
        "Crear documentación técnica y Swagger/OpenAPI de la API",
        4
    )[2]

    user_manual_id = gestor.crear_tarea(
        "Manual de Usuario",
        "Crear guías y tutoriales para usuarios finales",
        3
    )[2]

    deployment_guide_id = gestor.crear_tarea(
        "Guía de Despliegue",
        "Documentar proceso de instalación y configuración",
        4
    )[2]

    # Agregar dependencias entre tareas

    print("\n🔗 Creando dependencias entre tareas...")

    # Dependencias de la fase de planificación
    gestor.agregar_dependencia(analisis_id, diseño_arq_id)  # Análisis -> Arquitectura
    gestor.agregar_dependencia(analisis_id, bd_id)         # Análisis -> BD
    gestor.agregar_dependencia(analisis_id, api_id)        # Análisis -> API
    gestor.agregar_dependencia(investigacion_id, diseño_arq_id)  # Investigación -> Arquitectura
    gestor.agregar_dependencia(diseño_arq_id, setup_id)    # Arquitectura -> Setup

    # Dependencias del Backend
    gestor.agregar_dependencia(diseño_arq_id, auth_model_id)
    gestor.agregar_dependencia(diseño_arq_id, user_model_id)
    gestor.agregar_dependencia(diseño_arq_id, service_core_id)
    gestor.agregar_dependencia(api_id, auth_controller_id)
    gestor.agregar_dependencia(api_id, user_controller_id)
    gestor.agregar_dependencia(bd_id, auth_model_id)
    gestor.agregar_dependencia(bd_id, user_model_id)
    gestor.agregar_dependencia(auth_model_id, auth_controller_id)
    gestor.agregar_dependencia(user_model_id, user_controller_id)
    gestor.agregar_dependencia(service_core_id, validations_id)

    # Dependencias de Integraciones
    gestor.agregar_dependencia(diseño_arq_id, email_id)
    gestor.agregar_dependencia(diseño_arq_id, storage_id)

    # Dependencias del Frontend
    gestor.agregar_dependencia(setup_id, setup_frontend_id)
    gestor.agregar_dependencia(api_id, routing_id)
    gestor.agregar_dependencia(diseño_arq_id, state_management_id)
    gestor.agregar_dependencia(setup_frontend_id, components_base_id)
    gestor.agregar_dependencia(auth_controller_id, auth_ui_id)
    gestor.agregar_dependencia(service_core_id, dashboard_id)
    gestor.agregar_dependencia(user_controller_id, user_forms_id)
    gestor.agregar_dependencia(components_base_id, auth_ui_id)

    # Dependencias de Testing
    gestor.agregar_dependencia(auth_controller_id, unit_backend_id)
    gestor.agregar_dependencia(user_controller_id, unit_backend_id)
    gestor.agregar_dependencia(service_core_id, unit_backend_id)
    gestor.agregar_dependencia(unit_backend_id, integration_backend_id)
    gestor.agregar_dependencia(components_base_id, unit_frontend_id)
    gestor.agregar_dependencia(components_base_id, e2e_id)

    # Dependencias de Despliegue
    gestor.agregar_dependencia(unit_backend_id, docker_id)
    gestor.agregar_dependencia(unit_frontend_id, docker_id)
    gestor.agregar_dependencia(docker_id, ci_cd_id)
    gestor.agregar_dependencia(ci_cd_id, deploy_staging_id)
    gestor.agregar_dependencia(deploy_staging_id, deploy_production_id)
    gestor.agregar_dependencia(deploy_production_id, monitoring_id)

    # Dependencias de Documentación
    gestor.agregar_dependencia(api_id, api_docs_id)
    gestor.agregar_dependencia(components_base_id, user_manual_id)
    gestor.agregar_dependencia(ci_cd_id, deployment_guide_id)

    # Marcar algunas tareas como ya completadas para demostrar el flujo
    print("\n✅ Marcando algunas tareas como completadas...")

    tasks_to_complete = [
        analisis_id, investigacion_id, diseño_arq_id, setup_id, bd_id, api_id,
        setup_frontend_id, components_base_id
    ]

    for task_id in tasks_to_complete:
        gestor.marcar_completada(task_id)

    # Actualizar algunas tareas con fechas límite
    print("\n📅 Agregando fechas límite a tareas clave...")

    # Establecer fechas límite realistas
    now = datetime.now()

    # Fases tempranas - deadline ya pasado para simular progreso
    for task_id in [analisis_id, investigacion_id, diseño_arq_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = now - timedelta(days=10)
        gestor.actualizar_tarea(task)

    # Fases actuales - deadlines próxim
    deadline_week1 = now + timedelta(days=7)
    for task_id in [auth_model_id, user_model_id, service_core_id, routing_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_week1
        gestor.actualizar_tarea(task)

    # Fases medias - deadlines en 2 semanas
    deadline_week2 = now + timedelta(days=14)
    for task_id in [auth_controller_id, user_controller_id, dashboard_id, unit_backend_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_week2
        gestor.actualizar_tarea(task)

    # Fases finales - deadlines en 1 mes
    deadline_month = now + timedelta(days=30)
    for task_id in [deploy_production_id, monitoring_id, api_docs_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_month
        gestor.actualizar_tarea(task)

    gestor.cerrar()
    print(f"\n🎉 ¡Proyecto de ejemplo creado exitosamente en {db_path}!")
    return True

def main():
    """Función principal"""
    print("🏗️  CREANDO PROYECTO DE DESARROLLO DE SOFTWARE DE EJEMPLO")
    print("=" * 60)

    databases = [
        "gestor_tareas.db",           # Para GUI
        "gestor_tareas_cli.db",       # Para CLI
        "gestor_tareas_web.db"        # Para Web
    ]

    for db_path in databases:
        try:
            crear_proyecto_ejemplo(db_path)
            print(f"✅ Base de datos '{db_path}' creada con datos de ejemplo")
        except Exception as e:
            print(f"❌ Error creando {db_path}: {e}")
            return False

    print("\n" + "=" * 60)
    print("🎉 ¡TODAS LAS BASES DE DATOS HAN SIDO INICIALIZADAS CON DATOS DE EJEMPLO!")
    print("\n📋 RESUMEN DEL PROYECTO CREADO:")
    print("   • 30 tareas de desarrollo de software")
    print("   • 5 fases del proyecto (Inicio, Desarrollo, Testing, Despliegue, Documentación)")
    print("   • +30 dependencias entre tareas")
    print("   • 8 tareas ya completadas para demostrar flujo de trabajo")
    print("   • Fechas límite configuradas")
    print("\n🚀 YA PUEDES USAR CUALQUIER INTERFAZ:")
    print("   • Web: python3 web_interface.py (recomendado)")
    print("   • CLI: python3 main_cli.py")
    print("   • GUI: python3 main.py")

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)