'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 7/29/2024
LAST CHANGES: CONVERSION START
'''

import numpy as np
from numpy import fromfile
from pandas import DataFrame
import pandas as pd

def read_bin(filename, dtype):
    return pd.DataFrame(np.fromfile(filename, dtype))

def convert_data(data_read, date, sensName, colorListB, colorListH):
    color_dict = {color: name for color, name in zip(colorListB, sensName)}
    data_read['source'] = data_read['source'].map(color_dict)
    data_read['time'] = pd.to_datetime(date + ' ' + data_read['time'].astype(str), format="%Y-%m-%d %H:%M:%S.%f")
    data_read['color'] = data_read['source'].map(dict(zip(sensName, colorListH)))
    return data_read

filePath = "/home/shib/Desktop/piData/"
data_type_bin_new = [('source', 'S6'), ('datetime', 'S26'), ('temperature', 'f8'), ('color', 'S8')]
data_type_bin_old = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']

##pi03##
pi = 'pi03' #pi name
sensName = ['pi03-1', 'pi03-2', 'pi03-3', 'pi03-4', 'pi03-5', 'pi03-6', 'pi03-7'] #Sensor names for pi03
colorListH=['#6b7c85', '#0165fc', '#bf77f6', '#01ff07', 
           '#fffd01', '#ff5b00', '#e50000'] #Plot colors for pi03 hex
'''
##pi02##
pi = 'pi02' #pi name
sensName = ['pi02-1', 'pi02-2', 'pi02-3', 'pi02-4', 'pi02-5', 'pi02-6', 'pi02-7'] #Sensor names for pi02
colorListH=['#d8dcd6', '#75bbfd', '#eecffe', '#c7fdb5', 
           '#fbeeac', '#ffb07c', '#fe019a'] #Plot colors for pi02 hex
'''
'''
##pi04##
pi = 'pi04' #pi name
sensName = ['pi04-1', 'pi04-2', 'pi04-3', 'pi04-4', 'pi04-5', 'pi04-6', 'pi04-7'] #Sensor names for pi04
colorListH=['#000000', '#047495', '#7e1e9c', '#15b01a', 
           '#f4d054', '#c65102', '#980002'] #Plot colors for pi04 hex
'''

try:
    filePath = "/home/shib/Desktop/piData/"
    file_txt = input("Enter text file name (Omit \".txt\"): ")
    text = np.loadtxt(f"{filePath}{file_txt}.txt", str)
    date = text[1, 0]
    header = text[0, :]
    numSen = len(header) - 2
    file_bin = input(f"Enter binary file name (Omit \".bin\"): ")
    data_read = read_bin(f"{filePath}{file_bin}.bin", data_type_bin_old)
    data_read = convert_data(data_read, date, sensName, colorListB, colorListH)

    with open(f"{filePath}{file_bin}{pi}Converted.bin", 'ab') as fileBin:
        for i in range(len(data_read['source'])):
            dataPoint = (data_read.loc[i, 'source'], data_read.loc[i, 'time'], 
                         data_read.loc[i, 'temperature'], data_read.loc[i, 'color'])
            structuredData = np.array([dataPoint], dtype = data_type_bin_new)
            structuredData.tofile(fileBin)
            if i % 50000 == 0:
                print(i)
except Exception as e:
    print(e)
