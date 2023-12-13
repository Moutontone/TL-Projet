from mip import *
import sys
from itertools import combinations
import copy
import time

import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
from python.verifSolution import *


###############################################################
################### Optimization arguments ####################
###############################################################

argc = len(sys.argv)-1

optMode = '-O2'
if argc > 1:
  optMode = sys.argv[2]

###############################################################
######################## Initialization #######################
###############################################################

# Verbosity booleans
greedyVerbose = False # prints the whole greedy solution
toursVerbose = True # prints the ammount of tours of the greedy solution and the upper bound for the optimal solution
solverVerbose = True # prints extra details of the solving process
optSolve = True # solves the MIP formulation
optVerbose = True # prints the whole solution

# Replace with the data repository of your choice
datapath = 'newdata'
if argc >= 1:
  datapath = sys.argv[1]

# Getting data from corresponding data folder
instance = Instance(datapath)

# Creating index lists for tours in the model
tours = [t for t in range(instance.nbFarmers)]

###############################################################
####### Greedy Heuristic Solution: Shortest Path First ########
###############################################################

greedySol = [[[0 for i in instance.relevant] for j in instance.relevant] for t in tours]
greedyCountdown = instance.nbFarmers
greedyPos = 0
greedyCap = 0
greedyVisited = [0 for i in instance.relevant]
greedyTour = 0

while greedyCountdown > 0:
  while greedyPos != -1:
    greedyClosest = -1
    for j in instance.farmers:
      if greedyVisited[j] == 0 and j != greedyPos and instance.sum_demand_farmer(j-1)+greedyCap <= instance.capacity:
        greedyClosest = j
        break
    if greedyClosest == -1:
      greedyClosest = 0
    else:
      for j in instance.farmers:
        if instance.dist(greedyPos,j) < instance.dist(greedyPos, greedyClosest) and greedyVisited[j] != 1 and greedyPos != j:
          if j == 0:
            greedyClosest = j
          else:
            if instance.sum_demand_farmer(j-1)+greedyCap <= instance.capacity:
              greedyClosest = j
    greedySol[greedyTour][greedyPos][greedyClosest] = 1
    greedyPos = greedyClosest
    greedyVisited[greedyPos] = 1
    greedyCap += instance.sum_demand_farmer(greedyPos-1)
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
greedyValid = verifSol(greedySol, instance.nbFarmers+1, greedyTour)
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
  for i in instance.relevant:
    for j in instance.relevant:
      if greedySol[t][i][j] == 1:
        greedyDist += instance.dist(i, j)
        greedyStart.append((t,i,j))

###############################################################
############### Printing the greedy solution ##################
###############################################################

if greedyVerbose == True:
  print('The solution provided with the shortest path first heuristic is:\n')
  for t in range(greedyTour):
    print('\n #################################\n')
    for i in instance.relevant:
      for j in instance.relevant:
        print(greedySol[t][i][j], end='  ')
      print('')
if greedyValid == False:
  greedyStart = []

###############################################################
###### Improving the upper bound of the number of tours #######
###############################################################

maxOptTours = instance.nbFarmers
if optMode == '-O2':
  distFromDep = copy.deepcopy(instance.distanceMatrix[0])
  distFromDep.sort()
  maxOptTours = 0
  tempDist = 0
  while tempDist < greedyDist and maxOptTours*2+1 <= instance.nbFarmers:
    tempDist += distFromDep[maxOptTours*2]
    tempDist += distFromDep[maxOptTours*2 + 1]
    maxOptTours += 1
  maxOptTours = min(maxOptTours, instance.nbFarmers)

newtours = [i for i in range(maxOptTours)]

if toursVerbose == True:
  print('\nOptimal Solution has at most {} tours\n\n'.format(maxOptTours))

###############################################################
################## MIP Model of the Problem ###################
###############################################################

m = Model()
m.verbose = solverVerbose

newtours=tours

x = [[[m.add_var(var_type=BINARY) for i in instance.relevant] for j in instance.relevant] for t in newtours]
y = [[m.add_var(var_type=INTEGER) for i in instance.relevant] for t in newtours]

for i in instance.farmers:
  m += xsum(xsum(x[t][i][j] for j in instance.relevant)for t in newtours) == 1
for i in instance.relevant:
    for t in newtours:
      m += xsum(x[t][i][j] for j in instance.relevant) == xsum(x[t][j][i] for j in instance.relevant)
      m += x[t][i][i] == 0

""" forall tₜ """
for t in newtours:
  # ∑ᵢ ∑ⱼ(xᵗᵢⱼ * ∑ₖ wₖᵢ) <= C
  m += xsum(xsum(x[t][i][j]*instance.sum_demand_farmer(i-1) for i in instance.farmers) for j in instance.relevant) <= instance.capacity
  m += instance.nbFarmers*xsum(x[t][0][j] for j in instance.farmers) >= xsum(xsum(x[t][i][j] for i in instance.farmers)for j in instance.farmers)
  m += xsum(x[t][0][j] for j in instance.farmers) <= 1
for t in newtours[:len(newtours)-1]:
  m.add_lazy_constr( xsum(xsum(x[t][i][j]*instance.dist(i, j) for i in instance.relevant) for j in instance.relevant) >=\
                     xsum(xsum(x[t+1][i][j]*instance.dist(i, j) for i in instance.relevant) for j in instance.relevant) )

if optMode == '-O0':
  #Too many constraints with this formulation
  for k in range(1, instance.nbFarmers+1):
    for it in combinations(instance.farmers, k):
      m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
if optMode == '-O1' or optMode == '-O2':
  for i in instance.farmers:
    for j in instance.farmers:
      for t in newtours:
        m += y[t][i]-(instance.nbFarmers+1)*x[t][i][j] >= y[t][j] - instance.nbFarmers

m.objective = minimize(xsum(xsum(xsum(x[t][i][j]*instance.dist(i, j) for i in instance.relevant)for j in instance.relevant)for t in newtours))

# Giving the solution of the greedy heuristic as a starting point TODO: give a non-partial solution
#m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]
# m.start = [[[(x[t][i][j], greedySol[t][i][j]) for t in newtours] for i in relevant] for j in relevant]

###############################################################
############## Resolution of the MIP problem ##################
###############################################################

if optSolve == True:
  solution = [[[0 for i in instance.relevant] for j in instance.relevant] for t in tours]
  status = m.optimize(max_seconds=300)
  for t in newtours:
    for i in instance.relevant:
      for j in instance.relevant:
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
  validSol = verifSol(solution, instance.nbFarmers+1, maxOptTours)
  # assert validSol == True
  if validSol == True:
    print('\nThe solution provided has a valid format\n')
  else:
    print('\nERROR: The solution provided does not have a valid format\n')
