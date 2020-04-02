import csv
import matplotlib.pyplot as plt
import numpy as np

with open("AAPL.csv", mode='r') as csvFile:
    csvReader = csv.DictReader(csvFile)
    lineCount = 0
    for row in csvReader:
        if lineCount == 0:
            print(f'Column names: {", ".join(row)}')
            lineCount += 1
        #print(f'{row["Close"]} , {type(row["Close"])}')
        lineCount += 1
    #print(f'Processed {lineCount} lines.')
