import fileReader as fr
import matplotlib.pyplot as plt
import random as rdm
from math import exp

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
        self.day = 0

        # sum of all demands for farmer i (we supppose that we take everything at once from a farmer)
        self.demandSums = [0 for i in self.farmers]
        for i in self.farmers:
            for k in self.clients:
                self.demandSums[i-1] += self.demands[self.day][k-self.nbFarmers-1][i-1]
            # to check feasibility of capacity constraint
            # print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))
            assert self.demandSums[i-1] <= self.capacity
            if self.demandSums[i-1] > self.capacity:
                print('\nERROR: The solver can not yet modelize a problem with higher single farmer demand than capacity\n')

    def dist(self, i, j):
        return self.distanceMatrix[i][j]

    def sum_demand_farmer(self, i):
        return self.demandSums[i-1]
        

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
    inst = Instance("../data")
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
