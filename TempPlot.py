'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 7/10/2024
LAST CHANGES: Live Plot Toggle
'''

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from numpy import fromfile
from pandas import DataFrame
import pandas as pd

def read_bin(filename, dtype):
    return DataFrame(fromfile(filename, dtype))

DATE_TODAY = datetime.date.today()
TICKS = 15
wantPng = False
valid = False
plotName = ''

filePath = "/home/shib/Desktop/"
data_type_txt = [('source', 'S6'), ('date', 'S10'), ('time', 'S16'), ('temperature', 'f8')]
data_type_bin = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
dataSourceList = []
colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']
colorList = ['Black', 'Gray', 'Purple', 'Green', 'Yellow', 'Orange', 'Red']
sensColor = ['Black/White', 'White/Gray', 'Purple/Gray', 
             'Green/Yellow', 'Yellow/Orange', 'Orange/Red', 'Red/Brown']

while not valid:
    try:
        yn = input(f"Do you want to load {DATE_TODAY} data? y/n: ")
        
        if yn == 'y':
            text = np.loadtxt(f"{filePath}{DATE_TODAY}.txt", str)
            title = f'Temperature Over Time ({DATE_TODAY})'
        if yn == 'n':
            file = input("Enter text file name (Omit \".txt\".): ")
            text = np.loadtxt(f"{filePath}{file}.txt", str)
            date = text[1, 0]
            title = f'Temperature Over Time ({date})'
        header = text[0,:]
        numSen = len(header) - 2
        valid = True
    except:
        print("ERROR: Text file not open, check file name and put on desktop. Omit \".txt\".")


valid = False

while not valid:
    try:
        if yn == 'y':
            data_read = read_bin(f"{filePath}{DATE_TODAY}.bin", data_type_bin)
        if yn == 'n':
            file = input("Enter binary file name (Omit \".bin\".): ")
            data_read = read_bin(f"{filePath}{file}.bin", data_type_bin)
        valid = True
    except:
        print("ERROR: Binary file not open, check file name and put on desktop. Omit \".bin\".")

valid = False

while not valid:
    try:
        xmin = input("Set x-axis start time in \'HH:MM:SS\': ")
        xmin = pd.to_datetime(xmin, format="%H:%M:%S.%f")
        valid = True
    except:
        print("Wrong format dummy read better!")

valid = False

while not valid:
    try:
        xmax = input("Set x-axis end time in \'HH:MM:SS\': ")
        xmax = pd.to_datetime(xmax, format="%H:%M:%S.%f")
        valid = True
    except:
        print("Wrong format dummy read better!")

valid = False

yn = input("Do you want to save plot? y/n: ")
if yn == 'y':
    wantPng = True
    plotName = input("Desired name of plot file (Omit \".png\"): ")

#Condense data to input interval:
data_read['time'] = data_read['time'].astype(str)
data_read['time'] = pd.to_datetime(data_read['time'], format="%H:%M:%S.%f")
filtered_data = data_read[(data_read['time'] >= xmin) & (data_read['time'] <= xmax)]

for i in range(numSen) :
    dataSourceList.append(filtered_data[filtered_data['source'] == colorListB[i]])
    #checkSize = len(dataSourceList[i]['temperature'])
    #print(checkSize)

timeDiff = (xmax - xmin).total_seconds()
interval = int(round(timeDiff / TICKS))

plt.figure(figsize=(10,8))
plt.xlim(xmin, xmax)
#plt.ylim(-10, 60)

ax = plt.gca()
for i in range(numSen):
    ax.plot(dataSourceList[i]['time'], dataSourceList[i]['temperature'], 
            '.', label=f'{sensColor[i]}', color=f'{colorList[i]}')
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)
plt.xlabel('Time') #x-axis time
plt.ylabel('Temperature (Celsius)') #y-axis in celcius
plt.title(title)
plt.legend()
if wantPng:
    plt.savefig(f'{plotName}.png')
plt.show()