#To view your results :

python3 viewResults.py ../data/subject_1_depots.txt ../data/test_routes.txt ../data/test_allocation.txt

//In order to use viewResults.py you should create the following files (with the format that will be indicated below) :
     -A file containing the routes
     -A file containing an allocation
     -A file containing a set of depots (only for subject 2.2)

#info_instance.txt explanation:

farmers 21 #there are 21 farmers
clients 39 #there are 39 clients
capacity 1000 #the vehicle has a capacity of 1T
locationCost 10000 #opening a new depot has a cost of 10000 (only subject 2.2)
costPerKm 3.5 #We consider that 10 pixels are worth 1 km. Costs are in euros. The distance in pixels between two locations in the coordinate file is their euclidean distance (sqrt((x2-x1)**2 + (y2-y1)**2)). The distance in km is then the euclidean distance in pixels divided by 10.
nbOfDates 208 #The demand file has 208 order matrices.

//info_instance.txt should NOT be modified. You can create your own instances.

#Depots file format:

depot1, depot2, ..., depotN

//depoti corresponds to the index in the coordinate file that you wish to open as a depot. In subject 1, the only depot opened is in the location of index 0. 
//Location 0 is a depot both in subject 2.1 and subject 2.2. No cost should be allocated to location 0. In subject 2.2, new depots are opened at the farms (and only at the farms).
//A cost must also be allocated to the farms in which a depot is opened. For subject 2.1, the viewer should be executed with subject_1_depots.txt (do NOT modify it). 

#Route file format:

depot_route_1, location_1_route_1, location_2_route_1, ..., location_n_route_1, depot_route_1
depot_route_2, location_1_route_2,         ...            , location_l_route_2, depot_route_2
...
depot_route_p, location_1_route_p,         ...            , location_o_route_p, depot_route_p

//The locations and the depots are represented as indexes in the coordinate file.

#Allocation file format:

val1, val2, ..., valm

//vali is the value allocated to farmer i.

#Coordinates file format:

x_depot, y_depot
x_farmer_1, y_farmer_1
x_farmer_2, y_farmer_2
...
x_farmer_21, y_farmer_21
x_client_1, y_client_1,
...
x_client_39, y_client_39

#Demands file format:

#1:
order_client_1_to_farmer_1_day_1, order_client_1_to_farmer_2_day_1, ..., order_client_1_to_farmer_21_day_1
...
order_client_39_to_farmer_1_day_1,                   ...               , order_client_39_to_farmer_21_day_1
#2:
...
#208:
order_client_1_to_farmer_1_day_208,                  ...               , order_client_1_to_farmer_21_day_208
...
order_client_39_to_farmer_1_day_1,                   ...               , order_client_39_to_farmer_21_day_1

//order_client_i_to_farmer_j_day_t corresponds to the number of kg that client i ordered to farmer j in day t.
//demands.txt should NOT be modified. You can create your own demand files.

#cost_matrix.txt file format:

cost_location_1_to_location_1, ... cost_location_1_to_location_60
...
cost_location_60_to_location_1, ..., cost_location_60_to_location_60
