import random as rdm
from math import exp
import numpy as np


def proba_accept(T, cost_candidate, cost_sol):
    if cost_candidate < cost_sol:
        return 1.
    return exp((cost_sol - cost_candidate) / T)

def cooling_naive(t, alpha):
    return t * alpha

def delta_moy(solution, epoch):
    delta = 0
    for _ in range(epoch):
        neighbor = solution.generate_neighbor()
        diff = neighbor.cost - solution.cost
        if diff > 0: 
            delta += diff
        solution = neighbor
    return delta / epoch 

def generate_parameters(sol, proba_init, mult_epoch, proba_last):
    # neighboorhood size
    n = len(sol.sol)
    neighborhood_size = int(n*(n-1)/2)
    # number of epoch
    nb_iterations = int(mult_epoch * neighborhood_size)
    # calculate T0
    delta = delta_moy(sol, neighborhood_size * 2)
    temperature_initial = - delta / np.log(proba_init)
    # calculated cooling factor
    Tm = - delta / np.log(proba_last)
    cooling_rate = (Tm / temperature_initial) ** (1/(nb_iterations-1))
    return nb_iterations, temperature_initial, cooling_rate
    

def simulated_annealing(sol, proba_init, mult_epoch, proba_last):
    nb_iterations, temperature_initial, cooling_rate = generate_parameters(sol.copy(), proba_init, mult_epoch, proba_last)
    # print(f"{nb_iterations, temperature_initial, cooling_rate}")
    return simulated_annealing_alg(sol, nb_iterations, temperature_initial, cooling_rate)

def simulated_annealing_alg(solution_initial, max_iteration, temperature_initial, cooling_rate, proba_fn = proba_accept, cooling_fn = cooling_naive):
    """
    Perform simulated annealing optimization to minimize the cost of a solution.

    Returns:
    - list: Cost history, showing the cost of the solution at each iteration.
    """
    # init parameters
    iteration = 0
    temperature = temperature_initial
    solution = solution_initial
    history = [solution]
    # main loop
    while(iteration < max_iteration):
        neighbor = solution.generate_neighbor()
        if proba_fn(temperature, neighbor.cost, solution.cost) > rdm.random():
            solution = neighbor
        # update parameters
        iteration += 1
        temperature = cooling_fn(temperature, cooling_rate)
        history.append(solution)
    return history

