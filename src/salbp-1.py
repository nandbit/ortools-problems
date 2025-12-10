# There is an assembly line with workstations
# There are N tasks, each with:
#  - Duration t_i
#  - Precedence constraints
#  - Cycle time C (maximum time allowed per workstation)
#
# Goal:
#  - Assign tasks to the minimum number of workstations such that:
#   - Each task assigned to exactly one workstation
#   - Precedence constraints respected (if task A must precede task B, they can be at the same station only if A comes first, or A at an earlier station)
#   - Total time at each workstation ≤ cycle time C
#
# Precedence graph
#
#    0 (3)
#   / \
#  1   2
# (2) (4)
#  |   |
#  3   4
# (1) (2)
#   \ /
#    5
#   (3)

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

cycle_time = 6

model = cp_model.CpModel()

num_stations = model.new_int_var(0, len(tasks), "num_workstations")

# Is the station being used
station_assigned = []
for i in range(len(tasks)):
    station_assigned.append(model.new_bool_var(f"station_{i}_assigned"))

# Which station task is assigned to
station_of_task = []
for i in range(len(tasks)):
    station_of_task.append(model.new_int_var(0, len(tasks), f"station_of_task_{i}"))

# Task i assigned to station j
task_is_at_station = {}
for i in range(len(tasks)): # for each task
    for j in range(len(tasks)): # for each workstation
        task_is_at_station[i, j] = model.new_bool_var(f"task_{i}_assigned_to_station_{j}")

# Link task -> station assignment to the boolean vars
for i in range(len(tasks)): # for each task
    for j in range(len(tasks)): # for each workstation
        model.add(station_of_task[i] == j).only_enforce_if(task_is_at_station[i, j])

        # Without the following line, the solver can set station_of_task[i] == j
        # but leave task_is_at_station[i, j] as 0
        model.add(station_of_task[i] != j).only_enforce_if(task_is_at_station[i, j].Not())

# ensure every task is only assigned to one station
for i in range(len(tasks)):
    assignment = 0
    for j in range(len(tasks)):
        assignment = assignment + task_is_at_station[i, j]
    model.add(assignment == 1)

# Set station to NOT assigned if it has no tasks
for j in range(len(tasks)): # for each workstation
    for i in range(len(tasks)): # for each task
        model.add(task_is_at_station[i, j] <= station_assigned[j])

# Precedence constraint
for i in range(len(tasks)): # for each workstation
    for j in tasks[i]['predecessors']: # for each of its predecessors
        model.add(station_of_task[j] <= station_of_task[i])

# Ensure that each station doesn't exceed cycle time
for i in range(len(tasks)): # for each workstation
    load = 0
    for j in range(len(tasks)): # for each task
        load = load + (tasks[j]['duration'] * task_is_at_station[j, i])
    model.add(load <= cycle_time)

model.add(num_stations == sum(station_assigned))

model.minimize(num_stations)

solver = cp_model.CpSolver()
solution = solver.solve(model)

print(solution_status(solution))

print(f"Number of stations used: {solver.value(num_stations)}")

for i in range(len(tasks)):
    result_station_assigned = solver.value(station_assigned[i])
    if result_station_assigned == 1:
        print(f"Station {i} is used")

for i in range(len(tasks)):
    result_task_is_at_station = solver.value(station_of_task[i])
    print(f"Task {i} is assigned to station {result_task_is_at_station}")
