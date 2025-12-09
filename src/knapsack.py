# Given weights and profits of a set of items, as well as a maximum
# capacity, choose items which maximize profit.

from ortools.sat.python import cp_model

from utils import solution_status

weights = [2, 3, 4, 5]
profits = [3, 4, 5, 6]
capacity = 8

model = cp_model.CpModel()

item_taken = []
for i in range(len(weights)):
    item_taken.append(model.new_bool_var(f"item_{i}_taken"))

profit = 0
for i in range(len(profits)):
    profit = profit + (profits[i] * item_taken[i])

load = 0
for i in range(len(weights)):
    load = load + (weights[i] * item_taken[i])

model.add(load <= capacity)
model.maximize(profit)

solver = cp_model.CpSolver()
solution = solver.solve(model)

print(solution_status(solution))
print(f"Optimal profit: {solver.value(profit)}")

for i in range(len(item_taken)):
    if solver.value(item_taken[i]) == 1:
        print(f"Item {i} taken")
