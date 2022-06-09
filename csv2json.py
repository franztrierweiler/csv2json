#!/bin/python3

import csv
import json

fileOrigin = './input_files'
csvFilePath = fileOrigin + '/jazz.csv'
jsonFilePath = fileOrigin + '/jazz.json'

data = {}

print("Travail dans " + fileOrigin)

with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        id = row['id']
        data[id] = row

print(data)

with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))
