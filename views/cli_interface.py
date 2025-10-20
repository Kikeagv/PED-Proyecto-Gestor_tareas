"""
Interfaz de Línea de Comandos
Alternativa sin GUI para compatibilidad con macOS
"""

import os
import sys
from datetime import datetime
from typing import List, Optional
from controllers.gestor_proyecto import GestorProyecto

class GestorTareasCLI:
    """Interfaz de línea de comandos para el gestor de tareas"""

    def __init__(self, db_path: str = "gestor_tareas_cli.db"):
        """Inicializa la CLI"""
        self.gestor = GestorProyecto(db_path)
        self.limpiar_pantalla = 'clear' if os.name == 'posix' else 'cls'

    def limpiar(self):
        """Limpia la pantalla"""
        os.system(self.limpiar_pantalla)

    def mostrar_titulo(self):
        """Muestra el título de la aplicación"""
        print("=" * 60)
        print("📋 GESTOR DE TAREAS CON DEPENDENCIAS")
        print("Versión CLI - Compatible con cualquier macOS")
        print("=" * 60)
        print()

    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("🎯 MENÚ PRINCIPAL")
        print("-" * 30)
        print("1. ➕ Crear nueva tarea")
        print("2. 📋 Ver todas las tareas")
        print("3. 🔗 Agregar dependencia")
        print("4. 📊 Ver orden de ejecución")
        print("5. 🎯 Ver tareas ejecutables")
        print("6. ⭐ Obtener siguiente tarea")
        print("7. ✅ Marcar tarea como completada")
        print("8. 📈 Ver estadísticas del proyecto")
        print("9. 🗑️  Eliminar tarea")
        print("10. 💾 Plan diario")
        print("0. 🚪 Salir")
        print()

    def mostrar_tareas(self, tareas: List):
        """Muestra una lista de tareas"""
        if not tareas:
            print("ℹ️  No hay tareas para mostrar.")
            return

        print("\n" + "=" * 80)
        print(f"{'ID':<4} {'NOMBRE':<25} {'ESTADO':<12} {'PRIORIDAD':<10} {'LÍMITE':<12}")
        print("=" * 80)

        for tarea in tareas:
            estado_emoji = {
                'pendiente': '⏳',
                'en_progreso': '🔄',
                'completada': '✅'
            }.get(tarea.estado, '❓')

            fecha_limite = ""
            if tarea.fecha_limite:
                fecha_limite = tarea.fecha_limite.strftime("%d/%m/%Y")

            print(f"{tarea.id:<4} {tarea.nombre[:24]:25} {estado_emoji} {tarea.estado:<10} {tarea.prioridad:<10} {fecha_limite:<12}")

        print("=" * 80)

    def crear_tarea(self):
        """Crea una nueva tarea vía CLI"""
        print("\n➕ CREAR NUEVA TAREA")
        print("-" * 30)

        nombre = input("Nombre de la tarea: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío.")
            input("Presione Enter para continuar...")
            return

        descripcion = input("Descripción (opcional): ").strip()

        try:
            prioridad = int(input("Prioridad (1-5, por defecto 3): ") or "3")
            if not 1 <= prioridad <= 5:
                print("❌ La prioridad debe estar entre 1 y 5.")
                input("Presione Enter para continuar...")
                return
        except ValueError:
            print("❌ Prioridad inválida. Usando valor por defecto (3).")
            prioridad = 3

        exito, mensaje, tarea_id = self.gestor.crear_tarea(nombre, descripcion, prioridad)

        if exito:
            print(f"✅ {mensaje}")
            print(f"📝 ID de la tarea creada: {tarea_id}")
        else:
            print(f"❌ Error: {mensaje}")

        input("Presione Enter para continuar...")

    def ver_todas_tareas(self):
        """Muestra todas las tareas"""
        self.limpiar()
        self.mostrar_titulo()
        print("📋 LISTA COMPLETA DE TAREAS")
        print("-" * 30)

        tareas = self.gestor.obtener_todas_tareas()
        self.mostrar_tareas(tareas)

        input("\nPresione Enter para continuar...")

    def agregar_dependencia(self):
        """Agrega una dependencia entre tareas"""
        self.limpiar()
        self.mostrar_titulo()
        print("🔗 AGREGAR DEPENDENCIA")
        print("-" * 30)

        tareas = self.gestor.obtener_todas_tareas()
        if len(tareas) < 2:
            print("❌ Se necesitan al menos 2 tareas para crear dependencias.")
            input("Presione Enter para continuar...")
            return

        print("Tareas disponibles:")
        self.mostrar_tareas(tareas)

        try:
            origen_id = int(input("\nID de la tarea prerequisito: "))
            destino_id = int(input("ID de la tarea dependiente: "))

            exito, mensaje = self.gestor.agregar_dependencia(origen_id, destino_id)

            if exito:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ Error: {mensaje}")

        except ValueError:
            print("❌ IDs inválidos. Debe ingresar números enteros.")

        input("Presione Enter para continuar...")

    def ver_orden_ejecucion(self):
        """Muestra el orden de ejecución (topológico)"""
        self.limpiar()
        self.mostrar_titulo()
        print("📊 ORDEN DE EJECUCIÓN VÁLIDO")
        print("-" * 30)

        resultado = self.gestor.calcular_orden_ejecucion()

        if resultado is None:
            print("❌ Hay ciclos en las dependencias del proyecto.")
        elif not resultado:
            print("ℹ️  No hay tareas pendientes.")
        else:
            print("\n📋 ORDEN SUGERIDO:")
            print("=" * 50)
            for i, tarea in enumerate(resultado, 1):
                prioridad_icon = "🔥" if tarea.prioridad == 5 else "⭐" if tarea.prioridad >= 3 else "📋"
                print(f"{i}ª. {prioridad_icon} {tarea.nombre} (Prioridad: {tarea.prioridad})")
                if tarea.descripcion:
                    print(f"     📝 {tarea.descripcion[:60]}...")
            print("=" * 50)

        input("\nPresione Enter para continuar...")

    def ver_tareas_ejecutables(self):
        """Muestra las tareas ejecutables ahora"""
        self.limpiar()
        self.mostrar_titulo()
        print("🎯 TAREAS EJECUTABLES AHORA")
        print("-" * 30)

        ejecutables = self.gestor.obtener_tareas_ejecutables()

        if not ejecutables:
            print("ℹ️  No hay tareas ejecutables en este momento.")
            print("\nEsto puede suceder porque:")
            print("• Hay dependencias pendientes")
            print("• Todas las tareas están completadas")
        else:
            print(f"\n📅 Total de tareas disponibles: {len(ejecutables)}")
            print("=" * 60)
            for i, tarea in enumerate(ejecutables, 1):
                prioridad_icon = "🔥" if tarea.prioridad == 5 else "⭐" if tarea.prioridad >= 3 else "📋"
                print(f"{i}ª. {prioridad_icon} {tarea.nombre} (Prioridad: {tarea.prioridad}/5)")
                if tarea.fecha_limite:
                    print(f"     📅 Límite: {tarea.fecha_limite.strftime('%d/%m/%Y')}")
            print("=" * 60)

        input("\nPresione Enter para continuar...")

    def obtener_siguiente_tarea(self):
        """Muestra la siguiente tarea recomendada"""
        self.limpiar()
        self.mostrar_titulo()
        print("⭐ SIGUIENTE TAREA RECOMENDADA")
        print("-" * 30)

        siguiente = self.gestor.obtener_siguiente_tarea()

        if not siguiente:
            print("ℹ️  No hay tareas disponibles para ejecutar.")
            print("\nRevisa el estado de tus dependencias.")
        else:
            print("\n🎯 TU PRÓXIMA TAREA:")
            print("=" * 50)
            print(f"📝 {siguiente.nombre}")

            if siguiente.descripcion:
                print(f"📋 {siguiente.descripcion}")

            print(f"⭐ Prioridad: {siguiente.prioridad}/5")

            if siguiente.fecha_limite:
                print(f"📅 Límite: {siguiente.fecha_limite.strftime('%d/%m/%Y')}")

            if siguiente.estimacion_horas > 0:
                print(f"⏱️  Tiempo estimado: {siguiente.estimacion_horas} horas")

            print("=" * 50)

        input("\nPresione Enter para continuar...")

    def marcar_completada(self):
        """Marca una tarea como completada"""
        self.limpiar()
        self.mostrar_titulo()
        print("✅ MARCAR TAREA COMO COMPLETADA")
        print("-" * 30)

        # Mostrar tareas pendientes
        tareas = self.gestor.obtener_todas_tareas()
        pendientes = [t for t in tareas if t.estado != 'completada']

        if not pendientes:
            print("ℹ️  No hay tareas pendientes por completar.")
            input("Presione Enter para continuar...")
            return

        print("Tareas pendientes:")
        self.mostrar_tareas(pendientes)

        try:
            tarea_id = int(input("\nID de la tarea a completar: "))

            # Verificar que exista y no esté completada
            tarea = self.gestor.obtener_tarea(tarea_id)
            if not tarea:
                print("❌ Tarea no encontrada.")
                input("Presione Enter para continuar...")
                return

            if tarea.estado == 'completada':
                print("ℹ️  Esta tarea ya está completada.")
                input("Presione Enter para continuar...")
                return

            confirmacion = input(f"¿Completar '{tarea.nombre}'? (s/N): ").strip().lower()
            if confirmacion in ['s', 'si', 'sí']:
                exito, mensaje, tareas_desbloqueadas = self.gestor.marcar_completada(tarea_id)

                if exito:
                    print(f"✅ {mensaje}")

                    if tareas_desbloqueadas:
                        print("\n🎉 ¡Tareas desbloqueadas!")
                        for tid in tareas_desbloqueadas:
                            t = self.gestor.obtener_tarea(tid)
                            if t:
                                print(f"   📋 {t.nombre}")
                else:
                    print(f"❌ Error: {mensaje}")
            else:
                print("❌ Operación cancelada.")

        except ValueError:
            print("❌ ID inválido. Debe ingresar un número entero.")

        input("Presione Enter para continuar...")

    def ver_estadisticas(self):
        """Muestra estadísticas del proyecto"""
        self.limpiar()
        self.mostrar_titulo()
        print("📈 ESTADÍSTICAS DEL PROYECTO")
        print("-" * 30)

        stats = self.gestor.obtener_estadisticas()

        print(f"📋 Total de Tareas: {stats['total_tareas']}")
        print(f"✅ Completadas: {stats['completadas']}")
        print(f"🔄 En Progreso: {stats['en_progreso']}")
        print(f"⏳ Pendientes: {stats['pendientes']}")
        print(f"🎯 Ejecutables Ahora: {stats['ejecutables']}")
        print(f"🔗 Total de Dependencias: {stats['total_dependencias']}")
        print(f"📈 Progreso del Proyecto: {stats['porcentaje_completado']:.1f}%")

        # Barra de progreso
        progreso = stats['porcentaje_completado'] / 100
        bar_length = 30
        filled_length = int(bar_length * progreso)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\n📊 Progreso: [{bar}] {stats['porcentaje_completado']:.1f}%")

        input("\nPresione Enter para continuar...")

    def eliminar_tarea(self):
        """Elimina una tarea"""
        self.limpiar()
        self.mostrar_titulo()
        print("🗑️  ELIMINAR TAREA")
        print("-" * 30)

        tareas = self.gestor.obtener_todas_tareas()
        if not tareas:
            print("ℹ️  No hay tareas para eliminar.")
            input("Presione Enter para continuar...")
            return

        print("Tareas disponibles:")
        self.mostrar_tareas(tareas)

        try:
            tarea_id = int(input("\nID de la tarea a eliminar: "))
            tarea = self.gestor.obtener_tarea(tarea_id)

            if not tarea:
                print("❌ Tarea no encontrada.")
                input("Presione Enter para continuar...")
                return

            confirmacion = input(f"¿Eliminar '{tarea.nombre}'? Esta acción no se puede deshacer. (s/N): ").strip().lower()
            if confirmacion in ['s', 'si', 'sí']:
                exito, mensaje = self.gestor.eliminar_tarea(tarea_id)

                if exito:
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ Error: {mensaje}")
            else:
                print("❌ Operación cancelada.")

        except ValueError:
            print("❌ ID inválido. Debe ingresar un número entero.")

        input("Presione Enter para continuar...")

    def ver_plan_diario(self):
        """Muestra el plan diario"""
        self.limpiar()
        self.mostrar_titulo()
        print("💾 PLAN DIARIO")
        print("-" * 30)

        plan = self.gestor.obtener_plan_diario()

        if not plan:
            print("ℹ️  No hay tareas en el plan diario.")
            print("Puedes agregar tareas ejecutables al plan diario.")
        else:
            print(f"\n📅 Plan diario ({len(plan)} tareas):")
            print("=" * 50)
            for i, tarea in enumerate(plan, 1):
                pri_icon = "🔥" if tarea.prioridad == 5 else "⭐" if tarea.prioridad >= 3 else "📋"
                print(f"{i}ª. {pri_icon} {tarea.nombre}")
                if tarea.descripcion:
                    print(f"     📝 {tarea.description[:40]}...")
            print("=" * 50)

        input("\nPresione Enter para continuar...")

    def ejecutar(self):
        """Ejecuta el bucle principal de la CLI"""
        while True:
            try:
                self.limpiar()
                self.mostrar_titulo()
                self.mostrar_menu()

                opcion = input("Seleccione una opción (0-10): ").strip()

                if opcion == "0":
                    print("\n👋 ¡Gracias por usar el Gestor de Tareas!")
                    self.gestor.cerrar()
                    break

                elif opcion == "1":
                    self.crear_tarea()
                elif opcion == "2":
                    self.ver_todas_tareas()
                elif opcion == "3":
                    self.agregar_dependencia()
                elif opcion == "4":
                    self.ver_orden_ejecucion()
                elif opcion == "5":
                    self.ver_tareas_ejecutables()
                elif opcion == "6":
                    self.obtener_siguiente_tarea()
                elif opcion == "7":
                    self.marcar_completada()
                elif opcion == "8":
                    self.ver_estadisticas()
                elif opcion == "9":
                    self.eliminar_tarea()
                elif opcion == "10":
                    self.ver_plan_diario()
                else:
                    print("\n❌ Opción inválida. Por favor seleccione un número entre 0 y 10.")
                    input("Presione Enter para continuar...")

            except KeyboardInterrupt:
                print("\n\n\n¡Hasta luego! 👋")
                self.gestor.cerrar()
                break
            except Exception as e:
                print(f"\n\n❌ Error inesperado: {e}")
                print("Continuando con el programa...")
                input("Presione Enter para continuar...")


def main():
    """Función principal para la CLI"""
    try:
        cli = GestorTareasCLI()
        cli.ejecutar()
    except Exception as e:
        print(f"❌ Error al iniciar la CLI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()