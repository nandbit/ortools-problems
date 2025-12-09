# There is 1 machine and N jobs. 
# Each job has processing time p_j (duration)
# Some jobs must finish before others can start
#
# Goal: Schedule all jobs on the machine to minimize total completion time (makespan) while respecting:
#   - No two jobs overlap
#   - Precedence constraints (e.g. job B can't start until job A finishes)

from ortools.sat.python import cp_model

from utils import solution_status

jobs = [
    {"duration": 3, "predecessors": []},      # Job 0: can start immediately
    {"duration": 2, "predecessors": [0]},     # Job 1: needs Job 0 to finish first
    {"duration": 4, "predecessors": [0]},     # Job 2: needs Job 0 to finish first
    {"duration": 2, "predecessors": [1, 2]},  # Job 3: needs both Job 1 and 2 to finish first
]

model = cp_model.CpModel()

horizon = sum([item['duration'] for item in jobs])

starts = []
ends = []
intervals = []
makespan = horizon
for i in range(len(jobs)):
    start = model.new_int_var(0, horizon, f"start_of_job_{i}")
    end = model.new_int_var(0, horizon, f"end_of_job_{i}")
    duration = model.new_interval_var(start, jobs[i]['duration'], end, f"job_{i}_interval")

    starts.append(start)
    intervals.append(duration)
    ends.append(end)

for i in range(len(jobs)):
    for j in jobs[i]['predecessors']:
        model.add(starts[i] >= ends[j])

model.add_no_overlap(intervals)

solver = cp_model.CpSolver()
solution = solver.solve(model)

print(solution_status(solution))

if solution == cp_model.OPTIMAL or solution == cp_model.FEASIBLE:
    print(f"\nMakespan: {solver.value(makespan)}\n")
    
    for i in range(len(jobs)):
        start_time = solver.value(starts[i])
        end_time = solver.value(ends[i])
        print(f"Job {i}: starts at {start_time}, ends at {end_time} (duration: {jobs[i]['duration']})")
else:
    print("No solution found")
