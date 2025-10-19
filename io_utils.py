import csv

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
