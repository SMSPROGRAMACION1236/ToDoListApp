import tkinter as tk


class TaskManager:
  def __init__(self):
    self.tasks = []
  def add_task(self, task):
    if task:
      self.tasks.append(task)
      return True
    return False