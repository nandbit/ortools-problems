# Given N vertices, and M edges, assign a color to each vertex
# such that no adjacent vertices have the same color.
# Adjacent vertices are those that have an edge between them.
# Use as few colors as possible.

from ortools.sat.python import cp_model

from utils import solution_status
# 0 --- 1
# |   / |
# |  /  |
# | /   |
# 2 --- 3
# |     |
# 4 --- 5
num_vertices = 6
edges = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 5),
]

model = cp_model.CpModel()

colors = []

for v in range(1, num_vertices + 1):
    colors.append(model.new_int_var(0, num_vertices, f"vertex_{v}_color"))

for edge in edges:
    model.add(colors[edge[0]] != colors[edge[1]])

num_colors = model.new_int_var(1, num_vertices, "num_colors")

for color in colors:
    model.add(num_colors > color)

model.minimize(num_colors)

solver = cp_model.CpSolver()

status = solver.solve(model)
print(solution_status(status))

print(f"Solved using {solver.value(num_colors)} colors")
for i in range(len(colors)):
    print(solver.value(colors[i]))
