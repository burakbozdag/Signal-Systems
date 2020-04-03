import csv
from datetime import datetime
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *


date = [] # Dates
close = [] # Useful data
with open("AAPL.csv", mode='r') as csvFile: # Reading csv file
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        date.append(datetime.strptime(row["Date"], "%Y-%m-%d"))
        close.append(float(row["Close"]))


def rms(close_values): # Root Mean Square Function
    sq = 0
    avg = 0
    for i in range(0, len(close_values)):
        sq += (close_values[i]**2)
    avg = (sq / (float(len(close_values))))
    return sqrt(avg)


def plot():
    startDate = datetime.strptime(e1.get(), "%Y-%m-%d")
    endDate = datetime.strptime(e2.get(), "%Y-%m-%d")
    startIndex = date.index(startDate)
    endIndex = date.index(endDate)

    date1 = []
    close1 = []
    label = "Variation"

    if startIndex > endIndex: # Start-end determination
        temp = startIndex
        startIndex = endIndex
        endIndex = temp

    for i in range(startIndex, endIndex): # Date interval
        date1.append(date[i])
        close1.append(close[i])

    if check.get(): # Moving average
        label = "Moving Average"
        close1[1] = (close1[0] + close1[1]) / 2
        for i in range(2, len(close1)):
            close1[i] = (close1[i] + close1[i - 1] + close1[i - 2]) / 3

    average = np.mean(close1)
    standardDeviation = np.std(close1)
    rootMeanSquare = rms(close1)

    label += "\nAverage: {}\nStandard Deviation: {}\nRoot Mean Square: {}"\
        .format(average, standardDeviation, rootMeanSquare)
    plt.plot(date1, close1, label=label)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('AAPL Stock Price')
    plt.legend()
    plt.show()


startIndex = 0
endIndex = len(close) - 1
startDate = date[startIndex].strftime("%Y-%m-%d")
endDate = date[endIndex].strftime("%Y-%m-%d")

root = Tk()
root.title("HW1")

frame = Frame(root)
Label(frame, text='Date Interval: ').grid()
e1 = Entry(frame, textvariable=startDate)
e1.insert(0, startDate)
e1.grid()
e2 = Entry(frame, textvariable=endDate)
e2.insert(0, endDate)
e2.grid()
Button(frame, text='Draw Variation', command=plot).grid()
check = IntVar()
Checkbutton(frame, text='Apply Moving Average FIR Filter', variable=check).grid()
frame.pack()

root.resizable(width=False, height=False)
root.mainloop()
