import random as rdm

class Solution2():

    val = None

    def __init__(self, inst) -> None:
       self.inst = inst

    def initialize(self) -> None:
        self.sol = [k for k in inst.farmers] + [k for k in inst.clients]
        rdm.shuffle(self.sol)
        self.make_feasible()
        self.evaluate()

    def is_feasible(self):
        for ind, c in enumerate(self.sol):
            if c.is_client():
                for f in range(ind, len(self.sol)):
                    location = self.sol[f]
                    if location.is_farmer() and location in c.farmer_before():
                        

        


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
