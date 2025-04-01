import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.matrix_size = tk.IntVar(value=3)
        self.generate_matrices()
        
        self.task = tk.StringVar(value="Transpose")
        self.entries = []

        # Center frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True)

        # Task Selection
        tk.Label(self.main_frame, text="Select Task:", font=("Arial", 14)).grid(row=0, column=0, pady=5, sticky="ew")
        self.task_menu = tk.OptionMenu(self.main_frame, self.task, "Transpose", "Addition", "Multiplication", command=self.update_task)
        self.task_menu.config(font=("Arial", 14), width=10)
        self.task_menu.grid(row=0, column=1, pady=5, sticky="ew")

        # Matrix Size Selection
        tk.Label(self.main_frame, text="Matrix Size:", font=("Arial", 14)).grid(row=0, column=2, pady=5, sticky="ew")
        self.size_menu = tk.OptionMenu(self.main_frame, self.matrix_size, 2, 3, 4, 5, command=self.update_size)
        self.size_menu.config(font=("Arial", 14), width=5)
        self.size_menu.grid(row=0, column=3, pady=5, sticky="ew")

        # Matrix Display
        self.matrix_frame_A = tk.Frame(self.main_frame)
        self.matrix_frame_A.grid(row=1, column=0, pady=5)

        self.matrix_frame_B = tk.Frame(self.main_frame)
        self.matrix_frame_B.grid(row=1, column=2, pady=5)

        self.operator_label = tk.Label(self.main_frame, text="", font=("Arial", 18, "bold"))
        self.operator_label.grid(row=1, column=1)

        # Input Grid
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # Check Answer Button
        self.check_button = tk.Button(self.main_frame, text="Check Answer", font=("Arial", 14, "bold"), command=self.check_answers)
        self.check_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
        
        self.update_task(self.task.get())

    def generate_matrices(self):
        size = self.matrix_size.get()
        self.matrix_A = np.random.randint(1, 10, (size, size))
        self.matrix_B = np.random.randint(1, 10, (size, size))

    def update_matrix_display(self):
        for widget in self.matrix_frame_A.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame_B.winfo_children():
            widget.destroy()

        self.show_matrix(self.matrix_frame_A, self.matrix_A)
        
        if self.task.get() in ["Addition", "Multiplication"]:
            self.show_matrix(self.matrix_frame_B, self.matrix_B)
            self.operator_label.config(text="+" if self.task.get() == "Addition" else "x")
            self.matrix_frame_B.grid()
            self.operator_label.grid()
        else:
            self.matrix_frame_B.grid_remove()
            self.operator_label.config(text="")
            self.operator_label.grid_remove()
            self.matrix_frame_A.grid(row=1, column=1, pady=5)
            return

        self.matrix_frame_A.grid(row=1, column=0, pady=5)

    def show_matrix(self, frame, matrix):
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                cell = tk.Label(frame, text=str(matrix[i, j]), font=("Arial", 18, "bold"), 
                                width=4, height=2, relief="solid", borderwidth=2, bg="lightgray")
                cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    def create_input_grid(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
        size = self.matrix_size.get()
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.input_frame, width=4, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_task(self, selected_task):
        self.update_matrix_display()
        self.create_input_grid()

    def update_size(self, _):
        self.generate_matrices()
        self.update_matrix_display()
        self.create_input_grid()

    def check_answers(self):
        user_matrix = []
        for i in range(self.matrix_size.get()):
            row_values = []
            for j in range(self.matrix_size.get()):
                try:
                    value = int(self.entries[i][j].get())
                    row_values.append(value)
                except ValueError:
                    messagebox.showerror("Error", "Please enter only numbers.")
                    return
            user_matrix.append(row_values)

        user_matrix = np.array(user_matrix)
        correct_matrix = self.get_correct_answer()

        if np.array_equal(user_matrix, correct_matrix):
            messagebox.showinfo("Result", "Correct! Well done!")
        else:
            messagebox.showerror("Result", f"Incorrect.\nExpected:\n{correct_matrix}")
            
            if self.task.get() == "Transpose":
                self.generate_matrices()
                self.update_matrix_display()
                self.create_input_grid()

    def get_correct_answer(self):
        if self.task.get() == "Transpose":
            return self.matrix_A.T
        elif self.task.get() == "Addition":
            return self.matrix_A + self.matrix_B
        elif self.task.get() == "Multiplication":
            return np.dot(self.matrix_A, self.matrix_B)

if __name__ == "__main__":
    root = tk.Tk()
    game = MatrixGame(root)
    root.mainloop()

