import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TODO_FILE = 'todo_list.json'

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        self.tasks = self.load_tasks()

        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.pack(pady=10)

        self.update_task_listbox()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.add_btn = tk.Button(btn_frame, text="Add Task", command=self.add_task)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.update_btn = tk.Button(btn_frame, text="Update Task", command=self.update_task)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete Task", command=self.delete_task)
        self.delete_btn.grid(row=0, column=2, padx=5)

    def load_tasks(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(TODO_FILE, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = 'Done' if task['completed'] else 'Not Done'
            self.task_listbox.insert(tk.END, f"{task['title']} - {status}")

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter the task title:")
        if title:
            self.tasks.append({'title': title, 'completed': False})
            self.save_tasks()
            self.update_task_listbox()
            messagebox.showinfo("Task Added", "Task added successfully.")

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("No Selection", "Please select a task to update.")
            return

        task_index = selected_task_index[0]
        task = self.tasks[task_index]

        new_title = simpledialog.askstring("Update Task", "Enter the new title for the task:", initialvalue=task['title'])
        if new_title:
            task['title'] = new_title
            task['completed'] = messagebox.askyesno("Task Status", "Is the task completed?")
            self.save_tasks()
            self.update_task_listbox()
            messagebox.showinfo("Task Updated", "Task updated successfully.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        task_index = selected_task_index[0]
        self.tasks.pop(task_index)
        self.save_tasks()
        self.update_task_listbox()
        messagebox.showinfo("Task Deleted", "Task deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
