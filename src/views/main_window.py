"""
Interfaz Gráfica Principal
Ventana principal usando Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from typing import Optional
from controllers.gestor_proyecto import GestorProyecto
from models.tarea import Tarea

class AplicacionGestorTareas:
    """Aplicación principal con interfaz gráfica"""

    def __init__(self):
        """Inicializa la aplicación"""
        self.gestor = GestorProyecto()
        self.root = tk.Tk()
        self.configurar_ventana()
        self.crear_widgets()
        self.actualizar_vistas()

    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("Gestor de Tareas con Dependencias")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')

    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # ===== FRAME PRINCIPAL =====
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # ===== TÍTULO =====
        titulo = tk.Label(main_frame, text="📋 Gestor de Tareas con Dependencias",
                         font=('Arial', 20, 'bold'), fg='#2c3e50')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # ===== PANEL IZQUIERDO - ACCIONES =====
        panel_izq = ttk.LabelFrame(main_frame, text="Acciones", padding="10")
        panel_izq.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Botones de acciones
        ttk.Button(panel_izq, text="➕ Nueva Tarea",
                  command=self.crear_tarea_dialog, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="🔗 Agregar Dependencia",
                  command=self.agregar_dependencia_dialog, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="✓ Marcar Completada",
                  command=self.marcar_completada_dialog, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="📊 Ver Orden de Ejecución",
                  command=self.mostrar_orden_ejecucion, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="🎯 Tareas Ejecutables",
                  command=self.mostrar_tareas_ejecutables, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="⭐ Siguiente Tarea",
                  command=self.mostrar_siguiente_tarea, width=20).pack(pady=5, fill=tk.X)

        ttk.Separator(panel_izq, orient=tk.HORIZONTAL).pack(pady=10, fill=tk.X)

        ttk.Button(panel_izq, text="📅 Ver Plan Diario",
                  command=self.mostrar_plan_diario, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="🔄 Actualizar Vista",
                  command=self.actualizar_vistas, width=20).pack(pady=5, fill=tk.X)

        ttk.Separator(panel_izq, orient=tk.HORIZONTAL).pack(pady=10, fill=tk.X)

        ttk.Button(panel_izq, text="📈 Estadísticas",
                  command=self.mostrar_estadisticas, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(panel_izq, text="🚪 Salir",
                  command=self.salir, width=20).pack(pady=5, fill=tk.X)

        # ===== PANEL CENTRAL - LISTA DE TAREAS =====
        panel_centro = ttk.LabelFrame(main_frame, text="Todas las Tareas", padding="10")
        panel_centro.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Treeview para tareas
        columns = ('ID', 'Nombre', 'Estado', 'Prioridad', 'Fecha Límite')
        self.tree_tareas = ttk.Treeview(panel_centro, columns=columns, show='headings', height=15)

        # Configurar columnas
        self.tree_tareas.heading('ID', text='ID')
        self.tree_tareas.heading('Nombre', text='Nombre')
        self.tree_tareas.heading('Estado', text='Estado')
        self.tree_tareas.heading('Prioridad', text='Prioridad')
        self.tree_tareas.heading('Fecha Límite', text='Fecha Límite')

        self.tree_tareas.column('ID', width=50, anchor='center')
        self.tree_tareas.column('Nombre', width=250)
        self.tree_tareas.column('Estado', width=120)
        self.tree_tareas.column('Prioridad', width=80, anchor='center')
        self.tree_tareas.column('Fecha Límite', width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(panel_centro, orient=tk.VERTICAL, command=self.tree_tareas.yview)
        self.tree_tareas.configure(yscrollcommand=scrollbar.set)

        self.tree_tareas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        panel_centro.columnconfigure(0, weight=1)
        panel_centro.rowconfigure(0, weight=1)

        # ===== PANEL DERECHO - INFORMACIÓN =====
        panel_der = ttk.LabelFrame(main_frame, text="Información de Tarea", padding="10")
        panel_der.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Text widget para mostrar detalles
        self.text_info = tk.Text(panel_der, width=35, height=20, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(panel_der, orient=tk.VERTICAL, command=self.text_info.yview)
        self.text_info.configure(yscrollcommand=info_scrollbar.set)

        self.text_info.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        panel_der.columnconfigure(0, weight=1)
        panel_der.rowconfigure(0, weight=1)

        # Eventos
        self.tree_tareas.bind('<<TreeviewSelect>>', self.mostrar_detalles_tarea)
        self.tree_tareas.bind('<Double-1>', self.doble_click_tarea)

        # Barra de estado
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def actualizar_vistas(self):
        """Actualiza todas las vistas de la aplicación"""
        # Limpiar treeview
        for item in self.tree_tareas.get_children():
            self.tree_tareas.delete(item)

        # Cargar tareas
        tareas = self.gestor.obtener_todas_tareas()
        for tarea in tareas:
            estado_display = tarea.estado.replace('_', ' ').title()
            fecha_limite_display = ""
            if tarea.fecha_limite:
                fecha_limite_display = tarea.fecha_limite.strftime("%d/%m/%Y")

            self.tree_tareas.insert('', 'end', values=(
                tarea.id,
                tarea.nombre,
                estado_display,
                f"⭐{tarea.prioridad}",
                fecha_limite_display
            ))

        self.status_bar.config(text=f"Total de tareas: {len(tareas)}")

    def mostrar_detalles_tarea(self, event):
        """Muestra los detalles de la tarea seleccionada"""
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            self.text_info.delete(1.0, tk.END)
            return

        item = self.tree_tareas.item(seleccion[0])
        tarea_id = item['values'][0]
        tarea = self.gestor.obtener_tarea(tarea_id)

        if tarea:
            detalles = f"ID: {tarea.id}\n"
            detalles += f"Nombre: {tarea.nombre}\n"
            detalles += f"Descripción: {tarea.descripcion}\n"
            detalles += f"Estado: {tarea.estado}\n"
            detalles += f"Prioridad: {tarea.prioridad} (1-5)\n"
            detalles += f"Fecha Creación: {tarea.fecha_creacion.strftime('%d/%m/%Y %H:%M')}\n"
            if tarea.fecha_limite:
                detalles += f"Fecha Límite: {tarea.fecha_limite.strftime('%d/%m/%Y')}\n"
            if tarea.estimacion_horas > 0:
                detalles += f"Tiempo Estimado: {tarea.estimacion_horas} horas\n"

            # Cargar dependencias
            dependencias = self.gestor.obtener_dependencias(tarea.id)
            if dependencias:
                detalles += f"\nDepende de:\n"
                for dep in dependencias:
                    detalles += f"  • {dep.nombre}\n"

            # Cargar dependientes
            dependientes = self.gestor.obtener_dependientes(tarea.id)
            if dependientes:
                detalles += f"\nTareas que dependen de esta:\n"
                for dep in dependientes:
                    detalles += f"  • {dep.nombre}\n"

            self.text_info.delete(1.0, tk.END)
            self.text_info.insert(1.0, detalles)

    def doble_click_tarea(self, event):
        """Maneja doble click en una tarea"""
        self.marcar_completada_dialog()

    def crear_tarea_dialog(self):
        """Diálogo para crear nueva tarea"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nueva Tarea")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()

        # Campos
        ttk.Label(dialog, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        entry_nombre = ttk.Entry(dialog, width=40)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Descripción:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=5)
        entry_desc = tk.Text(dialog, width=40, height=5)
        entry_desc.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Prioridad (1-5):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        frame_prioridad = ttk.Frame(dialog)
        frame_prioridad.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        tk.IntVar(value=3)
        spin_prioridad = ttk.Spinbox(frame_prioridad, from_=1, to=5, width=10)
        spin_prioridad.set(3)
        spin_prioridad.pack(side=tk.LEFT)

        ttk.Label(frame_prioridad, text="(1=Baja, 5=Alta)").pack(side=tk.LEFT, padx=(10, 0))

        def crear():
            nombre = entry_nombre.get().strip()
            descripcion = entry_desc.get(1.0, tk.END).strip()
            prioridad = int(spin_prioridad.get())

            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return

            exito, mensaje, tarea_id = self.gestor.crear_tarea(nombre, descripcion, prioridad)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                dialog.destroy()
                self.actualizar_vistas()
            else:
                messagebox.showerror("Error", mensaje)

        # Botones
        frame_botones = ttk.Frame(dialog)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(frame_botones, text="Crear", command=crear).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        entry_nombre.focus()

    def agregar_dependencia_dialog(self):
        """Diálogo para agregar dependencia"""
        tareas = self.gestor.obtener_todas_tareas()
        if len(tareas) < 2:
            messagebox.showwarning("Aviso", "Se necesitan al menos 2 tareas para crear dependencias")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Dependencia")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Tarea prerequisito (debe completarse primero):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        combo_origen = ttk.Combobox(dialog, width=30, state="readonly")
        combo_origen.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Tarea dependiente (requiere la primera):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        combo_destino = ttk.Combobox(dialog, width=30, state="readonly")
        combo_destino.grid(row=1, column=1, padx=10, pady=10)

        # Llenar comboboxes con tareas
        nombres_tareas = [(t.id, f"{t.id} - {t.nombre}") for t in tareas]
        combo_origen['values'] = [nombre for _, nombre in nombres_tareas]
        combo_destino['values'] = [nombre for _, nombre in nombres_tareas]

        def agregar():
            if not combo_origen.get() or not combo_destino.get():
                messagebox.showerror("Error", "Debe seleccionar ambas tareas")
                return

            # Obtener IDs
            origen_id = next(t_id for t_id, nombre in nombres_tareas if nombre == combo_origen.get())
            destino_id = next(t_id for t_id, nombre in nombres_tareas if nombre == combo_destino.get())

            exito, mensaje = self.gestor.agregar_dependencia(origen_id, destino_id)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                dialog.destroy()
                self.actualizar_vistas()
            else:
                messagebox.showerror("Error", mensaje)

        frame_botones = ttk.Frame(dialog)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(frame_botones, text="Agregar", command=agregar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def marcar_completada_dialog(self):
        """Marca la tarea seleccionada como completada"""
        seleccion = self.tree_tareas.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una tarea para marcar como completada")
            return

        item = self.tree_tareas.item(seleccion[0])
        tarea_id = item['values'][0]
        tarea = self.gestor.obtener_tarea(tarea_id)

        if tarea:
            if tarea.estado == 'completada':
                messagebox.showinfo("Aviso", "Esta tarea ya está completada")
                return

            if messagebox.askyesno("Confirmar", f"¿Marcar la tarea '{tarea.nombre}' como completada?"):
                exito, mensaje, tareas_desbloqueadas = self.gestor.marcar_completada(tarea_id)
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    if tareas_desbloqueadas:
                        nombres_desbloqueadas = []
                        for tid in tareas_desbloqueadas:
                            t = self.gestor.obtener_tarea(tid)
                            if t:
                                nombres_desbloqueadas.append(t.nombre)
                        if nombres_desbloqueadas:
                            messagebox.showinfo("Tareas Desbloqueadas",
                                f"Tareas ahora disponibles: {', '.join(nombres_desbloqueadas)}")
                    self.actualizar_vistas()
                else:
                    messagebox.showerror("Error", mensaje)

    def mostrar_orden_ejecucion(self):
        """Muestra el orden de ejecución(topológico)"""
        resultado = self.gestor.calcular_orden_ejecucion()
        if resultado is None:
            messagebox.showerror("Error", "Hay ciclos en las dependencias del proyecto")
            return

        if not resultado:
            messagebox.showinfo("Orden de Ejecución", "No hay tareas pendientes")
            return

        # Crear ventana para mostrar resultado
        dialog = tk.Toplevel(self.root)
        dialog.title("Orden de Ejecución Sugerido")
        dialog.geometry("600x400")
        dialog.transient(self.root)

        text = tk.Text(dialog, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        text.insert(tk.END, "ORDEN DE EJECUCIÓN VÁLIDO\n")
        text.insert(tk.END, "=" * 40 + "\n\n")

        for i, tarea in enumerate(resultado, 1):
            estado_icon = "⭐" if tarea.prioridad >= 4 else "📋"
            text.insert(tk.END, f"{i}. {estado_icon} {tarea.nombre} (Prioridad: {tarea.prioridad})\n")
            if tarea.descripcion:
                text.insert(tk.END, f"   {tarea.descripcion[:80]}...\n")
            text.insert(tk.END, "\n")

        text.configure(state='disabled')

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def mostrar_tareas_ejecutables(self):
        """Muestra las tareas que pueden ejecutarse ahora"""
        ejecutables = self.gestor.obtener_tareas_ejecutables()

        if not ejecutables:
            messagebox.showinfo("Tareas Ejecutables",
                "No hay tareas ejecutables en este momento.\n\n" +
                "Esto puede suceder porque:\n" +
                "• Hay dependencias pendientes\n" +
                "• Todas las tareas están completadas")
            return

        # Crear ventana para mostrar resultado
        dialog = tk.Toplevel(self.root)
        dialog.title("Tareas Ejecutables Ahora")
        dialog.geometry("500x400")
        dialog.transient(self.root)

        text = tk.Text(dialog, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        text.insert(tk.END, "TAREAS DISPONIBLES PARA EJECUTAR\n")
        text.insert(tk.END, "=" * 40 + "\n\n")
        text.insert(tk.END, f"Total: {len(ejecutables)} tarea(s)\n\n")

        for i, tarea in enumerate(ejecutables, 1):
            prioridad_icon = "🔥" if tarea.prioridad == 5 else "⭐" if tarea.prioridad >= 3 else "📋"
            text.insert(tk.END, f"{i}. {prioridad_icon} {tarea.nombre}\n")
            text.insert(tk.END, f"   Prioridad: {tarea.prioridad}/5\n")
            if tarea.fecha_limite:
                text.insert(tk.END, f"   Límite: {tarea.fecha_limite.strftime('%d/%m/%Y')}\n")
            if tarea.descripcion:
                text.insert(tk.END, f"   {tarea.descripcion[:60]}...\n")
            text.insert(tk.END, "\n")

        text.configure(state='disabled')

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def mostrar_siguiente_tarea(self):
        """Muestra la siguiente tarea recomendada"""
        siguientetarea = self.gestor.obtener_siguiente_tarea()

        if not siguientetarea:
            messagebox.showinfo("Siguiente Tarea",
                "No hay tareas disponibles para ejecutar.\n\n" +
                "Revisa el estado de tus dependencias.")
            return

        # Crear diálogo para la siguiente tarea
        dialog = tk.Toplevel(self.root)
        dialog.title("Siguiente Tarea Recomendada")
        dialog.geometry("500x300")
        dialog.transient(self.root)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="🎯 SIGUIENTE TAREA RECOMENDADA",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(frame, text=f"Nombre: {siguientetarea.nombre}",
                 font=('Arial', 12, 'bold')).pack(pady=5)

        if siguientetarea.descripcion:
            ttk.Label(frame, text=f"Descripción: {siguientetarea.descripcion}").pack(pady=5)

        ttk.Label(frame, text=f"Prioridad: {siguientetarea.prioridad}/5").pack(pady=5)

        if siguientetarea.fecha_limite:
            ttk.Label(frame,
                     text=f"Fecha límite: {siguientetarea.fecha_limite.strftime('%d/%m/%Y')}").pack(pady=5)

        if siguientetarea.estimacion_horas > 0:
            ttk.Label(frame,
                     text=f"Tiempo estimado: {siguientetarea.estimacion_horas} horas").pack(pady=5)

        ttk.Button(dialog, text="Aceptar", command=dialog.destroy).pack(pady=20)

    def mostrar_plan_diario(self):
        """Muestra el plan diario"""
        plan = self.gestor.obtener_plan_diario()

        if not plan:
            messagebox.showinfo("Plan Diario", "No hay tareas en el plan diario.\n\n" +
                               "Agarra tareas ejecutables al plan diario para organizar tu día.")
            return

        # Crear ventana para mostrar resultado
        dialog = tk.Toplevel(self.root)
        dialog.title("Plan Diario")
        dialog.geometry("500x400")
        dialog.transient(self.root)

        text = tk.Text(dialog, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        text.insert(tk.END, "PLAN DIARIO DE TRABAJO\n")
        text.insert(tk.END, "=" * 40 + "\n\n")

        for i, tarea in enumerate(plan, 1):
            text.insert(tk.END, f"{i}. {tarea.nombre}\n")
            if tarea.descripcion:
                text.insert(tk.END, f"   {tarea.descripcion[:60]}...\n")
            text.insert(tk.END, "\n")

        text.configure(state='disabled')

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def mostrar_estadisticas(self):
        """Muestra estadísticas del proyecto"""
        stats = self.gestor.obtener_estadisticas()

        # Crear ventana de estadísticas
        dialog = tk.Toplevel(self.root)
        dialog.title("Estadísticas del Proyecto")
        dialog.geometry("400x350")
        dialog.transient(self.root)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="📊 ESTADÍSTICAS DEL PROYECTO",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        stats_text = f"""
📋 Total de Tareas: {stats['total_tareas']}

✅ Completadas: {stats['completadas']}
🔄 En Progreso: {stats['en_progreso']}
⏳ Pendientes: {stats['pendientes']}

🎯 Ejecutables Ahora: {stats['ejecutables']}

🔗 Total de Dependencias: {stats['total_dependencias']}

📈 Progreso del Proyecto: {stats['porcentaje_completado']:.1f}%
"""

        text = tk.Text(frame, wrap=tk.WORD, height=12, width=40)
        text.insert(1.0, stats_text)
        text.configure(state='disabled')
        text.pack(pady=10)

        ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            self.gestor.cerrar()
            self.root.quit()
            self.root.destroy()

    def iniciar(self):
        """Inicia la aplicación"""
        self.root.mainloop()