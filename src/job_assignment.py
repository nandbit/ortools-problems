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

job_is_assigned = []
for i in range(len(jobs)):
    job_is_assigned.append(model.new_bool_var(f"job_{i}_is_assigned"))

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
        model.add(jobs[i]['skill'] in workers[j]['skills']).only_enforce_if(assignments[i, j])
    
# ensure no workers exceeds their capacity
for i in range(len(workers)):
    load = 0
    for j in range(len(jobs)):
        load = load + (jobs[j]['time'] * assignments[j, i])
    model.add(load <= workers[i]['capacity'])

# ensure every job is assigned
model.add(sum(job_is_assigned) == len(jobs))

solver = cp_model.CpSolver()
solution = solver.solve(model)


# -------------------- SOLUTION PRINTING -----------------------
print(solution_status(solution))

total = 0
for i in range(len(jobs)):
    total += solver.value(job_is_assigned[i])

if total == len(jobs):
    print("All jobs assigned")

worker_time = defaultdict(int)
for i in range(len(jobs)):
    for j in range(len(workers)):
        assignment = solver.value(assignments[i, j])
        if assignment == 1:
            worker_time[j] += jobs[i]['time']
            print(f"Job {i} assigned to worker {j}")

for k, v in worker_time.items():
    print(f"Worker {k} work time: {v}")
