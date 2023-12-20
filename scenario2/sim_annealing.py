import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
import python.annealing as sim
import matplotlib.pyplot as plt
import random as rdm
import visualizer.main as viz

import matplotlib.animation as animation


class Solution_general():
    def __init__(self, inst) -> None:
       self.inst = inst
       self.sol = []
       self.cost = -1

    def initialize(self) -> None:
        # action (k, 0) is for pick up command k
        # action (k, 1) is for deliver command k
        self.sol = []
        commands = list(range(self.inst.nbCommands))
        rdm.shuffle(commands)
        for k in commands:
            self.sol.append((k, 0))
            self.sol.append((k, 1))
        self.evaluate()

    def is_feasible(self):
        q = 0
        command_in_truck = [False for _ in range(self.inst.nbCommands)]
        for (k, mod) in self.sol:
            if mod == 0:
                if command_in_truck[k]:
                    return False
                command_in_truck[k] = True
                q += self.inst.command_quantity(k)
            else:
                if not command_in_truck[k]:
                    return False
                command_in_truck[k] = False
                q -= self.inst.command_quantity(k)
            if q > self.inst.capacity or q < 0:
                return False
        return True

    def evaluate(self):
        dist = 0
        current_location = 0
        for (k, mod) in self.sol:
            if mod == 0:
                destination = self.inst.command_farmer(k)
            else:
                destination = self.inst.command_client(k)
            if current_location != destination:
                dist += self.inst.dist(current_location, destination)
            current_location = destination
        # go back to Depot
        dist += self.inst.dist(current_location, 0)
        self.cost = dist

    def generate_neighbor(self):
        neighbor = self.copy()
        i,j = rdm.sample(range(len(self.sol)), 2)
        neighbor.swap(i, j)
        while not neighbor.is_feasible():
            neighbor = self.copy()
            i,j = rdm.sample(range(len(self.sol)), 2)
            neighbor.swap(i, j)
        neighbor.evaluate()
        return neighbor

    def swap(self, i, j):
        self.sol[i], self.sol[j] = self.sol[j], self.sol[i]

    def copy(self):
        new = Solution_general(self.inst)
        new.cost = self.cost 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.cost) + " " + self.sol.__str__() 

    def list_locations(self):
        locations = [0]
        for command, type in self.sol:
            if type == 0:
                destination = self.inst.command_farmer(command)
            else:
                destination = self.inst.command_client(command)
            locations.append(destination)
        locations.append(0)
        return locations

class Solution():

    wrong_pred = 0
    wrong_capa = 0

    def __init__(self, inst) -> None:
       self.inst = inst
       self.sol = []
       self.cost = -1

    def initialize(self) -> None:
        self.sol = [f for f in inst.farmers] + [c for c in inst.clients]
        #rdm.shuffle(self.sol)
        print(f"sol_init: {self.sol}")
        count = 0
        while not self.is_feasible():
            count += 1
            rdm.shuffle(self.sol)
            if count%1000 == 0 :
                print(f"still trying to generate a feasible solution {count}, pred: {self.wrong_pred}, capa: {self.wrong_capa}")
        self.evaluate()

    def is_feasible(self):
        # commands are in good order
        for ind, c in enumerate(self.sol):
            if inst.is_client(c):
                for k in range(ind + 1, len(self.sol)):
                    f = self.sol[k]
                    if inst.is_farmer(f) and f in inst.client_predecesors(c):
                        self.wrong_pred += 1
                        return False
        # capacity is respected
        q = 0
        for ind, location in enumerate(self.sol):
            if inst.is_farmer(location):
                q += inst.sum_demand_farmer(location)
            else:
                q -= inst.sum_demand_client(location)
            if q > inst.capacity or q < 0:
                self.wrong_capa += 1
                return False
        return True
                        
    def evaluate(self):
        dist = 0
        current_location = 0
        for destination in self.sol:
            dist += self.inst.dist(current_location, destination)
            current_location = destination
        # go back to Depot
        dist += self.inst.dist(current_location, 0)
        self.cost = dist

    def generate_neighbor(self):
        neighbor = self.copy()
        i,j = rdm.sample(range(len(self.sol)), 2)
        neighbor.swap(i, j)
        while not neighbor.is_feasible():
            neighbor = self.copy()()
            i,j = rdm.sample(range(len(self.sol)), 2)
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

    def swap(self, i, j):
        self.sol[i], self.sol[j] = self.sol[j], self.sol[i]

    def copy(self):
        new = Solution(self.inst)
        new.cost = self.cost 
        new.sol = self.sol.copy()
        return new
        
    def __str__(self) -> str:
        return str(self.cost) + " " + self.sol.__str__() 


def draw_path(sol, instance):
    F, C, D = instance.getCoordinates()

    path= []

    for loc in sol.list_locations():
        path.append(instance.getCoordinate(loc))

    fig, ax = plt.subplots()
    # plot farmer path
    viz.plot_locations(F, C, D, ax)
    viz.plot_path(path, ax, "black")
    ###

    plt.axis('off')
    plt.show()

def draw_animation(history, instance):
    F, C, D = instance.getCoordinates()
    fig, ax = plt.subplots()
    viz.plot_locations(F, C, D, ax)

    lines = []
    def update(frame):
        sol = history[frame]
        # clear lines
        global line_path
        if len(lines) > 0:
            for l in lines[-1]:
                l.remove()
        # update path
        path= []
        for loc in sol.list_locations():
            path.append(instance.getCoordinate(loc))
        X, Y = [], []
        for x, y in path:
            X.append(x)
            Y.append(y)
        line_path = ax.plot(X,Y, color = "black", zorder=-1)
        lines.append(line_path)
        return line_path


    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(history), interval=25)
    plt.show()


if __name__ == "__main__":
    rdm.seed()
    inst = Instance("data")
    inst = Instance("smalldata")
    sol = Solution_general(inst)
    sol.initialize()
    max_iterations = 10_000
    t0 = 1000
    history = sim.simulated_annealing(sol, max_iterations, t0)
    sol = history[-1]
    values = [s.cost for s in history]

    # plot
    # draw_path(sol,inst)
    print("start annimation")
    draw_animation(history, inst)
    exit()
    Ys = values
    plt.plot(Ys)
    plt.ylim(0, max(Ys) * 1.1)
    plt.show()
