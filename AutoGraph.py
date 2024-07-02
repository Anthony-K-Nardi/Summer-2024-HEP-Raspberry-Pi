import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

TICKS = 15
filePath = "/home/shib/Desktop/"

def AutoGraph(autoDate):

    data_type_bin = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
    dataSourceList = []
    colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']
    colorList = ['Black', 'Gray', 'Purple', 'Green', 'Yellow', 'Orange', 'Red']
    sensColor = ['Black/White', 'White/Gray', 'Purple/Gray', 
                'Green/Yellow', 'Yellow/Orange', 'Orange/Red', 'Red/Brown']

    text = np.loadtxt(f"{filePath}{autoDate}.txt", str)
    title = f'Temperature vs Time ({autoDate})'
    header = text[0,:]
    numSen = len(header) - 2

    with open(f"{filePath}{autoDate}.bin", 'rb') as f:
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
    plt.savefig(f'{filePath}{autoDate}.png')