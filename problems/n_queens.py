from ortools.sat.python import cp_model

N = 8

model = cp_model.CpModel()

queens: list[cp_model.IntVar] = [] # index: row value: column
diagonals_pos: list[cp_model.LinearExprT] = []
diagonals_neg: list[cp_model.LinearExprT] = []

for i in range(N):
    queens.append(model.new_int_var(0, N, f"queen_at_row_{i}"))
    diagonals_pos.append(queens[i] + i)
    diagonals_neg.append(queens[i] - i)

model.add_all_different(queens)
model.add_all_different(diagonals_pos)
model.add_all_different(diagonals_neg)

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

for i in range(N):
    print(solver.value(queens[i]))

for i in range(N):
    col = solver.value(queens[i])
    row_str = ". " * col + "Q " + ". " * (N - col - 1)
    print(row_str)
