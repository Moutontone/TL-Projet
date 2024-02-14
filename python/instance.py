import python.fileReader as fr

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
        self.set_day(0)

    def set_day(self, c):
        self.day = c
        self.demandSumsFarmer = [0 for _ in self.farmers]
        self.demandSumsClient = [0 for _ in self.clients]
        self.clientPredecesors = [[] for _ in self.clients]
        self.farmerSuccessors = [[] for _ in self.farmers]
        self.demandsFarmersClients = []
        # list of triplet (farmer, client, quantity)
        self.commandList = []
        for f in self.farmers:
            for c in self.clients:
                # update demand sums
                self.demandSumsFarmer[f-1] += self.demands[self.day][c-self.nbFarmers-1][f-1]
                self.demandSumsClient[c-self.nbFarmers-1] += self.demands[self.day][c-self.nbFarmers-1][f-1]
                # update successors and predecessors
                q = self.demands[self.day][c-self.nbFarmers-1][f-1]
                if q > 0:
                    self.demandsFarmersClients.append([f,c])
                    if c not in self.farmerSuccessors[f-1]:
                        self.farmerSuccessors[f-1].append(c)
                    if f not in self.clientPredecesors[c-self.nbFarmers-1]:
                        self.clientPredecesors[c-self.nbFarmers-1].append(f)
                    # add to commandList
                    self.commandList.append((f, c, q))

            # to check feasibility of capacity constraint
            # print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))
            assert self.demandSumsFarmer[f-1] <= self.capacity
            assert self.demandSumsClient[f-1] <= self.capacity
            
            if self.demandSumsFarmer[f-1] > self.capacity or self.demandSumsClient[f-1] > self.capacity:
                print('\nERROR: The solver can not yet modelize a problem with higher single farmer demand than capacity\n')
        self.nbCommands = len(self.commandList)

    def dist(self, i, j):
        return self.distanceMatrix[i][j]

    def sum_demand_farmer(self, i):
        return self.demandSumsFarmer[i-1]
    
    def sum_demand_client(self, i):
        return self.demandSumsClient[i-1-self.nbFarmers]
    
    def client_predecesors(self, c):
        return self.clientPredecesors[c-self.nbFarmers-1]
    
    def farmer_successors(self, f):
        return self.farmerSuccessors[f-1]

    def is_client(self, c):
        return c in self.clients

    def is_farmer(self, f):
        return f in self.farmers

    def command_farmer(self, k):
        return self.commandList[k][0]

    def command_client(self, k):
        return self.commandList[k][1]

    def command_quantity(self, k):
        return self.commandList[k][2]

    def farmerSuccessors(self, i):
        return self.farmerSuccessors[i]
    
    def getCoordinates(self):
        return [(self.coordinates[x][0], self.coordinates[x][1]) for x in self.farmers], [(self.coordinates[x][0], self.coordinates[x][1]) for x in self.clients], (self.coordinates[0][0], self.coordinates[0][1])

    def getCoordinate(self, i):
        return (self.coordinates[i][0], self.coordinates[i][1])
