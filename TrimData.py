'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 08/08/2024
LAST CHANGES: FINAL READY TO PUBLISH
PURPOSE: TRIMS UNWANTED DATA BY INTERVAL
'''

import numpy as np
import pandas as pd

def read_bin(filename, dtype):
    return pd.DataFrame(np.fromfile(filename, dtype))

filePath = "/home/shib/Desktop/piData/"
data_type_bin_new = [('source', 'S6'), ('datetime', 'S26'), ('temperature', 'f8'), ('color', 'S8')]
data_type_bin_old = [('source', 'S6'), ('time', 'S15'), ('temperature', 'f8')]
colorListB = [b'Black', b'Gray', b'Purple', b'Green', b'Yellow', b'Orange', b'Red']

try:
    filePath = "/home/shib/Desktop/piData/"
    file_bin = input(f"Enter binary file name (Omit \".bin\"): ")
    data_read = read_bin(f"{filePath}{file_bin}.bin", data_type_bin_new)
    data_read['datetime'] = data_read['datetime'].astype(str)
    data_read['datetime'] = pd.to_datetime(data_read['datetime'], format="ISO8601")
    xmin = input("Input starting time for what you want to trim out in format \'YYYY-mm-dd HH:MM:SS.0\': ")
    xmax = input("Input ending time for what you want to trim out in format \'YYYY-mm-dd HH:MM:SS.0\': ")
    xmin = pd.to_datetime(xmin, format="%Y-%m-%d %H:%M:%S.%f")
    xmax = pd.to_datetime(xmax, format="%Y-%m-%d %H:%M:%S.%f")
    
    filtered_data = data_read[(data_read['datetime'] <= xmin)]
    filtered_data_max = data_read[(data_read['datetime'] >= xmax)]
    filtered_data = pd.concat([filtered_data, filtered_data_max], ignore_index=True)

    with open(f"{filePath}{file_bin}Trimmed.bin", 'ab') as fileBin:
        for i in range(len(data_read['source'])):
            try:
                dataPoint = (filtered_data.loc[i, 'source'], filtered_data.loc[i, 'datetime'], 
                            filtered_data.loc[i, 'temperature'], filtered_data.loc[i, 'color'])
                structuredData = np.array([dataPoint], dtype = data_type_bin_new)
                structuredData.tofile(fileBin)
                if i % 50000 == 0:
                    print(i)
            except:
                data_type_bin_old = 0
except Exception as e:
    print('error')
    print(e)
