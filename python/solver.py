from mip import *
import sys
import fileReader as fr
from itertools import combinations
import copy
from verifSolution import *

###############################################################
######################## Initialization #######################
###############################################################

# Verbosity booleans
greedyVerbose = False # prints the whole greedy solution
toursVerbose = True # prints the ammount of tours of the greedy solution and the upper bound for the optimal solution
solverVerbose = True # prints extra details of the solving process
optSolve = True # solves the MIP formulation
optVerbose = False # prints the whole solution

# Replace with the data repository of your choice
datapath = 'newdata'
if len(sys.argv) > 1:
  datapath = sys.argv[1]

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
  # print('farmer {} has a total demand of {}'.format(i, demandSums[i-1]))
  if demandSums[i-1] > capacity:
    print('\nERROR: The solver can not yet modelize a problem with higher single farmer demand than capacity\n')

###############################################################
####### Greedy Heuristic Solution: Shortest Path First ########
###############################################################

greedySol = [[[0 for i in relevant] for j in relevant] for t in tours]
greedyCountdown = nbFarmers
greedyPos = 0
greedyCap = 0
greedyVisited = [0 for i in relevant]
greedyTour = 0

while greedyCountdown > 0:
  while greedyPos != -1:
    greedyClosest = -1
    for j in farmers:
      if greedyVisited[j] == 0 and j != greedyPos and demandSums[j-1]+greedyCap <= capacity:
        greedyClosest = j
        break
    if greedyClosest == -1:
      greedyClosest = 0
    else:
      for j in farmers:
        if distanceMatrix[greedyPos][j] < distanceMatrix[greedyPos][greedyClosest] and greedyVisited[j] != 1 and greedyPos != j:
          if j == 0:
            greedyClosest = j
          else:
            if demandSums[j-1]+greedyCap <= capacity:
              greedyClosest = j
    greedySol[greedyTour][greedyPos][greedyClosest] = 1
    greedyPos = greedyClosest
    greedyVisited[greedyPos] = 1
    greedyCap += demandSums[greedyPos-1]
    greedyCountdown -= 1
    if greedyPos == 0:
      greedyCountdown += 1
      greedyPos = -1
  greedyPos = 0
  greedyCap = 0
  greedyTour += 1
  greedyVisited[0] = 0

if toursVerbose == True:
  print('\nA solution with the greedy heuristic found (that has {} tours)\n'.format(greedyTour))

# This algorithm works...   source: trust me bro
# Verification of the solution
greedyValid = verifSol(greedySol, nbFarmers+1, greedyTour)
if greedyValid == False:
  print('\nERROR: The greedy heuristic solution is incorrect\n')
else:
  print('\nThe solution provided is of a correct format\n')
assert greedyValid == True

###############################################################
##### Formatting the greedy solution to give to the solver ####
###############################################################

greedyDist = 0
greedyStart = []
for t in tours:
  for i in relevant:
    for j in relevant:
      if greedySol[t][i][j] == 1:
        greedyDist += distanceMatrix[i][j]
        greedyStart.append((t,i,j))

###############################################################
############### Printing the greedy solution ##################
###############################################################

if greedyVerbose == True:
  print('The solution provided with the shortest path first heuristic is:\n')
  for t in range(greedyTour):
    print('\n #################################\n')
    for i in relevant:
      for j in relevant:
        print(greedySol[t][i][j], end='  ')
      print('')
if greedyValid == False:
  greedyStart = []

###############################################################
###### Improving the upper bound of the number of tours #######
###############################################################

distFromDep = copy.deepcopy(distanceMatrix[0])
distFromDep.sort()
maxOptTours = 0
tempDist = 0
while tempDist < greedyDist:
  tempDist += distFromDep[maxOptTours*2]
  tempDist += distFromDep[maxOptTours*2 + 1]
  maxOptTours += 1

maxOptTours = min(maxOptTours, nbFarmers)

newtours = [i for i in range(maxOptTours)]

if toursVerbose == True:
  print('\nOptimal Solution has at most {} tours\n\n'.format(maxOptTours))

###############################################################
################## MIP Model of the Problem ###################
###############################################################

m = Model()
m.verbose = solverVerbose

x = [[[m.add_var(var_type=BINARY) for i in relevant] for j in relevant] for t in newtours]
y = [[m.add_var(var_type=INTEGER) for i in relevant] for t in newtours]

for i in farmers:
  m += xsum(xsum(x[t][i][j] for j in relevant)for t in newtours) == 1
for i in relevant:
    for t in newtours:
      m += xsum(x[t][i][j] for j in relevant) == xsum(x[t][j][i] for j in relevant)
      m += x[t][i][i] == 0

""" forall tₜ """
for t in newtours:
  # ∑ᵢ ∑ⱼ(xᵗᵢⱼ * ∑ₖ wₖᵢ) <= C
  m += xsum(xsum(x[t][i][j]*demandSums[i-1] for i in farmers) for j in relevant) <= capacity
  m += nbFarmers*xsum(x[t][0][j] for j in farmers) >= xsum(xsum(x[t][i][j] for i in farmers)for j in farmers)
  m += xsum(x[t][0][j] for j in farmers) <= 1
for t in newtours[:len(newtours)-1]:
  m.add_lazy_constr( xsum(xsum(x[t][i][j]*distanceMatrix[i][j] for i in relevant) for j in relevant) >=\
                     xsum(xsum(x[t+1][i][j]*distanceMatrix[i][j] for i in relevant) for j in relevant) )

""" Too many constraints with this formulation
for k in range(1, nbFarmers+1):
  for it in combinations(farmers, k):
    m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
"""
for i in farmers:
  for j in farmers:
    for t in newtours:
      m += y[t][i]-(nbFarmers+1)*x[t][i][j] >= y[t][j] - nbFarmers

m.objective = minimize(xsum(xsum(xsum(x[t][i][j]*distanceMatrix[i][j] for i in relevant)for j in relevant)for t in newtours))

# Giving the solution of the greedy heuristic as a starting point TODO: give a non-partial solution
m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]
# m.start = [[[(x[t][i][j], greedySol[t][i][j]) for t in newtours] for i in relevant] for j in relevant]

###############################################################
############## Resolution of the MIP problem ##################
###############################################################

if optSolve == True:
  solution = [[[0 for i in relevant] for j in relevant] for t in tours]
  status = m.optimize(max_seconds=300)
  for t in newtours:
    for i in relevant:
      for j in relevant:
        solution[t][i][j] = x[t][i][j].xi(0)
        if optVerbose == True:
          print(int(x[t][i][j].xi(0)),end='  ')
      if optVerbose == True:
        print('')
    if optVerbose == True:
      print('\n  #############################################\n')
  if status == OptimizationStatus.OPTIMAL:
    print('\nAn optimal solution was found with an objective value of {}'.format(m.objective_value))
  elif status == OptimizationStatus.FEASIBLE:
    print('\nA feasible solution was found with an objective value of {} and a lower bound of {}'.format(m.objective_value, m.objective_bound))
  else:
    print('\nNo solution was found')
  validSol = verifSol(solution, nbFarmers+1, maxOptTours)
  assert validSol == True
  if validSol == True:
    print('\nThe solution provided has a valid format\n')
  else:
    print('\nERROR: The solution provided does not have a valid format\n')
