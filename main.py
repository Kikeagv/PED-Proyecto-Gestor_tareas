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