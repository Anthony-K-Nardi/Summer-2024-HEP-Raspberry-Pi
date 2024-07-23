'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 7/23/2024
LAST CHANGES: Auto-Scaler
'''

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from numpy import fromfile
from pandas import DataFrame
import pandas as pd
from pynput import keyboard

def read_bin(filename, dtype):
    return DataFrame(fromfile(filename, dtype))

def clear_data(ax):
    for artist in ax.lines + ax.collections:
        artist.remove()

def remove_lines(lines):
    for line in lines:
        line.remove()

DATE_TODAY = datetime.date.today()
TICKS = 15

valid = False
stop = False
plotName = ''
filePath = "/home/shib/Desktop/piData/"
data_type_txt = [('source', 'S6'), ('date', 'S10'), ('time', 'S16'), ('temperature', 'f8')]
data_type_bin = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
dataSourceList = []
colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']
colorList = ['Black', 'Gray', 'Purple', 'Green', 'Yellow', 'Orange', 'Red']
sensColor = ['Black/White', 'Gray/White', 'Purple/Gray', 
             'Green/Yellow', 'Yellow/Orange', 'Orange/Red', 'Red/Brown']

##Text file##
while not valid:
    try:
        yn = input(f"Do you want to load {DATE_TODAY} data? y/n: ")

        #Load today's text file:
        if yn == 'y':
            text = np.loadtxt(f"{filePath}{DATE_TODAY}.txt", str)
            title = f'Temperature Over Time ({DATE_TODAY})'
        
        #Load other text file:
        if yn == 'n':
            file = input("Enter text file name (Omit \".txt\".): ")
            text = np.loadtxt(f"{filePath}{file}.txt", str)
            date = text[1, 0]
            title = f'Temperature Over Time ({date})'
        
        #Pull number of sensors from file header:
        header = text[0,:]
        numSen = len(header) - 2
        linesList = [None]*numSen
        valid = True
    except:
        print("ERROR: Text file not open, check file name and put in piData folder. Omit \".txt\".")

##Binary file##
valid = False
while not valid:
    try:
        #Load today's binary file:
        if yn == 'y':
            data_read = read_bin(f"{filePath}{DATE_TODAY}.bin", data_type_bin)
        
        #Load other binary file:
        if yn == 'n':
            file = input("Enter binary file name (Omit \".bin\".): ")
            data_read = read_bin(f"{filePath}{file}.bin", data_type_bin)

        valid = True
    except:
        print("ERROR: Binary file not open, check file name and put in piData folder. Omit \".bin\".")

##Auto-Scaler##
autoScale = False
yn = input("Would you like to use all of the data? y/n: ")
if yn == "y":
    autoScale = True

##Start time##
valid = False
while not valid and not autoScale:
    try:
        #Get start time:
        xmin = input("Set x-axis start time in \'HH:MM:SS.0\': ")
        xmin = pd.to_datetime(xmin, format="%H:%M:%S.%f")

        valid = True
    except:
        print("Wrong format dummy read better!")

##Stop time##
valid = False
while not valid and not autoScale:
    try:
        #Get stop time:
        xmax = input("Set x-axis end time in \'HH:MM:SS.0\': ")
        xmax = pd.to_datetime(xmax, format="%H:%M:%S.%f")

        valid = True
    except:
        print("Wrong format dummy read better!")

##Data##
#Condense data to input interval:
data_read['time'] = data_read['time'].astype(str)
data_read['time'] = pd.to_datetime(data_read['time'], format="%H:%M:%S.%f")
if autoScale:
    xmin = data_read['time'][0]
    xmax = data_read['time'][len(data_read['time'])-1]
filtered_data = data_read[(data_read['time'] >= xmin) & (data_read['time'] <= xmax)]

#Collect data to list:
for i in range(numSen) :
    dataSourceList.append(filtered_data[filtered_data['source'] == colorListB[i]])

#Calculate interval of x-axis for TICKS steps:
timeDiff = (xmax - xmin).total_seconds()
interval = int(round(timeDiff / TICKS))

##Plotting##
#Set plot parameters:
plt.figure(figsize=(10,8))
plt.xlim(xmin, xmax)
#plt.ylim(0, 50) #If needed
ax = plt.gca()

#Set line object and append to line list:
for i in range(numSen):
    line, = ax.plot(dataSourceList[i]['time'], dataSourceList[i]['temperature'],
            linestyle='solid', linewidth=1,
            label=f'{sensColor[i]}', color=f'{colorList[i]}')
    linesList[i] = line

#Set x-axis:
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

#Set plot titles and labels:
plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)
plt.xlabel('Time') #x-axis time
plt.ylabel('Temperature (Celsius)') #y-axis in celcius
plt.title(title)
legend = plt.legend()
legend.set_zorder(numSen + 1)
plt.show(block=False)

##Warning##
print("\n***IF YOU WANT THE ORIGINAL PLOT SAVE NOW!***\n")

##Manipulation of plot##
while not stop:
    check = input("Press \'s\' to stop. Press \'m\' to manipulate all lines. Or continue to bring to front: ")
    
    if check == 's':
        stop = True
    else:
        ##Manipulate##
        if check == 'm':
            print("Input draw order (back to front)")
            print(f"Valid inputs: {colorList[:numSen]} or \'None\'")
            clear_data(ax)
            usedColors = []

            #Start manipulate loop:
            for i in range(numSen):
                valid = False

                while not valid:
                    #Take color and check for repeat:
                    color = input(f"Color {i+1}: ")
                    repeat = color in usedColors

                    if not repeat:
                        #Search for color:
                        for j in range(numSen):
                            #If found use index:
                            if color == colorList[j]:
                                #Set line object:
                                linesList[j], = ax.plot(dataSourceList[j]['time'], dataSourceList[j]['temperature'],
                                                            linestyle='solid', linewidth=1,
                                                            label=f'{sensColor[j]}', color=f'{colorList[j]}')
                                #Append found color to mark as used:
                                usedColors.append(color)
                                valid = True
                            #Condition for no color:
                            elif color == 'None':
                                valid = True
                        #Condition for not found:
                        if not valid:
                            print("Color not found.")
                    else:
                        print("Duplicate color.")
            #End manipulate loop:
            plt.show(block=False)

        ##Bring to front##
        else:
            print("Input color to bring to front")
            print(f"Valid inputs: {colorList[:numSen]} or \'q\' to quit.")
            quitt = False
            
            #Start bring to front loop:
            while not quitt:
                valid = False
                color = input("Color: ")
                
                #Search for color:
                for i in range(numSen):
                    #If found use index:
                    if color == colorList[i]:
                        #Erase and reset line object:
                        remove_lines([linesList[i]])
                        linesList[i], = ax.plot(dataSourceList[i]['time'], dataSourceList[i]['temperature'],
                                                    linestyle='solid', linewidth=1,
                                                    label=f'{sensColor[i]}', color=f'{colorList[i]}')
                        plt.show(block=False)
                        valid = True
                    #Condition for quit:
                    elif color == 'q':
                        quitt = True
                        valid = True
                #Condition for not found:
                if not valid:
                    print("Color not found.")
