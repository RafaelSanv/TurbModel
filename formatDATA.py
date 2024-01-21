# -*- coding: utf-8 -*-
""" --------------------------------------------------------------------------------------------------------------
#   Code created by: Rafaël Sanvicente (rafael.sanvicente.116@cranfield.ac.uk) for the turbulence modeling assignment
#                   part of the MSc in CFD course.
#
#    Formats the .dat files of fluent ASCII export to match the input format required by P.Hoyos matlab script
#    Goes through all files and folders inside the script repository and deletes the first row and column of the files
#    and saves a copy with the extension '_modified'
#
#   LICENCE:
#   This script is free of use for any student / research related work, NON-COMMERCIAL USE ONLY.
#   If you are brought to use this project, the author kindly asks for this work to be referenced.
#   Feel free to improve this file as you wish and implement further capabilities 
#
#   Created: 01/2024
#   V1.0
 ---------------------------------------------------------------------------------------------------------------- """


import os

# Définir le suffixe à ajouter au fichier modifié
suffix = '_modified'

# Fonction pour retirer la première colonne et écrire un nouveau fichier
def remove_first_column_and_save(new_path, lines):
    # Retirer la première colonne
    modified_lines = [','.join(line.split(',')[1:]) for line in lines]
    # Écrire les lignes modifiées dans le nouveau fichier
    with open(new_path, 'w') as file:
        file.writelines(modified_lines)

# Parcourir le répertoire d'exécution et les sous-dossiers
for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.dat'):
            # Chemin complet du fichier original
            original_path = os.path.join(root, filename)
            # Lire le contenu du fichier
            with open(original_path, 'r') as file:
                lines = file.readlines()
            
            # Créer le chemin du nouveau fichier
            new_filename = f"{os.path.splitext(filename)[0]}{suffix}{os.path.splitext(filename)[1]}"
            new_path = os.path.join(root, new_filename)
            
            # Appeler la fonction pour retirer la première colonne et sauvegarder le fichier
            remove_first_column_and_save(new_path, lines)

print("La première colonne a été retirée de tous les fichiers .dat dans le répertoire et les sous-dossiers.")
