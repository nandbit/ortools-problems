# Resource-Constrained Project Scheduling Problem
# N jobs, each with:
#  - Duration d_j
#  - Resource requirements (e.g., needs 2 workers, 1 machine)
#  - Precedence constraints
#
# M resource types, each with:
#  - Capacity C_r (e.g., 3 workers available, 2 machines available)
#
# Goal
#  - Schedule all jobs to minimize makespan while:
#   - Respecting precedence constraints
#   - Ensuring total resource usage never exceeds capacity

from ortools.sat.python import cp_model

from utils import solution_status

jobs = [
    {"duration": 3, "workers": 2, "machines": 1, "predecessors": []},
    {"duration": 2, "workers": 1, "machines": 1, "predecessors": [0]},
    {"duration": 4, "workers": 2, "machines": 0, "predecessors": [0]},
    {"duration": 2, "workers": 1, "machines": 1, "predecessors": [1, 2]},
]

resources = {
    "workers": 3,
    "machines": 2,
}

model = cp_model.CpModel()

horizon = sum([x['duration'] for x in jobs])

starts = []
ends = []
intervals = []

for i in range(len(jobs)):
    start = model.new_int_var(0, horizon, f"job_{i}_start")
    end = model.new_int_var(0, horizon, f"job_{i}_end")
    interval = model.new_interval_var(start, jobs[i]['duration'], end, f"job_{i}_interval")

    starts.append(start)
    ends.append(end)
    intervals.append(interval)

for i in range(len(jobs)):
    for j in jobs[i]['predecessors']:
        model.add(starts[i] >= ends[j])

worker_demands = [j['workers'] for j in jobs]
machine_demands = [j['machines'] for j in jobs]

model.add_cumulative(intervals, worker_demands, resources['workers'])
model.add_cumulative(intervals, machine_demands, resources['machines'])

makespan = model.new_int_var(0, horizon, 'makespan')

for i in range(len(jobs)):
    model.add(makespan >= ends[i])

model.minimize(makespan)

solver = cp_model.CpSolver()
solution = solver.solve(model)

# -------------------- SOLUTION PRINTING -----------------------
print(solution_status(solution))

for i in range(len(jobs)):
    print(f"Job {i} starts at: {solver.value(starts[i])} ends at {solver.value(ends[i])}")
