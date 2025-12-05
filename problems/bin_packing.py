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

items = [4, 8, 1, 4, 2, 1]
max_capacity = 10


