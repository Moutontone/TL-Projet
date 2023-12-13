import fileReader as fr
import matplotlib.pyplot as plt
import random as rdm
from math import exp

import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance

class Instance():

    def __init__(self, datapath) -> None:
        self.nbClients, self.nbFarmers, self.capacity, self.ocationCost, self.costPerKm = fr.readInfoInstanceFile(datapath+'/info_instance.txt')
        self.coordinates = fr.readCoordFile(datapath+'/coordinates.txt')# for each point we have list of 2 values [x, y] size=(60,2) first depot, next farmers, next clients
        self.distanceMatrix = fr.readDistanceMatrixFile(datapath+'/cost_matrix.txt') # for each point we have a list of distance to points size=(60,60)
        self.demands = fr.readDemandMatrixFile(datapath+'/demands.txt') # size=(208,39,21)

        self.hub = [0]
        self.farmers = [i for i in range(1,self.nbFarmers+1)]
        self.clients = [i for i in range(self.nbFarmers+1,self.nbFarmers+self.nbClients+1)]
        # self.tours = [t for t in range(self.nbFarmers)]
        self.relevant = [i for i in range(self.nbFarmers+1)]
        self.demands = self.demands[1:]#first line is empty

        self.day(0)



    def day(self, d):
        self.day = d

        # sum of all demands for farmer i (we supppose that we take everything at once from a farmer)
        self.sum_demand_farmers = [0 for _ in self.farmers]
        for i in self.farmers:
            for k in self.clients:
                self.sum_demand_farmers[i-1] += self.demands[self.day][k-self.nbFarmers-1][i-1]
            # to check feasibility of capacity constraint
            # print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))
            assert self.sum_demand_farmers[i-1] <= self.capacity
            if self.sum_demand_farmers[i-1] > self.capacity:
                print('\nERROR: The solver can not yet modelize a problem with higher single farmer demand than capacity\n')

        self.sum_demand_clients = [0 for _ in self.clients]
        for i in self.clients:
            for k in self.farmers:
                self.sum_demand_clients[i - 1 - self.nbFarmers] += self.demands[self.day][i - 1 - self.nbFarmers][k-1]


    def dist(self, i, j):
        return self.distanceMatrix[i][j]

    def sum_demand_farmer(self, i):
        return self.sum_demand_farmers[i-1]
        

class Solution1():

    empty = True
    val = None

    def __init__(self, inst) -> None:
       self.inst = inst

    def initialize(self) -> None:
        self.sol = [k for k in inst.farmers]
        rdm.shuffle(self.sol)
        self.empty = False
        self.evaluate()

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

    def generate_neighbor(self):
        i,j = rdm.sample(range(len(self.sol)), 2)
        neighbor = self.copy()
        neighbor.swap(i, j)
        neighbor.evaluate()
        return neighbor
        pass

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
        new = Solution1(self.inst)
        new.empty = self.empty
        new.val = self.val
        new.dist = self.dist 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.dist) + " " + self.sol.__str__() 

"""
    Simulated annealing
"""

def simulated_annealing(sol, max_iteration, temperature_initial):
    # init parameters
    iteration = 0
    temperature = temperature_initial
    history = [sol.dist]
    # main loop
    while(iteration < max_iteration):
        neighbor = sol.generate_neighbor()
        if proba_accept(temperature, neighbor.dist, sol.dist) > rdm.random():
            sol = neighbor
        # update parameters
        iteration += 1
        temperature = cooling(temperature)
        history.append(sol.dist)
    return history

def proba_accept(T, candidat, sol):
    if candidat < sol:
        return 1.
    return exp((sol - candidat) / T)

def cooling(t):
    return t * 0.95


"""
    Main 
"""
if __name__ == "__main__":
    rdm.seed()
    inst = Instance("../data")
    sol = Solution1(inst)
    sol.initialize()
    max_iterations = 1000
    t0 = 1000
    values = simulated_annealing(sol, max_iterations, t0)
    # plot
    Ys = values
    plt.plot(Ys)
    plt.ylim(0, max(Ys) * 1.1)
    plt.show()

    print(f"result: {values[-1]}")


"""
todo and optimizations
    do better code.
    verify how good it is. make some test
    do version for other pbs
"""
