import tkinter as tk
from functions.task_manager import TaskManager

class TodoList(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ToDoList")
        self.resizable(True, True)
        self.task_manager = TaskManager()
        self.show_entry()
        self.show_button()
        self.show_listbox()

    def show_entry(self):
        self.label_entry = tk.Label(self, text="Enter a task: ")
        self.label_entry.pack()
        self.task_entry = tk.Entry(self)
        self.task_entry.pack()

    def show_button(self):
        self.task_button_entry = tk.Button(self, text="Add Task", command=self.add_task_to_gui)
        self.task_button_entry.pack()

    def show_listbox(self):
        self.list_box_tasks = tk.Listbox(self)
        self.list_box_tasks.pack()

    def add_task_to_gui(self):
        task = self.task_entry.get()
        if self.task_manager.add_task(task):
            self.list_box_tasks.insert('end', task)
            self.task_entry.delete(0, 'end')