import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.size_A = tk.IntVar(value=3)
        self.size_B = tk.IntVar(value=3)
        self.task = tk.StringVar(value="Transpose")
        self.entries = []

        self.generate_matrices()
        
        # Main Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True)

        # Task Selection
        tk.Label(self.main_frame, text="Select Task:", font=("Arial", 14)).grid(row=0, column=0, pady=5, sticky="ew")
        self.task_menu = tk.OptionMenu(self.main_frame, self.task, "Transpose", "Addition", "Multiplication", command=self.update_task)
        self.task_menu.config(font=("Arial", 14), width=12)
        self.task_menu.grid(row=0, column=1, pady=5, sticky="ew")

        # Matrix Size Selection
        tk.Label(self.main_frame, text="Matrix A Size:", font=("Arial", 14)).grid(row=0, column=2, pady=5, sticky="ew")
        self.size_menu_A = tk.OptionMenu(self.main_frame, self.size_A, 2, 3, 4, 5, command=self.update_size)
        self.size_menu_A.config(font=("Arial", 14), width=5)
        self.size_menu_A.grid(row=0, column=3, pady=5, sticky="ew")

        tk.Label(self.main_frame, text="Matrix B Size:", font=("Arial", 14)).grid(row=0, column=4, pady=5, sticky="ew")
        self.size_menu_B = tk.OptionMenu(self.main_frame, self.size_B, 2, 3, 4, 5, command=self.update_size)
        self.size_menu_B.config(font=("Arial", 14), width=5)
        self.size_menu_B.grid(row=0, column=5, pady=5, sticky="ew")

        # Matrix Display Frames
        self.matrix_frame_A = tk.Frame(self.main_frame)
        self.matrix_frame_A.grid(row=1, column=0, pady=5, columnspan=6)

        self.matrix_frame_B = tk.Frame(self.main_frame)
        self.matrix_frame_B.grid(row=1, column=3, pady=5, columnspan=2)

        
        self.operator_label = tk.Label(self.main_frame, text="", font=("Arial", 18, "bold"))
        self.operator_label.grid(row=1, column=2)

        # Size Labels Below Matrices
        self.size_label_A = tk.Label(self.main_frame, font=("Arial", 12, "bold"))
        self.size_label_A.grid(row=2, column=0, columnspan=6, pady=5)

        self.size_label_B = tk.Label(self.main_frame, font=("Arial", 12, "bold"))
        self.size_label_B.grid(row=2, column=3, columnspan=2, pady=5)

        # Input Grid
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=3, column=0, columnspan=5, pady=10)

        # Check Answer Button
        self.check_button = tk.Button(self.main_frame, text="Check Answer", font=("Arial", 14, "bold"), command=self.check_answers)
        self.check_button.grid(row=4, column=0, columnspan=5, pady=10, sticky="ew")

        # Rules Button
        self.rules_button = tk.Button(self.main_frame, text="Rules", font=("Arial", 14, "bold"), command=self.show_rules)
        self.rules_button.grid(row=4, column=3, columnspan=2, pady=10, sticky="ew")
        
        self.update_task(self.task.get())

    def generate_matrices(self):
        self.matrix_A = np.random.randint(1, 10, (self.size_A.get(), self.size_A.get()))
        self.matrix_B = np.random.randint(1, 10, (self.size_B.get(), self.size_B.get()))

    def update_matrix_display(self):
        # Clear current widgets in matrix frames
        for widget in self.matrix_frame_A.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame_B.winfo_children():
            widget.destroy()

        task = self.task.get()
        print("TASK: ", task)
        if task == "Transpose":
            self.show_matrix(self.matrix_frame_A, self.matrix_A)
            self.matrix_frame_A.grid(row=1, column=0, pady=5, columnspan=6, sticky="nsew")  # Center Matrix A
            self.matrix_frame_B.grid_remove()  # Hide Matrix B
            self.operator_label.grid_remove()
            self.size_label_A.config(text=f"Size: {self.size_A.get()} x {self.size_A.get()}")
            self.size_label_A.grid(row=2, column=0, columnspan=6, pady=5)  # Position Size Label underneath Matrix A
            self.size_label_B.grid_remove()  # Hide B's size label
        else:
            self.show_matrix(self.matrix_frame_A, self.matrix_A)
            self.show_matrix(self.matrix_frame_B, self.matrix_B)
            self.operator_label.config(text="+" if task == "Addition" else "x")
            self.operator_label.grid()
            self.size_label_A.config(text=f"Size: {self.size_A.get()} x {self.size_A.get()}")
            self.size_label_B.config(text=f"Size: {self.size_B.get()} x {self.size_B.get()}")
            self.matrix_frame_A.grid(row=1, column=0, pady=5, columnspan=2)
            self.matrix_frame_B.grid(row=1, column=3, pady=5, columnspan=2)
            self.size_label_A.grid(row=2, column=0, columnspan=2, pady=5)
            self.size_label_B.grid(row=2, column=3, columnspan=2, pady=5)

        self.validate_operation()

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
        size = self.size_A.get()
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.input_frame, width=4, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_task(self, _):
        task = self.task.get()
        
        # Disable Matrix B size selection for Transpose
        if task == "Transpose":
            self.size_menu_B.config(state=tk.DISABLED)
        else:
            self.size_menu_B.config(state=tk.NORMAL)

        self.update_matrix_display()
        self.create_input_grid()

    def update_size(self, _):
        self.generate_matrices()
        self.update_matrix_display()
        self.create_input_grid()

    def validate_operation(self):
        task = self.task.get()
        size_A = self.size_A.get()
        size_B = self.size_B.get()

        if task == "Addition" and size_A != size_B:
            self.check_button.config(state=tk.DISABLED, text="Invalid Size for Addition")
        elif task == "Multiplication" and size_A != size_B:
            self.check_button.config(state=tk.DISABLED, text="Invalid Size for Multiplication")
        else:
            self.check_button.config(state=tk.NORMAL, text="Check Answer")

    def check_answers(self):
        user_matrix = np.array([[int(entry.get()) if entry.get().isdigit() else 0 for entry in row] for row in self.entries])
        correct_matrix = self.get_correct_answer()

        if np.array_equal(user_matrix, correct_matrix):
            messagebox.showinfo("Result", "Correct! Well done!")
        else:
            messagebox.showerror("Result", f"Incorrect.\nExpected:\n{correct_matrix}")

    def get_correct_answer(self):
        return self.matrix_A.T if self.task.get() == "Transpose" else (self.matrix_A + self.matrix_B if self.task.get() == "Addition" else np.dot(self.matrix_A, self.matrix_B))

    def show_rules(self):
        rules = {
            "Transpose": "Transpose: Rows become columns, and columns become rows.",
            "Addition": "Addition: Add corresponding elements of two matrices.",
            "Multiplication": "Multiplication: Multiply rows of the first matrix by columns of the second."
        }
        rules_text = f"Welcome to the Matrix Learning Game!\n\n- {rules[self.task.get()]}\n\nEnter your answer and press 'Check Answer'!"
        messagebox.showinfo("Matrix Rules", rules_text)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Make sure the columns expand properly
    for i in range(6):
        root.grid_columnconfigure(i, weight=1, uniform="equal")
    
    game = MatrixGame(root)
    root.mainloop()
