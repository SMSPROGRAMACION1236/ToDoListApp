import tkinter as tk
from functions.task_manager import TaskManager


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

    def show_listbox(self):
        self.list_box_tasks = tk.Listbox(self, width=60, height=15, font=("Arial", 12))
        self.list_box_tasks.place(x=30, y=170)
        self.list_box_tasks.bind('<Double-Button-1>', self.put_task_as_completed)

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
        if index in self.completed_tasks:
            # Desmarcar
            self.completed_tasks.remove(index)
            new_text = "[ ] " + task
        else:
            # Marcar
            self.completed_tasks.add(index)
            new_text = "[✔] " + task
        self.list_box_tasks.delete(index)
        self.list_box_tasks.insert(index, new_text)
        self.list_box_tasks.selection_clear(0, 'end')
        self.list_box_tasks.selection_set(index)


if __name__ == "__main__":
    app = TodoList()
    app.mainloop()
