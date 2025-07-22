class TaskManager:
    """
    Manages the list of tasks for the ToDoList application.
    Provides methods to add, remove, and retrieve tasks.
    """
    def __init__(self):
        """
        Initializes the TaskManager with an empty list of tasks.
        """
        self.tasks = []

    def add_task(self, task):
        """
        Adds a new task to the list.
        Args:
            task (str): The task to add.
        Returns:
            bool: True if the task was added, False if the task is empty.
        """
        if task:
            self.tasks.append(task)
            return True
        return False

    def remove_task(self, task):
        """
        Removes a task from the list.
        Args:
            task (str): The task to remove.
        Returns:
            bool: True if the task was removed, False if the task was not found.
        """
        if task in self.tasks:
            self.tasks.remove(task)
            return True
        return False

    def get_all_tasks(self):
        """
        Returns the list of all tasks.
        Returns:
            list: The list of tasks.
        """
        return self.tasks
