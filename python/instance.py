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
        self.day(0)



    def day(self, k):
        self.day = k
        self.demandSumsFarmer = [0 for i in self.farmers]
        self.demandSumsClient = [0 for i in self.clients]
        self.demandsFarmersClients = []
        self.clientPredecesors = {}
        self.farmerSuccessors = {}
        for i in self.farmers:
            for k in self.clients:
                self.demandSumsFarmer[i-1] += self.demands[self.day][k-self.nbFarmers-1][i-1]
                self.demandSumsClient[k-self.nbFarmers-1] += self.demands[self.day][k-self.nbFarmers-1][i-1]
                if self.demands[self.day][k-self.nbFarmers-1][i-1]>0:
                    self.demandsFarmersClients.append([i,k])
                    if k not in self.clientPredecesors.keys():
                        self.clientPredecesors[k] = [i]
                    else:
                        self.clientPredecesors[k].append(i)
                    if i not in self.farmerSuccessors.keys():
                        self.farmerSuccessors[i] = [k]
                    else:
                        self.farmerSuccessors[i].append(k)
            # to check feasibility of capacity constraint
            # print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))
            assert self.demandSumsFarmer[i-1] <= self.capacity
            assert self.demandSumsClient[i-1] <= self.capacity
            
            if self.demandSumsFarmer[i-1] > self.capacity or self.demandSumsClient[i-1] > self.capacity:
                print('\nERROR: The solver can not yet modelize a problem with higher single farmer demand than capacity\n')

    def dist(self, i, j):
        return self.distanceMatrix[i][j]

    def sum_demand_farmer(self, i):
        return self.demandSumsFarmer[i-1]
    
    def sum_demand_client(self, i):
        return self.demandSumsClient[i-1]
    
    def clientPredecesors(self, i):
        return self.clientPredecesors[i]
    
    def farmerSuccessors(self, i):
        return self.farmerSuccessors[i]
    
    def getCoordinates(self):
        return [(self.coordinates[x][0],self.coordinates[x][1]) for x in self.farmers], [(self.coordinates[x][0],self.coordinates[x][1]) for x in self.clients], (self.coordinates[0][0], self.coordinates[0][1])
