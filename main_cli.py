"""
Gestor de Tareas con Dependencias
Punto de entrada principal - Versión CLI (compatible con macOS)
"""

import sys
import os

# Agregar el directorio views y src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'views'))

def main():
    """Función principal que inicia la aplicación CLI"""
    try:
        from cli_interface import GestorTareasCLI
        cli = GestorTareasCLI()
        cli.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación CLI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()