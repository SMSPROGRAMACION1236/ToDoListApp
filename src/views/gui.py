import tkinter as tk
from functions.task_manager import TaskManager


class TodoList(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ToDoList")
        self.resizable(True, True)
        self.configure(bg="Red")

        self.task_manager = TaskManager()

        self.show_entry()
        self.show_buttons()
        self.show_listbox()
        self.update_task_count()  # Initialize task count

    def show_entry(self):
        self.label_entry = tk.Label(self, text="Enter a task:")
        self.label_entry.pack()

        self.task_entry = tk.Entry(self)
        self.task_entry.pack()

    def show_buttons(self):
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task_to_gui)
        self.add_button.pack()

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_task_to_gui)
        self.remove_button.pack()

        self.show_button = tk.Button(self, text="Show Tasks", command=self.show_tasks)
        self.show_button.pack()

    def show_listbox(self):
        self.list_box_tasks = tk.Listbox(self)
        self.list_box_tasks.pack()

        # Add task count label below the listbox
        self.task_count_label = tk.Label(self, text="")
        self.task_count_label.pack()

    def update_task_count(self):
        count = len(self.task_manager.get_all_tasks())
        self.task_count_label.config(text=f"Total Tasks: {count}")

    def add_task_to_gui(self):
        task = self.task_entry.get().strip()
        if task and self.task_manager.add_task(task):
            self.list_box_tasks.insert('end', task)
            self.task_entry.delete(0, 'end')
            self.update_task_count()

    def remove_task_to_gui(self):
        selected_indices = self.list_box_tasks.curselection()
        if not selected_indices:
            return

        for index in selected_indices[::-1]:  # reverse to avoid index shift
            task = self.list_box_tasks.get(index)
            if self.task_manager.remove_task(task):
                self.list_box_tasks.delete(index)

        self.task_entry.delete(0, 'end')
        self.update_task_count()

    def show_tasks(self):
        self.list_box_tasks.delete(0, 'end')  # clear current list
        for task in self.task_manager.get_all_tasks():
            self.list_box_tasks.insert('end', task)
        self.update_task_count()


if __name__ == "__main__":
    app = TodoList()
    app.mainloop()
