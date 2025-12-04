#!/usr/bin/env python3
"""
Script para agregar datos de ejemplo de un proyecto de Dashboard Financiero
"""

import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.gestor_proyecto import GestorProyecto

def crear_proyecto_ejemplo(db_path):
    """Crea un proyecto de Dashboard Financiero completo"""
    print(f"💰 Creando proyecto Dashboard Financiero en {db_path}...")

    gestor = GestorProyecto(db_path)

    # Fase 1: Análisis y Planificación Financiera
    print("\n📊 Creando tareas de Análisis Financiero...")

    # Tareas de análisis financiero
    analisis_requisitos_id = gestor.crear_tarea(
        "Análisis de Requisitos Financieros",
        "Levantar y documentar todos los requerimientos para el dashboard financiero: métricas, KPIs, reportes needed",
        5
    )[2]

    investigacion_fuentes_id = gestor.crear_tarea(
        "Investigación de Fuentes de Datos",
        "Identificar y evaluar fuentes de datos: APIs bancarias, sistemas contables, mercados financieros",
        5
    )[2]

    diseno_arquitectura_id = gestor.crear_tarea(
        "Diseño de Arquitectura Financiera",
        "Diseñar arquitectura para procesamiento de datos financieros con seguridad y compliance",
        5
    )[2]

    # Setup inicial
    setup_entorno_id = gestor.crear_tarea(
        "Configuración del Entorno de Desarrollo",
        "Configurar entorno seguro para desarrollo financiero con control de versiones y herramientas",
        4
    )[2]

    bd_financiera_id = gestor.crear_tarea(
        "Diseño de Base de Datos Financiera",
        "Diseñar esquema para transacciones, cuentas, presupuestos, inversiones con auditoría",
        5
    )[2]

    api_financiera_id = gestor.crear_tarea(
        "Diseño de API Financiera",
        "Definir endpoints seguros para operaciones bancarias, reportes y análisis de datos",
        4
    )[2]

    # Fase 2: Backend Financiero
    print("\n💻 Creando tareas de Backend Financiero...")

    # Seguridad y Autenticación Financiera
    auth_segura_id = gestor.crear_tarea(
        "Autenticación Segura Financiera",
        "Implementar autenticación multi-factor, encriptación y compliant con PSD2 para usuarios financieros",
        5
    )[2]

    auth_controller_id = gestor.crear_tarea(
        "Controlador de Sesiones Financieras",
        "Crear endpoints seguros para login/logout con auditoría y tokens JWT de larga duración",
        5
    )[2]

    # Gestión de Cuentas y Permisos
    cuentas_model_id = gestor.crear_tarea(
        "Modelo de Cuentas Financieras",
        "Crear entidades para cuentas bancarias, tarjetas, inversiones y perfiles de usuario financiero",
        5
    )[2]

    cuentas_controller_id = gestor.crear_tarea(
        "CRUD de Cuentas Financieras",
        "Implementar endpoints para gestión completa de cuentas con validaciones y límites de seguridad",
        5
    )[2]

    # Procesamiento de Transacciones
    transacciones_service_id = gestor.crear_tarea(
        "Motor de Transacciones",
        "Implementar motor de procesamiento de transacciones con conciliación y validación financiera",
        5
    )[2]

    validaciones_financieras_id = gestor.crear_tarea(
        "Validaciones y Reglas Financieras",
        "Implementar reglas de negocio: límites, AML, KYC y controles de fraude",
        5
    )[2]

    # Integraciones Financieras
    api_bancaria_id = gestor.crear_tarea(
        "Integración APIs Bancarias",
        "Conectar con APIs de bancos (Plaid, Open Banking) para sincronización de cuentas",
        4
    )[2]

    mercado_datos_id = gestor.crear_tarea(
        "Conexión Mercados Financieros",
        "Integrar con APIs de mercados para precios de acciones, ETFs, criptomonedas en tiempo real",
        4
    )[2]

    # Fase 3: Frontend del Dashboard Financiero
    print("\n🎨 Creando tareas de Frontend Financiero...")

    setup_financiero_id = gestor.crear_tarea(
        "Setup Frontend Financiero",
        "Configurar React/Next.js con Chart.js, D3.js para visualizaciones financieras",
        5
    )[2]

    routing_financiero_id = gestor.crear_tarea(
        "Rutas del Dashboard Financiero",
        "Implementar routing para: overview, cuentas, inversiones, reportes, configuración",
        4
    )[2]

    state_financiero_id = gestor.crear_tarea(
        "Estado de Datos Financieros",
        "Configurar Redux/Redux Toolkit para estado global de datos financieros en caché",
        4
    )[2]

    components_financieros_id = gestor.crear_tarea(
        "Componentes Financieros Base",
        "Crear CurrencyInputs, FinancialCards, DatePickers, Formatos de moneda",
        4
    )[2]

    auth_financiera_ui_id = gestor.crear_tarea(
        "UI Autenticación Financiera",
        "Crear login con 2FA, registro con validación KYC, recuperación segura",
        5
    )[2]

    dashboard_principal_id = gestor.crear_tarea(
        "Dashboard Principal Financiero",
        "Crear overview con balances, gastos vs ingresos, net worth, alerts",
        5
    )[2]

    # Componentes Especializados
    graficos_financieros_id = gestor.crear_tarea(
        "Gráficos Financieros Interactivos",
        "Implementar charts: lineas de tiempo, pie charts de gastos, barras de ingresos",
        4
    )[2]

    cuentas_ui_id = gestor.crear_tarea(
        "Interfaz de Gestión de Cuentas",
        "Crear vistas para cuentas bancarias, tarjetas, balances y movimientos",
        4
    )[2]

    # Fase 4: Testing Financiero
    print("\n🧪 Creando tareas de Testing Financiero...")

    unit_backend_financiero_id = gestor.crear_tarea(
        "Tests Unitarios Backend Financiero",
        "Crear pruebas unitarias para transacciones, validaciones AML y cálculos financieros",
        5
    )[2]

    integration_financiero_id = gestor.crear_tarea(
        "Tests de Integración Financiera",
        "Probar integración con APIs bancarias y sincronización de datos financieros",
        5
    )[2]

    security_testing_id = gestor.crear_tarea(
        "Tests de Seguridad Financiera",
        "Pentesting, auditoría de encriptación y tests de cumplimiento PSD2/GDPR",
        5
    )[2]

    unit_frontend_financiero_id = gestor.crear_tarea(
        "Tests Unitarios Frontend Financiero",
        "Probar componentes financieros: formatos de moneda, gráficos, validaciones",
        4
    )[2]

    e2e_financiero_id = gestor.crear_tarea(
        "Tests End-to-End Financieros",
        "Probar flujos completos: onboarding KYC, transacciones, reportes mensuales",
        5
    )[2]

    # Fase 5: Despliegue Seguro Financiero
    print("\n🚀 Creando tareas de Despliegue Financiero...")

    docker_financiero_id = gestor.crear_tarea(
        "Containerización Segura Financiera",
        "Crear Dockerfiles con security hardening y secrets management para finanzas",
        5
    )[2]

    ci_cd_financiero_id = gestor.crear_tarea(
        "Pipeline CI/CD Financiero",
        "Configurar pipelines con escaneo de seguridad, tests AML y despliegue gradual",
        5
    )[2]

    staging_financiero_id = gestor.crear_tarea(
        "Ambiente Staging Financiero",
        "Configurar ambiente seguro con datos anonimizados y monitoreo real",
        4
    )[2]

    deploy_production_financiero_id = gestor.crear_tarea(
        "Despliegue Producción Financiera",
        "Despliegue con blue-green deployment, rollback automático y certificaciones",
        5
    )[2]

    monitoring_financiero_id = gestor.crear_tarea(
        "Monitoreo y Alertas Financieras",
        "Implementar: fraude detection, anomaly detection, audits logs y alertas regulatorias",
        4
    )[2]

    # Fase 6: Documentación Financiera y Cumplimiento
    print("\n📚 Creando tareas de Documentación Financiera...")

    api_docs_financieros_id = gestor.crear_tarea(
        "Documentación API Financiera",
        "Crear API docs con OpenAPI/Swagger incluyendo schemas de transacciones y compliance",
        4
    )[2]

    compliance_docs_id = gestor.crear_tarea(
        "Documentación de Cumplimiento",
        "Documentar políticas KYC, AML, GDPR y procedimientos regulatorios financieros",
        5
    )[2]

    manual_financiero_id = gestor.crear_tarea(
        "Manual de Usuario Financiero",
        "Crear guías de onboarding KYC, configuración de cuentas y uso de dashboard",
        4
    )[2]

    deployment_financiero_guide_id = gestor.crear_tarea(
        "Guía Despliegue Seguro",
        "Documentar proceso de instalación segura, configuración de certificados y auditorías",
        4
    )[2]

    # Agregar dependencias financieras realistas
    print("\n🔗 Creando dependencias financieras entre tareas...")

    # Dependencias de Análisis y Arquitectura
    gestor.agregar_dependencia(analisis_requisitos_id, diseno_arquitectura_id)  
    gestor.agregar_dependencia(analisis_requisitos_id, bd_financiera_id)         
    gestor.agregar_dependencia(analisis_requisitos_id, api_financiera_id)        
    gestor.agregar_dependencia(investigacion_fuentes_id, diseno_arquitectura_id)  
    gestor.agregar_dependencia(diseno_arquitectura_id, setup_entorno_id)    

    # Dependencias Backend Financiero
    gestor.agregar_dependencia(diseno_arquitectura_id, auth_segura_id)
    gestor.agregar_dependencia(diseno_arquitectura_id, cuentas_model_id)
    gestor.agregar_dependencia(diseno_arquitectura_id, transacciones_service_id)
    gestor.agregar_dependencia(api_financiera_id, auth_controller_id)
    gestor.agregar_dependencia(api_financiera_id, cuentas_controller_id)
    gestor.agregar_dependencia(bd_financiera_id, auth_segura_id)
    gestor.agregar_dependencia(bd_financiera_id, cuentas_model_id)
    gestor.agregar_dependencia(auth_segura_id, auth_controller_id)
    gestor.agregar_dependencia(cuentas_model_id, cuentas_controller_id)
    gestor.agregar_dependencia(transacciones_service_id, validaciones_financieras_id)

    # Dependencias de Integraciones Financieras
    gestor.agregar_dependencia(diseno_arquitectura_id, api_bancaria_id)
    gestor.agregar_dependencia(diseno_arquitectura_id, mercado_datos_id)

    # Dependencias Frontend Financiero
    gestor.agregar_dependencia(setup_entorno_id, setup_financiero_id)
    gestor.agregar_dependencia(api_financiera_id, routing_financiero_id)
    gestor.agregar_dependencia(diseno_arquitectura_id, state_financiero_id)
    gestor.agregar_dependencia(setup_financiero_id, components_financieros_id)
    gestor.agregar_dependencia(auth_controller_id, auth_financiera_ui_id)
    gestor.agregar_dependencia(transacciones_service_id, dashboard_principal_id)
    gestor.agregar_dependencia(cuentas_controller_id, cuentas_ui_id)
    gestor.agregar_dependencia(components_financieros_id, auth_financiera_ui_id)
    gestor.agregar_dependencia(components_financieros_id, graficos_financieros_id)

    # Dependencias Testing Financiero
    gestor.agregar_dependencia(auth_controller_id, unit_backend_financiero_id)
    gestor.agregar_dependencia(cuentas_controller_id, unit_backend_financiero_id)
    gestor.agregar_dependencia(transacciones_service_id, unit_backend_financiero_id)
    gestor.agregar_dependencia(unit_backend_financiero_id, integration_financiero_id)
    gestor.agregar_dependencia(auth_segura_id, security_testing_id)
    gestor.agregar_dependencia(components_financieros_id, unit_frontend_financiero_id)
    gestor.agregar_dependencia(dashboard_principal_id, e2e_financiero_id)

    # Dependencias Despliegue Financiero
    gestor.agregar_dependencia(unit_backend_financiero_id, docker_financiero_id)
    gestor.agregar_dependencia(unit_frontend_financiero_id, docker_financiero_id)
    gestor.agregar_dependencia(security_testing_id, docker_financiero_id)
    gestor.agregar_dependencia(docker_financiero_id, ci_cd_financiero_id)
    gestor.agregar_dependencia(ci_cd_financiero_id, staging_financiero_id)
    gestor.agregar_dependencia(staging_financiero_id, deploy_production_financiero_id)
    gestor.agregar_dependencia(deploy_production_financiero_id, monitoring_financiero_id)

    # Dependencias Documentación Financiera
    gestor.agregar_dependencia(api_financiera_id, api_docs_financieros_id)
    gestor.agregar_dependencia(compliance_docs_id, manual_financiero_id)
    gestor.agregar_dependencia(ci_cd_financiero_id, deployment_financiero_guide_id)
    gestor.agregar_dependencia(transacciones_service_id, compliance_docs_id)

    # Marcar algunas tareas como ya completadas para demostrar el flujo
    print("\n✅ Marcando algunas tareas financieras como completadas...")

    tasks_to_complete = [
        analisis_requisitos_id, investigacion_fuentes_id, diseno_arquitectura_id, 
        setup_entorno_id, bd_financiera_id, api_financiera_id,
        setup_financiero_id, components_financieros_id
    ]

    for task_id in tasks_to_complete:
        gestor.marcar_completada(task_id)

    # Actualizar algunas tareas con fechas límite financieras realistas
    print("\n📅 Agregando fechas límite financieras a tareas clave...")

    # Establecer fechas límite realistas con horizonte temporal financiero
    now = datetime.now()

    # Fases tempranas - deadline ya pasado para simular progreso inicial
    for task_id in [analisis_requisitos_id, investigacion_fuentes_id, diseno_arquitectura_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = now - timedelta(days=15)
        gestor.actualizar_tarea(task)

    # Fases de desarrollo financiero - deadlines próximos (semanal)
    deadline_week1 = now + timedelta(days=7)
    for task_id in [auth_segura_id, cuentas_model_id, transacciones_service_id, routing_financiero_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_week1
        gestor.actualizar_tarea(task)

    # Fases de integración y frontend - deadlines en 2 semanas
    deadline_week2 = now + timedelta(days=14)
    for task_id in [auth_controller_id, cuentas_controller_id, dashboard_principal_id, unit_backend_financiero_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_week2
        gestor.actualizar_tarea(task)

    # Fases de testing y despliegue - deadlines en 3-4 semanas
    deadline_week3 = now + timedelta(days=21)
    for task_id in [integration_financiero_id, security_testing_id, docker_financiero_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_week3
        gestor.actualizar_tarea(task)

    # Fases finales y producción - deadlines en 1 mes
    deadline_month = now + timedelta(days=30)
    for task_id in [deploy_production_financiero_id, monitoring_financiero_id, api_docs_financieros_id]:
        task = gestor.obtener_tarea(task_id)
        task.fecha_limite = deadline_month
        gestor.actualizar_tarea(task)

    gestor.cerrar()
    print(f"\n💰 ¡Proyecto Dashboard Financiero creado exitosamente en {db_path}!")
    return True

def main():
    """Función principal"""
    print("💰 CREANDO PROYECTO DASHBOARD FINANCIERO DE EJEMPLO")
    print("=" * 60)

    databases = [
        "gestor_tareas.db",           # Para GUI
        "gestor_tareas_cli.db",       # Para CLI
        "gestor_tareas_web.db"        # Para Web
    ]

    for db_path in databases:
        try:
            crear_proyecto_ejemplo(db_path)
            print(f"✅ Base de datos '{db_path}' creada con dashboard financiero")
        except Exception as e:
            print(f"❌ Error creando {db_path}: {e}")
            return False

    print("\n" + "=" * 60)
    print("💰 ¡TODAS LAS BASES DE DATOS HAN SIDO INICIALIZADAS CON DASHBOARD FINANCIERO!")
    print("\n📊 RESUMEN DEL PROYECTO FINANCIERO CREADO:")
    print("   • 26+ tareas especializadas de finanzas y tecnología")
    print("   • 6 fases financieras (Análisis, Backend, Frontend, Testing, Despliegue, Compliance)")
    print("   • 35+ dependencias financieras realistas")
    print("   • 8 tareas ya completadas para demostrar flujo de trabajo")
    print("   • Fechas límite financieras configuradas")
    print("   • Seguridad y cumplimiento regulatorio integrado")
    print("\n💡 CARACTERÍSTICAS DEL DASHBOARD FINANCIERO:")
    print("   • APIs bancarias y Open Banking")
    print("   • KYC, AML y PSD2 compliance") 
    print("   • Visualizaciones financieras interactivas")
    print("   • Testing de seguridad financiera")
    print("   • Despliegue seguro con auditoría")
    print("\n🚀 YA PUEDES USAR CUALQUIER INTERFAZ PARA PROBAR:")
    print("   • Web: python3 start_web.py (recomendado)")
    print("   • CLI: python3 main_cli.py") 
    print("   • GUI: python3 main.py")

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)