# -*- coding: utf-8 -*-
"""
Comparaison des cumuls de précipitations entre pluviomètres et cumuls radars
"""

from math import floor
import numpy as np
from calculSpherique import distance
import os
import csv

"""
Tableau des cumuls mensuels radar
Les valeurs sont dérivées du pluviomètre de Pors Raden pour le mois de janvier
- chaque valeur est le cumul de pluie en mm  pour 1 mois pour un carré de 500 mètres
- les coordonnées GPS de cette matrice sont données pour le coin supérieur gauche
- il y autant de matrices que de périodes mesurées. Ici il n'y a qu'un seul mois (janvier).
"""
origineLatitude = 48.85
origineLongitude = -3.60
cumulRadar = np.array([
    [65,57,78,62,60,65,78,55,59,60,57,67,76,70,75,65,66,58,70,73,76,59,73,76,66,77,77,77,67,53],
    [67,62,68,76,68,78,73,56,62,73,60,66,62,72,68,61,52,59,78,70,73,54,69,61,71,75,66,71,75,55],
    [60,52,75,57,66,55,75,74,76,57,75,52,65,70,71,73,74,67,70,75,73,64,77,58,61,57,56,66,75,59],
    [70,76,61,53,66,57,65,72,53,64,76,72,53,53,59,71,64,62,58,76,73,54,59,55,62,57,71,75,58,66],
    [78,56,59,72,71,53,62,72,76,76,56,57,67,60,67,70,77,53,54,70,70,60,72,65,54,66,58,66,66,75],
    [78,63,53,70,73,68,73,56,63,60,64,60,52,68,70,69,66,66,57,75,75,73,54,53,59,64,77,77,68,75],
    [56,62,71,70,71,66,53,60,52,77,57,61,68,57,78,63,57,64,59,56,66,68,56,55,55,54,64,52,70,69],
    [64,65,63,71,57,53,65,64,67,66,53,71,63,65,71,59,73,71,60,66,68,55,58,64,68,67,71,73,53,75],
    [73,62,62,55,77,74,52,60,73,57,72,69,62,70,70,62,68,64,60,68,77,71,60,78,58,78,58,69,77,52],
    [58,75,66,77,64,60,77,57,68,71,62,53,56,72,76,63,64,64,74,65,64,64,77,76,58,58,63,73,62,70],
    [55,65,71,62,62,55,53,53,78,58,56,77,71,56,78,71,57,76,64,54,66,57,72,69,77,64,59,66,77,61],
    [70,58,75,66,60,68,70,77,60,72,66,64,61,78,73,72,52,59,71,67,53,63,65,54,71,63,73,57,75,65],
    [60,67,71,68,66,58,70,54,57,55,72,75,68,66,66,54,73,75,78,65,54,71,63,57,64,54,77,73,62,59],
    [74,72,62,72,54,60,77,60,66,65,60,62,67,75,73,73,58,58,68,60,77,56,75,78,75,64,70,55,64,53],
    [66,60,58,70,55,58,58,53,63,69,65,54,75,55,52,62,77,71,60,60,62,66,69,75,69,56,57,71,66,62],
    [59,66,69,68,72,64,66,70,70,73,53,64,58,72,77,60,71,71,56,72,58,70,60,77,66,57,77,77,60,60],
    [62,53,62,64,75,77,76,64,57,62,59,64,73,71,66,70,53,74,69,59,58,71,60,75,56,59,61,73,60,60],
    [71,72,62,58,77,62,57,60,66,78,55,69,54,68,53,60,66,52,77,65,59,73,56,58,58,71,76,53,52,73],
    [73,74,53,70,59,62,66,60,73,68,59,64,63,68,59,53,64,55,54,62,70,62,73,54,72,71,78,68,55,61],
    [78,62,71,61,53,66,71,58,56,77,61,65,71,64,77,62,53,61,52,62,71,70,66,60,55,75,55,56,55,55],
    [56,77,53,56,64,68,74,62,56,78,54,76,64,78,61,62,60,76,69,66,69,70,58,76,76,74,73,55,60,73],
    [72,54,61,77,73,60,59,77,71,72,77,64,72,55,60,76,59,73,68,62,73,61,63,75,65,65,60,58,65,75],
    [66,73,75,53,77,58,55,66,70,66,73,52,75,71,66,52,66,54,64,71,74,68,75,63,77,58,71,58,57,66],
    [79,70,57,54,73,57,59,68,55,65,71,77,68,77,76,71,72,62,75,64,70,65,71,78,77,58,66,53,70,62],
    [72,60,60,76,61,52,70,70,65,57,70,52,62,54,59,66,64,71,66,64,62,61,60,63,66,57,57,58,58,57],
    [66,65,71,59,62,60,77,63,75,55,57,55,73,76,68,61,57,75,61,77,74,54,65,60,53,63,68,71,56,72],
    [64,77,73,57,69,68,77,67,66,71,55,76,71,66,57,77,54,66,69,63,71,56,72,78,62,60,69,57,60,58],
    [66,57,61,56,53,60,64,54,58,53,69,55,55,68,65,52,68,60,55,61,58,65,74,70,60,73,66,64,73,61],
    [55,77,66,75,55,55,65,70,71,73,75,55,53,76,54,70,58,66,65,68,69,73,77,78,75,52,72,57,62,62],
    [74,57,53,64,58,62,68,66,54,58,66,54,53,75,75,58,52,68,56,68,72,62,77,53,66,71,75,64,58,72]
    ])

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

mois = 1                # mois pour lequel on effectue la comparaison entre pluviomètres
ecartNormal = 0.1       # écart acceptable entre le cumul du pluviomètre et celui du radar en pourcentage

# suppression de l'ancien fichier des anomalies
try:
    os.remove('anomalieRadar.csv')
except OSError as erreur:
    print(erreur)

# parcours du tableau pluviometre (boucle principale)
for i in range (0,len(pluviometre)):

    # reé-initialisation des variables pour le nouveau pluviomètre examiné    
    anomalie = False
    
    # mémorisation des coordonnées du pluviomètre
    latitude = pluviometre[i,1]
    longitude = pluviometre[i,2]
    print('----------------------------------------')   
    print('pluviomètre numéro ' + str(pluviometre[i,0]))
    
    # détermination de la ligne de la matrice de Météo France où se trouve le pluviomètre d'après sa latitude
    # chaque chiffre de la matrice de Météo France représente un carré de 500 mètres
    ligne = distance(origineLatitude, 0, latitude, 0)   # distance en kilomètres
    ligne = ligne / 0.5 # carré de 500 mètres
    ligne = floor(ligne) # arrondi inférieur (la matrice commence à l'index 0)
    #print('ligne = ' + str(ligne))

    # détermination de la colonne de la matrice de Météo France où se trouve le pluviomètre d'après sa longitude
    # chaque chiffre de la matrice de Météo France représente un carré de 500 mètres
    colonne = distance(0,origineLongitude, 0, longitude)   # distance en kilomètres
    colonne = colonne / 0.5 # carré de 500 mètres
    colonne = floor(colonne) # arrondi inférieur (la matrice commence à l'index 0)
    #print('colonne = ' + str(colonne))
    
    # mémorisation du cumil radar correspondant au pluviomètre
    cumulMeteoFrance = cumulRadar[ligne,colonne]
    print('cumul du radar = ' + str(cumulMeteoFrance) + ' mm')

    # recherche de la pluviométrie de la station pour le mois voulu
    for k in range (0, len(cumulPluviometre)):
        if int(cumulPluviometre[k,0]) == pluviometre[i,0] and int(cumulPluviometre[k,3]) == mois:
            cumulStation = int(cumulPluviometre[k,4])
            print('cumul du pluviomètre = ' + str(cumulStation) + ' mm')
            
    # calcul de l'écart du cumul de la station avec le cumul du radar
    # et détection anomalie si supérieur à l'écart normal
    ecart = abs(cumulStation - cumulMeteoFrance) / cumulStation
    print('écart de précipitation = ' + str(ecart) + ' mm')
    if (ecart > ecartNormal):
        anomalie = True
        print ('**** anomalie par rapport au radar ****')
        
    # écriture du résultat dans un fichier
    # sous la forme : (id du pluviomètre; écart en pourcentage; anomlie True ou False)    
    with open('anomalieRadar.csv', 'a') as fichier:
        writer = csv.writer(fichier, delimiter = ';', lineterminator = '\n')
        writer.writerow([pluviometre[i,0], ecart, anomalie])
