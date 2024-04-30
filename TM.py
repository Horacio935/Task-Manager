import tkinter as tk
import threading
import time

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.process_list = []
        self.mode_fifo = tk.BooleanVar(value=True)  # Modo FIFO activo por defecto
        self.mode_lifo = tk.BooleanVar(value=True)  # Modo LIFO activo por defecto

        self.process_frame = tk.Frame(self.root)
        self.process_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.process_label = tk.Label(self.process_frame, text="Procesos:")
        self.process_label.pack()

        self.process_listbox = tk.Listbox(self.process_frame, selectmode=tk.MULTIPLE)
        self.process_listbox.pack()
 
        self.process_entry = tk.Entry(self.process_frame)
        self.process_entry.pack()

        self.add_button = tk.Button(self.process_frame, text="Añadir Proceso", command=self.add_process)
        self.add_button.pack()

        self.remove_button = tk.Button(self.process_frame, text="Eliminar Proceso", command=self.remove_process)
        self.remove_button.pack()

        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.mode_label = tk.Label(self.mode_frame, text="Modo de Ejecución:")
        self.mode_label.pack()

        self.fifo_button = tk.Checkbutton(self.mode_frame, text="FIFO", variable=self.mode_fifo)
        self.fifo_button.pack()

        self.lifo_button = tk.Checkbutton(self.mode_frame, text="LIFO", variable=self.mode_lifo)
        self.lifo_button.pack()

        self.compare_button = tk.Button(self.mode_frame, text="Ejecutar", command=self.compare_execution)
        self.compare_button.pack()

        self.tasks_frame_fifo = tk.Frame(self.root)
        self.tasks_frame_fifo.pack(side=tk.LEFT, padx=10, pady=10)

        self.tasks_label_fifo = tk.Label(self.tasks_frame_fifo, text="Tareas FIFO:")
        self.tasks_label_fifo.pack()

        self.tasks_display_fifo = tk.Text(self.tasks_frame_fifo, width=40, height=10)
        self.tasks_display_fifo.pack()

        self.tasks_frame_lifo = tk.Frame(self.root)
        self.tasks_frame_lifo.pack(side=tk.RIGHT, padx=10, pady=10)

        self.tasks_label_lifo = tk.Label(self.tasks_frame_lifo, text="Tareas LIFO:")
        self.tasks_label_lifo.pack()

        self.tasks_display_lifo = tk.Text(self.tasks_frame_lifo, width=40, height=10)
        self.tasks_display_lifo.pack()

        self.running_processes_fifo = []  # Procesos FIFO en ejecución
        self.waiting_processes_fifo = []  # Procesos FIFO en espera
        self.running_processes_lifo = []  # Procesos LIFO en ejecución
        self.waiting_processes_lifo = []  # Procesos LIFO en espera

    def add_process(self):
        process = self.process_entry.get()
        if process:
            self.process_list.append(process)
            self.process_listbox.insert(tk.END, process)
            self.process_entry.delete(0, tk.END)
            self.waiting_processes_fifo.append(process)
            self.waiting_processes_lifo.append(process)

    def remove_process(self):
        selected_indices = self.process_listbox.curselection()
        for index in reversed(selected_indices):
            process = self.process_list[index]
            self.process_listbox.delete(index)
            del self.process_list[index]
            if process in self.waiting_processes_fifo:
                self.waiting_processes_fifo.remove(process)
            if process in self.waiting_processes_lifo:
                self.waiting_processes_lifo.remove(process)

    def execute_processes_fifo(self):
        while self.waiting_processes_fifo:
            process = self.waiting_processes_fifo.pop(0)
            self.running_processes_fifo.append(process)
            self.update_display_fifo(process)
            for countdown in range(4, -1, -1):
                time.sleep(1)
                self.update_display_fifo(process, countdown)
            self.running_processes_fifo.remove(process)
            self.update_display_fifo(process, 0)

    def execute_processes_lifo(self):
        while self.waiting_processes_lifo:
            process = self.waiting_processes_lifo.pop()
            self.running_processes_lifo.append(process)
            self.update_display_lifo(process)
            for countdown in range(4, -1, -1):
                time.sleep(1)
                self.update_display_lifo(process, countdown)
            self.running_processes_lifo.remove(process)
            self.update_display_lifo(process, 0)

    def update_display_fifo(self, process, countdown=None):
        self.tasks_display_fifo.delete(1.0, tk.END)
        self.tasks_display_fifo.insert(tk.END, "Ejecutando FIFO:\n")
        for p in self.process_list:
            if p in self.running_processes_fifo:
                if p == process and countdown is not None:
                    self.tasks_display_fifo.insert(tk.END, f"Proceso: {p} - {countdown}s\n")
                else:
                    self.tasks_display_fifo.insert(tk.END, f"Proceso: {p} - 4s\n")
            elif p in self.waiting_processes_fifo:
                self.tasks_display_fifo.insert(tk.END, f"Proceso: {p} - En espera\n")

    def update_display_lifo(self, process, countdown=None):
        self.tasks_display_lifo.delete(1.0, tk.END)
        self.tasks_display_lifo.insert(tk.END, "Ejecutando LIFO:\n")
        for p in reversed(self.process_list):
            if p in self.running_processes_lifo:
                if p == process and countdown is not None:
                    self.tasks_display_lifo.insert(tk.END, f"Proceso: {p} - {countdown}s\n")
                else:
                    self.tasks_display_lifo.insert(tk.END, f"Proceso: {p} - 4s\n")
            elif p in self.waiting_processes_lifo:
                self.tasks_display_lifo.insert(tk.END, f"Proceso: {p} - En espera\n")

    def compare_execution(self):
        if self.mode_fifo.get():
            thread_fifo = threading.Thread(target=self.execute_processes_fifo)
            thread_fifo.start()

        if self.mode_lifo.get():
            thread_lifo = threading.Thread(target=self.execute_processes_lifo)
            thread_lifo.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()