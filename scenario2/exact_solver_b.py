from mip import *

import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
from python.verifSolution import *

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
if len(instance.demands) == 1:
	instance.demands = instance.demands[0] # to not iterate over days, since we have only one day to test

list_of_demand_indices = [0] #index of each node

list_of_demands = [0]# demand for the given index
print('demands:', instance.demands)
print('distance:')
for x in instance.distanceMatrix:
	print(x)
for client in range(len(instance.clients)):
	print('client id', instance.clients[client])
	print(client, instance.demands[client])
	for farmer in range(len(instance.farmers)):
		if instance.demands[client][farmer] > 0:
			list_of_demand_indices.append(instance.farmers[farmer])
			list_of_demand_indices.append(instance.clients[client])

			list_of_demands.append(instance.demands[client][farmer])
			list_of_demands.append(-instance.demands[client][farmer])
print(list_of_demand_indices)

tmp_dist_matrix = [[0]]
#tmp_demand_matrix = [[]]
#tmp_demand_matrix[0] = [0 for _ in range(len(list_of_demand_indices))]

for index in list_of_demand_indices[1:]:
	#print(index)
	for x in range(len(tmp_dist_matrix)):
		tmp_dist_matrix[x].append(instance.distanceMatrix[list_of_demand_indices[x]][index])
	tmp_list = [row[-1] for row in tmp_dist_matrix] + [0]
	tmp_dist_matrix.append(tmp_list)

	#print(tmp_list)

'''for i in range(1,len(list_of_demand_indices),2):
	tmp_demand_matrix.append([0 for _ in range(len(list_of_demand_indices))])
	tmp_demand_matrix.append([0 for _ in range(len(list_of_demand_indices))])
	tmp_demand_matrix[i][i+1] = instance.demands[list_of_demand_indices[i+1]-1-instance.nbFarmers][list_of_demand_indices[i]-1]
	tmp_demand_matrix[i+1][i] = -instance.demands[list_of_demand_indices[i+1]-1-instance.nbFarmers][list_of_demand_indices[i]-1]
'''
#print(tmp_demand_matrix)
print(tmp_dist_matrix)

m = Model()
m.verbose = solverVerbose

all_locations = [i for i in range(instance.nbFarmers+instance.nbClients+1)]

x = [[m.add_var(var_type=BINARY) for _ in list_of_demand_indices] for _ in list_of_demand_indices]
y = [[m.add_var(var_type=BINARY) for _ in list_of_demand_indices] for _ in list_of_demand_indices]
z = [m.add_var(var_type=CONTINUOUS) for _ in list_of_demand_indices]
load = [[m.add_var(var_type=INTEGER) for _ in list_of_demand_indices] for _ in list_of_demand_indices]

for i in range(len(list_of_demand_indices)): #without depot
    #m += load[0][i] == 0                                          #load_1
    #m += load[i][0] == 0                                          #load_2

    #m += xsum(x[j][i] for j in all_locations) == xsum(x[i][k] for k in all_locations) #flow_1
    #m += xsum(x[j][i] for j in all_locations) <= 1
    
  
    for j in range(len(list_of_demand_indices)):
        m += y[i][j]+y[j][i] <= 1                                   #precedence_1
        #m += x[i][j] <= y[i][j]                                     #precedence_3

        m += load[i][j] <= instance.capacity * x[i][j]                       #load_4
    
        for k in range(len(list_of_demand_indices)):
            m += x[j][i]+y[i][j]+y[j][k]+y[k][i] <= 2                 #precedence_2

#for order in instance.demandsFarmersClients:
#    m += y[order[0]][order[1]] == 1

#m += xsum(x[0][j] for j in all_locations[1:]) == 1 #depot_1
#m += xsum(x[i][0] for i in all_locations[1:]) == 1 #depot_2

#for i in instance.farmers:
    #for j in instance.clients:
for i in range(1,len(list_of_demand_indices),2):
    m += y[i][i+1] == 1    #precedence_4

for j in range(len(list_of_demand_indices)):     
    m += xsum(load[i][j] for i in range(len(list_of_demand_indices))) == xsum(load[j][k] for k in range(len(list_of_demand_indices))) - list_of_demands[j] #load_3
    


for i in range(len(list_of_demand_indices)):
    m += x[i][i] == 0 #flow_2
    m += xsum(x[i][j] for j in range(len(list_of_demand_indices))) == xsum(x[k][i] for k in range(len(list_of_demand_indices)))
    m += xsum(x[j][i] for j in range(len(list_of_demand_indices))) == 1
    m += load[0][i] == 0                                          #load_1
    m += load[i][0] == 0 
    for j in range(1,len(list_of_demand_indices)):
        m += x[j][i] <= y[j][i]
    #m += load[i][i] == 0
'''
if optMode == '-O0':
  Too many constraints with this formulation
  for k in range(1, instance.nbFarmers+1):
    for it in combinations(instance.farmers, k):
      m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
if optMode == '-O1' or optMode == '-O2':'''
for i in range(1,len(list_of_demand_indices)):
    for j in range(len(list_of_demand_indices)):
        m += z[i]-(len(list_of_demand_indices)+1)*x[i][j] >= z[j] - len(list_of_demand_indices)
        m += z[i]-(len(list_of_demand_indices)+1)*y[i][j] >= z[j] - len(list_of_demand_indices)

m.objective = minimize(xsum(xsum(x[i][j]*tmp_dist_matrix[i][j] for i in range(len(list_of_demand_indices)))for j in range(len(list_of_demand_indices))))

# Giving the solution of the greedy heuristic as a starting point TODO: give a non-partial solution
#m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]
# m.start = [[[(x[t][i][j], greedySol[t][i][j]) for t in newtours] for i in relevant] for j in relevant]

###############################################################
############## Resolution of the MIP problem ##################
###############################################################

if optSolve == True:
    solution = [[0 for _ in list_of_demand_indices] for _ in list_of_demand_indices]
    status = m.optimize(max_seconds=60)
    if status == OptimizationStatus.OPTIMAL:
        print('\nAn optimal solution was found with an objective value of {}'.format(m.objective_value))

        if optVerbose == True:
            print('x')
        for i in range(len(list_of_demand_indices)):
            for j in range(len(list_of_demand_indices)):
                solution[i][j] = x[i][j].xi(0)
                if optVerbose == True:
                    print(int(x[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('y')
        for i in range(len(list_of_demand_indices)):
            for j in range(len(list_of_demand_indices)):
                if optVerbose == True:
                    print(int(y[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('load')
        for i in range(len(list_of_demand_indices)):
            for j in range(len(list_of_demand_indices)):
                if optVerbose == True:
                    print(int(load[i][j].xi(0)),end='  ')
            if optVerbose == True:
                print('')
        if optVerbose == True:
            print('z')
        for j in range(len(list_of_demand_indices)):
            if optVerbose == True:
                print(float(z[j].xi(0)),end='  ')
        if optVerbose == True:
            print('')
        if optVerbose == True:
            print('the path')
            the_path = [0]
            curr_index = 0
            while True:
                for i in range(len(list_of_demand_indices)):
                    if int(x[curr_index][i].xi(0)) == 1:
                        the_path.append(list_of_demand_indices[i])
                        curr_index = i
                        break
                if curr_index == 0:
                    break
            print(list_of_demand_indices)
            print(the_path)
                        
					
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
