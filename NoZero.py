'''
AUTHORED: HUNTER
LAST EDITED: 08/14/2024
LAST CHANGES: Made it work with fast writing to binary
PURPOSE: Removes any zero temperatures from old data
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

zero_to_None ={0 : np.nan}
filePath = "/home/shib/Desktop/piData/"
file_bin = input(f"Enter binary file name: ")
data_read = read_bin(f"{filePath}{file_bin}", DATA_TYPE_BIN)
data_read.replace({'temperature': zero_to_None}, inplace=True)
data_read['source'] = data_read['source'].astype('S6')
data_read['color'] = data_read['color'].astype('S8')
data_read['temperature'] = data_read['temperature'].astype('<f8')
data_read['datetime'] = data_read['datetime'].astype(str)
data_read['datetime'] = pd.to_datetime(data_read['datetime'], format="ISO8601")
file_bin = file_bin[:-4]
data = data_read.to_records(index = False)
with open(f"{filePath}{file_bin}NoZero.bin", 'ab') as fileBin:
    np.recarray.tofile(data, fileBin)
    