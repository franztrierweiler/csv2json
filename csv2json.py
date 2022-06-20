#!/bin/python3

import csv
import json
import os
import sys

# Constantes
fileOrigin = './input_files'
csvFilePath = fileOrigin + '/segur.csv'

def write_json_file(file_name, data):
    with open(file_name, "w", encoding="utf-8") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))

    # Enlever les quotes et autres curiosités de Python
    os.system("sed -i 's/\"false\"/false/g' " + file_name)
    os.system("sed -i 's/\"true\"/true/g' " + file_name)
    os.system("sed -i 's/\"null\"/null/g' " + file_name)

def process_csv_dict(max_entries, json_base_name, csvReader):

    nombre_lignes = 0
    indice_fichier = 0

    # Entête
    entete_fichier = {
        'impId': 'null',
        'numeroAns': '0123456789',
        'siret': "38042372300028",
        'lignesImport': []
    }

    print(csvReader)

    for data in csvReader:

        print(data)

        # La condition unique de prise en compte est d'avoir un numéro de bon de commande non vide
        if (data['ref bdc'] != ""):

            # Ligne du CSV en cours
            nombre_lignes = nombre_lignes + 1

            # Construction du bloc "demande"
            demande = {
                'numLigne': '',
                'typeAction': 'C',
                'numeroASP': 'null',
                'numeroEditeur': 12345,
                'commande' : {},
                'beneficiaires': {},
                'piecesJustificatives': [],
                'scenarioInstallation': {},
                'codeTraitement': 'null',
                'libelleTraitement': 'null'
            }
            demande['numLigne'] = nombre_lignes
            demande['numeroEditeur'] = data['ref bdc']

            # Construction du bloc "commande"
            commande = {
                'dateCommande': 'null',
                'regimeTVA': 'null',
                'montantSegurHT': 'null',
            }
            commande['dateCommande'] = data['date commande']
            commande['regimeTVA'] = 'TTC'
            commande['montantSegurHT'] = 358.33
            # Ajout du bloc commande
            demande['commande'] = commande

            # Construction du bloc "beneficiaires"
            beneficiaires = {
                'commandePour': 'LIBERAL',
                'isMandataire': 'false',
                'isClientUnique': 'true',
                'nomMandataire': 'null',
                'emailMandataire': 'null',
                'telephoneMandataire': 'null',
                'liberal': [],
                'structure': {}
            }
            
            # Construction du bloc "liberal"
            liberal = {
                'nomMedecin': 'null',
                'emailMedecin': 'null',
                'telephoneMedecin': 'null',
                'RPPS': 'null'
            }
            liberal['nomMedecin'] = data['NomClient']
            liberal['emailMedecin'] = data['ADRMAIL']
            liberal['telephoneMedecin'] = data['telephoneMedecin']
            liberal['RPPS'] = data['RPPS']
            # Ajout du bloc "liberal"
            beneficiaires['liberal'].append(liberal)

            # Construction du bloc "structure"HT
            structure = {
                'nomResponsable': 'null',
                'emailResponsable': 'null',
                'telephoneResponsable': 'null',
                'FINESSJuridique': 'null',
                'FINESSGeo': []
            }

            # Ajout du bloc "structure"
            beneficiaires['structure'] = structure

            # Ajout du bloc "beneficiaires"
            demande['beneficiaires'] = beneficiaires

            # Construction du bloc "piecesJustificatives"
            pieces_justificatives = {
                'nomFichier': 'null',
                'formatFichier': 'null',
                'typeFichier': "null"
            }
            pieces_justificatives['nomFichier'] = data['nomFichier']
            pieces_justificatives['formatFichier'] = 'PDF'
            pieces_justificatives['typeFichier'] = 'BON_COMMANDE'
            # Ajout du bloc "piecesJustificatives"
            demande['piecesJustificatives'].append(pieces_justificatives)

            # Construction du bloc "scenarioInstallation"
            scenario_installation = {
                'isCentreDeSante': 'false',
                'operateurMessagerie': 'API_35',
                'isProSanteConnectNeeded': 'true',
                'isDirectToDMP': 'true',
                'isPFIToDMP': "false",
                'isDirectToMSSPro': 'true',
                'isPFIToMSSPro': 'false',
                'isDirectToMSSCitoyen': 'true',
                'isPFIToMSSCitoyen': 'false'
            }
            # Ajout du bloc "scenario_installation"
            demande['scenarioInstallation'] = scenario_installation

            # Ajout de la demande
            entete_fichier['lignesImport'].append(demande)

            # Contrôle de besoin d'écriture d'un fichier
            if (nombre_lignes == max_entries):
                jsonFilePath = './' + json_base_name + str(indice_fichier) + '.json'

                write_json_file(jsonFilePath, entete_fichier)

                # Et on repart pour un tour
                entete_fichier = {
                    'impId': 'null',
                    'numeroAns': '0123456789',
                    'SIRET': "38042372300028",
                    'lignesImport': []
                }

                nombre_lignes = 0
                indice_fichier = indice_fichier + 1

    # Fin du traitement, écrire éventuellement le reste qui n'a pas été écrit
    if (nombre_lignes < max_entries):
        jsonFilePath = './' + json_base_name + str(indice_fichier) + '.json'
        write_json_file(jsonFilePath, entete_fichier)


def main():

    print("Travail dans " + fileOrigin)
    print("- Lecture du fichier CSV")

    with open(csvFilePath, encoding='iso-8859-1') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=';')
        
        # Traitement du dictionnnaire d'entrée
        process_csv_dict(200, 'json', csvReader)
        
if __name__ == "__main__":
    main()