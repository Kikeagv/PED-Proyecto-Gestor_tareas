#!/usr/bin/env python3
"""
Script de inicio para la interfaz web moderna
Gestor de Tareas con Dependencias - Fase 2
Universidad Don Bosco - PED
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Funcion principal que inicia el servidor web"""
    try:
        from web_interface_modern import main as web_main
        print("\n" + "=" * 60)
        print("   GESTOR DE TAREAS CON DEPENDENCIAS")
        print("   Universidad Don Bosco - PED Fase 2")
        print("=" * 60)
        print("\n   Caracteristicas:")
        print("   - Interfaz web moderna y responsive")
        print("   - Gestion completa de tareas (CRUD)")
        print("   - Sistema de dependencias con grafos (DAG)")
        print("   - Ordenamiento topologico (Algoritmo de Kahn)")
        print("   - Deteccion automatica de ciclos")
        print("   - Plan diario con colas (FIFO)")
        print("   - Filtrado y busqueda de tareas")
        print("   - Estadisticas en tiempo real")
        print("=" * 60)
        
        web_main()

    except KeyboardInterrupt:
        print("\n\n   Gracias por usar el Gestor de Tareas!")
        print("   Los datos se han guardado en gestor_tareas_web.db\n")

    except Exception as e:
        print(f"\n   Error al iniciar la aplicacion: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())