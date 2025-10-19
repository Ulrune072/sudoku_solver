import tkinter as tk
from tkinter import messagebox, filedialog
import csv
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

        tk.Button(button_frame, text="Load CSV", command=self.load_csv).grid(row=0, column=0, padx=5)
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

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            grid = [[int(x) if x else 0 for x in row] for row in reader]
        self.write_grid_to_ui(grid)

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