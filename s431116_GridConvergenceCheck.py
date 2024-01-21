# -*- coding: utf-8 -*-
""" --------------------------------------------------------------------------------------------------------------
#   Code created by: Rafaël Sanvicente (rafael.sanvicente.116@cranfield.ac.uk) for the turbulence modeling assignment
#                   part of the MSc in CFD course.
#
#   Extract data from a 1D line across diff. meshes for grid convergence analysis purposes
#   Will extract any quantity of data from any number of files in the folder given
#   User is responsible for sorting the data files in the correct format and order before using the script 
#   (finer mesh = first file to be read)
#   
#
#   Based on the article by NASA (based on Roache 94) : https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
#   and a useful example / explanation : https://curiosityfluids.com/2016/09/09/establishing-grid-convergence/
#   for deeper understanding and explanation, consult the work by Roache: https://www3.nd.edu/~coast/jjwteach/www/www/60130/CourseLectureNotes/Roache_1994.pdf
#
#
#   LICENCE:
#   This script is free of use for any student / research related work, NON-COMMERCIAL USE ONLY.
#   If you are brought to use this project, the author kindly asks for this work to be referenced.
#   Feel free to improve this file as you wish and implement further capabilities 
#
#   Created: 01/2024
#   V1.0
 ---------------------------------------------------------------------------------------------------------------- """

import glob
import matplotlib.pyplot as plt
import math

# Remplacer ceci par le chemin de votre dossier contenant les fichiers .dat
folder_path = '*.dat'

# Recherche de tous les fichiers .dat dans le dossier
files = glob.glob(folder_path)

# Liste pour stocker les valeurs minimales de vitesse
min_velocities = []

# Créer une figure pour le tracé
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)  # 1 row, 2 columns, first plot

# Lire et traiter chaque fichier
for file_path in files:
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Initialiser la liste pour les données
        data = []

        # Analyser et stocker les données dans une liste
        for line in lines:
            if line.strip() and line[0].isdigit():
                x, y = map(float, line.split())
                data.append((x, y))

        # Trier les données par position (x)
        data.sort(key=lambda x: x[0])

        # Séparer les données triées en x et y
        x_data, y_data = zip(*data)

        # Stocker la valeur minimale de la vitesse
        min_velocity = min(y_data)
        min_velocities.append(min_velocity)

        # Tracer les données
        plt.plot(x_data, y_data, label=file_path.split('/')[-1])  # Utiliser le nom du fichier comme étiquette
        
# Ajouter des étiquettes et un titre
plt.xlabel('Position')
plt.ylabel('X Velocity')
plt.title('Centerline X-Velocity along the tunnel')
plt.legend()
plt.grid(True)


plt.subplot(1, 2, 2)  # 1 row, 2 columns, second plot
# Calcul si assez de valeurs sont présentes
if len(min_velocities) >= 3:

    r = 1.98  # = N1/N2 (cell nb) for a 1D analysis (TO BE MEASURED)
    #Fs = 3      #Safety factor for 2 grids     
    Fs = 1.25   #Safety factor for 3+ grids
    
    # ENSURE FILES ARE NAMED IN CORRECT ORDER 1= finest mesh
    f1, f2, f3 = min_velocities[:3] 
    print(f"Minimal Values reported: f1={f1} ; f2={f2} ; f3={f3}")
    p = math.log((f3 - f2)/(f2-f1))/math.log(r)
    print(f"computed value of p: {p}")
    
    #Calculates the Richardson extrapolation
    if r>=2:
        RichEx= (4/3*f1) - (1/3*f2)
    else:
        RichEx= f1 + (f1-f2)/(r**p - 1)
        
    print(f"Richardson Extrapolated value: {RichEx}")
    
    eps1 = abs((f2-f1)/f1)   # Calcul de epsilon pour le gci
    eps2 = abs((f3-f2)/f2)
    
    GCI1= (Fs*eps1)/(r**p - 1)*100
    GCI2= (Fs*eps2)/(r**p - 1)*100
    print("GCI_1,2(%): ", GCI1)
    print("GCI_2,3(%): ", GCI2)
    
    ARGCI= GCI2/(r**p*GCI1)
    print("Asymptotic range of convergence check: ",ARGCI,"  (should be app. 1)")
    
    # Tracé de f1, f2, f3, et RichEx
    x_coords = [1, 2, 4]  # Coordonnées x arbitraires pour le tracé
    f_values = [f1, f2, f3]
    
    # Tracer f1, f2 et f3
    plt.plot(x_coords, f_values, '-o', color='blue', label='f1, f2, f3')
   # Tracer RichEx avec un marqueur différent
    plt.scatter(0, RichEx, marker='d', color='red', label='RichEx (Diamond)')

    plt.xlabel('Normalized Grid spacing')
    plt.ylabel('Velocity Recovery')
    plt.title('Velocity Data Points and Richardson Extrapolated Value')
    plt.legend()
    plt.grid(True)
    # Afficher la figure avec les deux subplots
    plt.tight_layout()
    plt.show()

else:
    print("Pas assez de données pour calculer les indices de convergence.")
    