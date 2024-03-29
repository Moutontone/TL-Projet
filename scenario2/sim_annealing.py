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

def draw_animation(history, instance, iterations):
    speed = 100
    F, C, D = instance.getCoordinates()
    fig, (ax1, ax2) = plt.subplots(2)
    viz.plot_locations(F, C, D, ax1)


    X, Y = [], []
    line_path = ax1.plot(X,Y, color = "black", zorder=-1, label = "iteration 0")
    X = [i for i in range(len(history))]
    Y = [sol.cost for sol in history]
    ax2.plot(X,Y, color = "black")
    line_cost = ax2.plot([],[], color = "red", label = "iteration0")
    hlegend = ax2.legend(loc='upper right')

    lines1 = []
    lines2 = []
    def update(frame):
        frame = min(frame*speed, len(history)-1)
        sol = history[frame]
        # update legend
        # text.get_texts()[0].set_text("frame: " + str(frame))
        # clear lines
        if len(lines1) > 0:
            for l in lines1[-1]:
                l.remove()
        if len(lines2) > 0:
            for l in lines2[-1]:
                l.remove()
        # update path
        path= []
        for loc in sol.list_locations():
            path.append(instance.getCoordinate(loc))
        X, Y = [], []
        for x, y in path:
            X.append(x)
            Y.append(y)
        line_path = ax1.plot(X,Y, color = "black", zorder=-1)
        line_cost = ax2.plot([frame, frame],[0, sol.cost], color = "red", label = f"iteration{frame}" ) 
        lines2.append(line_cost)
        lines1.append(line_path)
        htext = hlegend.get_texts()[0]
        label_i = f"cost: {sol.cost:.2f}\niteration: {frame}"
        htext.set_text(label_i)
        # return line_path , htext


    ani = animation.FuncAnimation(fig=fig, func=update, frames=int(len(history)/speed), interval=1)
    f = r"animation.gif" 
    writergif = animation.PillowWriter(fps=30) 
    # ani.save(f, writer=writergif)

    plt.show()


if __name__ == "__main__":
    rdm.seed()
    inst = Instance("data")
    # inst = Instance("smalldata")
    # inst = Instance("toydata")
    sol = Solution_general(inst)
    sol.initialize()
    sol_init = sol.copy()

    mult_epoch = 10
    pi = 0.4
    pl = 0.0001

    for day in range(1): # range(207) days
        print(f"day: {day}")

        # history = sim.simulated_annealing_alg(sol, max_iterations, t0, 0.99)
        history = sim.simulated_annealing(sol, pi, mult_epoch, pl)
        best = history[-1].cost

        print(f"solution: {best}")

        # plot
        # draw_path(sol,inst)
        print("start annimation")
        draw_animation(history, inst, len(history))
        print("end annimation")
