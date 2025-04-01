import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        self.root.geometry("500x400")  # Initial window size
        self.root.resizable(True, True)  # Allow resizing
        
        self.matrix_size = 3  # 3x3 matrix
        self.generate_matrices()  # Initialize matrices
        
        self.task = tk.StringVar(value="Transpose")
        self.entries = []  # Stores user input fields
        self.resize_id = None  # To debounce resize events

        # Create the main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Task selection
        self.task_label = tk.Label(self.main_frame, text="Select Task:", font=("Arial", 14))
        self.task_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.task_menu = tk.OptionMenu(self.main_frame, self.task, "Transpose", "Addition", "Multiplication", command=self.update_task)
        self.task_menu.config(font=("Arial", 14))
        self.task_menu.grid(row=0, column=3, columnspan=2, sticky="nsew")

        # Display matrices
        self.label_A = tk.Label(self.main_frame, text=f"Matrix A:\n{self.matrix_A}", font=("Arial", 16, "bold"))
        self.label_A.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        self.label_B = tk.Label(self.main_frame, text=f"Matrix B:\n{self.matrix_B}", font=("Arial", 16, "bold"))
        self.label_B.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.update_task(self.task.get())  # Hide/show matrices based on initial selection
        
        # Input Grid
        self.create_input_grid()
        
        # Check Answer Button
        self.check_button = tk.Button(self.main_frame, text="Check Answer", font=("Arial", 14, "bold"), command=self.check_answers)
        self.check_button.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")
        
        # Allow dynamic resizing
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.main_frame.grid_rowconfigure(i, weight=1)

        # Bind resizing event with debounce
        self.root.bind("<Configure>", self.debounce_resize)

    def generate_matrices(self):
        """Generate new matrices for a fresh round."""
        self.matrix_A = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))
        self.matrix_B = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))

    def create_input_grid(self):
        """Create or reset the input grid."""
        for widget in self.main_frame.grid_slaves():
            if int(widget.grid_info()["row"]) >= 3:
                widget.destroy()
        
        self.entries.clear()
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = tk.Entry(self.main_frame, width=5, font=("Arial", 16), justify="center")
                entry.grid(row=i+3, column=j, padx=5, pady=5, sticky="nsew")
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
                self.root.update_idletasks()  # Refresh UI to fit new matrix

    def get_correct_answer(self):
        """Return the correct answer based on the selected task."""
        if self.task.get() == "Transpose":
            return self.matrix_A.T
        elif self.task.get() == "Addition":
            return self.matrix_A + self.matrix_B
        elif self.task.get() == "Multiplication":
            return np.dot(self.matrix_A, self.matrix_B)

    def debounce_resize(self, event):
        """Debounce the resize event to prevent UI freezing."""
        if self.resize_id:
            self.root.after_cancel(self.resize_id)
        self.resize_id = self.root.after(200, lambda: self.on_resize(event))

    def on_resize(self, event):
        """ Adjust font sizes dynamically when window resizes. """
        new_size = max(12, int(event.width / 40))  # Adjust font size based on width
        new_matrix_size = max(14, int(event.width / 35))  # Slightly larger for matrices
        
        self.label_A.config(font=("Arial", new_matrix_size, "bold"))
        self.label_B.config(font=("Arial", new_matrix_size, "bold"))
        self.task_label.config(font=("Arial", new_size))
        self.check_button.config(font=("Arial", new_size, "bold"))
        self.task_menu.config(font=("Arial", new_size))
        
        for row in self.entries:
            for entry in row:
                entry.config(font=("Arial", new_matrix_size))

if __name__ == "__main__":
    root = tk.Tk()
    game = MatrixGame(root)
    root.mainloop()
