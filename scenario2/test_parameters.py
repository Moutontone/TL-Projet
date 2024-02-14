import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
import python.annealing as sim
import random as rdm
from sim_annealing import *
import itertools

NB_INST = 3
NB_REP = 3

def test(proba_init, mult_epoch, proba_last, inst):

    res = []
    for _ in range(NB_INST):
        sol = Solution_general(inst)
        sol.initialize()
        for _ in range(NB_REP):
            history = sim.simulated_annealing(sol.copy(), proba_init, mult_epoch, proba_last)
            res.append(history[-1].cost)

    avg = sum(res)/len(res)
    var = sum([(x - avg)**2 for x in res])/(len(res)-1)

    return avg, var

if __name__ == "__main__":
    rdm.seed()
    inst = Instance("data")
    epoch_mul = [10, 100]
    proba_ini = [0.2, 0.4]
    proba_last = [0.01]
    bestAvg = -1
    bestZ = 0
    bestVar = 0
    for z in itertools.product(epoch_mul, proba_ini, proba_last):
        print(f"start test {z}")
        e, p1, pl = z
        avg, var = test(p1, e, pl, inst)
        print(f"avg: {avg}, var: {var}")
        print()
        if bestAvg == -1 or avg < bestAvg:
            bestAvg = avg
            bestZ = z
            bestVar = var
    print(f"best {bestZ} -> avg: {bestAvg}, var: {bestVar}")

