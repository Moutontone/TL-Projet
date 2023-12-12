import fileReader as fr

def setup_model():
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
    
    if optMode == '-O0':
      #Too many constraints with this formulation
      for k in range(1, nbFarmers+1):
        for it in combinations(farmers, k):
          m += xsum(xsum(xsum(x[t][i][j] for i in it) for j in it)for t in newtours) <= k-1
    if optMode == '-O1' or optMode == '-O2':
      for i in farmers:
        for j in farmers:
          for t in newtours:
            m += y[t][i]-(nbFarmers+1)*x[t][i][j] >= y[t][j] - nbFarmers
    
    m.objective = minimize(xsum(xsum(xsum(x[t][i][j]*distanceMatrix[i][j] for i in relevant)for j in relevant)for t in newtours))
    
    # Giving the solution of the greedy heuristic as a starting point TODO: give a non-partial solution
    m.start = [(x[greedyStart[k][0]][greedyStart[k][1]][greedyStart[k][2]], 1.0) for k in range(len(greedyStart))]
    # m.start = [[[(x[t][i][j], greedySol[t][i][j]) for t in newtours] for i in relevant] for j in relevant]
    
class Instance():
    def __init__(self, datapath) -> None:
        self.nbClients, self.nbFarmers, self.capacity, _locationCost, self.costPerKm \
                = fr.readInfoInstanceFile(datapath+'/info_instance.txt')
        # for each point we have list of 2 values [x, y] size=(60,2)
        # first depot, next farmers, next clients
        self.coordinates = fr.readCoordFile(datapath+'/coordinates.txt')
        # for each point we have a list of distance to points size=(60,60)
        self.distanceMatrix = fr.readDistanceMatrixFile(datapath+'/cost_matrix.txt')
        # size=(208,39,21)
        self.demands = fr.readDemandMatrixFile(datapath+'/demands.txt')

def get_instance(datapath):
    instance = Instance(datapath)
    return instance

def greedy_sol():
    pass

def main():
    # read arg
    # setup parameters
    # get instance
    # mis en forme
    # greedy sol
    # improve UB on t
    # setup MIP
    # solve()
    pass

if __name__ == "__main__":
    # verif arg?
    main()

"""
recherche pas liste de mots clés et différents base deonnées
puis restraindre la recheche pour limiter le nb de résultats

faire une carte des PB GPDP pour se rapprocher de notre pb et spécifier les différences

logicielle gestion references
mendeley
zotero firefox plugin

exemple fils rouge


But
enoncer les PBs BIEN!
proposer une facon de résoudre heuristique ok
demontrer les capacité de nos méthodes
choisir les bon outils
PLACE DANS LA LITTERATURE

open au proposition et différentes facon d'explorer le sujet

COMMENCER LA redaction vite!
prendre du temps pour redigier => gain de temps

fn pour associer un cout a un fermier   

cas dégénéré
"""
