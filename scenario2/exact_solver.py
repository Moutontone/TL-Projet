from mip import *
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

###############################################################
################## MIP Model of the Problem ###################
###############################################################

m = Model()
m.verbose = solverVerbose

all_locations = [i for i in range(instance.nbFarmers+instance.nbClients+1)]

x = [[m.add_var(var_type=BINARY) for _ in all_locations] for _ in all_locations]
y = [[m.add_var(var_type=BINARY) for _ in all_locations] for _ in all_locations]
z = [m.add_var(var_type=CONTINUOUS) for _ in all_locations]
load = [[m.add_var(var_type=INTEGER) for _ in all_locations] for _ in all_locations]

for i in all_locations: #without depot
    #m += load[0][i] == 0                                          #load_1
    #m += load[i][0] == 0                                          #load_2

    #m += xsum(x[j][i] for j in all_locations) == xsum(x[i][k] for k in all_locations) #flow_1
    #m += xsum(x[j][i] for j in all_locations) <= 1
    
  
    for j in all_locations:
        #m += y[i][j]+y[j][i] <= 1                                   #precedence_1
        #m += x[i][j] <= y[i][j]                                     #precedence_3

        m += load[i][j] <= instance.capacity * x[i][j]                       #load_4
    
        for k in all_locations:
            m += x[j][i]+y[i][j]+y[j][k]+y[k][i] <= 2                 #precedence_2

#for order in instance.demandsFarmersClients:
#    m += y[order[0]][order[1]] == 1

#m += xsum(x[0][j] for j in all_locations[1:]) == 1 #depot_1
#m += xsum(x[i][0] for i in all_locations[1:]) == 1 #depot_2

for i in instance.farmers:
    for j in instance.clients:
        m += instance.capacity*y[i][j] >= instance.demands[instance.day][j-instance.nbFarmers-1][i-1]    #precedence_4

for j in instance.farmers:     
    m += xsum(load[i][j] for i in all_locations) == xsum(load[j][k] for k in all_locations) - xsum(instance.demands[instance.day][k-instance.nbFarmers-1][j-1] for k in instance.clients) #load_3a
    

for j in instance.clients:
    m += xsum(load[i][j] for i in all_locations) - xsum(instance.demands[instance.day][j-instance.nbFarmers-1][i-1] for i in instance.farmers) == xsum(load[j][k] for k in all_locations) #load_3a

for i in all_locations:
    m += x[i][i] == 0 #flow_2
    m += xsum(x[i][j] for j in all_locations) == xsum(x[k][i] for k in all_locations)
    m += xsum(x[j][i] for j in all_locations) == 1
    m += load[0][i] == 0                                          #load_1
    m += load[i][0] == 0 
    for i in all_locations[1:]:
        m += x[j][i] <= y[j][i]
    #m += load[i][i] == 0
'''
if optMode == '-O0':
  Too many constraints with this formulation
  for k in range(1, instance.nbFarmers+1):
    for it in combinations(instance.farmers, k):
      m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
if optMode == '-O1' or optMode == '-O2':'''
for i in all_locations[1:]:
    for j in all_locations:
        m += z[i]-(all_locations[-1]+1)*x[i][j] >= z[j] - all_locations[-1]
        m += z[i]-(all_locations[-1]+1)*y[i][j] >= z[j] - all_locations[-1]

m.objective = minimize(xsum(xsum(x[i][j]*instance.dist(i, j) for i in all_locations)for j in all_locations))

# Giving the solution of the greedy heuristic as a starting point TODO: give a non-partial solution
#m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]
# m.start = [[[(x[t][i][j], greedySol[t][i][j]) for t in newtours] for i in relevant] for j in relevant]

###############################################################
############## Resolution of the MIP problem ##################
###############################################################

if optSolve == True:
    solution = [[0 for _ in all_locations] for _ in all_locations]
    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('\nAn optimal solution was found with an objective value of {}'.format(m.objective_value))

        if optVerbose == True:
            print('x')
        for i in all_locations:
            for j in all_locations:
                solution[i][j] = x[i][j].xi(0)
                if optVerbose == True:
                    print(int(x[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('y')
        for i in all_locations:
            for j in all_locations:
                if optVerbose == True:
                    print(int(y[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('load')
        for i in all_locations:
            for j in all_locations:
                if optVerbose == True:
                    print(int(load[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('z')
        for j in all_locations:
            if optVerbose == True:
                print(float(z[j].xi(0)),end='  ')
        if optVerbose == True:
            print('')
        if optVerbose == True:
            print('\n  #############################################\n')
    elif status == OptimizationStatus.FEASIBLE:
        print('\nA feasible solution was found with an objective value of {} and a lower bound of {}'.format(m.objective_value, m.objective_bound))
    else:
        print('\nNo solution was found')
    '''validSol = verifSol(solution, instance.nbFarmers+1, maxOptTours)
    # assert validSol == True
    #if validSol == True:
        print('\nThe solution provided has a valid format\n')
    else:
        print('\nERROR: The solution provided does not have a valid format\n')'''