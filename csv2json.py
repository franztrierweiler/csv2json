#!/bin/python3

import csv
import json

# Constantes
fileOrigin = './input_files'
csvFilePath = fileOrigin + '/segur.csv'
jsonFilePath ='./segur.json'

# Variables globales
nombre_lignes = 0

# Entête
entete_fichier = {
    'impId': 'null',
    'numeroAns': '0123456789',
    'SIRET': '0123456789ABCD',
    'lignesImport': []
}

# Debug
dict2 = {
    'idd1': {'id1': '124', 'id2': '658', 'id3': '878'},
    'idd2': {'id1': '748', 'id2': '748', 'id3': '114'},
    'idd3': {'id1': '987', 'id2': '332', 'id3': '662'}
}

print("Travail dans " + fileOrigin)

print("- Lecture du fichier CSV")
with open(csvFilePath, encoding='iso-8859-1') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=';')
    for data in csvReader:

        print("***")
        print(data)
        print("***")

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
            'piecesjustificatives': {},
            'scenarioInstallation': {},
            'codeTraitement': 'null',
            'libelleTraitement': 'null'
        }
        demande['numLigne'] = nombre_lignes

        # Construction du bloc "commande"
        commande = {
            'dateCommande': 'null',
            'regimeTVA': 'null',
            'montantSegurHT': 'null',
        }
        commande['dateCommande'] = ''
        commande['regimeTVA'] = ''
        commande['montantSegurHT'] = ''
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
            'structure': []
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

        # Ajout du bloc "beneficiaires"
        demande['beneficiaires'] = beneficiaires

        # Ajout de la demande
        entete_fichier['lignesImport'].append(demande)


with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(entete_fichier, indent=4))
