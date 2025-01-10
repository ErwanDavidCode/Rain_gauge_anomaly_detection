#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonction de calcul de la distance entre 2 points du globe à partir des coordonnées GPS décimales.
On considère (pour cette version) que la terre est une sphère parfaite.
La disatnce est calculée en kilomètres.

source documentaire = IGN (Institut national de l'information géographique et forestière): https://geodesie.ign.fr
    
Comment obtenir la distance entre deux points connus en longitude et latitude sur la sphère ?

Connaissant la position de deux points A et B sur une sphère, calculer la distance entre
eux revient à calculer l'abscisse curviligne S (AB) sur le grand cercle passant par A et B.
Si l’on considère deux points A et B sur la sphère, de latitudes φA et φB et de longitudes λA et λB,
alors la distance angulaire en radians SA-B entre A et B est donnée par la relation fondamentale de trigonométrie sphérique :

    dλ = λB – λA : 
    SA-B = arc cos (sin φA sin φB + cos φA cos φB cos dλ)

La distance S en mètres, s’obtient en multipliant SA-B par un rayon de la Terre conventionnel (6 378 137 mètres pour une sphère parfaite).

    S = (SA-B) * 6 78 137
    

Exemples

Soient deux points A et B :
λA = 0°                       (0 radian)
φA = 45°                      (0.7854 radians)
λB = 1° 50’ 03.156468′′       (0.0320 radians)
φB = 46° 15’ 28.463641′′      (0.8074 radians)
La distance entre A et B calculée est S = 200 km

Soient deux points A et B :
λA = -5°                      (-0.0873 radians)
φA = 40°                      (0.6981 radians)
λB = -3° 18’ 44.877103′′      (-0.0578 radians)
φB = 41° 15’ 40.924579′′      (0.7201 radians)
La distance entre A et B calculée est S = 200 km

"""

def distance(longitudeAdecimal,latitudeAdecimal,longitudeBdecimal, latitudeBdecimal):

    from math import cos, sin, acos, radians
    
    rayonTerre = 6378137 # rayon de la terre en mètres
    
    """
    # exemples pour test : 
    longitudeA = 0       # φA
    latitudeA = 0.7854   # λA
    longitudeB = 0.0320  # φB
    latitudeB = 0.8074   # λB
    
    longitudeA = -0.0873 # φA
    latitudeA = 0.6981   # λA
    longitudeB = -0.0578 # φB
    latitudeB = 0.7201   # λB
    """
    
    # conversion des corodonnées GPS décimales en radians
    longitudeA = radians(longitudeAdecimal)
    latitudeA = radians(latitudeAdecimal)
    longitudeB = radians(longitudeBdecimal)
    latitudeB = radians(latitudeBdecimal)
    
    # calcul de l'écart angulaire entre les 2 points A et B
    ecartLongitude = longitudeB - longitudeA   # dλ = λB – λA
    #print('Ecart longitude = ' + str(ecartLongitude))
    
    # calcul de la distance angulaire entre ces 2 points
    distanceAngulaire = acos( ( sin(latitudeA) * sin(latitudeB) ) + ( cos(latitudeA) * cos(latitudeB) * cos(ecartLongitude) ) )
    #print('Distance angulaire = ' + str(distanceAngulaire))
                             
    # calcul de la distance en kilomètres entre ces 2 points
    distance = (distanceAngulaire * rayonTerre) / 1000
    #print('Distance = ' + str(distance) + ' km')

    return(distance)
