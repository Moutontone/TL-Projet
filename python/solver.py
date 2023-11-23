from mip import *
import fileReader as fr
from itertools import combinations

# Replace with the data repository of your choice
datapath = 'toydata'

# Getting data from corresponding data folder
nbClients, nbFarmers, capacity, locationCost, costPerKm = fr.readInfoInstanceFile(datapath+'/info_instance.txt')
coordinates = fr.readCoordFile(datapath+'/coordinates.txt')# for each point we have list of 2 values [x, y] size=(60,2) first depot, next farmers, next clients
distanceMatrix = fr.readDistanceMatrixFile(datapath+'/cost_matrix.txt') # for each point we have a list of distance to points size=(60,60)
demands = fr.readDemandMatrixFile(datapath+'/demands.txt') # size=(208,39,21)

# Creating index lists for simpler formulation in the model
hub = [0]
farmers = [i for i in range(1,nbFarmers+1)]
clients = [i for i in range(nbFarmers+1,nbFarmers+nbClients+1)]
tours = [t for t in range(nbFarmers)]
relevant = [i for i in range(nbFarmers+1)]
demands = demands[1:]#first line is empty

day = 0

# sum of all demands for farmer i (we supppose that we take everything at once from a farmer)
demandSums = [0 for i in farmers]
for i in farmers:
  for k in clients:
    demandSums[i-1] += demands[day][k-nbFarmers-1][i-1]
  # to check feasibility of capacity constraint
  #print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))

####### Greedy Heuristic Solution: Shortest Path First ########

greedySol = [[[0 for i in relevant] for j in relevant] for t in tours]
greedyCountdown = nbFarmers
greedyPos = 0
greedyCap = 0
greedyVisited = [0 for i in relevant]
greedyVisited[0] = 1
greedyTour = 0

while greedyCountdown > 0:
  newPos = 0
  for i in relevant:
    if greedyVisited[i] != 1 and i != greedyPos:
      newPos = i
      break
  if newPos == 0:
    greedySol[greedyTour][greedyPos][newPos] = 1
    break
  for i in relevant:
    if i != greedyPos and greedyVisited[i] != 1:
      if (distanceMatrix[greedyPos][i] < distanceMatrix[greedyPos][newPos] and greedyCap + demandSums[i-1] <= capacity):
        newPos = i
  if greedyCap + demandSums[newPos-1] > capacity:
    newPos = 0
  else:
    greedyCap += demandSums[newPos-1]
    greedyVisited[newPos] = 1
  if newPos == 0:
    greedySol[greedyTour][greedyPos][newPos] = 1
    greedyTour += 1
    greedyCap = 0
  else:
    greedySol[greedyTour][greedyPos][newPos] = 1
    greedyCountdown -= 1
  greedyPos = newPos

greedyStart = []
for t in tours:
  for i in relevant:
    for j in relevant:
      if greedySol[t][i][j] == 1:
        greedyStart.append((t,i,j))
"""
print(greedyStart)

print('The solution provided with the shortest path first heuristic is:\n')
for t in tours:
  print('\n ################################# \n')
  for i in relevant:
    for j in relevant:
      print(greedySol[t][i][j], end='  ')
    print('')
"""


################## MIP Model of the Problem ###################
m = Model()

x = [[[m.add_var(var_type=BINARY) for i in relevant] for j in relevant] for t in tours]

for i in farmers:
  m += xsum(xsum(x[t][i][j] for j in relevant)for t in tours) == 1
  m += xsum(xsum(x[t][j][i] for j in relevant)for t in tours) == 1
for i in relevant:
    for t in tours:
      m += xsum(x[t][i][j] for j in relevant) == xsum(x[t][j][i] for j in relevant)

for t in tours:
  m += xsum(xsum(x[t][i][j]*demandSums[i-1] for i in farmers) for j in relevant) <= capacity
  m += nbFarmers*xsum(x[t][0][j] for j in farmers) >= xsum(xsum(x[t][i][j] for i in farmers)for j in farmers)
  m += xsum(x[t][0][j] for j in farmers) <= 1
for t in tours[:len(tours)-1]:
  m.add_lazy_constr( xsum(xsum(x[t][i][j]*distanceMatrix[i][j] for i in relevant) for j in relevant) >=\
                     xsum(xsum(x[t+1][i][j]*distanceMatrix[i][j] for i in relevant) for j in relevant) )
for k in range(1, nbFarmers+1):
  for it in combinations(farmers, k):
    m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in tours) <= k-1

m.objective = minimize(xsum(xsum(xsum(x[t][i][j]*distanceMatrix[i][j] for i in relevant)for j in relevant)for t in tours))

"""
start = [[[0 for i in relevant] for j in relevant] for t in tours]
for t in tours:
  start[t][t+1][0] = 1
  start[t][0][t+1] = 1
"""

# Giving the solution of the greedy heuristic as a starting point
m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]

m.optimize(max_seconds=120)

for t in tours:
  for i in relevant:
    for j in relevant:
      print(int(x[t][i][j].xi(0)),end='  ')
    print('')
  print('\n  #############################################\n')
