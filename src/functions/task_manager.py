import tkinter as tk

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        if task:
            self.tasks.append(task)
            return True
        return False

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False

    def get_all_tasks(self):
        return self.tasks
