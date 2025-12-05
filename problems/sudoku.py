# It's sudoku

from ortools.sat.python import cp_model

puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

model = cp_model.CpModel()
rows = []
N = 9

for r in range(N):
    row = []
    for c in range(N):
        value = puzzle[r][c]
        if (value != 0):
            row.append(model.new_constant(value))
            continue
        row.append(model.new_int_var(1, N, f"value_{r}_{c}"))
    rows.append(row)

for i in range(len(rows)):
    model.add_all_different(rows[i])
    model.add_all_different([row[i] for row in rows])


for r in range(0, N, 3):
    for c in range(0, N, 3):
        sub_matrix = []
        for j in range(3):
            for k in range(3):
                sub_matrix.append(rows[j+r][k+c])
        model.add_all_different(sub_matrix)

solver = cp_model.CpSolver()

status = solver.solve(model)

if status == cp_model.OPTIMAL:
    print("Optimal solution found")
elif status == cp_model.FEASIBLE:
    print("Feasible solution found")
elif status == cp_model.INFEASIBLE:
    print("No solution exists")
elif status == cp_model.MODEL_INVALID:
    print("Model is invalid")
elif status == cp_model.UNKNOWN:
    print("Unknown - solver stopped before finding a solution (e.g., timeout)")

for row in range(N):
    if (row % 3 == 0) and row != 0:
        print("-------------------")
    for col in range(N):
        if (col % 3 == 0) and col != 0:
            print("|", end="")
        value = solver.value(rows[row][col])
        print(f"{value} ", end="")
    print("\n", end="")
