'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 6/25/2024
LAST CHANGES: AUTOGRAPH FUNCTION
'''

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import board
import busio
import datetime
#import keyboard
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time

NUM_SENSORS = 7  #MAX SEVEN
R25 = 10000      #Resistance of thermistor at 25C
MAXBIT = 32767   #2^15 - 1 (From I2C)
FSVOLT = 4.096   #Full Scale Voltage (From I2C)
PLOT_PAUSE = 0.1      #Limit the live plot in additional seconds
PAUSE = 0.4           #Limit the program runtime in additional seconds
FSVOLT_MAXBIT = FSVOLT / MAXBIT   #EFFICIENCY
MAXBIT_FSVOLT = MAXBIT / FSVOLT   #EFFICIENCY
TICKS = 15
FILE_PATH = "/home/shib/Desktop/"
a = 3.3540154*pow(10, -3)   #DATASHEET [0, 50]
b = 2.5627725*pow(10, -4)   #DATASHEET [0, 50]
c = 2.0829210*pow(10, -6)   #DATASHEET [0, 50]
d = 7.3003206*pow(10, -8)   #DATASHEET [0, 50]
aa = -1.4141963*pow(10, 1)
bb = 4.4307830*pow(10, 3)
cc = -3.4078983*pow(10, 4)
dd = -8.8941929*pow(10, 6)

#Do we want stuff?
wantVerify = False
wantPlot = True
wantFile = False
wantPrint = True
wantAuto = False  #!!! ONLY ACCESSIBLE IF wantFile == True !!!#

def I2CToTemp(z, live_voltage):
    vT = z * (FSVOLT_MAXBIT) #Voltage thermistor
    vR = live_voltage - vT #Voltage across resistor
    I = vR / rFix #Current
    rT = vT / I #Resistance thermistor
    temp = 1 / (a + b*np.log(rT / R25) + c*pow(np.log(rT / R25),2) + d*pow(np.log(rT / R25),3)) #Datasheet Method
    return (temp - 273.15) #Temperature in celcius

def TempToI2C(temp, live_voltage):
    temp = temp + 273.15
    rT = R25 * np.exp(aa + bb / temp + cc / pow(temp, 2) + dd / pow(temp, 3)) #Resistance thermistor datasheet
    vT = live_voltage / (1 + rFix/rT) #Voltage thermistor
    z = vT * (MAXBIT_FSVOLT) #I2C integer
    return z

def AutoGraph(autoDate):
    data_type_bin = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
    dataSourceList = []
    colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']
    colorList = ['Black', 'Gray', 'Purple', 'Green', 'Yellow', 'Orange', 'Red']
    sensColor = ['Black/White', 'White/Gray', 'Purple/Gray', 
                'Green/Yellow', 'Yellow/Orange', 'Orange/Red', 'Red/Brown']

    text = np.loadtxt(f"{FILE_PATH}{autoDate}.txt", str)
    title = f'Temperature vs Time ({autoDate})'
    header = text[0,:]
    numSen = len(header) - 2

    with open(f"{FILE_PATH}{autoDate}.bin", 'rb') as f:
        data_read = np.fromfile(f, dtype = data_type_bin)

    xmin = "00:00:00"
    xmin = mdates.datestr2num(xmin)

    xmax = "23:59:59"
    xmax = mdates.datestr2num(xmax)
    
    for i in range(numSen) :
        dataSourceList.append(data_read[data_read['source'] == colorListB[i]])

    timeDiff = (xmax - xmin) * 86400
    interval = int(round(timeDiff / TICKS))

    plt.figure(figsize=(10,8))
    plt.xlim(xmin, xmax)
    plt.ylim(-10, 60)

    ax = plt.gca()
    for i in range(numSen):
        ax.plot(mdates.datestr2num(dataSourceList[i]['time']), dataSourceList[i]['temperature'], 
                '.', label=f'{sensColor[i]}', color=f'{colorList[i]}')
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    plt.ylabel('Temperature in C')
    plt.title(title)
    plt.legend()
    plt.savefig(f'{FILE_PATH}{autoDate}.png')

#Prepare I2C and ADS for each sensor:
i2c = busio.I2C(board.SCL, board.SDA)
#Sensor 0 at first address
ads0 = ADS.ADS1115(i2c, address=0x48)
ads0.mode = Mode.SINGLE
ads0.data_rate = 860
#Sensor 1 at second address
ads1 = ADS.ADS1115(i2c, address=0x49)
ads1.mode = Mode.SINGLE
ads1.data_rate = 860

#Prepare readings for each sensor:
a0 = AnalogIn(ads0, ADS.P0)       #Voltage measurement from I2C48 pin A0
blkWht = AnalogIn(ads0, ADS.P1)   #Sensor 1 from I2C48 pin A1
gryWht = AnalogIn(ads0, ADS.P2)   #Sensor 2 from I2C48 pin A2
prpGry = AnalogIn(ads0, ADS.P3)   #Sensor 3 from I2C48 pin A3
grnYel = AnalogIn(ads1, ADS.P0)   #Sensor 4 from I2C49 pin A0
orgYel = AnalogIn(ads1, ADS.P1)   #Sensor 5 from I2C49 pin A1
redOrg = AnalogIn(ads1, ADS.P2)   #Sensor 6 from I2C49 pin A2
redBrn = AnalogIn(ads1, ADS.P3)   #Sensor 7 from I2C49 pin A3
sensorList = [blkWht, gryWht, prpGry, grnYel, orgYel, redOrg, redBrn]

#MAKE ALL THE LISTS !!!
X = [[] for _ in range(NUM_SENSORS)]
Y = [[] for _ in range(NUM_SENSORS)]
rFixList = [8890, 9010, 8940, 8930, 8950, 8960, 8970]
colorList = ['Black', 'Gray', 'Purple', 'Green', 'Yellow', 'Orange', 'Red']
hexList = ['#18191a', '#808080', '#9529df', '#008751', '#ffec27', '#ffa300', '#ff004d']
dataPointList = []
currentYList = []
currentXList=[]


if wantPlot :
    #Prepare plot and plot origin:
    plt.figure(figsize=(10,9))
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=90)
    plt.ylim(-10, 60) #-10C - 60C
    plt.xlabel('Time(seconds)') #x-axis in seconds
    plt.ylabel('Temperature(celsius)') #y-axis in celcius
    plt.title('Temperature Over Time')
    lines = [plt.plot([], [], label=f"Temp {colorList[i]}", 
                      color=hexList[i])[0] for i in range(NUM_SENSORS)]
    plt.legend()
    plt.show(block=False)

if wantFile :
    #Prepare files for text and binary recording
    date_today = datetime.date.today()
    fileBin = open(f"{FILE_PATH}{date_today}.bin", 'ab')
    #Create header
    header = '    Date        Time         '
    for i in range(NUM_SENSORS):
        header += f'{colorList[i]}   '
    header += '\n'
    #Write header to file
    with open(f"{FILE_PATH}{date_today}.txt", 'a') as fileText:
        fileText.write(header)

#Mark start time
begin = datetime.datetime.now()

while True:
    '''
    if keyboard.is_pressed('l'):
        if wantPlot == True:
            wantPlot = False
        else:
            wantPlot = True
            PlotFormat()
    '''
    if wantFile :
        #Condition for midnight
        date_check = datetime.date.today()
        if date_check != date_today:
            #Put autograph call here
            fileBin.close()
            if wantAuto :
                AutoGraph(date_today)
            date_today = date_check
            with open(f"{FILE_PATH}{date_today}.txt", 'a') as fileText:
                fileText.write(header)
            fileBin = open(f"{FILE_PATH}{date_today}.bin", 'ab')
    
    for i in range(NUM_SENSORS):
        #Set circuit specific voltage and resistance
        live_voltage = a0.voltage*2
        rFix = rFixList[i]

        #Acquire sensor temperature and verify
        y = I2CToTemp(sensorList[i].value, live_voltage)
        if wantVerify :
            verify = TempToI2C(y, live_voltage)
            print(sensorList[i].value, " ", round(verify))
        
        #Get data for binary
        timeNow = datetime.datetime.now().strftime("%H:%M:%S.%f")
        plotTime = datetime.datetime.now()
        dataPoint = (colorList[i], timeNow, y)
        dataPointList.append(dataPoint)

        #Append verified sensor point
        currentYList.append(y)
        currentXList.append(plotTime)

        #Write data to binary
        if wantFile :
            data_type = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
            structuredData = np.array([dataPointList[i]], dtype = data_type)
            structuredData.tofile(fileBin)

    if wantFile:
        #Write to text file every two seconds
        check = datetime.datetime.now()
        if check >= begin + datetime.timedelta(seconds = 2):
            begin = check
            with open(f"{FILE_PATH}{date_today}.txt", 'a') as fileText:
                #Create content
                content = f"{check}   "
                for i in range(NUM_SENSORS):
                    temp = "%.2f" % round(currentYList[i],2)
                    content += f'{temp}   '
                content += '\n'
                #Write content
                fileText.write(content)

    if wantPrint:
        #Create content
        content = ""
        for i in range(NUM_SENSORS):
            temp = "%.2f" % round(currentYList[i],2)
            content += f'{temp}   '
        #Write content and reset list
        print(content)

    if wantPlot :
        #Add to X and Y lists
        for i in range(NUM_SENSORS):
            X[i].append(currentXList[i])
            Y[i].append(currentYList[i])
            lines[i].set_data(X[i], Y[i])
        #Plot sensor point and pause
        plt.pause(PLOT_PAUSE)
        ax.relim()
        ax.autoscale_view(True, True, True)

    dataPointList = []
    currentYList = []
    currentXList = []
    time.sleep(PAUSE)