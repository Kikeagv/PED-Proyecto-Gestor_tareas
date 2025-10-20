#!/usr/bin/env python3
"""
Script de inicio simple para la interfaz web
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Función principal que inicia el servidor web"""
    try:
        from web_interface_fixed import main as web_main
        print("🌐 Iniciando Interfaz Web del Gestor de Tareas...")
        print("=" * 50)
        print("🎯 Características disponibles:")
        print("   • Visualización completa de tareas")
        print("   • Creación y gestión de tareas")
        print("   • Agregado de dependencias")
        print("   • Ordenamiento topológico")
        print("   • Tareas ejecutables")
        print("   • Estadísticas en tiempo real")
        print("   • Diseño responsive")
        print("=" * 50)
        print("🚀 Iniciando servidor...")

        # Iniciar el servidor web
        web_main()

    except KeyboardInterrupt:
        print("\n\n👋 ¡Gracias por usar el Gestor de Tareas Web!")
        print("📋 Los datos se han guardado en gestor_tareas_web.db")

    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        print("🐛 Por favor reporta este error")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())