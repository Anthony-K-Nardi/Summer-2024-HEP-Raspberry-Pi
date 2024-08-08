'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 08/08/2024
LAST CHANGES: FINAL READY TO PUBLISH
'''

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import board
import busio
import datetime
import threading
from sshkeyboard import listen_keyboard
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time
import math

#Do we want stuff?
wantFile = True
wantPlot = False #Keep as False but won't break if True
wantPrint = False #Keep as False but won't break if True
wantVerify = False #Keep as False but won't break if True
clearFigure = False #Keep as False but won't break if True

DATE_TODAY = datetime.date.today() #Today's date
NUM_SENSORS = 7  #MAX SEVEN
R25 = 10000      #Resistance of thermistor at 25C
MAXBIT = 32767   #2^15 - 1 (From I2C)
FSVOLT = 4.096   #Full Scale Voltage (From I2C)
TICKS = 15       #Amount of marks on x-axis
PLOT_PAUSE = 0.1    #Limit the live plot in additional seconds
PAUSE = 0.4         #Limit the program runtime in seconds
FSVOLT_MAXBIT = FSVOLT / MAXBIT     #EFFICIENCY
MAXBIT_FSVOLT = MAXBIT / FSVOLT     #EFFICIENCY
FILE_PATH = "/home/shib/Desktop/piData/"   #Make path to desktop

a = 3.3540154*pow(10, -3)    #DATASHEET [0, 50]
b = 2.5627725*pow(10, -4)    #DATASHEET [0, 50]
c = 2.0829210*pow(10, -6)    #DATASHEET [0, 50]
d = 7.3003206*pow(10, -8)    #DATASHEET [0, 50]
aa = -1.4141963*pow(10, 1)   #DATASHEET for reverse
bb = 4.4307830*pow(10, 3)    #DATASHEET for reverse
cc = -3.4078983*pow(10, 4)   #DATASHEET for reverse
dd = -8.8941929*pow(10, 6)   #DATASHEET for reverse

def I2CToTemp(z, live_voltage):
    vT = z * (FSVOLT_MAXBIT) #Voltage thermistor
    vR = live_voltage - vT #Voltage across resistor
    I = vR / rFix #Current
    rT = vT / I #Resistance thermistor
    #Datasheet method for temp:
    temp = 1 / (a + b*np.log(rT / R25) + c*pow(np.log(rT / R25),2) + d*pow(np.log(rT / R25),3))
    return (temp - 273.15) #Temperature in celcius

def TempToI2C(temp, live_voltage):
    temp = temp + 273.15 #Temperature in Kelvin
    #Datasheet method for resistance thermistor:
    rT = R25 * np.exp(aa + bb / temp + cc / pow(temp, 2) + dd / pow(temp, 3))

    vT = live_voltage / (1 + rFix/rT) #Voltage thermistor
    z = vT * (MAXBIT_FSVOLT) #I2C integer
    return z

def press_g():
    #Live graph hotkey
    global wantPlot
    global clearFigure
    global X
    global Y

    if wantPlot:
        wantPlot = False
        X = [[] for _ in range(NUM_SENSORS)]
        Y = [[] for _ in range(NUM_SENSORS)]
        clearFigure = True
    else:
        wantPlot = True

def press_p():
    #Print temperatures to terminal hotkey
    global wantPrint

    if wantPrint:
        wantPrint = False
    else:
        wantPrint = True

def press_v():
    #Print integers to terminal hotkey
    global wantVerify

    if wantVerify:
        wantVerify = False
    else:
        wantVerify = True

def key_event(key):
    #If live graph
    if key == 'g':
        press_g()

    #If print temperatures
    elif key == 'p':
        press_p()

    #If print integers
    elif key == 'v':
        press_v()

def start_listening():
    #Listener function
    listen_keyboard(on_press=key_event)

def check_midnight(date_today):
    #Is it midnight?
    check = datetime.date.today()
    if check != date_today:
        return True #Is midnight
    else:
        return False #Not midnight

#Prepare I2C and ADS for each sensor:
i2c = busio.I2C(board.SCL, board.SDA)
#ADS 0 at first address
ads0 = ADS.ADS1115(i2c, address=0x48)
ads0.mode = Mode.SINGLE
ads0.data_rate = 860
#ADS 1 at second address
ads1 = ADS.ADS1115(i2c, address=0x49)
ads1.mode = Mode.SINGLE
ads1.data_rate = 860
'''
#Prepare each sensor:
#pi03 setup
a0 = AnalogIn(ads0, ADS.P0)      #Voltage measurement from I2C48 pin A0
sens0 = AnalogIn(ads0, ADS.P1)   #Sensor 1 from I2C48 pin A1
sens1 = AnalogIn(ads0, ADS.P2)   #Sensor 2 from I2C48 pin A2
sens2 = AnalogIn(ads0, ADS.P3)   #Sensor 3 from I2C48 pin A3
sens3 = AnalogIn(ads1, ADS.P0)   #Sensor 4 from I2C49 pin A0
sens4 = AnalogIn(ads1, ADS.P1)   #Sensor 5 from I2C49 pin A1
sens5 = AnalogIn(ads1, ADS.P2)   #Sensor 6 from I2C49 pin A2
sens6 = AnalogIn(ads1, ADS.P3)   #Sensor 7 from I2C49 pin A3
pi = 'pi03' #pi name
sensName = ['pi03-1', 'pi03-2', 'pi03-3', 'pi03-4', 'pi03-5', 'pi03-6', 'pi03-7'] #Sensor names for pi03
colorListH=['#6b7c85', '#0165fc', '#bf77f6', '#01ff07', 
           '#fffd01', '#ff5b00', '#e50000'] #Plot colors for pi03 hex
#colorList=['xkcd:battleship grey', 'xkcd:bright blue', 'xkcd:light purple', 'xkcd:bright green', 
#           'xkcd:bright yellow', 'xkcd:bright orange', 'xkcd:red']
'''
#pi04 setup
a0 = AnalogIn(ads1, ADS.P3)      #Voltage measurement from I2C49 pin A3
sens0 = AnalogIn(ads0, ADS.P0)   #Sensor 1 from I2C48 pin A0
sens1 = AnalogIn(ads0, ADS.P1)   #Sensor 2 from I2C48 pin A1
sens2 = AnalogIn(ads0, ADS.P2)   #Sensor 3 from I2C48 pin A2
sens3 = AnalogIn(ads0, ADS.P3)   #Sensor 4 from I2C48 pin A3
sens4 = AnalogIn(ads1, ADS.P0)   #Sensor 5 from I2C49 pin A0
sens5 = AnalogIn(ads1, ADS.P1)   #Sensor 6 from I2C49 pin A1
sens6 = AnalogIn(ads1, ADS.P2)   #Sensor 7 from I2C49 pin A2
pi = 'pi04' #pi name
sensName = ['pi04-1', 'pi04-2', 'pi04-3', 'pi04-4', 'pi04-5', 'pi04-6', 'pi04-7'] #Sensor names for pi04
colorListH=['#000000', '#047495', '#7e1e9c', '#15b01a', 
           '#f4d054', '#c65102', '#980002'] #Plot colors for pi04 hex
#colorList=['xkcd:black', 'xkcd:sea blue', 'xkcd:purple', 'xkcd:green', 
#           'xkcd:maize', 'xkcd:dark orange', 'xkcd:blood red']
'''
#pi02 setup
a0 = AnalogIn(ads1, ADS.P0)      #Voltage measurement from I2C49 pin A0
sens0 = AnalogIn(ads1, ADS.P1)   #Sensor 1 from I2C49 pin A1
sens1 = AnalogIn(ads1, ADS.P2)   #Sensor 2 from I2C49 pin A2
sens2 = AnalogIn(ads1, ADS.P3)   #Sensor 3 from I2C49 pin A3
sens3 = AnalogIn(ads0, ADS.P0)   #Sensor 4 from I2C48 pin A0
sens4 = AnalogIn(ads0, ADS.P1)   #Sensor 5 from I2C48 pin A1
sens5 = AnalogIn(ads0, ADS.P2)   #Sensor 6 from I2C48 pin A2
sens6 = AnalogIn(ads0, ADS.P3)   #Sensor 7 from I2C48 pin A3
pi = 'pi02' #pi name
sensName = ['pi02-1', 'pi02-2', 'pi02-3', 'pi02-4', 'pi02-5', 'pi02-6', 'pi02-7'] #Sensor names for pi02
colorListH=['#d8dcd6', '#75bbfd', '#eecffe', '#c7fdb5', 
           '#fbeeac', '#ffb07c', '#fe019a'] #Plot colors for pi02 hex
#colorList=['xkcd:light gray', 'xkcd:sky blue', 'xkcd:pale lavender', 'xkcd:pale green', 
#           'xkcd:light tan', 'xkcd:peach', 'xkcd:neon pink']
'''
#Dictionary for sensor names
sensName_to_loc =  {'pi02-1': 'T-16-C', 'pi02-2': 'T-40-C', 'pi02-3': 'B-CCM-B', 'pi02-4': 'B-16-L',
                    'pi02-5': 'R-00-M-02', 'pi02-6': 'T-11-C', 'pi02-7': 'B-14-L',
                    'pi03-1': 'B-24-L', 'pi03-2': 'T-24-C', 'pi03-3': 'B-23-H', 'pi03-4': 'B-CCM-A',
                    'pi03-5': 'R-00-M-03', 'pi03-6': 'T-22-C', 'pi03-7': 'B-25-L',
                    'pi04-1': 'B-42-C', 'pi04-2': 'B-31-C', 'pi04-3': 'B-22-H', 'pi04-4': 'T-46-H',
                    'pi04-5': 'R-00-M-04', 'pi04-6': 'B-CEN', 'pi04-7': 'T-21-C',
                    'pi09-0': 'R-00-M-09', 'pi09-1': 'T-41-H', 'pi09-2': 'T-42-H', 'pi09-3': 'T-IN',
                    'pi09-4': 'T-MID', 'pi09-5': 'T-OUT', 'pi09-6': 'B-RM-3', 'pi09-7': 'T-RM-3'}
#MAKE ALL THE LISTS !!!
X = [[] for _ in range(NUM_SENSORS)]
Y = [[] for _ in range(NUM_SENSORS)]
sensList = [sens0, sens1, sens2, sens3, sens4, sens5, sens6]
data_type_bin = [('source', 'S6'), ('datetime', 'S26'),
                 ('temperature', 'f8'), ('color', 'S8')]
dataPointList = []
currentYList = []
currentXList = []
prevYList = [0]*NUM_SENSORS
rFixList = [6110, 6110, 6110, 6110, 6110, 6110, 6110] #Measured out of circuit
#rFixList = [8990, 8990, 8990, 8990, 8990, 8990, 8990] #Jumper Values

if wantFile :
    #Prepare files for text and binary recording
    fileBin = open(f"{FILE_PATH}{DATE_TODAY}{pi}.bin", 'ab')
    #Create header
    header = '    Date        Time         '
    for i in range(NUM_SENSORS):
        header += f'{sensName[i]}  '
    header += '\n'
    #Write header to file
    with open(f"{FILE_PATH}{DATE_TODAY}{pi}.txt", 'a') as fileText:
        fileText.write(header)
        fileText.flush()

#Mark start time
begin = datetime.datetime.now()

#Prepare plot and plot origin:
title = f'Temperature Over Time ({DATE_TODAY} {pi})'
plt.figure(figsize=(16,8))
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=90)
plt.xlabel('Time') #x-axis time
plt.ylabel('Temperature (Celsius)') #y-axis in celcius
plt.title(title)
lines = [plt.plot([], [], '-', label=f'{sensName_to_loc[sensName[i]]}',
                  color=colorListH[i])[0] for i in range(NUM_SENSORS)]
leg = plt.legend(bbox_to_anchor=(1.01, .5), loc="center left", borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(8.0)
plt.show(block=False)

#Set listener and start:
listener_thread = threading.Thread(target=start_listening, daemon=True)
listener_thread.start()

while True:
    #Condition for midnight
    if check_midnight(DATE_TODAY):
        #Update title
        new_day = datetime.date.today()
        title = f'Temperature Over Time ({new_day} {pi})'
        #Update date
        DATE_TODAY = new_day
    
    #Corrupt prevention
    fileBin.flush()
    
    for i in range(NUM_SENSORS):
        #Set circuit specific voltage and resistance
        rFix = rFixList[i]

        #Acquire sensor temperature and verify
        try:
            timeNow = datetime.datetime.now()
            y = I2CToTemp(sensList[i].value, a0.voltage*2)
            live_voltage = a0.voltage*2
            if y > 100 or math.isnan(y):
                y = prevYList[i]
        except Exception as e:
            y = prevYList[i]
            print(e, "I2C ERROR", timeNow)
        
        if wantVerify: 
            verify = TempToI2C(y, live_voltage)
            print(sensList[i].value, " ", round(verify))

        #Get data for binary
        dataPoint = (sensName[i], timeNow, y, colorListH[i])
        dataPointList.append(dataPoint)

        #Get data for plot
        currentYList.append(y)
        currentXList.append(timeNow)

        #Write data to binary on right day
        if wantFile and (not check_midnight(DATE_TODAY)):
            structuredData = np.array([dataPointList[i]], dtype = data_type_bin)
            structuredData.tofile(fileBin)

    #Don't write after midnight!
    if not check_midnight(DATE_TODAY):
        if wantFile:
            #Write to text file every two seconds
            check = datetime.datetime.now()

            if check >= begin+datetime.timedelta(seconds=2):
                begin = check
                with open(f"{FILE_PATH}{DATE_TODAY}{pi}.txt", 'a') as fileText:
                    #Create content
                    content = f"{timeNow}   "
                    
                    for i in range(NUM_SENSORS):
                        temp = "%.2f" % round(currentYList[i],2)
                        content += f'{temp}   '
                    content += '\n'
                    
                    #Write content
                    fileText.write(content)
                    fileText.flush()

        if wantPrint:
            #Create content
            content = ""
            
            for i in range(NUM_SENSORS):
                temp = "%.2f" % round(currentYList[i],2)
                content += f'{temp}   '
            
            #Write content and reset list
            print(content)

        if wantPlot:
            #Add to X and Y lists
            for i in range(NUM_SENSORS):
                X[i].append(currentXList[i])
                Y[i].append(currentYList[i])
                lines[i].set_data(X[i], Y[i])
            
            #Plot sensor point and pause
            plt.pause(PLOT_PAUSE)
            ax.relim()
            ax.autoscale_view(True, True, True)

        if clearFigure:
            #Close and reset:
            plt.close()
            clearFigure = False

            #Reset formatting:
            plt.figure(figsize=(16,8))
            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.xticks(rotation=90)
            plt.xlabel('Time') #x-axis time
            plt.ylabel('Temperature (Celsius)') #y-axis in celcius
            plt.title(title)
            lines = [plt.plot([], [], '-', label=f'{sensName_to_loc[sensName[i]]}',
                    color=colorListH[i])[0] for i in range(NUM_SENSORS)]
            leg = plt.legend(bbox_to_anchor=(1.01, .5), loc="center left", borderaxespad=0)
            for line in leg.get_lines():
                line.set_linewidth(8.0)
            plt.show(block=False)         
    #Clear lists:
    prevYList = currentYList
    dataPointList = []
    currentYList = []
    currentXList = []

    time.sleep(PAUSE)
