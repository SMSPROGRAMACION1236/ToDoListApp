import tkinter
from tkinter import *

def resize_callback(event):

    pass


root = Tk()
root.title("To Do List")        # Set the window title
button = tkinter.Button(root, text="Add Task", activebackground="red", activeforeground="white")
button.pack()
button.place(x=150, y=50)
button = tkinter.CENTER
root.resizable(True, True)
root.bind("<Configure>", resize_callback)
root.geometry("400x300")        # Set the window size (width x height)

root.configure(bg="orange")
w = Label(root, text="To Do List", font=("Helvetica", 20, "bold"))

w.pack(pady=20)
w.configure(bg="orange")

root.mainloop()
