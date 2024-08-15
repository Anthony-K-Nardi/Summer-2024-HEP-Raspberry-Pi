'''
AUTHORED: HUNTER JAYDEN TONY
LAST EDITED: 07/08/2024
LAST CHANGES: Moved to new file, still needed
'''


import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

intervals = [np.arange(1, 4), np.arange(7, 10), np.arange(13, 16)]
x = np.arange(0, 50)
y = np.random.rand(len(x))

x_1 = x[(x >= intervals[0][0]) & (x <= intervals[0][-1])]
y_1 = y[(x >= intervals[0][0]) & (x <= intervals[0][-1])]
x_2 = x[(x >= intervals[1][0]) & (x <= intervals[1][-1])]
y_2 = y[(x >= intervals[1][0]) & (x <= intervals[1][-1])]
x_3 = x[(x >= intervals[2][0]) & (x <= intervals[2][-1])]
y_3 = y[(x >= intervals[2][0]) & (x <= intervals[2][-1])]














































def clear_m():
    import webbrowser as wb
    wb.open('https://www.youtube.com/watch?v=oPLObjVAvIU')
    print("You've been rolled! LMAO XD GG")
