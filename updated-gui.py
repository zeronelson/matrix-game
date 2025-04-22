import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk, ImageOps
import random

class MatrixGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Learning Game")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.title_label = tk.Label(
        self.root,
        text="Matrix Quest",
        font=("Arial", 60, "bold"),
        fg="#582c83",
        anchor="center"
    )
        self.title_label.pack(pady=(10, 0))
        self.size_A = tk.IntVar(value=3)
        self.size_B = tk.IntVar(value=3)
        self.task = tk.StringVar(value="Transpose")
        self.entries = []

        self.generate_matrices()
        
        # Load and place logo in corner
        logo_image = Image.open("/Users/zeronelson/Downloads/Prairie_view_univ_athletics_textlogo.png")  # Your image file
        logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS) # Resize if needed
        self.logo = ImageTk.PhotoImage(logo_image)  # Keep reference!

        self.logo_label = tk.Label(self.root, image=self.logo)
        #self.logo_label.place(x=10, y=10)  # Adjust position if needed
        self.logo_label.place(relx=1.0, x=-40, y=10, anchor="ne")


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

        self.label_matrix_B = tk.Label(self.main_frame, text="Matrix B Size:", font=("Arial", 14))
        self.label_matrix_B.grid(row=0, column=4, pady=5, sticky="ew")
        self.size_menu_B = tk.OptionMenu(self.main_frame, self.size_B, 2, 3, 4, 5, command=self.update_size)
        self.size_menu_B.config(font=("Arial", 14), width=5)
        self.size_menu_B.grid(row=0, column=5, pady=5, sticky="ew")

        # Matrix Frames
        self.matrix_frame_A = tk.Frame(self.main_frame)
        self.matrix_frame_A.grid(row=1, column=0, pady=5, columnspan=6)

        self.matrix_frame_B = tk.Frame(self.main_frame)
        self.matrix_frame_B.grid(row=1, column=3, pady=5, columnspan=2)

        self.operator_label = tk.Label(self.main_frame, text="", font=("Arial", 18, "bold"))
        self.operator_label.grid(row=1, column=2)

        # Size Labels
        self.size_label_A = tk.Label(self.main_frame, font=("Arial", 12, "bold"))
        self.size_label_A.grid(row=2, column=0, columnspan=6, pady=5)

        self.size_label_B = tk.Label(self.main_frame, font=("Arial", 12, "bold"))
        self.size_label_B.grid(row=2, column=3, columnspan=2, pady=5)

        # Input Grid
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=3, column=0, columnspan=6, pady=10)

        # Buttons
        self.check_button = tk.Button(self.main_frame, text="Check Answer", font=("Arial", 14, "bold"), command=self.check_answers)
        self.check_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        self.rules_button = tk.Button(self.main_frame, text="Rules", font=("Arial", 14, "bold"), command=self.show_rules)
        self.rules_button.grid(row=4, column=3, columnspan=2, pady=10, sticky="ew")
        
        self.fun_facts_button = tk.Button(self.main_frame, text="Show Global Fact", font=("Arial", 14, "bold"), command=self.show_fun_fact)
        self.fun_facts_button.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        self.update_task(self.task.get())

        self.fun_facts = [
    "The world’s population reached 8 billion people in November 2022.",
    "Over 2 billion people in the world still lack access to clean water.",
    "Did you know? There are more than 7,000 languages spoken across the world.",
    "Over 8 million tons of plastic end up in our oceans each year.",
    "The Great Barrier Reef, the world’s largest coral reef, is visible from space.",
    "Deforestation in the Amazon rainforest contributes to climate change.",
    "1 in 9 people worldwide are living without electricity.",
    "Global life expectancy has increased by more than 10 years in the last 50 years.",
    "More than 80%% of the world’s population lives in the Northern Hemisphere.",
    "Mathematics and matrices are used in predicting climate change trends and weather patterns.",
    "Did you know? The Earth’s crust is divided into seven major tectonic plates.",
    "Matrices are used in weather prediction models to simulate global climate systems.",
    "Google’s search engine uses a matrix-based algorithm called PageRank to rank websites.",
    "Image processing—used in satellite imagery, MRI scans, and facial recognition—relies heavily on matrix math.",
    "Population growth models across regions are simulated using matrices in demography.",
    "Epidemic spread models like SIR models use matrices to simulate disease progression globally.",
    "Self-driving cars use matrix transformations to process images and detect lanes and obstacles.",
    "In economics, matrices are used in input-output models to understand global trade flows.",
    "Cryptography systems rely on matrices to secure communication around the world.",
    "Matrices are used in 3D video games and AR apps, many of which are enjoyed globally.",
    "GPS systems use matrix algebra to triangulate your position on Earth.",
    
    "Access to quality math education improves GDP per capita in many developing countries.",
    "Over 250 million children worldwide lack access to basic arithmetic education.",
    "International tests like PISA assess math literacy among 15-year-olds in over 80 countries.",
    "Matrix algebra is a core concept in STEM curricula around the world.",
    "Countries that invest more in math education tend to lead in technological innovation.",
    
    "Matrices help model CO₂ emissions across sectors and track environmental impact by region.",
    "Electrical grids across continents are optimized using matrix-based network analysis.",
    "The UN’s Sustainable Development Goals are tracked using statistical indicators—often compiled in large matrix datasets.",
    "Seismologists use matrices to simulate how earthquakes propagate across tectonic plates.",
    "Scientists use matrix-based models to simulate biodiversity loss and its global effects.",
    
    "The Earth’s landmass is divided into over 190 countries—each tracked using geographic matrix grids in GIS systems.",
    "NASA models global orbital paths using matrix rotation and transformation systems.",
    "Artificial intelligence systems trained on global datasets use matrices at their core.",
    "The World Health Organization uses matrix-based modeling to allocate vaccines equitably.",
    "Matrices are used in financial risk models across global banking systems.",
    
    "Translation software (like Google Translate) uses matrix embeddings of word meanings from hundreds of languages.",
    "The Human Genome Project uses matrix math to decode billions of DNA base pairs.",
    "Movie recommendation systems (like Netflix) use matrix factorization to predict what viewers around the globe will like.",
    "Ocean currents and global temperature changes are simulated using massive matrix models.",
    "Airline route planning across continents uses adjacency matrices to optimize fuel and time."
]

    def show_fun_fact(self):
        fact = random.choice(self.fun_facts)  # Choose a random fact
        messagebox.showinfo("Global Awareness Fact", fact)

    def adjust_window_size(self):
        if self.size_B.get() > self.size_A.get():
            size = self.size_B.get()
        else:
            size = self.size_A.get()
        
        
        # Base dimensions
        base_width = 700
        base_height = 600

        # Increase dimensions based on size (especially vertically)
        new_width = base_width + (size - 3) * 50
        new_height = base_height + (size - 3) * 100

        self.root.geometry(f"{new_width}x{new_height}")

    def generate_matrices(self):
        size_A = self.size_A.get()
        size_B = self.size_B.get()
        self.matrix_A = np.random.randint(1, 10, (size_A, size_A))
        self.matrix_B = np.random.randint(1, 10, (size_B, size_B))

    def update_matrix_display(self):
        for widget in self.matrix_frame_A.winfo_children():
            widget.destroy()
        for widget in self.matrix_frame_B.winfo_children():
            widget.destroy()

        task = self.task.get()
        if task == "Transpose":
            self.show_matrix(self.matrix_frame_A, self.matrix_A)
            self.matrix_frame_B.grid_remove()
            self.operator_label.grid_remove()
            self.size_label_A.config(text=f"Size: {self.size_A.get()} x {self.size_A.get()}")
            self.size_label_A.grid(row=2, column=0, columnspan=6)
            self.size_label_B.grid_remove()
        else:
            self.show_matrix(self.matrix_frame_A, self.matrix_A)
            self.show_matrix(self.matrix_frame_B, self.matrix_B)
            self.operator_label.config(text="+" if task == "Addition" else "x")
            self.operator_label.grid()
            self.size_label_A.config(text=f"Size: {self.size_A.get()} x {self.size_A.get()}")
            self.size_label_B.config(text=f"Size: {self.size_B.get()} x {self.size_B.get()}")
            self.matrix_frame_A.grid(row=1, column=0, pady=5, columnspan=2)
            self.matrix_frame_B.grid(row=1, column=3, pady=5, columnspan=2)
            self.size_label_A.grid(row=2, column=0, columnspan=2)
            self.size_label_B.grid(row=2, column=3, columnspan=2)

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
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def update_task(self, _):
        task = self.task.get()

        if task == "Transpose":
            self.label_matrix_B.grid_remove()
            self.size_menu_B.grid_remove()
            self.size_label_B.grid_remove()
        else:
            self.label_matrix_B.grid()
            self.size_menu_B.grid()
            self.size_label_B.grid()

        self.update_matrix_display()
        self.create_input_grid()
        # task = self.task.get()
        # self.size_menu_B.config(state=tk.NORMAL if task != "Transpose" else tk.DISABLED)
        # self.update_matrix_display()
        # self.create_input_grid()

    def update_size(self, _):
        self.generate_matrices()
        self.update_matrix_display()
        self.create_input_grid()
        self.adjust_window_size()

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
        try:
            user_matrix = np.array([
                [int(entry.get().strip()) for entry in row]
                for row in self.entries
            ])
        except ValueError:
            messagebox.showerror("Input Error", "Please enter only valid integers in all cells.")
            return

        correct_matrix = self.get_correct_answer()
        if np.array_equal(user_matrix, correct_matrix):
            messagebox.showinfo("Result", "✅ Correct! Great job!")
        else:
            messagebox.showerror("Result", f"❌ Incorrect.\n\nCorrect Answer:\n{correct_matrix}")

    def get_correct_answer(self):
        task = self.task.get()
        if task == "Transpose":
            return self.matrix_A.T
        elif task == "Addition":
            return self.matrix_A + self.matrix_B
        elif task == "Multiplication":
            return np.dot(self.matrix_A, self.matrix_B)

    def show_rules(self):
        rules = {
            "Transpose": "Transpose: Flip the matrix over its diagonal (rows become columns).",
            "Addition": "Addition: Add corresponding elements of Matrix A and Matrix B.",
            "Multiplication": "Multiplication: Multiply rows of Matrix A by columns of Matrix B."
        }
        rules_text = f"Welcome to the Matrix Learning Game!\n\n- {rules[self.task.get()]}\n\nFill in the result matrix and click 'Check Answer'."
        messagebox.showinfo("Matrix Rules", rules_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = MatrixGame(root)
    root.mainloop()
