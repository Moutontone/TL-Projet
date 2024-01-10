import fileReader as fr
import instance as ist
import sys

def main(args):
  argc = len(sys.argv)

  # Replace with the data repository of your choice
  datapath = '../toydata'
  if argc > 1:
    datapath = args[1]

  instance = ist.Instance(datapath)

  print(instance.demands)
  for d in range(100):
    instance.setDay(d)
    #personal cost calculations for every farmer.
    #max cost  
    farmerMaxCost = [0 for i in instance.farmers]
    for i in instance.farmers:
      #print("looking at farmer: ", i)
      cost = 0
      #go to the farmer and come back
      cost += instance.dist(0,i)*2
      for j in instance.clients:
        #if the client asked for something from this farmer, go there and come back.
        if instance.demands[instance.day][j-instance.nbFarmers-1][i-1] != 0:
            #print("looking at pair: ", i, " ", j)
            cost += instance.dist(0,j)*2
      farmerMaxCost[i-1]=cost
    print("max cost for farmers:", farmerMaxCost)
    #Worst case cost

    farmerWorstCost = [0 for i in instance.farmers]
    for i in instance.farmers:
      #print("farmmer ", i, ": ")
      cost = 0
      cost += instance.dist(0,i)*2
      visited = []
      done = False
      #start from the depot
      position = 0
      while(not done):
        smallestcost = None
        destination = None
        #consider each client
        for j in instance.clients:
          #if a client order from the farmer AND we havent visited it yet
          if instance.demands[instance.day][j-instance.nbFarmers-1][i-1] != 0 and j not in visited:
            #if first client to be considered or shorter path
            if smallestcost==None or smallestcost>instance.dist(position,j):
              smallestcost = instance.dist(position,j)
              destination = j
        #we visited every client
        if destination == None:
          cost += instance.dist(position,0)
          done = True
        else:
          #print("  pair: ", position, " ", destination)
          cost += instance.dist(position,destination)
          position = destination
          visited.append(position)
      farmerWorstCost[i-1]=cost
    print("Worst cost for farmers",farmerWorstCost)
      
    farmerHypoCost = [0 for i in instance.farmers]
    for i in instance.farmers:
      #print("farmer ", i, ": ")
      cost = 0
      visited = []
      done = False
      position = i
      while(not done):
        smallestcost = None
        destination = None
        #consider each client
        for j in instance.clients:
          #if a client order from the farmer AND we havent visited it yet
          if instance.demands[instance.day][j-instance.nbFarmers-1][i-1] != 0 and j not in visited:
            #if first client to be considered or shorter path
            if smallestcost==None or smallestcost>instance.dist(position,j):
              smallestcost = instance.dist(position,j)
              destination = j
        #we visited every client
        if destination == None:
          #print("  pair: ", position, " ", i, " ", distanceMatrix[position][i])
          cost += instance.dist(position,i)
          done = True
        else:
          #print("  pair: ", position, " ", destination, " ", distanceMatrix[position][destination])
          cost += instance.dist(position,destination)
          position = destination
          visited.append(position)
      farmerHypoCost[i-1]=cost
    print("Hypothetical cost for farmers: ", farmerHypoCost)

if __name__ == "__main__":
    main(sys.argv)