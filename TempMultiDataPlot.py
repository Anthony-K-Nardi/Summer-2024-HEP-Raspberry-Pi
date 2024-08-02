'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 7/30/2024
LAST CHANGES: Legend size and location edits
'''

import datetime
from re import T
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from numpy import fromfile
from pandas import DataFrame
import pandas as pd
import time

def read_bin(filename, dt):
    return DataFrame(np.fromfile(filename, dtype=dt))

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
data=[]
xticksList=[]
intervalsList=[]
fileCount = 0
fileCountBin = 0
fileCountDat = 0

#Dittmann Stuff
rawVars = ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','T0','T1','T2','T3','T4','T5','T6','T7']
rawVars += ['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15']
var_names = ['time'] + rawVars
pi09 = [(name, '<f8') for name in var_names]
pi09colorList = ['#6e750e', '#c20078', "#653700", '#88b378', '#7ef4cc', '#d46a7e', '#ac9362', '#d99b82']
#pi09colorListxkcd = ['#xkcd:olive', "xkcd:magenta", "xkcd:brown", "xkcd:sage green", "xkcd:light turquoise", "xkcd:pinkish", "xkcd:dark biege", "xkcd:pinkish tan"]
dataType=pi09
#dataType = data_type_bin
#Collect data from all files
while not done:
    valid = False
    while not valid:
        try:
            #Start file
            fileRepeat = False 
            file = input(f"Enter file name {fileCount + 1} or 'DONE': ")

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
                try:
                    if file[-1] == "n":
                        dataType = data_type_bin
                    elif file[-1] == "t":
                        dataType = pi09
                    #print(dataType)

                    print("before data_read")
                    data_read = read_bin(f"{filePath}{file}", dataType)
                    print("Done reading")

                except Exception as e:
                    print(e)
                if file != 'DONE':
                    fileList.append(file)

                if file[-1] == "n":

                    #Collect first file data
                    if fileCountBin == 0:
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
                    
                    fileCountBin += 1

                elif file[-1] == "t":
                    if fileCountDat == 0:
                        data09 = data_read
                    else:
                        data09 = pd.concat([data09, data_read], ignore_index=True)
                    fileCountDat += 1

                #Reset for new file
                fileCount += 1
                fileRepeat = True
                valid = True
        except Exception as e:
            print(e)
            print("ERROR: File not open, check file name and put in piData folder.")
#Define needed variables from gathered data
senNot09=len(sensName)

if fileCountDat != 0:
    data09 = data09.sort_values(by=['time'])
    dates = (data09['time']-3600*5).astype('datetime64[s]') + np.mod(1000*data09['time'],1000).astype('timedelta64[ms]')
    n_points = len(dates)
    xmin09 = dates[0]
    xmax09 = dates[n_points-1]
    for m in range(8):
        sensName.append(f'pi09-{m}')
    colorList += pi09colorList
    if fileCountBin == 0:
        dateTimeMin = xmin09
        dateTimeMax = xmax09

if fileCountBin != 0:
    data = data.sort_values(by=['datetime'])
    dateTimeMin = data['datetime'][0]
    dateTimeMax = data['datetime'][len(data['datetime']) - 1]
    if fileCountDat != 0:
        if dateTimeMin > xmin09:
            dateTimeMin = xmin09
        if dateTimeMax < xmax09:
            dateTimeMax = xmax09


date = dateTimeMin.strftime("%Y-%m-%d")
dateMin = dateTimeMin.strftime("%Y-%m-%d")
dateMax = dateTimeMax.strftime("%Y-%m-%d")
title = f'Temperature Over Time ({date})'
numSen = len(sensName)
linesList = [None]*(numSen)

def retint(intdate, min, max):
    '''
    min = pd.to_datetime(intdate + ' ' + min, format="%Y-%m-%d %H:%M:%S.%f")
    max = pd.to_datetime(intdate + ' ' + max, format="%Y-%m-%d %H:%M:%S.%f")
    '''
    if dateMin == dateMax:
        min = pd.to_datetime(intdate + ' ' + min, format="%Y-%m-%d %H:%M:%S.%f")
        max = pd.to_datetime(intdate + ' ' + max, format="%Y-%m-%d %H:%M:%S.%f")
    else:
        min = pd.to_datetime(min, format="%Y-%m-%d %H:%M:%S.%f")
        max = pd.to_datetime(max, format="%Y-%m-%d %H:%M:%S.%f")
    
    interval = (min, max)
    return interval
#intervalList = [retint('2024-07-27', '13:10:00.0', '13:20:00.0'), retint('2024-07-27', '17:20:00.0', '17:30:00.0'), 
             #retint('2024-07-27', '21:15:00.0', '21:25:00.0'), retint('2024-07-27', '22:20:00.0', '22:30:00.0'), retint('2024-07-31', '13:30:00.0', '13:50:00.0')]

#Check to make sure data is one for one
if numSen != len(colorList):
    print("Error! Sensor number and color number not equal!")
    exit()
done = False

ynInterval = input("Do you want to plot all of you data? y/n: ")
if ynInterval == "y":
    intervalsList.append((dateTimeMin,dateTimeMax))
else:
    while not done:
        try:
            if dateMin == dateMax:
                interval = input("Input time interval in (\'HH:MM:SS.0\', \'HH:MM:SS.0\') or \'DONE\' \n input: ")
                if interval == 'DONE':
                    if len(intervalsList) != 0:
                        done = True
                elif len(interval) != 24:
                    print("Wrong interval format, try again")
                    print("example of correctly formatted input: (16:16:16.0, 17:29:48.0)")
                else:
                    intMin = interval[1:11]
                    intMax = interval[-11:-1]
                    intervalsList.append(retint(dateMin, intMin, intMax))
            else:
                interval = input("Input time interval in (\'YYYY-mm-dd HH:MM:SS.0\', \'YYYY-mm-dd HH:MM:SS.0\') or \'DONE\' \n input: ")
                if interval == 'DONE':
                    if len(intervalsList) != 0:
                        done = True
                elif len(interval) != 46:
                    print("Wrong interval format, try again")
                    print("example of correctly formatted input: (2024-07-27 16:16:16.0, 2024-07-27 17:29:48.0)")
                else:
                    intMin = interval[1:22]
                    intMax = interval[-22:-1]
                    intervalsList.append(retint(dateMin, intMin, intMax))


        except Exception as e:
            print(e)
            print("Wrong format, try again")

##Auto-Scaler##
'''
autoScale = False
yn = input("Would you like to use all of the data? y/n: ")
if yn == "y":
    autoScale = True

valid = False
if not autoScale:
    done = False
    while not done:
        ##Start time##
        valid = False
        while not valid:
            try:
                #Check if all the data is contained within a single day
                if dateTimeMin.strftime("%Y-%m-%d") == dateTimeMax.strftime("%Y-%m-%d"):
                    #Get start time
                    xmin = input("Set x-axis start time in \'HH:MM:SS.0\': ")
                    xmin = pd.to_datetime(date + ' ' + xmin, format="%Y-%m-%d %H:%M:%S.%f")
                else:
                    #Get start time
                    xmin = input("Set x-axis start time in \'YYYY-mm-dd HH:MM:SS.0\': ")
                    xmin = pd.to_datetime(xmin, format="%Y-%m-%d %H:%M:%S.%f")
                    multiDay = True

                valid = True
            except Exception as e:
                print(e)
                print("Wrong format!")

        ##Stop time##
        valid = False
        while not valid:
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
        intervalsList.append((xmin, xmax))
        yn = input("Done inputting intervals? 'y/n': ")
        if yn == 'y':
            done = True

##Data##
#Condense data to input interval
if autoScale:
    #Probably overkill but format important
    try:
        xmin = dateTimeMin
        xmax = dateTimeMax
        
        if xmin > xmin09:
            xmin = xmin09
        if xmax < xmax09:
            xmax = xmax09
        
    except Exception as e:
        print(e)
'''

#filtered_data = data[(data['datetime'] >= xmin) & (data['datetime'] <= xmax)]

#Collect data to list
if fileCountBin != 0:
    for i in range(numSen):
        dataSourceList.append(data[data['source'] == sensName[i]])
#for i in range(numSen):
#    dataSourceList.append(filtered_data[filtered_data['source'] == sensName[i]])

#Calculate interval of x-axis for TICKS steps
for i in range(len(intervalsList)):
    timeDiff = (intervalsList[i][1] - intervalsList[i][0]).total_seconds() #Hours to total seconds
    if len(intervalsList) == 1:
        numticks = 15
    else:
        numticks = 5
    xtickInt = int(round(timeDiff / numticks)) #Evenly space out total seconds for x-axis
    if xtickInt < 1:
        xtickInt = 1 #Ensure interval is never zero
    xticksList.append(xtickInt)


##Plotting##
#Set plot parameters

f, axs = plt.subplots(1, len(intervalsList), figsize=(18,10), sharey='all')
if len(intervalsList) == 1:
    axs = [axs]
#plt.figure(figsize=(16,8))
#plt.xlim(xmin, xmax)
#ax = plt.gca()

#Set line object and append to line list
for i in range(numSen):
    for j in range(len(intervalsList)):
        if i >= senNot09:
            #line, = (ax.plot(dates, temp09[i-senNot09],
            #                linestyle='solid', linewidth=1,
            #                label=f'{sensName[i]}', color=f'{colorList[i]}'),
            axs[j].plot(dates, data09[f'T{i-senNot09}'],
                    linestyle='solid', linewidth=1,
                    label=f'{sensName[i]}', color=f'{colorList[i]}')
            #linesList[i] = line
        else:
            #line, = (ax.plot(dataSourceList[i]['datetime'], dataSourceList[i]['temperature'],
            #                linestyle='solid', linewidth=1,
            #                label=f'{sensName[i]}', color=f'{colorList[i]}')
            axs[j].plot(dataSourceList[i]['datetime'], dataSourceList[i]['temperature'],
                    linestyle='solid', linewidth=1,
                    label=f'{sensName[i]}', color=f'{colorList[i]}')
            #linesList[i] = line
#Set x-axis
#ax.xaxis.set_major_locator(mdates.SecondLocator(interval=60))
for j in range(len(intervalsList)):
    axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    axs[j].set_xlim(intervalsList[j])
    axs[j].tick_params('x', labelrotation=90)
    axs[j].grid(True)
    axs[j].xaxis.set_major_locator(mdates.SecondLocator(interval=xticksList[j]))
    axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    if j != len(intervalsList)-1:
        axs[j].spines['right'].set_linewidth(3)
        plt.setp(axs[j].get_xticklabels()[-1], visible=False)


#Set plot titles and labels
#plt.gcf().autofmt_xdate()
#plt.xticks(rotation=90)
axs[int(len(intervalsList)/2)].set_xlabel('Time', fontsize=14) #x-axis time
axs[0].set_ylabel('Temperature (Celsius)', fontsize=14) #y-axis in celcius
f.suptitle(title, fontsize=24)
try:
    leg = axs[-1].legend(bbox_to_anchor=(1.01, .5), loc="center left", borderaxespad=0)
    for line in leg.get_lines():
        line.set_linewidth(8.0)
except:
    print("No legend for you!")
plt.subplots_adjust(wspace=0)
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
            print(f"Valid inputs: {sensName[:(numSen)]} or \'DONE\'")
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
                                if j >= senNot09:
                                    linesList[j], = ax.plot(dates, data09[f'T{i-senNot09}'],
                                                    linestyle='solid', linewidth=1,
                                                    label=f'{sensName[j]}', color=f'{colorList[j]}')

                                else:
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
            print(f"Valid inputs: {sensName[:(numSen)]} or \'q\' to quit.")
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
                        if i >= senNot09:
                            linesList[i], = ax.plot(dates, data09[f'T{i-senNot09}'],
                                            linestyle='solid', linewidth=1,
                                            label=f'{sensName[i]}', color=f'{colorList[i]}')
                            plt.show(block=False)

                        else:
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
