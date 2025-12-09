# Goal: Pack a set of items with different sizes into the fewest number of fixed-capacity bins
#
# Given:
#  - N items, each with a size/weight
#  - M Bins with a fixed capacity
#
# Find:
#  - An assignment of each item to a bin using as few bins as possible
# 
# Conditions
#  - No bin exceeds its capacity
#  - All bins are identical
#
# We're trying to minimize M

from ortools.sat.python import cp_model

from utils import solution_status

items = [4, 8, 1, 4, 2, 1]
max_capacity = 10

model = cp_model.CpModel()

# Initial number of bins is len(items)

bin_used = []
for i in range(len(items)):
    bin_used.append(model.new_bool_var(f"bin_{i}_used"))

# Boolean variables for items being in bins
# is in that bin
item_in_bin = {} # bin : item
for i in range(len(items)): # for each bin
    for j in range(len(items)): # for each item
        item_in_bin[i, j] = model.new_bool_var(f"item_{j}_in_bin_{i}")

# Ensure that each item is only in one bin
for i in range(len(items)): # for each item
    total = 0
    for j in range(len(items)): # for each bin
        total += item_in_bin[j, i]
    model.add(total == 1)

# Ensure that capacity of each bin doesn't exceed max
for i in range(len(items)): # for each bin
    load = 0
    for j in range(len(items)): # for each item
      # load = load + item_weight * (0 or 1)
      # so if item is in this bin, add its weight to the load  
        load = load + items[j] * item_in_bin[i, j]
    model.add(load <= max_capacity)

# Make bin used to TRUE if there is an item in it
for i in range(len(items)): # for each bin
    for j in range(len(items)): # for each item
        # if item_in_bin is 1 then bin used will be <= 1
        # if item_in_bin is 0 then bin used will be <= 0
        model.add(item_in_bin[i, j] <= bin_used[i])

model.minimize(sum(bin_used))
solver = cp_model.CpSolver()

status = solution_status(solver.solve(model))
print(status)


print(f"Bins used: {solver.value(sum(bin_used))}")
for k, v in item_in_bin.items():
    if (solver.value(v) == 1):
        print(f"Item {k[1]} in bin {k[0]}")
    
