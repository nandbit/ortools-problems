from ortools.sat.python import cp_model

def solution_status(status):
    if status == cp_model.OPTIMAL:
        return "Optimal solution found"
    elif status == cp_model.FEASIBLE:
        return "Feasible solution found"
    elif status == cp_model.INFEASIBLE:
        return "No solution exists"
    elif status == cp_model.MODEL_INVALID:
        return "Model is invalid"
    elif status == cp_model.UNKNOWN:
        return "Unknown - solver stopped before finding a solution (e.g., timeout)"
