# There is an assembly line with workstations
# There are N tasks, each with:
#  - Duration t_i
#  - Precedence constraints
#  - Cycle time C (maximum time allowed per workstation)
#
# Goal:
#  - Assign tasks to the set number of workstations such that:
#   - Each task assigned to exactly one workstation
#   - Precedence constraints respected (if task A must precede task B, they can be at the same station only if A comes first, or A at an earlier station)
#
# Minimize the cycle time

from ortools.sat.python import cp_model

from utils import solution_status

tasks = [
    {"duration": 3, "predecessors": []},
    {"duration": 2, "predecessors": [0]},
    {"duration": 4, "predecessors": [0]},
    {"duration": 1, "predecessors": [1]},
    {"duration": 2, "predecessors": [2]},
    {"duration": 3, "predecessors": [3, 4]},
]

num_stations = 3

model = cp_model.CpModel()

max_cycle_time = model.new_int_var(0, sum([x['duration'] for x in tasks]), "max_cycle_time")

# Task assignment
station_of_task = []
for i in range(len(tasks)):
    station_of_task.append(model.new_int_var(0, num_stations-1, f"station_of_task_{i}"))

# Boolean vars of whether task i is assigned to station j
task_is_at_station = {}
for i in range(len(tasks)):
    for j in range(num_stations):
        task_is_at_station[i, j] = model.new_bool_var(f"task_{i}_assigned_to_station_{j}")

# Tying together assignment and boolean vars
for i in range(len(tasks)):
    for j in range(num_stations):
        model.add(station_of_task[i] == j).only_enforce_if(task_is_at_station[i, j])
        model.add(station_of_task[i] != j).only_enforce_if(task_is_at_station[i, j].Not())

# Precedence constraint
for i in range(len(tasks)):
    for j in tasks[i]['predecessors']:
        model.add(station_of_task[i] >= station_of_task[j])

# Cycle time
for i in range(num_stations):
    cycle_time = 0
    for j in range(len(tasks)):
        cycle_time = cycle_time + (tasks[j]['duration'] * task_is_at_station[j, i])
    model.add(max_cycle_time >= cycle_time)

model.minimize(max_cycle_time)

solver = cp_model.CpSolver()
solution = solver.solve(model)

print(solution_status(solution))

print(f"Number of stations used: {solver.value(num_stations)}")
print(f"Cycle time: {solver.value(max_cycle_time)}")

for i in range(len(tasks)):
    result_task_is_at_station = solver.value(station_of_task[i])
    print(f"Task {i} is assigned to station {result_task_is_at_station}")
