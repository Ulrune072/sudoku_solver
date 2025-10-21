import csv
import sys

# define function for read data from csv
def read_csv_to_grid(path):
    grid = []
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            parsed = []
            for cell in row:
                cell = cell.strip()
                if cell in ('', '.', '0'):
                    parsed.append(0)
                else:
                    try:
                        n = int(cell)
                        parsed.append(n if 1 <= n <= 9 else 0)
                    except ValueError:
                        parsed.append(0)
            grid.append(parsed)
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("CSV must contain 9 rows with 9 columns (use 0 or . for empty).")
    return grid

# define function for read data from txt (assuming space-separated or comma-separated values per line)
def read_txt_to_grid(path):
    grid = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Replace commas with spaces for uniform splitting
            row = [x.strip() for x in line.replace(',', ' ').split()]
            if len(row) != 9:
                continue  # Skip invalid rows
            parsed = []
            for cell in row:
                if cell in ('', '.', '0'):
                    parsed.append(0)
                else:
                    try:
                        n = int(cell)
                        parsed.append(n if 1 <= n <= 9 else 0)
                    except ValueError:
                        parsed.append(0)
            grid.append(parsed)
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("TXT must contain 9 rows with 9 columns (use 0 or . for empty, separated by spaces or commas).")
    return grid

# define function for manual input from terminal
def read_from_terminal():
    grid = []
    print("Enter the Sudoku grid row by row (9 rows, each with 9 values).")
    print("Use spaces or commas to separate values, and 0 or . for empty cells.")
    for i in range(9):
        while True:
            try:
                row_str = input(f"Row {i+1}: ").strip()
                # Replace commas with spaces for uniform splitting
                row = [x.strip() for x in row_str.replace(',', ' ').split()]
                if len(row) != 9:
                    raise ValueError("Each row must have exactly 9 values.")
                parsed = []
                for cell in row:
                    if cell in ('', '.', '0'):
                        parsed.append(0)
                    else:
                        try:
                            n = int(cell)
                            if not 1 <= n <= 9:
                                raise ValueError("Values must be between 1 and 9.")
                            parsed.append(n)
                        except ValueError:
                            raise ValueError(f"Invalid value: {cell}")
                grid.append(parsed)
                break
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
    return grid