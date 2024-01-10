import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
import python.annealing as sim
import matplotlib.pyplot as plt
import random as rdm
import visualizer.main as viz
from sim_annealing import *
import itertools

NB_INST = 3
NB_REP = 1

def test(proba_init, mult_epoch, inst):

    # print(f"start test with parameters :\np1: {proba_init}, mult_epoch: {mult_epoch}")
    average_best = 0
    for _ in range(NB_INST):
        sol = Solution_Farmers(inst)
        sol.initialize()
        for _ in range(NB_REP):
            nb_iterations, temperature_initial, cooling_rate = sim.generate_parameters(sol.copy(), proba_init, mult_epoch)
            # print(f"nb_iterations: {nb_iterations}, temperature_initial: {temperature_initial}, cooling_rate: {cooling_rate}")
            history = sim.simulated_annealing(sol.copy(), nb_iterations, temperature_initial, cooling_rate)
            # print(f"best : {history[-1].cost}")
            average_best += history[-1].cost


    return average_best/(NB_REP * NB_INST)

if __name__ == "__main__":
    rdm.seed()
    inst = Instance("data")
    epoch_mul = [1000, 5000, 10_000]
    proba_ini = [0.99, 0.4, 0.6, 0.8, 0.9]
    best = -1
    bestZ = 0
    for z in itertools.product(epoch_mul, proba_ini):
        print(f"start test {z}")
        e, p1 = z
        avg = test(0.9, 1000, inst)
        print(f"avg: {avg}")
        if best == -1 or avg < best:
            best = avg
            bestZ = z
    print(f"best -> {bestZ}: {best}")

