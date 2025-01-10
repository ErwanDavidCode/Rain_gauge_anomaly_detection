# -*- coding: utf-8 -*-
"""
Comparaison des cumuls de précipitations entre pluviomètres voisins
"""

import numpy as np
import statistics
from calculSpherique import distance
import os
import csv

"""
Tableau des pluviomètres du réseau
- data 1 = id pluviomètre
- data 2 = latitude décimale
- data 3 = longitude décimale
- data 4 = altitude en mètres
"""
pluviometre = np.array([
    [1,48.760966,-3.573622,50],
    [2,48.760125,-3.577386,65],
    [3,48.760287,-3.564522,5],
    [4,48.764319,-3.569865,80],
    [5,48.769339,-3.564673,70],
    [6,48.769523,-3.584521,10],
    [7,48.807199,-3.567956,10],
    [8,48.785827,-3.523753,90],
    [9,48.797758,-3.504055,80],
    [10,48.833506,-3.514247,50]
    ])

"""
Tableau des cumuls mensuels des pluviomètres
Les valeurs sont dérivées d'observations réelles sur le pluviomètre de Pors Raden
- data 1 = id pluviomètre
- data 2 = type de période du cumul (m = mois)
- data 3 = année du cumul
- data 4 = mois du cumul
- data 5 = cumul (mensuel) en mm
"""
cumulPluviometre = np.array([
    [1,'m',2019,1,67],
    [1,'m',2019,2,35],
    [1,'m',2019,3,43],
    [1,'m',2019,4,38],
    [1,'m',2019,5,26],
    [1,'m',2019,6,65],
    [1,'m',2019,7,9],
    [1,'m',2019,8,34],
    [1,'m',2019,9,45],
    [1,'m',2019,10,111],
    [1,'m',2019,11,113],
    [1,'m',2019,12,75],
    [2,'m',2019,1,55],
    [2,'m',2019,2,30],
    [2,'m',2019,3,42],
    [2,'m',2019,4,31],
    [2,'m',2019,5,22],
    [2,'m',2019,6,73],
    [2,'m',2019,7,10],
    [2,'m',2019,8,29],
    [2,'m',2019,9,45],
    [2,'m',2019,10,108],
    [2,'m',2019,11,136],
    [2,'m',2019,12,68],
    [3,'m',2019,1,76],
    [3,'m',2019,2,35],
    [3,'m',2019,3,42],
    [3,'m',2019,4,36],
    [3,'m',2019,5,22],
    [3,'m',2019,6,77],
    [3,'m',2019,7,8],
    [3,'m',2019,8,41],
    [3,'m',2019,9,38],
    [3,'m',2019,10,132],
    [3,'m',2019,11,128],
    [3,'m',2019,12,74],
    [4,'m',2019,1,70],
    [4,'m',2019,2,32],
    [4,'m',2019,3,41],
    [4,'m',2019,4,44],
    [4,'m',2019,5,21],
    [4,'m',2019,6,60],
    [4,'m',2019,7,8],
    [4,'m',2019,8,39],
    [4,'m',2019,9,47],
    [4,'m',2019,10,122],
    [4,'m',2019,11,133],
    [4,'m',2019,12,85],
    [5,'m',2019,1,79],
    [5,'m',2019,2,39],
    [5,'m',2019,3,40],
    [5,'m',2019,4,37],
    [5,'m',2019,5,25],
    [5,'m',2019,6,71],
    [5,'m',2019,7,10],
    [5,'m',2019,8,40],
    [5,'m',2019,9,43],
    [5,'m',2019,10,111],
    [5,'m',2019,11,122],
    [5,'m',2019,12,75],
    [6,'m',2019,1,65],
    [6,'m',2019,2,36],
    [6,'m',2019,3,40],
    [6,'m',2019,4,40],
    [6,'m',2019,5,22],
    [6,'m',2019,6,60],
    [6,'m',2019,7,9],
    [6,'m',2019,8,37],
    [6,'m',2019,9,48],
    [6,'m',2019,10,120],
    [6,'m',2019,11,125],
    [6,'m',2019,12,85],
    [7,'m',2019,1,60],
    [7,'m',2019,2,39],
    [7,'m',2019,3,44],
    [7,'m',2019,4,36],
    [7,'m',2019,5,24],
    [7,'m',2019,6,78],
    [7,'m',2019,7,9],
    [7,'m',2019,8,35],
    [7,'m',2019,9,45],
    [7,'m',2019,10,89],
    [7,'m',2019,11,136],
    [7,'m',2019,12,78],
    [8,'m',2019,1,75],
    [8,'m',2019,2,38],
    [8,'m',2019,3,42],
    [8,'m',2019,4,43],
    [8,'m',2019,5,31],
    [8,'m',2019,6,60],
    [8,'m',2019,7,10],
    [8,'m',2019,8,29],
    [8,'m',2019,9,49],
    [8,'m',2019,10,123],
    [8,'m',2019,11,119],
    [8,'m',2019,12,61],
    [9,'m',2019,1,74],
    [9,'m',2019,2,38],
    [9,'m',2019,3,35],
    [9,'m',2019,4,40],
    [9,'m',2019,5,28],
    [9,'m',2019,6,60],
    [9,'m',2019,7,10],
    [9,'m',2019,8,37],
    [9,'m',2019,9,39],
    [9,'m',2019,10,112],
    [9,'m',2019,11,102],
    [9,'m',2019,12,63],
    [10,'m',2019,1,58],
    [10,'m',2019,2,37],
    [10,'m',2019,3,39],
    [10,'m',2019,4,33],
    [10,'m',2019,5,23],
    [10,'m',2019,6,58],
    [10,'m',2019,7,7],
    [10,'m',2019,8,33],
    [10,'m',2019,9,47],
    [10,'m',2019,10,125],
    [10,'m',2019,11,133],
    [10,'m',2019,12,66]
    ])

distanceMaximum = 5.0   # définition de la distance maximum (en km) entre 2 pluviomètres pour qu'ils soient comparables
mois = 12               # mois pour lequel on effectue la comparaison entre pluviomètres
ecartMoyenne = 0.1      # écart acceptable entre la moyenne et le cumul de référence

# suppression de l'ancien fichier des anomalies
try:
    os.remove('anomaliePluviometre.csv')
except OSError as erreur:
    print(erreur)

# parcours du tableau pluviometre (boucle principale)
for i in range (0,len(pluviometre)):

    # remise à zéro du tableau où on stocke les cumuls à moyenner pour la comparaison  et ré-initialisation des variables pour chaque pluviomètre  
    cumulCompare = []
    cumulReference = 0
    anomalie = False
    
    # mémorisation des coordonnées du pluviomètre
    latitude = pluviometre[i,1]
    longitude = pluviometre[i,2]
    print('----------------------------------------')    
    print('pluviomètre numéro ' + str(pluviometre[i,0]))

    # recherche de sa pluviométrie pour le mois voulu, avec une commande SQL ce serait direct
    for k in range (0, len(cumulPluviometre)):
        if int(cumulPluviometre[k,0]) == pluviometre[i,0] and int(cumulPluviometre[k,3]) == mois:
            cumulReference = int(cumulPluviometre[k,4])
            print('cumul de référence = ' + str(cumulReference) + ' mm')
            print('................................')

    # parcours de tous les autres pluviomètres
    for j in range (0, len(pluviometre)):
        
        if i != j:
            # calcul de la distance entre 2 pluviomètres différents
            if (distance(latitude,longitude,pluviometre[j,1],pluviometre[j,2])) <= distanceMaximum:
                print('station proche numéro ' + str(pluviometre[j,0]))

                # parcours de la table cumulPluviometrie pour trouver le cumul du mois cherché pour le pluviomètre courant
                for k in range (0, len(cumulPluviometre)):
                    if int(cumulPluviometre[k,0]) == pluviometre[j,0] and int(cumulPluviometre[k,3]) == mois:
                        print('cumul = ' + str(cumulPluviometre[k,4]) + ' mm')
                        cumulCompare.append(int(cumulPluviometre[k,4]))
            
    # calcul de la moyenne arithmétique des pluviomètres comparables
    totalCumul = 0
    for j in range (0, len(cumulCompare)):
        totalCumul += int(cumulCompare[j])
    moyenne = totalCumul / len(cumulCompare)
    print('................................')
    print('moyenne = ' + str(moyenne) + ' mm')
    
    # calcul de la médiane et de l'écart type des pluviomètres comparables
    median = statistics.median(cumulCompare)
    ecartType = statistics.pstdev(cumulCompare)
    print('mediane = ' + str(median) + ' mm')
    print('écart type = ' + str(ecartType))

    # est-ce que le cumul du pluviomètre dépasse la moyenne de l'écart paramétré 
    ecart = abs(moyenne - cumulReference) / cumulReference
    if (ecart > ecartMoyenne):
        anomalie = True
        print('**** anomalie par rapport aux pluviomètres proches ****')
    print(' ')

    # écriture du résultat dans un fichier
    # sous la forme : (id du pluviomètre; écart en pourcentage; anomlie True ou False)    
    with open('anomaliePluviometre.csv', 'a') as fichier:
        writer = csv.writer(fichier, delimiter = ';', lineterminator = '\n')
        writer.writerow([pluviometre[i,0], ecart, anomalie])

    # Défaut du programme : si un des pluviomètres liés est en anomalie, alors la valeur de la moyenne sera faussée. 
    # Il vaudrait peut-être mieux prendre la médiane qui "gomme" les valeurs extrêmes ?
    
    