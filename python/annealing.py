import random as rdm
from math import exp


def proba_accept(T, cost_candidate, cost_sol):
    if cost_candidate < cost_sol:
        return 1.
    return exp((cost_sol - cost_candidate) / T)

def cooling_naive(t):
    return t * 0.98

def simulated_annealing(solution_initial, max_iteration, temperature_initial, proba_fn = proba_accept, cooling_fn = cooling_naive):
    """
    Perform simulated annealing optimization to minimize the cost of a solution.

    Returns:
    - list: Cost history, showing the cost of the solution at each iteration.
    """
    # init parameters
    iteration = 0
    temperature = temperature_initial
    sol = solution_initial
    cost_history = [sol.cost]
    # main loop
    while(iteration < max_iteration):
        neighbor = sol.generate_neighbor()
        if proba_fn(temperature, neighbor.cost, sol.cost) > rdm.random():
            sol = neighbor
        # update parameters
        iteration += 1
        temperature = cooling_fn(temperature)
        cost_history.append(sol.cost)
    return sol, cost_history
