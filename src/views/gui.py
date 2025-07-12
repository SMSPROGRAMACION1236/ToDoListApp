import tkinter as tk
from functions.task_manager import TaskManager
import json

class TodoList(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ToDoList")
        self.geometry("600x500")
        self.resizable(True, True)
        self.configure(bg="#e2aa87")

        self.task_manager = TaskManager()
        self.completed_tasks = set()  # Para guardar los índices de tareas completadas

        self.show_entry()
        self.show_buttons()
        self.show_search()
        self.show_listbox()
        self.update_task_count()  # Initialize task count

    def show_entry(self):
        self.label_entry = tk.Label(self, text="Enter a task:", width=10, font=("Arial", 15), bg="#ef8e7d", fg="#ddd")
        self.label_entry.place(x=25, y=20)

        self.task_entry = tk.Entry(self, width=40, font=("Arial", 12))
        self.task_entry.place(x=200, y=25)

    def show_buttons(self):
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task_to_gui, width=15, height=1, font=("Arial", 11), bg="#a2d3c7")
        self.add_button.place(x=100, y=70)

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_task_to_gui, width=15, height=1, font=("Arial", 11), bg="#fef7e1")
        self.remove_button.place(x=250, y=70)

        self.show_button = tk.Button(self, text="Show Tasks", command=self.show_tasks, width=15, height=1, font=("Arial", 11), bg="#e2aa87")
        self.show_button.place(x=400, y=70)

        self.complete_button = tk.Button(self, text="Marcar como completada", command=self.put_task_as_completed_button, width=20, height=1, font=("Arial", 11), bg="#edd8bb")
        self.complete_button.place(x=200, y=120)

        self.save_button = tk.Button(self, text="Guardar", command=self.guardar_tareas, width=10, height=1, font=("Arial", 11), bg="#b6e2d3")
        self.save_button.place(x=50, y=120)

        self.load_button = tk.Button(self, text="Cargar", command=self.cargar_tareas, width=10, height=1, font=("Arial", 11), bg="#b6cbe2")
        self.load_button.place(x=400, y=120)

    def show_search(self):
        self.search_label = tk.Label(self, text="Buscar:", font=("Arial", 12), bg="#e2aa87")
        self.search_label.place(x=30, y=155)
        self.search_entry = tk.Entry(self, width=30, font=("Arial", 12))
        self.search_entry.place(x=100, y=155)
        self.search_button = tk.Button(self, text="Buscar", command=self.buscar_tareas, width=10, font=("Arial", 11), bg="#e2aa87")
        self.search_button.place(x=350, y=152)
        self.clear_search_button = tk.Button(self, text="Limpiar", command=self.show_tasks, width=10, font=("Arial", 11), bg="#e2aa87")
        self.clear_search_button.place(x=450, y=152)

    def show_listbox(self):
        # Frame para contener Listbox y Scrollbars
        frame = tk.Frame(self)
        frame.place(x=30, y=190)

        self.list_box_tasks = tk.Listbox(frame, width=60, height=13, font=("Arial", 12), xscrollcommand=None)
        self.list_box_tasks.pack(side=tk.LEFT, fill=tk.BOTH)
        self.list_box_tasks.bind('<Double-Button-1>', self.put_task_as_completed)

        # Scrollbar vertical
        self.scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.list_box_tasks.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_box_tasks.config(yscrollcommand=self.scrollbar_y.set)

        # Scrollbar horizontal
        # self.scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.list_box_tasks.xview)
        # self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # self.list_box_tasks.config(xscrollcommand=self.scrollbar_x.set)

        # Add task count label below the listbox
        self.task_count_label = tk.Label(self, text="", font=("Arial", 12), bg="#ef8e7d", fg="white")
        self.task_count_label.place(x=60, y=450)

    def update_task_count(self):
        count = len(self.task_manager.get_all_tasks())
        self.task_count_label.config(text=f"Total Tasks: {count}")

    def add_task_to_gui(self):
        task = self.task_entry.get().strip()
        if task and self.task_manager.add_task(task):
            display_text = "[ ] " + task
            self.list_box_tasks.insert('end', display_text)
            self.task_entry.delete(0, 'end')
            self.update_task_count()

    def remove_task_to_gui(self):
        selected_indices = self.list_box_tasks.curselection()
        if not selected_indices:
            return

        for index in selected_indices[::-1]:  # reverse to avoid index shift
            # Elimina la tarea de la lógica y del Listbox
            display_text = self.list_box_tasks.get(index)
            task = display_text[4:]  # Quita el prefijo '[ ] ' o '[✔] '
            if self.task_manager.remove_task(task):
                self.list_box_tasks.delete(index)
                self.completed_tasks.discard(index)

        self.task_entry.delete(0, 'end')
        self.update_task_count()

    def show_tasks(self):
        self.list_box_tasks.delete(0, 'end')  # clear current list
        for i, task in enumerate(self.task_manager.get_all_tasks()):
            if i in self.completed_tasks:
                display_text = "[✔] " + task
            else:
                display_text = "[ ] " + task
            self.list_box_tasks.insert('end', display_text)
        self.update_task_count()

    def buscar_tareas(self):
        query = self.search_entry.get().strip().lower()
        self.list_box_tasks.delete(0, 'end')
        if not query:
            self.show_tasks()
            return
        for i, task in enumerate(self.task_manager.get_all_tasks()):
            if query in task.lower():
                display_text = ("[✔] " if i in self.completed_tasks else "[ ] ") + task
                self.list_box_tasks.insert('end', display_text)
        # No actualiza el contador porque no es la lista completa

    def put_task_as_completed(self, event):
        selection = self.list_box_tasks.curselection()
        if not selection:
            return
        index = selection[0]
        self.toggle_task_completed(index)

    def put_task_as_completed_button(self):
        selection = self.list_box_tasks.curselection()
        if not selection:
            return
        index = selection[0]
        self.toggle_task_completed(index)

    def toggle_task_completed(self, index):
        display_text = self.list_box_tasks.get(index)
        task = display_text[4:]  # Quita el prefijo
        # Buscar el índice real en la lista de tareas
        all_tasks = self.task_manager.get_all_tasks()
        real_index = None
        for i, t in enumerate(all_tasks):
            if t == task:
                real_index = i
                break
        if real_index is None:
            return
        if real_index in self.completed_tasks:
            # Desmarcar
            self.completed_tasks.remove(real_index)
            new_text = "[ ] " + task
        else:
            # Marcar
            self.completed_tasks.add(real_index)
            new_text = "[✔] " + task
        self.list_box_tasks.delete(index)
        self.list_box_tasks.insert(index, new_text)
        self.list_box_tasks.selection_clear(0, 'end')
        self.list_box_tasks.selection_set(index)

    def guardar_tareas(self, filename="tasks.json"):
        tareas = self.task_manager.get_all_tasks()
        completadas = list(self.completed_tasks)
        data = {
            "tareas": tareas,
            "completed_tasks": completadas
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def cargar_tareas(self, filename="tasks.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.task_manager.tasks = data.get("tareas", [])
            self.completed_tasks = set(data.get("completed_tasks", []))
            self.show_tasks()
        except FileNotFoundError:
            pass  # Si no existe el archivo, no hace nada

if __name__ == "__main__":
    app = TodoList()
    app.mainloop()
