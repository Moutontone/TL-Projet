import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
import python.annealing as sim
import matplotlib.pyplot as plt
import random as rdm
import visualizer.main as viz

class Solution_Client():

    def __init__(self, inst) -> None:
       self.inst = inst

    def initialize(self) -> None:
        self.sol = [k for k in inst.clients]
        rdm.shuffle(self.sol)
        self.evaluate()

    def evaluate(self):
        dist = 0
        q = 0
        q_max = self.inst.capacity
        current_location = 0
        self.vehicules = 1
        # fist farmer
        for destination in self.sol:
            # go to depot if capacity is not enought for the next stop
            if q + self.inst.sum_demand_client(destination) > q_max:
                self.vehicules += 1
                q = 0
                dist += self.inst.dist(current_location, 0)
                current_location = 0
            dist += self.inst.dist(current_location, destination)
            current_location = destination
            q += self.inst.sum_demand_client(destination) 
        # go back to Depot
        dist += self.inst.dist(current_location, 0)
        self.cost = dist

    def generate_neighbor(self):
        i,j = rdm.sample(range(len(self.sol)), 2)
        neighbor = self.copy()
        neighbor.swap(i, j)
        neighbor.evaluate()
        return neighbor

    def swap(self, i, j):
        self.sol[i], self.sol[j] = self.sol[j], self.sol[i]

    def copy(self):
        new = Solution_Client(self.inst)
        new.cost = self.cost 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.cost) + " " + self.sol.__str__() 

    def list_locations(self):
        locations = [0]
        q = 0
        q_max = self.inst.capacity
        for destination in self.sol:
            if q + self.inst.sum_demand_client(destination) > q_max:
                # go to depot do empty capacit
                q = 0
                locations.append(0)
            locations.append(destination)
            q += self.inst.sum_demand_client(destination) 
        if locations[-1] != 0:
            locations.append(0)
        return locations


class Solution_Farmers():

    def __init__(self, inst) -> None:
       self.inst = inst

    def initialize(self) -> None:
        self.sol = [k for k in self.inst.farmers]
        rdm.shuffle(self.sol)
        self.evaluate()

    def evaluate(self):
        dist = 0
        q = 0
        q_max = self.inst.capacity
        current_location = 0
        self.vehicules = 1
        # fist farmer
        for destination in self.sol:
            # go to depot if capacity is not enought for the next stop
            if q + self.inst.sum_demand_farmer(destination) > q_max:
                self.vehicules += 1
                q = 0
                dist += self.inst.dist(current_location, 0)
                current_location = 0
            dist += self.inst.dist(current_location, destination)
            current_location = destination
            q += self.inst.sum_demand_farmer(destination) 
        # go back to Depot
        dist += self.inst.dist(current_location, 0)
        self.cost = dist

    def generate_neighbor(self):
        i,j = rdm.sample(range(len(self.sol)), 2)
        neighbor = self.copy()
        neighbor.swap(i, j)
        neighbor.evaluate()
        return neighbor

    def generate_neighbors(self):
        neighbors = []
        # Iterate through each index in the solution
        for i in range(len(self.sol)):
            for j in range(i + 1, len(self.sol)):
                neighbor = self.copy()
                neighbor.swap(i, j)
                neighbors.append(neighbor)
        return neighbors

    def list_locations(self):
        locations = [0]
        q = 0
        q_max = self.inst.capacity
        for destination in self.sol:
            if q + self.inst.sum_demand_farmer(destination) > q_max:
                # go to depot do empty capacit
                q = 0
                locations.append(0)
            locations.append(destination)
            q += self.inst.sum_demand_farmer(destination) 
        if locations[-1] != 0:
            locations.append(0)
        return locations

    def swap(self, i, j):
        self.sol[i], self.sol[j] = self.sol[j], self.sol[i]

    def copy(self):
        new = Solution_Farmers(self.inst)
        new.cost = self.cost 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.cost) + " " + self.sol.__str__() 

def draw_path(solF, solC, instance, valuesF, valuesC):

    F, C, D = instance.getCoordinates()

    path_farmer = []
    path_client = []

    for loc in solF.list_locations():
        path_farmer.append(instance.getCoordinate(loc))
    for loc in solC.list_locations():
        path_client.append(instance.getCoordinate(loc))

    colors_tours = ["red", "blue", "purple", "black", "yellow"]
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
    # plot farmer path
    ax = ax1
    viz.plot_locations(F, [], D, ax)
    ax.legend()

    tour = [D]
    count_tour = 0
    for location in path_farmer[1:]:
        tour.append(location)
        if location == D:
            # print tour
            # viz.plot_path(tour, ax, colors_tours[count_tour])
            viz.plot_path(tour, ax, "black")
            count_tour += 1
            tour = [D]

    # plot client path
    ax = ax2
    viz.plot_locations([], C, D, ax)
    ax.legend()

    tour = [D]
    count_tour = 0
    for location in path_client[1:]:
        tour.append(location)
        if location == D:
            # print tour
            viz.plot_path(tour, ax,  "black")
            count_tour += 1
            tour = [D]

    # plot both path
    ax = ax3
    viz.plot_locations(F, C, D, ax)
    ax.legend()

    viz.plot_path(path_farmer, ax, "red")
    viz.plot_path(path_client, ax, "green")

    # plot evolution
    ax = ax4

    Ys = [valuesF[i] + valuesC[i] for i in range(len(valuesF))]
    ax.plot(Ys, color = "black")
    # plt.ylim(0, max(valuesF + valuesC) * 1.1)
    ###

    # plt.axis('off')
    plt.show()

if __name__ == "__main__":
    rdm.seed()
    inst = Instance("data")

    mult_epoch = 1000
    pi = 0.2
    pl = 0.0001

    for day in range(208):
        print(f"day: {day}")

        inst = Instance("data")
        inst.set_day(day)
        solF = Solution_Farmers(inst)
        solF.initialize()
        history = sim.simulated_annealing(solF, pi, mult_epoch, pl)
        bestF = history[-1].cost

        solC = Solution_Client(inst)
        solC.initialize()
        history = sim.simulated_annealing(solC, pi, mult_epoch, pl)
        bestC = history[-1].cost

        print(f"solution: {bestF + bestC}")


#     draw_path(best_solF, best_solC, inst, valuesF, valuesC)
# 
#     Ys = valuesF
#     plt.plot(Ys)
#     Ys = valuesC
#     plt.plot(Ys)
#     plt.ylim(0, max(valuesF + valuesC) * 1.1)
#     plt.show()
