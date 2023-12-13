import fileReader as fr
import matplotlib.pyplot as plt
import random as rdm
from math import exp


import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
        

class Solution():

    empty = True
    val = None

    def __init__(self, inst) -> None:
       self.inst = inst

    def initialize(self) -> None:
        self.sol = [k for k in inst.farmers]
        rdm.shuffle(self.sol)
        self.empty = False

    def evaluate(self):
        if self.empty:
            return
        dist = 0
        q = 0
        q_max = self.inst.capacity
        last_loc = 0
        self.vehicules = 0
        # fist farmer
        for f in self.sol:
            # go to depot if capacity is not enought for the next stop
            if q + self.inst.sum_demand_farmer(f) > q_max:
                self.vehicules += 1
                q = 0
                dist += self.inst.dist(last_loc, 0)
                last_loc = 0
            q += self.inst.sum_demand_farmer(f) 
            dist += self.inst.dist(last_loc, f)
            last_loc = f
        self.dist = dist

    def generate_neighbors(self):
        neighbors = []
        # Iterate through each index in the solution
        for i in range(len(self.sol)):
            for j in range(i + 1, len(self.sol)):
                neighbor = self.copy()
                neighbor.swap(i, j)
                neighbors.append(neighbor)
        return neighbors


    def swap(self, i, j):
        self.sol[i], self.sol[j] = self.sol[j], self.sol[i]

    def copy(self):
        new = Solution(self.inst)
        new.empty = self.empty
        new.val = self.val
        new.dist = self.dist 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.dist) + " " + self.sol.__str__() 


def simulated_annealing(inst):
    sol = Solution(inst)
    sol.initialize()
    sol.evaluate()
    print(f"starting simulated annealing")
    iteration = 0
    T = 1000
    val = [sol.dist]
    max_iteration = 1000
    while(iteration < max_iteration ):
        print(f"sol: {sol}\nT: {T}, iteration {iteration}")
        iteration += 1
        T = T * 0.95
        neighbors = sol.generate_neighbors() 
        candidate_sol = rdm.choice(neighbors)
        candidate_sol.evaluate()
        if proba_accept(T, candidate_sol.dist, sol.dist) > rdm.random():
            sol = candidate_sol
        val.append(sol.dist)
    return val
def proba_accept(T, candidat, sol):
    if candidat < sol:
        return 1.
    return exp((sol - candidat) / T)

if __name__ == "__main__":
    inst = Instance("data")
    val = simulated_annealing(inst)
    print("end of simulated annealing")
    # plot
    Ys = val
    plt.plot(Ys)
    plt.ylim(0, max(Ys) * 1.1)
    plt.show()


"""
todo and optimizations:
    do better code.
    generate neighbors one by one as needed
    abstract a bit more the simulated annealing
    verify how good it is. make some test
    do versino for other pbs
"""
