#######################################################
# Author: Nicolas Besson                              #
# TL-OR: Project                                      #
#######################################################

def writeCoordFile(coords, filename):
    coords_string = ""
    for c in coords:
        coords_string = coords_string + str(c[0]) + ", " + str(c[1]) + "\n"
    with open(filename, "w") as f:
        coordString = f.write(coords_string)

def readCoordFile(filename):
    with open(filename, "r") as f:
        coordStringLines = f.readlines()
    coords = []
    for coordStringLine in coordStringLines:
        lineArray = coordStringLine.split(", ")
        x, y = int(lineArray[0]), int(lineArray[1])
        coords.append([x, y])
    return coords

def readSolutionFile(filename):
    with open(filename, "r") as f:
        path_string = f.readlines()
    for line in path_string:
        path = [int(i) for i in line.split(", ")]
    return path

def writeSolutionFile(paths, filename):
    path_string = ""
    for i, path in enumerate(paths):
        for i in path[:-1]:
            path_string = path_string + str(i) + ", "
        path_string = path_string + str(path[-1]) + "\n"
    with open(filename, "w") as f:
        f.write(path_string)

def readDistanceMatrixFile(filename):
    with open(filename, "r") as f:
        matrixString = f.readlines()
    return [[float(i) for i in line.split(", ")] for line in matrixString]

def writeDistanceMatrixFile(distanceMatrix, filename):
    matrixString = ""
    for line in distanceMatrix:
        lineString = ""
        for i in line[:-1]:
            lineString = lineString + str(i) + ", "
        lineString = lineString + str(line[-1]) + "\n"
        matrixString += lineString
    with open(filename, "w") as f:
        f.write(matrixString)

def readDemandMatrixFile(filename):
    with open(filename, "r") as f:
        matrixString = f.readlines()
    demands = []
    currentDemandMatrix = []
    for line in matrixString:
        if line == "#1:":
            continue
        elif line[0] == "#":
            demands.append(currentDemandMatrix)
            currentDemandMatrix = []
        else:
            currentDemandMatrix.append([int(i) for i in line.split(", ")])
    return demands

    

def writeDemandMatrixFile(demands, filename):
    matrixString = ""
    for day in range(1, len(demands) + 1):
        matrixString = matrixString + "#" + str(day) + ":\n"
        currentDemandMatrix =  demands[day - 1]
        for line in currentDemandMatrix:
            lineString = ""
            for i in line[:-1]:
                lineString = lineString + str(i) + ", "
            lineString = lineString + str(line[-1]) + "\n"
            matrixString += lineString
    with open(filename, "w") as f:
        f.write(matrixString)

def readInfoInstanceFile(filename):
    with open(filename) as f:
        infoString = f.readlines()
    for lineString in infoString:
        line = lineString.split(" ")
        if line[0] == "clients":
            nbClients = int(line[1])
        if line[0] == "farmers":
            nbFarmers = int(line[1])
        if line[0] == "capacity":
            capacity = int(line[1])
        if line[0] == "locationCost":
            locationCost = int(line[1])
        if line[0] == "costPerKm":
            costPerKm = float(line[1])
    return nbClients, nbFarmers, capacity, locationCost, costPerKm

def writeAllocationFile(allocation, filename):
    string_allocation = ""
    for i, a in enumerate(allocation[:-1]):
        string_allocation = string_allocation + str(a) + ", "
    string_allocation += str(allocation[-1])
    with open(filename, "w") as f:
        f.write(string_allocation)

def readAllocationFile(filename):
    with open(filename, "r") as f:
        string_allocation = f.read()
    return [float(i) for i in string_allocation.split(", ")]
    
def readDepotsFile(filename):
    with open(filename, "r") as f:
        depots_string = f.read()
    return [int(i) for i in depots_string.split(", ")]

def writeDepotsFile(depot_set, filename):
    depots_string = ""
    for i in depot_set[1:]:
        depots_string += str(i)
    depots_string += str(depot_set[-1])
    with open(filename, "w") as f:
        f.write(depots_string)