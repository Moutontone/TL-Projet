import python.fileReader as fr
import math

coordinates = fr.readCoordFile('data/coordinates.txt')# for each point we have list of 2 values [x, y] size=(60,2)

costMatrix = []
for x in range(len(coordinates)):
    costMatrixForOneLocation = []
    for y in range(len(coordinates)):
        costMatrixForOneLocation.append(math.sqrt((coordinates[x][0]-coordinates[y][0])**2+(coordinates[x][1]-coordinates[y][1])**2)*3.5/10)
    costMatrix.append(costMatrixForOneLocation)
fr.writeDistanceMatrixFile(distanceMatrix=costMatrix, filename='data/cost_matrix.txt')