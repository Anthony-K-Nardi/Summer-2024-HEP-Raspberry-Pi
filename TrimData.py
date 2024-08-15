'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 08/14/2024
LAST CHANGES: Changed to new, faster way to write to binary
PURPOSE: TRIMS UNWANTED DATA BY INTERVAL
'''

import numpy as np
import pandas as pd

def read_bin(filename, dt):
    try:
        df = pd.DataFrame(np.fromfile(filename, dtype=dt))
        dummy = df['source'].astype(str)
    except:
        df = pd.DataFrame(np.fromfile(filename, dtype=DATA_TYPE_BIN_OTHER))
    return df

filePath = "/home/shib/Desktop/piData/"
DATA_TYPE_BIN = [('source', 'S6'), ('datetime', 'S26'), ('temperature', 'f8'), ('color', 'S8')]
DATA_TYPE_BIN_OTHER = [('source', 'S6'), ('datetime', '<M8[ns]'), ('temperature', '<f8'), ('color', 'S8')]

try:
    filePath = "/home/shib/Desktop/piData/"
    file_bin = input(f"Enter binary file name: ")
    data_read = read_bin(f"{filePath}{file_bin}", DATA_TYPE_BIN)
    data_read['source'] = data_read['source'].astype('S6')
    data_read['color'] = data_read['color'].astype('S8')
    data_read['temperature'] = data_read['temperature'].astype(float)
    data_read['datetime'] = data_read['datetime'].astype(str)
    data_read['datetime'] = pd.to_datetime(data_read['datetime'], format="ISO8601")
    xmin = input("Input starting time for what you want to trim out in format \'YYYY-mm-dd HH:MM:SS.0\': ")
    xmax = input("Input ending time for what you want to trim out in format \'YYYY-mm-dd HH:MM:SS.0\': ")
    xmin = pd.to_datetime(xmin, format="%Y-%m-%d %H:%M:%S.%f")
    xmax = pd.to_datetime(xmax, format="%Y-%m-%d %H:%M:%S.%f")
    
    filtered_data = data_read[(data_read['datetime'] <= xmin)]
    filtered_data_max = data_read[(data_read['datetime'] >= xmax)]
    filtered_data = pd.concat([filtered_data, filtered_data_max], ignore_index=True)
    file_bin = file_bin[:-4]
    data = filtered_data.to_records(index = False)
    with open(f"{filePath}{file_bin}Trimmed.bin", 'ab') as fileBin:
        np.recarray.tofile(data, fileBin)
except Exception as e:
    print('error')
    print(e)
