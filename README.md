# TL-Projet
Projet de groupe de l'UE Transport-Logistique du M2 ORCO

## Compte rendu des seances
## Seance 1
25/10/2023

Analyse du sujet et première réflexion.
Mise en place d'une première road map:
- Modélisation des 2 scénarios par un MIP dans le but de minimiser le cout du trajet
- recherche dans la littérature pour trouver d'autre modélisation et des heuristiques 
- Après résolution sur une instance, trouver une répartition "equitable" du cout entre les fermiers
- Analyser notre solution et ses limites
- Améliorer la solution et explorer des nouvelles pistes

## Seance 2
08/11/2023

Précisions pour le sujet 2:
On peut montrer qu'il n'y aura qu'une seule boucle, pas de passage dans au hub.
{On peut supposer que la capacité du camions Q permet de récupérer toutes les commande d'un fermier en 1 seule fois} -> finalement cette hypothese n'est peut etre pas necessaire.
De toute facon on fait nos propres hypothese et on assume.
Finalisation du modele pour le sénario 2. Il manque juste a lineariser les variables Ni

## Seance 3
15/11/2023

! TODO !

## Seance 4
22/11/2023
Utilisaton de la bibliotheque python : https://python-mip.readthedocs.io/en/latest/quickstart.html

## Seance 5
29/11/2023

State of the project:
Senario 2 -> looking in the literatur to find modeles as close as possible to our problem.
Senario 1 -> model found int the paper [ref]. We know how to use the solver and we are now tried the model.

Goal: senario 2 find a modelisation. senario 1: ameliorer le code et mieux comprendre le solver. Thibk about fairnes

Start the redaction of the Rapport on Overleaf. Starting finding definitions for fairness.
