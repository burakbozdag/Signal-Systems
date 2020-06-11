# Burak Bozdag
# 150170110

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from tkinter import *


date = [] # Dates
close = [] # Useful data
with open("AAPL.csv", mode='r') as csvFile: # Reading csv file
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        date.append(datetime.strptime(row["Date"], "%Y-%m-%d"))
        close.append(float(row["Close"]))

def standard():
    startDate = datetime.strptime(e1.get(), "%Y-%m-%d")
    endDate = datetime.strptime(e2.get(), "%Y-%m-%d")
    startIndex = date.index(startDate)
    endIndex = date.index(endDate)

    date1 = []
    close1 = []
    label = "Standardized Data"

    if startIndex > endIndex: # Start-end determination
        temp = startIndex
        startIndex = endIndex
        endIndex = temp

    for i in range(startIndex, endIndex): # Date interval
        date1.append(date[i])
        close1.append(close[i])

    standardDeviation = np.std(close1)

    for i in range(0, len(close1), 5):
        sum = 0
        index = i
        for j in range(index, index + 5):
            sum += close1[j]
        average = sum / 5
        index = i
        for j in range(index, index + 5):
            close1[j] = (close1[j] - average) / standardDeviation

    plt.plot(date1, close1, label=label)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('AAPL Stock Price')
    plt.legend()
    plt.show()

def normal():
    startDate = datetime.strptime(e1.get(), "%Y-%m-%d")
    endDate = datetime.strptime(e2.get(), "%Y-%m-%d")
    startIndex = date.index(startDate)
    endIndex = date.index(endDate)

    date1 = []
    close1 = []
    label = "Normalized Data"

    if startIndex > endIndex: # Start-end determination
        temp = startIndex
        startIndex = endIndex
        endIndex = temp

    min = float(1600)
    for i in range(startIndex, endIndex): # Date interval
        date1.append(date[i])
        close1.append(close[i])
        if min > close[i]:
            min = close[i]

    for i in range(0, len(close1), 5):
        max = 0
        index = i
        for j in range(index, index + 5):
            if max < close1[j]:
                max = close1[j]
        index = i
        for j in range(index, index + 5):
            close1[j] = (close1[j] - min) / (max - min)

    plt.plot(date1, close1, label=label)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('AAPL Stock Price')
    plt.legend()
    plt.show()

def convolution():
    startDate = datetime.strptime(e1.get(), "%Y-%m-%d")
    endDate = datetime.strptime(e2.get(), "%Y-%m-%d")
    startIndex = date.index(startDate)
    endIndex = date.index(endDate)

    date1 = []
    close1 = []
    label = "Maximum Convolution"

    if startIndex > endIndex:  # Start-end determination
        temp = startIndex
        startIndex = endIndex
        endIndex = temp

    min = float(1600)
    for i in range(startIndex, endIndex):  # Date interval
        date1.append(date[i])
        close1.append(close[i])
        if min > close[i]:
            min = close[i]

    for i in range(0, len(close1), 5):
        max = 0
        index = i
        for j in range(index, index + 5):
            if max < close1[j]:
                max = close1[j]
        index = i
        for j in range(index, index + 5):
            close1[j] = (close1[j] - min) / (max - min)

    h = []
    if hSel.get() == 1:
        h = [0.2, 0.4, 0.6, 0.8, 1]
        label += "\nh = [0.2, 0.4, 0.6, 0.8, 1]"
    elif hSel.get() == 2:
        h = [1, 0.5]
        label += "\nh = [1, 0.5]"
    elif hSel.get() == 3:
        h = [0.5, 0.5, 0.5, 0.5, 0.5]
        label += "\nh = [0.5, 0.5, 0.5, 0.5, 0.5]"
    elif hSel.get() == 4:
        h = [0.05, 0.1, 0.2, 0.4, 0.8]
        label += "\nh = [0.05, 0.1, 0.2, 0.4, 0.8]"
    else:
        print("Select an 'h' array.")
        return

    date2 = []
    close2 = []
    for i in range(0, len(close1), 5):
        date2.append(date1[i])
        x = []
        index = i
        for j in range(index, index + 5):
            x.append(close1[j])
        list = signal.convolve(x, h).tolist()
        max = float(0)
        for j in list:
            if max < j:
                max = j
        close2.append(max)

    plt.plot(date2, close2, label=label)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('AAPL Stock Price')
    plt.legend()
    plt.show()


startIndex = 1110 # First of the last 400 rows
endIndex = len(close) - 1
startDate = date[startIndex].strftime("%Y-%m-%d")
endDate = date[endIndex].strftime("%Y-%m-%d")

root = Tk()
root.geometry("200x260")
root.title("HW1")

frame = Frame(root)
Label(frame, text='Date Interval: ').grid()
e1 = Entry(frame, textvariable=startDate)
e1.insert(0, startDate)
e1.config(state=DISABLED)
e1.grid(padx=1, pady=1)
e2 = Entry(frame, textvariable=endDate)
e2.insert(0, endDate)
e2.config(state=DISABLED)
e2.grid(padx=1, pady=1)
Button(frame, text='Draw the Standardized Data', command=standard).grid(padx=1, pady=1)
Button(frame, text='Draw the Normalized Data', command=normal).grid(padx=1, pady=1)
frame.pack()
frame = Frame(root, width=200, height=1, bg="grey")
frame.pack()
frame = Frame(root)
hSel = IntVar()
Radiobutton(frame, text='h[n]=[0.2 0.4 0.6 0.8 1]', variable=hSel, value=1).grid(padx=1, pady=1)
Radiobutton(frame, text='h[n]=[1 0.5]', variable=hSel, value=2).grid(padx=1, pady=1)
Radiobutton(frame, text='h[n]=[0.5 0.5 0.5 0.5 0.5]', variable=hSel, value=3).grid(padx=1, pady=1)
Radiobutton(frame, text='h[n]=[0.05 0.1 0.2 0.4 0.8]', variable=hSel, value=4).grid(padx=1, pady=1)
Button(frame, text='Draw the Maximum Convolution', command=convolution).grid(padx=1, pady=1)
frame.pack()

root.resizable(width=False, height=False)
root.mainloop()
