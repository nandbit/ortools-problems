# There are M workers and N jobs.
# Each job has:
#   - Processing time t_j (how long it takes)
#   - Skill requirement s_j (e.g., "coding", "testing", "design")
#
# Each worker has:
#   - Skills they can perform (subset of all skills)
#   - Capacity C_i (max total time they can work)
#
# Goal: Assign each job to exactly one worker such that:
#   - Each job is assigned to a worker with the required skill
#   - No worker exceeds their time capacity
#   - Minimize the maximum workload across all workers (balance the load fairly)

from collections import defaultdict
from ortools.sat.python import cp_model

from utils import solution_status

jobs = [
    {"time": 3, "skill": "code"},
    {"time": 5, "skill": "test"},
    {"time": 2, "skill": "code"},
    {"time": 4, "skill": "design"},
    {"time": 3, "skill": "test"},
]

workers = [
    {"capacity": 8, "skills": ["code", "test"]},
    {"capacity": 7, "skills": ["test", "design"]},
    {"capacity": 6, "skills": ["code", "design"]},
]

model = cp_model.CpModel()

# This could be condensed in less loops but this is nice and explicit
# easier to read. The time bottleneck is still in the solver not in
# the problem definition.

largest_capacity = 0
for i in range(len(workers)):
    capacity = workers[i]['capacity']
    if capacity >= largest_capacity:
        largest_capacity = capacity

max_workload = model.new_int_var(0, largest_capacity, "max_workload")

assignments = {} # job : worker
for i in range(len(jobs)):
    for j in range(len(workers)):
        # job i is assigned to worker j
        assignments[i, j] = model.new_bool_var(f"job_{i}_assigned_to_worker_{j}")

# ensure every job is only assigned to one worker
for i in range(len(jobs)):
    assignment = 0
    for j in range(len(workers)):
        assignment = assignment + assignments[i, j]
    model.add(assignment == 1)

# add skill matching
for i in range(len(jobs)):
    for j in range(len(workers)):
        if jobs[i]['skill'] not in workers[j]['skills']:
            model.add(assignments[i, j] == 0)
    
# ensure no workers exceeds their capacity
for i in range(len(workers)):
    load = 0
    for j in range(len(jobs)):
        load = load + (jobs[j]['time'] * assignments[j, i])
    model.add(max_workload >= load)
    model.add(load <= workers[i]['capacity'])

model.minimize(max_workload)

solver = cp_model.CpSolver()
solution = solver.solve(model)


# -------------------- SOLUTION PRINTING -----------------------
print(solution_status(solution))

worker_time = defaultdict(int)
for i in range(len(jobs)):
    for j in range(len(workers)):
        assignment = solver.value(assignments[i, j])
        if assignment == 1:
            worker_time[j] += jobs[i]['time']
            print(f"Job {i} assigned to worker {j}")

for k, v in worker_time.items():
    print(f"Worker {k} work time: {v}")
