'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 7/30/2024
LAST CHANGES: Legend size and location edits
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

def clear_data(ax):
    for artist in ax.lines + ax.collections:
        artist.remove()

def remove_lines(lines):
    for line in lines:
        line.remove()

def find_sensors(dataFoo):
    start = ''
    sensNameFoo = []
    count = 0

    while start != dataFoo['source'][count]:
        if count == 0:
            start = dataFoo['source'][0]
        if dataFoo['source'][count] not in sensName:
            sensNameFoo.append(dataFoo['source'][count])
        count += 1

    return sensNameFoo

def find_colors(dataFoo):
    start = ''
    colorListFoo = []
    count = 0

    while start != dataFoo['color'][count]:
        if count == 0:
            start = dataFoo['color'][0]
        if dataFoo['color'][count] not in colorList:
            colorListFoo.append(dataFoo['color'][count])
        count += 1

    return colorListFoo

DATE_TODAY = datetime.date.today()
TICKS = 15

multiDay = False
valid = False
stop = False
done = False
plotName = ''
filePath = "/home/shib/Desktop/piData/"
data_type_bin = [('source', 'S6'), ('datetime', 'S26'), ('temperature', 'f8'), ('color', 'S8')]
dataSourceList = []
fileList=[]
sensName=[]
colorList=[]
fileCount = 0

#Collect data from all files
while not done:
    valid = False
    while not valid:
        try:
            #Start file
            fileRepeat = False 
            file = input(f"Enter binary file name {fileCount + 1} (Omit \".bin\".) or 'DONE': ")

            #Check for repeated file name
            if file in fileList:
                fileRepeat = True
                print("File name is same as previously entered, no repeats allowed!")
            #Exit all while loops
            elif file == 'DONE' and fileCount != 0:
                fileRepeat = True
                valid = True
                done = True

            while not fileRepeat:
                data_read = read_bin(f"{filePath}{file}.bin", data_type_bin)
                fileList.append(file)

                #Collect first file data
                if fileCount == 0:
                    #Convert data_read to proper format
                    data_read['source'] = data_read['source'].astype(str)
                    data_read['color'] = data_read['color'].astype(str)
                    data_read['datetime'] = data_read['datetime'].astype(str)
                    data_read['datetime'] = pd.to_datetime(data_read['datetime'], format='ISO8601')

                    #Get sensor names and colors
                    sensName = find_sensors(data_read)
                    colorList = find_colors(data_read)

                    #Collect everything
                    data = data_read

                #Collect subsequent file data
                else:
                    #Convert data_read to proper format
                    data_read['source'] = data_read['source'].astype(str)
                    data_read['color'] = data_read['color'].astype(str)
                    data_read['datetime'] = data_read['datetime'].astype(str)
                    data_read['datetime'] = pd.to_datetime(data_read['datetime'], format="ISO8601")
                    
                    #Get sensor names and colors
                    sensName += find_sensors(data_read)
                    colorList += find_colors(data_read)

                    #Collect everything
                    data = pd.concat([data, data_read], ignore_index=True)
                
                #Reset for new file
                fileCount += 1
                fileRepeat = True
                valid = True
        except Exception as e:
            print(e)
            print("ERROR: Binary file not open, check file name and put in piData folder. Omit \".bin\".")

#Define needed variables from gathered data
data = data.sort_values(by=['datetime'])
dateTimeMin = data['datetime'][0]
dateTimeMax = data['datetime'][len(data['datetime']) - 1]
date = dateTimeMin.strftime("%Y-%m-%d")
title = f'Temperature Over Time ({date})'
numSen = len(sensName)
linesList = [None]*numSen

#Check to make sure data is one for one
if numSen != len(colorList):
    print("Error! Sensor number and color number not equal!")
    exit()

##Auto-Scaler##
autoScale = False
yn = input("Would you like to use all of the data? y/n: ")
if yn == "y":
    autoScale = True

##Start time##
valid = False
while not valid and not autoScale:
    try:
        #Check if all the data is contained within a single day
        if dateTimeMin.strftime("%Y-%m-%d") == dateTimeMax.strftime("%Y-%m-%d"):
            #Get start time
            xmin = input("Set x-axis start time in \'HH:MM:SS.0\': ")
            xmin = pd.to_datetime(date + ' ' + xmin, format="%Y-%m-%d %H:%M:%S.%f")
        else:
            #Get stop time
            xmin = input("Set x-axis start time in \'YYYY-mm-dd HH:MM:SS.0\': ")
            xmin = pd.to_datetime(xmin, format="%Y-%m-%d %H:%M:%S.%f")
            multiDay = True

        valid = True
    except Exception as e:
        print(e)
        print("Wrong format!")

##Stop time##
valid = False
while not valid and not autoScale:
    try:
        #If data is contained within a single day do not need 'YYYY-mm-dd'
        if not multiDay:
            #Get stop time
            xmax = input("Set x-axis end time in \'HH:MM:SS.0\': ")
            xmax = pd.to_datetime(date + ' ' + xmax, format="%Y-%m-%d %H:%M:%S.%f")
        else:
            #Get stop time
            xmax = input("Set x-axis end time in \'YYYY-mm-dd HH:MM:SS.0\': ")
            xmax = pd.to_datetime(xmax, format="%Y-%m-%d %H:%M:%S.%f")
            multiDay = True

        valid = True
    except Exception as e:
        print(e)
        print("Wrong format!")

##Data##
#Condense data to input interval
if autoScale:
    #Probably overkill but format important
    try:
        xmin = dateTimeMin
        xmax = dateTimeMax
    except Exception as e:
        print(e)
filtered_data = data[(data['datetime'] >= xmin) & (data['datetime'] <= xmax)]

#Collect data to list
for i in range(numSen):
    dataSourceList.append(filtered_data[filtered_data['source'] == sensName[i]])

#Calculate interval of x-axis for TICKS steps
timeDiff = (xmax - xmin).total_seconds() #Hours to total seconds
interval = int(round(timeDiff / TICKS)) #Evenly space out total seconds for x-axis
if interval < 1:
    interval = 1 #Ensure interval is never zero

##Plotting##
#Set plot parameters
plt.figure(figsize=(16,8))
plt.xlim(xmin, xmax)
ax = plt.gca()

#Set line object and append to line list
for i in range(numSen):
    line, = ax.plot(dataSourceList[i]['datetime'], dataSourceList[i]['temperature'],
                    linestyle='solid', linewidth=1,
                    label=f'{sensName[i]}', color=f'{colorList[i]}')
    linesList[i] = line

#Set x-axis
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

#Set plot titles and labels
plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)
plt.xlabel('Time') #x-axis time
plt.ylabel('Temperature (Celsius)') #y-axis in celcius
plt.title(title)
leg = plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(8.0)
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
            print(f"Valid inputs: {sensName[:numSen]} or \'DONE\'")
            clear_data(ax)
            usedNames = []

            #Start manipulate loop
            for i in range(numSen):
                valid = False

                while not valid:
                    #Take name and check for repeat
                    name = input(f"Line {i+1}: ")
                    repeat = name in usedNames

                    if not repeat:
                        #Search for name
                        for j in range(numSen):
                            #If found use index
                            if name == sensName[j]:
                                #Set line object
                                linesList[j], = ax.plot(dataSourceList[j]['datetime'], dataSourceList[j]['temperature'],
                                                        linestyle='solid', linewidth=1,
                                                        label=f'{sensName[j]}', color=f'{colorList[j]}')
                                #Append found name to mark as used
                                usedNames.append(name)
                                valid = True
                            #Condition for done and want stop
                            elif name == 'DONE':
                                valid = True
                        #Condition for not found
                        if not valid:
                            print("Line not found.")
                    else:
                        print("Duplicate Line.")
                #Stop if done
                if name == 'DONE':
                    break
            #End manipulate loop
            plt.show(block=False)

        ##Bring to front##
        else:
            print("Input line to bring to front")
            print(f"Valid inputs: {sensName[:numSen]} or \'q\' to quit.")
            quitt = False
            
            #Start bring to front loop
            while not quitt:
                valid = False
                name = input("Line: ")
                
                #Search for name
                for i in range(numSen):
                    #If found use index
                    if name == sensName[i]:
                        #Erase and reset line object
                        remove_lines([linesList[i]])
                        linesList[i], = ax.plot(dataSourceList[i]['datetime'], dataSourceList[i]['temperature'],
                                                linestyle='solid', linewidth=1,
                                                label=f'{sensName[i]}', color=f'{colorList[i]}')
                        plt.show(block=False)
                        valid = True
                    #Condition for quit
                    elif name == 'q':
                        quitt = True
                        valid = True
                #Condition for not found
                if not valid:
                    print("Line not found.")
