import tkinter as tk
from tkinter import messagebox, filedialog
from io_utils import read_csv_to_grid, read_txt_to_grid  # Import io_utils functions
from solver import solve_sudoku

CELL_SIZE = 50
FONT = ("Arial", 20, "bold")
BG_NORMAL = "#ffffff"
BG_ALT = "#e9f1ff"
BORDER_COLOR = "#000000"

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = []
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        frame = tk.Frame(self.root, bg=BORDER_COLOR, padx=2, pady=2)
        frame.pack(padx=10, pady=10)

        for r in range(9):
            row = []
            for c in range(9):
                bg = BG_ALT if (r // 3 + c // 3) % 2 == 0 else BG_NORMAL

                entry = tk.Entry(
                    frame,
                    width=2,
                    font=FONT,
                    justify="center",
                    bg=bg,
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#888888",   # thin inner grid lines
                    highlightcolor="#888888"
                )

                # Determine padding for thick 3x3 borders
                pad_x = (2 if c % 3 == 0 else 0, 2 if (c + 1) % 3 == 0 else 0)
                pad_y = (2 if r % 3 == 0 else 0, 2 if (r + 1) % 3 == 0 else 0)

                entry.grid(row=r, column=c, padx=pad_x, pady=pad_y)
                row.append(entry)

            self.entries.append(row)

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Load File", command=self.load_file).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Solve", command=self.solve).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

    def get_grid_from_ui(self):
        grid = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.entries[r][c].get()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid

    def write_grid_to_ui(self, grid):
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                self.entries[r][c].delete(0, tk.END)
                if val != 0:
                    self.entries[r][c].insert(0, str(val))

    def clear(self):
        for row in self.entries:
            for e in row:
                e.delete(0, tk.END)
        self.status_label.config(text="")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        if not file_path:
            return
        try:
            # Check file extension and use appropriate reader
            if file_path.endswith('.csv'):
                grid = read_csv_to_grid(file_path)
            elif file_path.endswith('.txt'):
                grid = read_txt_to_grid(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file type. Use .csv or .txt.")
                return
            self.write_grid_to_ui(grid)
            self.status_label.config(text="File loaded successfully.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def solve(self):
        grid = self.get_grid_from_ui()
        solution, stats = solve_sudoku(grid)
        if solution is None:
            messagebox.showinfo("No Solution", "Puzzle cannot be solved.")
            return
        self.write_grid_to_ui(solution)
        self.status_label.config(
            text=f"Solved in {stats['time']:.3f}s | Steps: {stats['steps']} | Backtracks: {stats['backtracks']}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()