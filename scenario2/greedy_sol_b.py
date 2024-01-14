import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from python.instance import Instance
from python.verifSolution import *
from sim_annealing import *

import python.annealing as sim

from mip import *

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

sol = Solution_general(instance)
sol.initialize()
max_iterations = 10000
t0 = 1000
history = sim.simulated_annealing(sol, max_iterations, t0)
sol = history[-1]

print('total cost of simulated annealing', sol.cost)

#for command, type in sol.sol:
#    print(command, type)
#print(instance.commandList)

list_of_demand_indices = [0] + [x for xs in [[x[0], x[1]] for x in instance.commandList] for x in xs]
list_of_demands = [0] + [x for xs in [[x[2], -x[2]] for x in instance.commandList] for x in xs]
#print(list_of_demand_indices)
#print(list_of_demands)

x_start = [[0 for _ in list_of_demand_indices] for _ in list_of_demand_indices]
y_start = [[0 for _ in list_of_demand_indices] for _ in list_of_demand_indices]
z_start = [0 for _ in list_of_demand_indices]
load_start = [[0 for _ in list_of_demand_indices] for _ in list_of_demand_indices]

curr_index = 0
index_of_visiting = 0
for command, type in sol.sol:
    x_start[curr_index][2*command+type+1] = 1
    for j in range(len(list_of_demand_indices)):
        if y_start[j][curr_index] == 0 and j!=curr_index:
            y_start[curr_index][j] = 1
    load_start[curr_index][2*command+type+1] = sum([i[curr_index] for i in load_start])+list_of_demands[curr_index]
    z_start[curr_index] = index_of_visiting
    index_of_visiting += 1
    curr_index = 2*command+type+1
    
x_start[curr_index][0] = 1
z_start[curr_index] = index_of_visiting
for i in range(len(z_start)):
    z_start[i] = len(list_of_demand_indices)-1-z_start[i]
'''print('x')
for i in x:
    print(i)

print('y')
for i in range(len(y)):
    print(i, y[i])

print('load')
for i in range(len(load)):
    print(i, load[i])'''
print(z_start)

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
#print(tmp_dist_matrix)

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
        m += x[i][j] <= y[i][j]
    #m += load[i][i] == 0
'''
if optMode == '-O0':
  Too many constraints with this formulation
  for k in range(1, instance.nbFarmers+1):
    for it in combinations(instance.farmers, k):
      m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
if optMode == '-O1' or optMode == '-O2':'''
for i in range(1,len(list_of_demand_indices)):
    for j in range(1,len(list_of_demand_indices)):
        m += z[i]-(len(list_of_demand_indices)+1)*x[i][j] >= z[j] - len(list_of_demand_indices)
        m += z[i]-(len(list_of_demand_indices)+1)*y[i][j] >= z[j] - len(list_of_demand_indices)

m.objective = minimize(xsum(xsum(x[i][j]*tmp_dist_matrix[i][j] for i in range(len(list_of_demand_indices)))for j in range(len(list_of_demand_indices))))

#m.start = [(x,[[x_start[i][j] for i in range(len(x_start))] for j in range(len(x_start[0]))])]#,[[(y[i][j],y_start[i][j])for i in range(len(y_start))] for j in range(len(y_start[0]))],[(z[i],z_start[i]) for i in range(len(z_start))],[[(load[i][j],load_start[i][j])for i in range(len(load_start))] for j in range(len(load_start[0]))]]
input_x = [[(x[j][i],x_start[j][i]) for i in range(len(x_start))] for j in range(len(x_start[0]))]
input_y = [[(y[j][i],y_start[j][i]) for i in range(len(y_start))] for j in range(len(y_start[0]))]
input_load = [[(load[j][i],load_start[j][i]) for i in range(len(load_start))] for j in range(len(load_start[0]))]

m.start = [i for xs in input_x for i in xs] + [i for ys in input_y for i in ys] + [(z[i],z_start[i]) for i in range(len(z_start))] + [i for loads in input_load for i in loads]

def check_feasibility(x, y, z, load):
    for i in range(len(list_of_demand_indices)): #without depot
        #m += load[0][i] == 0                                          #load_1
        #m += load[i][0] == 0                                          #load_2

        #m += xsum(x[j][i] for j in all_locations) == xsum(x[i][k] for k in all_locations) #flow_1
        #m += xsum(x[j][i] for j in all_locations) <= 1
        
    
        for j in range(len(list_of_demand_indices)):
            if y[i][j]+y[j][i] > 1:
                print('y[i][j]+y[j][i] <= 1', i, j)                                   #precedence_1
            #m += x[i][j] <= y[i][j]                                     #precedence_3
            if load[i][j] > instance.capacity * x[i][j]:
                print('load[i][j] <= instance.capacity * x[i][j]', i, j)                       #load_4
        
            for k in range(len(list_of_demand_indices)):
                if x[j][i]+y[i][j]+y[j][k]+y[k][i] > 2:
                    print('x[j][i]+y[i][j]+y[j][k]+y[k][i] <= 2', i, j, k)
                #m += x[j][i]+y[i][j]+y[j][k]+y[k][i] <= 2                 #precedence_2

    #for order in instance.demandsFarmersClients:
    #    m += y[order[0]][order[1]] == 1

    #m += xsum(x[0][j] for j in all_locations[1:]) == 1 #depot_1
    #m += xsum(x[i][0] for i in all_locations[1:]) == 1 #depot_2

    #for i in instance.farmers:
        #for j in instance.clients:
    for i in range(1,len(list_of_demand_indices),2):
        if y[i][i+1] != 1:
            print('y[i][i+1] == 1', i)   #precedence_4

    for j in range(len(list_of_demand_indices)):     
        if sum([load[i][j] for i in range(len(list_of_demand_indices))]) != sum([load[j][k] for k in range(len(list_of_demand_indices))]) - list_of_demands[j]:
            print('xsum(load[i][j] for i in range(len(list_of_demand_indices))) == xsum(load[j][k] for k in range(len(list_of_demand_indices))) - list_of_demands[j]', j)
        #m += xsum(load[i][j] for i in range(len(list_of_demand_indices))) == xsum(load[j][k] for k in range(len(list_of_demand_indices))) - list_of_demands[j] #load_3
        


    for i in range(len(list_of_demand_indices)):
        if x[i][i] != 0:
            print('x[i][i] == 0', i)            #flow_2
        if sum([x[i][j] for j in range(len(list_of_demand_indices))]) != sum([x[k][i] for k in range(len(list_of_demand_indices))]):
            print('xsum(x[i][j] for j in range(len(list_of_demand_indices))) == xsum(x[k][i] for k in range(len(list_of_demand_indices)))', i)
        if sum([x[j][i] for j in range(len(list_of_demand_indices))]) != 1:
            print('xsum(x[j][i] for j in range(len(list_of_demand_indices))) == 1', i)
        if load[0][i] != 0:
            print('load[0][i] == 0', i)                                         #load_1
        if load[i][0] != 0:
            print('load[i][0] == 0', i)   
        for j in range(1,len(list_of_demand_indices)):
            if x[i][j] > y[i][j]:
                print('x[i][j] <= y[i][j]', i, j)
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
            if z[i]-(len(list_of_demand_indices)+1)*x[i][j] < z[j] - len(list_of_demand_indices):
                print('z[i]-(len(list_of_demand_indices)+1)*x[i][j] >= z[j] - len(list_of_demand_indices)', i, j)
            
            if z[i]-(len(list_of_demand_indices)+1)*y[i][j] < z[j] - len(list_of_demand_indices):
                print('z[i]-(len(list_of_demand_indices)+1)*y[i][j] >= z[j] - len(list_of_demand_indices)', i, j)


print('check feasibility')
#print(m.validate_mip_start())
check_feasibility(x_start, y_start, z_start, load_start)
print('end check')
for i in x_start:
    print(i)
print(z_start)
print(m.validate_mip_start())
if optSolve == True:
    solution = [[0 for _ in list_of_demand_indices] for _ in list_of_demand_indices]
    status = m.optimize(max_seconds=1200)
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
