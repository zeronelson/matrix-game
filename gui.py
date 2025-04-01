import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.matrix_size = 3
        self.generate_matrices()
        
        self.task = tk.StringVar(value="Transpose")
        self.entries = []
        self.resize_id = None

        # Center frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True)

        # Task Selection
        self.task_label = tk.Label(self.main_frame, text="Select Task:", font=("Arial", 14))
        self.task_label.grid(row=0, column=0, pady=5, sticky="ew")

        self.task_menu = tk.OptionMenu(self.main_frame, self.task, "Transpose", "Addition", "Multiplication", command=self.update_task)
        self.task_menu.config(font=("Arial", 14), width=10)  # Fixed size
        self.task_menu.grid(row=0, column=1, pady=5, sticky="ew")

        # Matrix Display
        self.matrix_frame_A = tk.Frame(self.main_frame)
        self.matrix_frame_A.grid(row=1, column=0, pady=5)

        self.matrix_frame_B = tk.Frame(self.main_frame)
        self.matrix_frame_B.grid(row=1, column=1, pady=5)

        # Input Grid
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Check Answer Button
        self.check_button = tk.Button(self.main_frame, text="Check Answer", font=("Arial", 14, "bold"), command=self.check_answers)
        self.check_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.update_task(self.task.get())
        self.root.bind("<Configure>", self.debounce_resize)

    def generate_matrices(self):
        """Generate two random matrices."""
        self.matrix_A = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))
        self.matrix_B = np.random.randint(1, 10, (self.matrix_size, self.matrix_size))

    def update_matrix_display(self):
        """Update displayed matrices based on the selected task."""
        for widget in self.matrix_frame_A.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame_B.winfo_children():
            widget.destroy()

        self.show_matrix(self.matrix_frame_A, self.matrix_A)

        if self.task.get() in ["Addition", "Multiplication"]:
            self.show_matrix(self.matrix_frame_B, self.matrix_B)
        else:
            self.matrix_frame_B.grid_remove()  # Hide Matrix B for Transpose
            return

        self.matrix_frame_B.grid()  # Show Matrix B when needed

    def show_matrix(self, frame, matrix):
        """Display a matrix with a visually appealing style."""
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                cell = tk.Label(frame, text=str(matrix[i, j]), font=("Arial", 18, "bold"), 
                                width=4, height=2, relief="solid", borderwidth=2, bg="lightgray")
                cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    def create_input_grid(self):
        """Create an input grid that dynamically adjusts to resizing."""
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.entries.clear()
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = tk.Entry(self.input_frame, width=4, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_task(self, selected_task):
        """Update the UI to show only relevant matrices."""
        self.update_matrix_display()
        self.create_input_grid()

    def check_answers(self):
        """Check user input and provide feedback."""
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

            if self.task.get() == "Transpose":
                self.generate_matrices()
                self.update_matrix_display()
                self.create_input_grid()

    def get_correct_answer(self):
        """Return the correct answer based on the selected task."""
        if self.task.get() == "Transpose":
            return self.matrix_A.T
        elif self.task.get() == "Addition":
            return self.matrix_A + self.matrix_B
        elif self.task.get() == "Multiplication":
            return np.dot(self.matrix_A, self.matrix_B)

    def debounce_resize(self, event):
        """Debounce resize events to avoid lagging."""
        if self.resize_id:
            self.root.after_cancel(self.resize_id)
        self.resize_id = self.root.after(200, self.on_resize)

    def on_resize(self):
        """Adjust UI components dynamically based on window size."""
        width = self.root.winfo_width()
        new_size = max(14, width // 40)
        matrix_size = max(18, width // 35)

        self.task_label.config(font=("Arial", new_size))
        self.task_menu.config(font=("Arial", new_size))
        self.check_button.config(font=("Arial", new_size, "bold"))

        for widget in self.matrix_frame_A.winfo_children():
            widget.config(font=("Arial", matrix_size, "bold"))

        for widget in self.matrix_frame_B.winfo_children():
            widget.config(font=("Arial", matrix_size, "bold"))

        for row in self.entries:
            for entry in row:
                entry.config(font=("Arial", matrix_size))

if __name__ == "__main__":
    root = tk.Tk()
    game = MatrixGame(root)
    root.mainloop()
