import random
import sys

# Requires 3 arguments
if len(sys.argv) < 4:
  print('ERROR: requires 3 arguments \'datapath nbFarmers nbClients\'')
  exit()
datapath = sys.argv[1]
nbFarmers = int(sys.argv[2])
nbClients = int(sys.argv[3])

# Opens the 3 main configuration files DOES NOT COMPUTE COST MATRIX (to be done by user afterwards)
info_instance = open(datapath+'/info_instance.txt', 'w')
coordinates = open(datapath+'/coordinates.txt', 'w')
demands = open(datapath+'/demands.txt', 'w')

# Writes in info_instance.txt
info_instance.write('farmers {}\nclients {}\ncapacity {}\nlocationCost {}\ncostPerKm {}\nnbOfDates {}\n'.format(nbFarmers, nbClients, (nbFarmers+nbClients)*100, 1000, 3.5, 1))

# Writes in coordinates.txt
for i in range(nbFarmers+nbClients+1):
  coordinates.write(str(random.randint(0, 1000))+', '+str(random.randint(0, 1000))+'\n')

# Writes in demands.txt
demands.write('#1\n')
for i in range(nbClients):
  for j in range(nbFarmers):
    coin = random.randint(0, nbFarmers//2)
    if coin == nbFarmers//2:
      demands.write(str(random.randint(0, 500)))
    else:
      demands.write('0')
    if j < nbFarmers-1:
      demands.write(', ')
  demands.write('\n')
demands.write('#\n')

info_instance.close()
coordinates.close()
demands.close()
