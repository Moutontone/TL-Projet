# Sections needed
- State of the art
- Problem modelisation
- data collection and manipulation

# Problem Definition
## General setting
A set of farmers F
A set of Client C
A unique depot D
L is the set of location := F u C u {D}

A cost matrix (d_ij) estimated cost from i to j in L
the cost include cost per km and cost per time

A set of dates T
A set of order per date t in T
an order is a weight of food demanded by a client to a farmer
one client can make multiple command to different farmer per date.
a farmer can receive commande from multiple client.
a client cannont order multiple times to the same farmer on the same date.
a client or a farmer can be iddle at some dates

A capacity Q for the vehicle

We assume that a client cannot order more than the capacity of the vehicule each date.
We assue that a farmer cannot being order more than Q each date.

A command cannot be delivierd or pick up in multiple times. A command is either pick/deliverd as a whole or not.
## Subject 1
the vehicule has to collect all deliveries at the farmers fist. Eventually it might make several stop at the Depot.
Only then the client will be delivered, eventually with stop at the depot to refiel commande.
## Subject 2
The vehicle start from the Depot. It needs to collect deliveries at famers and delivers them to client before returning to the Depot.


# Fairness
différents cout individuel

fairness naiv c_opt/n
fairness par chiffre (distribuer le gain en proportion/en absolue)

notion quel est le poids d'un fermier dans la solution commune ?
-> calculer le chemin opt sans ces commandes ?
maybe definire une repartition en fonction de ca.

comment evaluer une fariness par rapport a une autre ? 
justifier les fairness par des explications.
fairness jour a jour ou long terme ?
