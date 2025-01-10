# -*- coding: utf-8 -*-
"""
détection des pluviomètres en anomalies en pondérant les anomalies précédemment détectées
- les anomalies entre pluviomètres ont un poids de 6
- les anomalies avec les radars ont un poids de 4
Le seuil de défaut probable du pluviomètre est paramétré à 10%
"""

import os
import csv

print('')
print('*****************************************************')
print('comparaison entre pluviomètres')
print('*****************************************************')
print('')
try:
    import cumulPluviometresV3
except ImportError:
    print('erreur import cumulPluviometres')

print('')
print('*****************************************************')
print('comparaison avec les cumuls radars')
print('*****************************************************')
print('')
try:
    import cumulRadarsV3
except ImportError:
    print('erreur import cumulRadars')

print('')
print('')    
print('*****************************************************')
print('pondération des anomalies')
print('*****************************************************')
print('')


# intialisation des variables et ouverture des fichiers d'anomalies précédemment créés
anomalies = []
seuilAnomalie = 0.1
fichierPluviometre = open('anomaliePluviometre.csv')
fichierRadar = open('anomalieRadar.csv')

# lecture des 1er enregistrements
recordPluviometre = fichierPluviometre.readline()
recordRadar = fichierRadar.readline()

# parcours des fichiers et stockage des anomalies dans un tableau unique.
# Le fichier anomaliePluviometre est maître.
# chaque ligne du tableau correspond à un pluviomètre et ses 3 anomalies possibles (pluviometres, radars, normales).
while recordPluviometre != '':

    # récupération des données
    elementPluviometre = recordPluviometre.split(';')               # transforme le record en tableau
    elementPluviometre[2] = elementPluviometre[2].rstrip('\n')      # enlève le retour ligne \n
    elementRadar = recordRadar.split(';')
    elementRadar[2] = elementRadar[2].rstrip('\n')
    
    # stockage dans le tableau
    anomalie = elementPluviometre + elementRadar                    # concaténation des 3 records
    anomalies.append(anomalie)

    # lecture enregistrements suivants
    recordPluviometre = fichierPluviometre.readline()
    recordRadar = fichierRadar.readline()

fichierPluviometre.close()
fichierRadar.close()

# affichage du résumé des anomalies détectées précédemment
print('---- Résumé des anomalies ----')
print('Pluviomètre\tanomalie\t\t\tanomalie')
print('\t\t\tpluviomètres\t\tradars')
for i in range (0, len(anomalies)):
    anomalie = anomalies[i]
    print(f'{anomalie[0]:<12s} {anomalie[2]:<16s} {anomalie[5]:<12s}')
print('')

# affichage du résumé des écarts calculés précédemment
print('---- Résumé des écarts ----')
print('Pluviomètre\técart %\t\t\técart %')
print('\t\t\tpluviomètres\t\tradars')
for i in range (0, len(anomalies)):
    anomalie = anomalies[i]
    ecartPluviometre = str(round(float(anomalie[1]),4))
    ecartRadar = str(round(float(anomalie[4]),4))
    print(f'{anomalie[0]:<12s} {ecartPluviometre:<16s} {ecartRadar:<12s}')
print('')

# pondération des anomalies
# les anomalies entre pluviomètres ont un poids de 6
# les anomalies avec les radars ont un poids de 4
print('---- Anomalies pondérées ----')
print('Pluviomètre\t\técart pondéré %\tanomalie pondérée')
anomaliePonderee = ''
for i in range (0, len(anomalies)):
    anomalie = anomalies[i]
    ecart = (6 * float(anomalie[1])) + (4 * float(anomalie[4]))
    ecart = ecart / 10
    ecart = round(ecart,4)
    if ecart > seuilAnomalie:
        anomaliePonderee = 'défaut pluviomètre'
    print(f'{anomalie[0]:<16s} {str(ecart):<16s} {str(anomaliePonderee):<8s}')
    anomaliePonderee = ''

