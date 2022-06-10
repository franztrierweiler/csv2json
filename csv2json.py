#!/bin/python3

import csv
import json
import os

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

print("Travail dans " + fileOrigin)

print("- Lecture du fichier CSV")
with open(csvFilePath, encoding='iso-8859-1') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=';')
    for data in csvReader:

        print(data)

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

        # Construction du bloc "structure"
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
        pieces_justificatives['formatFichier'] = 'pdf'
        pieces_justificatives['typeFichier'] = 'BON_COMMANDE'
        # Ajout du bloc "piecesJustificatives"
        demande['piecesJustificatives'].append(pieces_justificatives)

        # Construction du bloc "scenarioInstallation"
        scenario_installation = {
            'isCentreDeSante': 'false',
            'operateurMessagerie': 'APICEM Apicrypt v2',
            'isProSanteConnectNeeded': 'true',
            'isDirectToDMP': 'true',
            'isPFIToDMP': "false",
            'isDirectToMSSPro': 'true',
            'isPFIToMSSPro': 'false',
            'isDirectToMSSCitoyen': 'true',
            'isPFIToMSSCitoyen': 'false'
        }
        # Ajout du bloc "scenario_installation"
        demande['piecesJustificatives'] = pieces_justificatives

        # Ajout de la demande
        entete_fichier['lignesImport'].append(demande)


with open(jsonFilePath, "w", encoding="utf-8") as jsonFile:
    jsonFile.write(json.dumps(entete_fichier, indent=4))


# Enlever les quotes et autres curiosités de Python
os.system("sed -i 's/\"false\"/false/g' " + jsonFilePath)
os.system("sed -i 's/\"true\"/true/g' " + jsonFilePath)
os.system("sed -i 's/\"null\"/null/g' " + jsonFilePath)