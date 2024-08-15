'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 08/14/2024
LAST CHANGES: Added additional data type for trimmed data
'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pandas import DataFrame
import pandas as pd
import datetime
#make sure program doesn't break if OldTesting.py is not downloaded and in the same location as TempPlot.py
#Program can run without this import, it will be missing a feature
try:
    from OldTesting import clear_m
except:
    dummy = 0

def read_bin(filename, dt):
    try:
        df = DataFrame(np.fromfile(filename, dtype=dt))
        dummy = df['source'].astype(str)
    except:
        df = DataFrame(np.fromfile(filename, dtype=DATA_TYPE_BIN_OTHER))
    return df

def read_dat(filename, dt):
    return(DataFrame(np.fromfile(filename, dtype=dt)))

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

def retint(min, max):
    if dateMin == dateMax:
        min = pd.to_datetime(dateMin + ' ' + min, format="%Y-%m-%d %H:%M:%S.%f")
        max = pd.to_datetime(dateMin + ' ' + max, format="%Y-%m-%d %H:%M:%S.%f")
    else:
        min = pd.to_datetime(min, format="%Y-%m-%d %H:%M:%S.%f")
        max = pd.to_datetime(max, format="%Y-%m-%d %H:%M:%S.%f")
    
    interval = [min, max]
    
    return interval

FILE_PATH = "/home/shib/Desktop/piData/"
DATA_TYPE_BIN = [('source', 'S6'), ('datetime', 'S26'), ('temperature', 'f8'), ('color', 'S8')]
DATA_TYPE_BIN_OTHER = [('source', 'S6'), ('datetime', '<M8[ns]'), ('temperature', '<f8'), ('color', 'S8')]

excel = False
valid = False
stop = False
done = False
data_type = None
colorList = []
dataSourceList = []
fileList = []
intervalsList = []
locList = []
sensName = []
xticksList = []
fileCount = 0
fileCountBin = 0
fileCountDat = 0
fileCountExcel = 0
dummy = 0

#Dittmann Stuff
rawVars = ['V0','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','T0','T1','T2','T3','T4','T5','T6','T7']
rawVars += ['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15']
var_names = ['time'] + rawVars
pi09 = [(name, '<f8') for name in var_names]
pi09colorList = ['#6e750e', '#c20078', "#653700", '#88b378', '#7ef4cc', '#d46a7e', '#ac9362', '#d99b82']
#pi09colorListxkcd = ["xkcd:olive", "xkcd:magenta", "xkcd:brown", "xkcd:sage green", 
#                     "xkcd:light turquoise", "xkcd:pinkish", "xkcd:dark biege", "xkcd:pinkish tan"]

#Dictionary for sensor names
sensName_to_loc = {'pi02-1': 'T-16-C', 'pi02-2': 'T-40-C', 'pi02-3': 'B-CCM-B', 'pi02-4': 'B-16-L',
                   'pi02-5': 'ROOM-02', 'pi02-6': 'T-11-C', 'pi02-7': 'B-14-L',
                   'pi03-1': 'B-24-L', 'pi03-2': 'T-24-C', 'pi03-3': 'B-23-H', 'pi03-4': 'B-CCM-A',
                   'pi03-5': 'ROOM-03', 'pi03-6': 'T-22-C', 'pi03-7': 'B-25-L',
                   'pi04-1': 'B-42-C', 'pi04-2': 'B-31-C', 'pi04-3': 'B-22-H', 'pi04-4': 'T-46-H',
                   'pi04-5': 'ROOM-04', 'pi04-6': 'B-CEN', 'pi04-7': 'T-21-C',
                   'pi09-0': 'ROOM-09', 'pi09-1': 'T-41-H', 'pi09-2': 'T-42-H', 'pi09-3': 'T-IN',
                   'pi09-4': 'T-MID', 'pi09-5': 'T-OUT', 'pi09-6': 'B-RM-3', 'pi09-7': 'T-RM-3'}

print("\n***TempPlot program by Hunter Buttrum, Jayden Blanchard, and Tony Nardi.***")
print("Designed to plot binary data collected from thermistors and edit afterwards if needed.")
print("See documentation for full capabilities, expected file formats, or other error handling.\n")
print("Accepted binary file types: '.bin' or '.dat'.")
print("Accepted interval file types: '.xlsx', '.xlsm', '.xltx', '.xltm', or '.csv'.")

##Collect data from all files##
while not done:
    valid = False
    while not valid:
        try:
            #Start file
            fileRepeat = False 
            file = input(f"Enter file name {len(fileList) + 1} or 'DONE': ")

            #Check for repeated file name
            if file in fileList:
                fileRepeat = True
                print("File name is the same as previously entered, no repeats.")
            
            #Exit all while loops
            elif file == 'DONE' and fileCount != 0:
                fileRepeat = True
                valid = True
                done = True

            while not fileRepeat:
                #Check if binary file
                if file[-4:] == ".bin":
                    data_type = DATA_TYPE_BIN
                    data_read = read_bin(f"{FILE_PATH}{file}", data_type)
                    
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
                    
                    fileList.append(file)
                    fileCountBin += 1

                #Check if pi09 file
                elif file[-4:] == ".dat":
                    data_type = pi09
                    data_read = read_dat(f"{FILE_PATH}{file}", data_type)
                    
                    #Collect first file data
                    if fileCountDat == 0:
                        data09 = data_read

                    #Collect subsequent file data
                    else:
                        data09 = pd.concat([data09, data_read], ignore_index=True)

                    fileList.append(file)
                    fileCountDat += 1
                
                #Check if Excel file
                elif file[-5:] == '.xlsx' or file[-5:] == '.xlsm' or file[-5:] == '.xltx' or file[-5:] == '.xltm':
                    
                    #Collect first file data
                    if fileCountExcel == 0:
                        excelData = pd.read_excel(f"{FILE_PATH}{file}", usecols=[0,1,2], names=['Start Time', 'End Time', 'SiPM Temp'])
                    
                    #Collect subsequent file data
                    else:
                        excelData = pd.concat([excelData, pd.read_excel(f"{FILE_PATH}{file}")], ignore_index=True)
                    
                    fileList.append(file)
                    fileCountExcel += 1
                    excel = True
                
                #Check if csv file
                elif file[-4:] == '.csv':

                    #Collect first file data
                    if fileCountExcel == 0:
                        excelData = pd.read_csv(f"{FILE_PATH}{file}", usecols=[0,1,2], names=['Start Time', 'End Time', 'SiPM Temp'], skiprows=1)
                    
                    #Collect subsequent file data
                    else:
                        excelData = pd.concat([excelData, pd.read_csv(f"{FILE_PATH}{file}")], ignore_index=True)
                    
                    fileList.append(file)
                    fileCountExcel += 1
                    excel = True

                #Catch non-valid
                else:
                    print("ERROR: Invalid file type.")
                
                #Reset for new file
                fileCount = fileCountDat + fileCountBin
                fileRepeat = True
                valid = True
        except Exception as e:
            print(e)
            print("ERROR: File read incomplete.")

#Define num sensors from binary files
senNot09 = len(sensName)

#Set needed vars from pi09 data
if fileCountDat != 0:
    colorList += pi09colorList
    data09['time'] = (data09['time']-3600*5).astype('datetime64[s]') + np.mod(1000*data09['time'],1000).astype('timedelta64[ms]')
    data09 = data09.sort_values(by=['time'])
    xmin09 = data09['time'][0]
    xmax09 = data09['time'][len(data09['time']) - 1]
    
    for m in range(8):
        sensName.append(f'pi09-{m}')
    
    #Set true min and max
    if fileCountBin == 0:
        dateTimeMin = xmin09
        dateTimeMax = xmax09

#Set needed vars from binary data
if fileCountBin != 0:
    data = data.sort_values(by=['datetime'])
    dateTimeMin = data['datetime'][0]
    dateTimeMax = data['datetime'][len(data['datetime']) - 1]
    
    #Set true min and max
    if fileCountDat != 0:
        if dateTimeMin > xmin09:
            dateTimeMin = xmin09
        if dateTimeMax < xmax09:
            dateTimeMax = xmax09

#Set additional vars using previously set vars
dateMin = dateTimeMin.strftime("%Y-%m-%d")
dateMax = dateTimeMax.strftime("%Y-%m-%d")
numSen = len(sensName)
for z in sensName:
    locList.append(sensName_to_loc[z])

#Check to make sure data is one for one
if numSen != len(colorList):
    print("ERROR: Sensor number and color number not equal!")
    quit()
'''
#Get rid of any temps = 0 from old data that stored errors as 0
zero_to_None ={0 : None}
data.replace({'temperature': zero_to_None}, inplace=True)
'''
#Check if excelData is empty
if fileCountExcel != 0 and excelData.empty:
    print("ERROR: No data from interval file, program will be stopped.")
    quit()

##Get intervals##
if excel == False:
    ynInterval = input("Do you want to plot all of your data? y/n: ")
    
    #Whole interval
    if ynInterval == "y":
        intervalsList.append((dateTimeMin,dateTimeMax))
    
    #Manual intervals
    else:
        if dateMin == dateMax:
            print("Input time interval in format \'[HH:MM:SS.0, HH:MM:SS.0]\' or \'DONE\':")
        else:
            print("Input time interval in format \'[YYYY-mm-dd HH:MM:SS.0, YYYY-mm-dd HH:MM:SS.0]\' or \'DONE\':")
        done = False

        while not done:
            interval = input(f"Interval {len(intervalsList)+1}: ")
            
            #Done if have interval
            if interval == 'DONE' and len(intervalsList) != 0:
                done = True
            
            #Check single day format
            elif dateMin == dateMax:
                try:
                    intMin = ''
                    intMax = ''
                    comma = False
                    
                    #Set intMin as string before the comma and intMax as string after comma
                    for i in range(len(interval)):
                        if interval[i] == ',':
                            comma = True
                            continue
                        if interval[i] != '[' and interval[i] != '(' and interval[i] != ']' and interval[i] != ')':
                            if not comma:
                                intMin += interval[i]
                            elif len(intMax) == 0 and interval[i] != ' ':
                                intMax += interval[i]
                            elif len(intMax) != 0:
                                intMax += interval[i]

                    #Add in decimal if not included in min
                    if not '.' in intMin:
                        intMin += '.0'
                    
                    #Add in decimal if not included in max
                    if not '.' in intMax:
                        intMax += '.0'
                    
                    #Check to see if interval has correct bounds and append
                    interval = retint(intMin, intMax)
                    if interval[1] > interval[0]:
                        intervalsList.append(interval)
                    else:
                        print("ERROR: Invalid interval bounds, try again.")
                except:
                    print("ERROR: Wrong interval format, try again.")
                    print("Example of correctly formatted input: [16:16:16.0, 17:29:48.0]")
            
            #Check multi-day format
            else:
                try:
                    intMin = ''
                    intMax = ''
                    comma = False
                    
                    #Set intMin as string before the comma and intMax as string after comma
                    for i in range(len(interval)):
                        if interval[i] == ',':
                            comma = True
                            continue
                        if interval[i] != '[' and interval[i] != '(' and interval[i] != ']' and interval[i] != ')':
                            if not comma:
                                intMin += interval[i]
                            elif len(intMax) == 0 and interval[i] != ' ':
                                intMax += interval[i]
                            elif len(intMax) != 0:
                                intMax += interval[i]

                    #Add in decimal if not included in min
                    if not '.' in intMin:
                        intMin += '.0'
                    
                    #Add in decimal if not included in max
                    if not '.' in intMax:
                        intMax += '.0'

                    #Check to see if interval has correct bounds and append
                    interval = retint(intMin, intMax)
                    if interval[1] > interval[0]:
                        intervalsList.append(interval)
                    else:
                        print("ERROR: Invalid interval bounds, try again.")
                except:
                    print("ERROR: Wrong interval format, try again.")
                    print("Example of correctly formatted input: [2024-07-27 16:16:16.0, 2024-07-27 17:29:48.0]")
#Excel interval
else:
    minMaxList = (excelData.iloc[:, 0], excelData.iloc[:, 1])
    for i in range(len(excelData.iloc[:, 0])):
        #Stop when empty
        if pd.isnull(minMaxList[0][i]):
            continue
        
        if isinstance(excelData.iloc[i, 0], datetime.datetime) and isinstance(excelData.iloc[i, 1], datetime.datetime):
            interval = [excelData.iloc[i, 0], excelData.iloc[i, 1]]
        elif isinstance(excelData.iloc[i, 0], str) and isinstance(excelData.iloc[i, 1], str):
            #Slashes to dashes in datetime
            if excelData.iloc[i, 0].find('/') != -1 or excelData.iloc[i, 1].find('/') != -1:
                excelData.iloc[i, 0] = excelData.iloc[i, 0].replace('/', '-')
                excelData.iloc[i, 1] = excelData.iloc[i, 1].replace('/', '-')
            
            #Add in decimal if not included in min
            if not "." in excelData.iloc[i, 0]:
                excelData.iloc[i, 0] += ".0"
            
            #Add in decimal if not included in max
            if not "." in excelData.iloc[i, 1]:
                excelData.iloc[i, 1] += ".0"    
            
            #Check to see if interval has correct bounds and append
            interval = retint(excelData.iloc[i, 0], excelData.iloc[i, 1])
        else:
            print("ERROR: Interval file is in the wrong format, program will be stopped.")
            quit()

        if interval[1] > interval[0]:
            intervalsList.append(interval)
        else:
            print("ERROR: Invalid interval bounds in Excel document, program will be stopped.")
            quit()

#Collect binary data to list
if fileCountBin != 0:
    for i in range(numSen):
        dataSourceList.append(data[data['source'] == sensName[i]])

##Plotting##
#Set title
intervalsListSorted = sorted(intervalsList)
if len(intervalsList) >= 2:
    sortyn = input("Do you want your intervals sorted by time? y/n: ")
    if sortyn == "y":
        intervalsList = sorted(intervalsList)
        if fileCountExcel != 0:
            excelData = excelData.sort_values(by=['Start Time'])
if intervalsListSorted[0][0].strftime("%Y-%m-%d") == intervalsListSorted[-1][1].strftime("%Y-%m-%d"):
    title = f'Temperature Over Time ({intervalsListSorted[0][0].strftime("%Y-%m-%d")})'
else:
    title = f'Temperature Over Time ({intervalsListSorted[0][0].strftime("%Y-%m-%d")} to {intervalsListSorted[-1][1].strftime("%Y-%m-%d")})'
#Set plot parameters
f, axs = plt.subplots(1, len(intervalsList), figsize=(18,10), sharey='all', gridspec_kw=dict(wspace=0))
if len(intervalsList) == 1:
    axs = [axs]
#Calculate interval of x-axis for TICKS steps
for i in range(len(intervalsList)):
    #Ticks for one plot
    if len(intervalsList) == 1:
        numticks = 15
    #Ticks for many plots
    elif len(intervalsList) > 8:
        numticks = 2
    #Ticks normal
    else:
        numticks = 5
    
    timeDiff = (intervalsList[i][1] - intervalsList[i][0]).total_seconds() #Hours to total seconds
    xtickInt = int(round(timeDiff / numticks)) #Evenly space out total seconds for x-axis
    
    #Ensure interval is never zero
    if xtickInt < 1:
        xtickInt = 1 
    
    xticksList.append(xtickInt)
#Set line object and append to line list
linesList = [None]*(numSen*len(intervalsList))
for j in range(len(intervalsList)):
    xmin = intervalsList[j][0]
    xmax = intervalsList[j][1]
    
    for i in range(numSen):
        #If is pi09 sensor
        if i >= senNot09:
            filtered_data = data09[(data09['time'] >= xmin) & (data09['time'] <= xmax)]
            line, = axs[j].plot(filtered_data['time'], filtered_data[f'T{i-senNot09}'],
                    linestyle='solid', linewidth=1,
                    label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
            linesList[i + numSen * j] = line
        
        #If other sensor
        else:
            filtered_data = dataSourceList[i][(dataSourceList[i]['datetime'] >= xmin) & (dataSourceList[i]['datetime'] <= xmax)]
            line, =axs[j].plot(filtered_data['datetime'], filtered_data['temperature'],
                    linestyle='solid', linewidth=1,
                    label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
            linesList[i + numSen * j] = line

#Formatting for each interval
axs[0].set_ylabel('Temperature (Celsius)', fontsize=14) #y-axis in celcius
for j in range(len(intervalsList)):
    axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    axs[j].set_xlim(intervalsList[j])
    axs[j].tick_params('x', labelrotation=90, pad=0.1, labelsize=9, )
    axs[j].grid(True)
    axs[j].set_ymargin(0.015)
    
    if intervalsListSorted[0][0].strftime("%Y-%m-%d") == intervalsListSorted[-1][1].strftime("%Y-%m-%d"):
        axs[j].xaxis.set_major_locator(mdates.SecondLocator(interval=xticksList[j]))
        axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    else:
        axs[j].xaxis.set_major_locator(mdates.SecondLocator(interval=xticksList[j]))
        axs[j].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.setp(axs[j].get_xticklabels()[:], ha='left')
    if j != len(intervalsList) - 1:
        axs[j].spines['right'].set_linewidth(3)
    if len(intervalsList) > 1:
        plt.setp(axs[j].get_xticklabels()[-1], visible=False)
    if len(intervalsList) > 8:
        plt.setp(axs[j].get_xticklabels()[1], visible=False)
    
    #Pluck SiPM temp for subplot title
    if excel:
        if len(f'{excelData.iloc[j, 2]}') < 5:
            axs[j].set_title(f'{(excelData.iloc[j, 2])} C', fontsize=6)
        else:
            axs[j].set_title(f'{(excelData.iloc[j, 2])} C', fontsize=6, rotation=30, ha='left')

#Set plot titles and labels
axs[int(len(intervalsList)/2)].set_xlabel('Time', fontsize=14) #x-axis time
f.suptitle(title, fontsize=24)
try:
    if len(intervalsList) >= 4:
        leg = axs[-1].legend(bbox_to_anchor=(1.05, .5), loc="center left", borderaxespad=0)
    else:
        leg = axs[-1].legend(bbox_to_anchor=(1.02, .5), loc="center left", borderaxespad=0)
    for line in leg.get_lines():
        line.set_linewidth(8.0)
except Exception as e:
    print(e)
    print("No legend for you!")
#plt.subplots_adjust(wspace=0)
plt.tight_layout()
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
            print(f"Valid inputs: {locList[:(numSen)]} or \'all\' or \'DONE\'.")
            for ax in axs:
                clear_data(ax)
            usedNames = []

            #Start manipulate loop
            for i in range(numSen):
                valid = False

                while not valid:
                    #Take name and check for repeat
                    name = input(f"Line {i+1}: ")
                    repeat = name in usedNames
                    if name == '':
                        try:
                            clear_m()
                        except:
                            dummy = 0
                    if not repeat:
                        #Search for name
                        for j in range(numSen):
                            #If found use index
                            if name == sensName_to_loc[sensName[j]] or name == sensName[j]:
                                for k in range(len(intervalsList)):
                                    try:
                                        #Set line object
                                        lineNum = j + numSen * k
                                        xmin = intervalsList[k][0]
                                        xmax = intervalsList[k][1]

                                        #If is pi09 sensor
                                        if j >= senNot09:
                                            filtered_data = data09[(data09['time'] >= xmin) & (data09['time'] <= xmax)]
                                            linesList[lineNum], = axs[k].plot(filtered_data['time'], filtered_data[f'T{j-senNot09}'],
                                                    linestyle='solid', linewidth=1,
                                                    label=f'{sensName_to_loc[sensName[j]]}', color=f'{colorList[j]}')
                                        #If other sensor
                                        else:
                                            filtered_data = dataSourceList[j][(dataSourceList[j]['datetime'] >= xmin) & (dataSourceList[j]['datetime'] <= xmax)]
                                            linesList[lineNum], =axs[k].plot(filtered_data['datetime'], filtered_data['temperature'],
                                                                    linestyle='solid', linewidth=1,
                                                                    label=f'{sensName_to_loc[sensName[j]]}', color=f'{colorList[j]}')
                                    except Exception as e:
                                        print(e)
                                #Append found name to mark as used
                                usedNames.append(sensName[j])
                                usedNames.append(sensName_to_loc[sensName[j]])
                                valid = True
                            
                            #Condition for done and want stop
                            elif name == 'DONE':
                                valid = True
                            
                            #Replot all lines
                            elif name == 'all':
                                for ax in axs:
                                    clear_data(ax)
                                for k in range(len(intervalsList)):
                                    for n in range(numSen):
                                        lineNum = n + numSen * k
                                        xmin = intervalsList[k][0]
                                        xmax = intervalsList[k][1]

                                        #If is pi09 sensor
                                        if n >= senNot09:
                                            filtered_data = data09[(data09['time'] >= xmin) & (data09['time'] <= xmax)]
                                            linesList[lineNum], = axs[k].plot(filtered_data['time'], filtered_data[f'T{n-senNot09}'],
                                                    linestyle='solid', linewidth=1,
                                                    label=f'{sensName_to_loc[sensName[n]]}', color=f'{colorList[n]}')

                                        #If other sensor
                                        else:
                                            filtered_data = dataSourceList[n][(dataSourceList[n]['datetime'] >= xmin) & (dataSourceList[n]['datetime'] <= xmax)]
                                            linesList[lineNum], =axs[k].plot(filtered_data['datetime'], filtered_data['temperature'],
                                                                    linestyle='solid', linewidth=1,
                                                                    label=f'{sensName_to_loc[sensName[n]]}', color=f'{colorList[n]}')
                                name = 'DONE'
                                valid = True
                        #Condition for not found
                        if not valid:
                            print("ERROR: Line not found.")
                    else:
                        print("ERROR: Duplicate line.")
                #Stop if done
                if name == 'DONE':
                    break
            #End manipulate loop
            plt.show(block=False)
        
        ##Bring to front##
        else:
            validInterval = []
            for m in range(len(intervalsList)):
                validInterval.append(m + 1)

            print("Input line to bring to front in format \'interval number, sensor name\'")
            print(f"Valid interval numbers: {validInterval[0:]} or \'all\'.")
            print(f"Valid sensor names: {locList[:(numSen)]} or \'q\' to quit.")
            quitt = False
            
            #Start bring to front loop
            while not quitt:
                valid = False
                intervalNum = ""
                name = ""
                lineName = input("Line: ")

                #Build interval until comma
                for j in range(len(lineName)):
                    if lineName[0] == "q":
                        name = "q"
                        intervalNum = "q"
                        break
                    if lineName[j] == ",":
                        break
                    intervalNum += lineName[j] 

                #If not quit set line name
                if name != "q":
                    name = lineName[(len(intervalNum)+2):]
                if intervalNum != "all" and name != "q":
                    try:
                        intervalNum = int(intervalNum) - 1
                    except Exception as e:
                        print(e)
                        print("ERROR: Invalid interval number.")
                        intervalNum = len(intervalsList) + 10
                        continue

                #Search for name
                for i in range(numSen):
                    #If found use index
                    if name == sensName_to_loc[sensName[i]] or name == sensName[i]:
                        #Use all intervals
                        if intervalNum == "all":
                            for k in range(len(intervalsList)):
                                lineNum = i + numSen * k
                                xmin = intervalsList[k][0]
                                xmax = intervalsList[k][1]
                                
                                #Erase and reset line object
                                try:
                                    #Remove all and catch if some don't exist
                                    try:
                                        remove_lines([linesList[lineNum]])
                                    except:
                                        dummy = 0

                                    #If is pi09 sensor
                                    if i >= senNot09:
                                        filtered_data = data09[(data09['time'] >= xmin) & (data09['time'] <= xmax)]
                                        linesList[lineNum], = axs[k].plot(filtered_data['time'], filtered_data[f'T{i-senNot09}'],
                                                linestyle='solid', linewidth=1,
                                                label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
                                        plt.show(block=False)

                                    #If other sensor
                                    else:
                                        filtered_data = dataSourceList[i][(dataSourceList[i]['datetime'] >= xmin) & (dataSourceList[i]['datetime'] <= xmax)]
                                        linesList[lineNum], =axs[k].plot(filtered_data['datetime'], filtered_data['temperature'],
                                                                linestyle='solid', linewidth=1,
                                                                label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
                                        plt.show(block=False)
                                except Exception as e:
                                    print(e)
                        
                        #Use specified interval
                        elif name != 'q':
                            lineNum = i + numSen * intervalNum
                            xmin = intervalsList[intervalNum][0]
                            xmax = intervalsList[intervalNum][1]
                            
                            #Erase and reset line object
                            try:
                                #Remove all and catch if some don't exist
                                try:
                                    remove_lines([linesList[lineNum]])
                                except:
                                    dummy = 0
                                
                                #If is pi09 sensor
                                if i >= senNot09:
                                    filtered_data = data09[(data09['time'] >= xmin) & (data09['time'] <= xmax)]
                                    linesList[lineNum], = axs[intervalNum].plot(filtered_data['time'], filtered_data[f'T{i-senNot09}'],
                                            linestyle='solid', linewidth=1,
                                            label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
                                    plt.show(block=False)

                                #If other sensor
                                else:
                                    filtered_data = dataSourceList[i][(dataSourceList[i]['datetime'] >= xmin) & (dataSourceList[i]['datetime'] <= xmax)]
                                    linesList[lineNum], =axs[intervalNum].plot(filtered_data['datetime'], filtered_data['temperature'],
                                                            linestyle='solid', linewidth=1,
                                                            label=f'{sensName_to_loc[sensName[i]]}', color=f'{colorList[i]}')
                                    plt.show(block=False)
                            except Exception as e:
                                print(e)
                        valid = True
                    #Condition for quit
                    elif name == 'q':
                        quitt = True
                        valid = True
                #Condition for not found
                if not valid:
                    print("ERROR: Line not found.")
            #End bring to front loop
