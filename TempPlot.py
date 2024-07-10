import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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

yn = input(f"Do you want to load {DATE_TODAY} data? y/n: ")

while not valid:
    try:
        if yn == 'y':
            text = np.loadtxt(f"{filePath}{DATE_TODAY}.txt", str)
            title = f'Temperature vs Time ({DATE_TODAY})'
        if yn == 'n':
            file = input("Enter text file name (Omit \".txt\".): ")
            text = np.loadtxt(f"{filePath}{file}.txt", str)
            date = text[1, 0]
            title = f'Temperature vs Time ({date})'
        header = text[0,:]
        numSen = len(header) - 2
        valid = True
    except:
        print("ERROR: Text file not open, check file name and put on desktop. Omit \".txt\".")

valid = False

while not valid:
    try:
        if yn == 'y':
            with open(f"{filePath}{DATE_TODAY}.bin", 'rb') as f:
                data_read = np.fromfile(f, dtype = data_type_bin)
        if yn == 'n':
            file = input("Enter binary file name (Omit \".bin\".): ")
            with open(f"{filePath}{file}.bin", 'rb') as f:
                data_read = np.fromfile(f, dtype = data_type_bin)
        valid = True
    except:
        print("ERROR: Binary file not open, check file name and put on desktop. Omit \".bin\".")

valid = False

while not valid:
    try:
        xmin = input("Set x-axis start time in \'HH:MM:SS\': ")
        xmin = mdates.datestr2num(xmin)
        valid = True
    except:
        print("Wrong format dummy read better!")

valid = False

while not valid:
    try:
        xmax = input("Set x-axis end time in \'HH:MM:SS\': ")
        xmax = mdates.datestr2num(xmax)
        valid = True
    except:
        print("Wrong format dummy read better!")

valid = False

yn = input("Do you want to save plot? y/n: ")
if yn == 'y':
    wantPng = True
    plotName = input("Desired name of plot file (Omit \".png\"): ")

#Condense data to input interval:
data_read = data_read[mdates.datestr2num(data_read['time']) >= xmin]
data_read = data_read[mdates.datestr2num(data_read['time']) <= xmax]

for i in range(numSen) :
    dataSourceList.append(data_read[data_read['source'] == colorListB[i]])
    #checkSize = len(dataSourceList[i]['temperature'])
    #print(checkSize)

timeDiff = (xmax - xmin) * 86400
interval = int(round(timeDiff / TICKS))

plt.figure(figsize=(10,8))
plt.xlim(xmin, xmax)
#plt.ylim(-10, 60)

ax = plt.gca()
for i in range(numSen):
    ax.plot(mdates.datestr2num(dataSourceList[i]['time']), dataSourceList[i]['temperature'], 
            '-', label=f'{sensColor[i]}', color=f'{colorList[i]}')
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=interval))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

plt.gcf().autofmt_xdate()
plt.xticks(rotation=90)
plt.xlabel('Time')
plt.ylabel('Temperature in C')
plt.title(title)
plt.legend()
if wantPng:
    plt.savefig(f'{plotName}.png')
plt.show()