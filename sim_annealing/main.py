if __name__ == "__main__":
    pass

# Getting data from corresponding data folder
nbClients, nbFarmers, capacity, locationCost, costPerKm = fr.readInfoInstanceFile(datapath+'/info_instance.txt')
coordinates = fr.readCoordFile(datapath+'/coordinates.txt')# for each point we have list of 2 values [x, y] size=(60,2) first depot, next farmers, next clients
distanceMatrix = fr.readDistanceMatrixFile(datapath+'/cost_matrix.txt') # for each point we have a list of distance to points size=(60,60)
demands = fr.readDemandMatrixFile(datapath+'/demands.txt') # size=(208,39,21)
