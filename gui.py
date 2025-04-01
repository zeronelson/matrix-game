import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        
        self.matrix_size = 3  # 3x3 matrix
        self.generate_matrices()  # Initialize matrices
        
        self.task = tk.StringVar(value="Transpose")
        self.entries = []  # Stores user input fields

        # Task selection
        tk.Label(root, text="Select Task:", font=("Arial", 12)).grid(row=0, column=0, columnspan=3)
        tk.OptionMenu(root, self.task, "Transpose", "Addition", "Multiplication", command=self.update_task).grid(row=0, column=3, columnspan=2)

        # Display matrices
        self.label_A = tk.Label(root, text=f"Matrix A:\n{self.matrix_A}", font=("Arial", 12))
        self.label_A.grid(row=1, column=0, columnspan=3)
        
        self.label_B = tk.Label(root, text=f"Matrix B:\n{self.matrix_B}", font=("Arial", 12))
        self.label_B.grid(row=2, column=0, columnspan=3)

        self.update_task(self.task.get())  # Hide/show matrices based on initial selection
        
        # Input Grid
        self.create_input_grid()
        
        # Check Answer Button
        tk.Button(root, text="Check Answer", font=("Arial", 12), command=self.check_answers).grid(row=6, column=0, columnspan=3, pady=10)

    def generate_matrices(self):
        """Generate new matrices for a fresh round."""
        self.matrix_A = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))
        self.matrix_B = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))

    def create_input_grid(self):
        """Create or reset the input grid."""
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3:
                widget.destroy()
        
        self.entries.clear()
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = tk.Entry(self.root, width=5, font=("Arial", 14), justify="center")
                entry.grid(row=i+3, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)
    
    def update_task(self, selected_task):
        """ Update the UI to show/hide Matrix B based on selected task """
        if selected_task == "Transpose":
            self.label_B.grid_remove()  # Hide Matrix B
        else:
            self.label_B.grid()  # Show Matrix B
        
        self.create_input_grid()
    
    def check_answers(self):
        """Check user answers and update the matrix if needed."""
        user_matrix = []
        for i in range(self.matrix_size):
            row_values = []
            for j in range(self.matrix_size):
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

            # If the task is "Transpose," generate a new Matrix A
            if self.task.get() == "Transpose":
                self.generate_matrices()
                self.label_A.config(text=f"Matrix A:\n{self.matrix_A}")  # Update label
                self.create_input_grid()  # Reset input fields

    def get_correct_answer(self):
        """Return the correct answer based on the selected task."""
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