import time

# Define function for take non empty values from row

def row_vals(grid, r):
    return set(grid[r]) - {0}

# Define function for take non empty values from column

def col_vals(grid, c):
    return {grid[r][c] for r in range(9)} - {0}

# Define function for take non empty values from sub grid

def box_vals(grid, r, c):
    br, bc = 3 * (r // 3), 3 * (c // 3)
    vals = set()
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            v = grid[rr][cc]
            if v:
                vals.add(v)
    return vals

# Define function for take values that can be put in empty cells

def candidates(grid, r, c):
    used = row_vals(grid, r) | col_vals(grid, c) | box_vals(grid, r, c)
    return set(range(1, 10)) - used

# Define function for take cells with the less amount of candidates for less posibility of error

def select_mrv_cell(grid):
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = candidates(grid, r, c)
                if not cand:
                    return (r, c, set())  # prune: no valid candidate
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if len(cand) == 1:
                        return best
    return best


# Check duplicate in row, column and sub grids, if yes - return False.

def is_valid_placement(grid, r, c, val):
    if val in row_vals(grid, r): return False
    if val in col_vals(grid, c): return False
    if val in box_vals(grid, r, c): return False
    return True

# Check, do grid follow rules after put a specific value in empty cell

def is_valid_grid(grid):
    for i in range(9):
        row = [x for x in grid[i] if x != 0]
        if len(row) != len(set(row)):
            return False
        col = [grid[r][i] for r in range(9) if grid[r][i] != 0]
        if len(col) != len(set(col)):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = []
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    v = grid[r][c]
                    if v != 0:
                        block.append(v)
            if len(block) != len(set(block)):
                return False
    return True


def solve_sudoku(grid):
    # if not valid grid - return None
    if not is_valid_grid(grid):
        return None, {"steps": 0, "backtracks": 0, "time": 0.0}

    # create a copy of grid for backtrack and create some stats
    grid_copy = [row[:] for row in grid]
    stats = {"steps": 0, "backtracks": 0}
    start_time = time.perf_counter()

    # define backtrack function
    def backtrack():
        # choose the best candidates cell for solving sudoku
        sel = select_mrv_cell(grid_copy)
        if sel is None:
            return [row[:] for row in grid_copy]  # solved

        r, c, cand = sel
        if not cand:
            return None
        # check each possible values from candidates list, if is write - put them, if not backtrack
        for val in sorted(cand):
            if is_valid_placement(grid_copy, r, c, val):
                stats["steps"] += 1
                grid_copy[r][c] = val
                result = backtrack()
                if result is not None:
                    return result
                # Backtrack
                grid_copy[r][c] = 0
                stats["backtracks"] += 1
        return None

    solution = backtrack()
    stats["time"] = time.perf_counter() - start_time
    return solution, stats