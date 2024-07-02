import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

time1 = '23:59:59'
time2 = '06:00:04'
time1_obj = datetime.datetime.strptime(time1, "%H:%M:%S")
time2_obj = datetime.datetime.strptime(time2, "%H:%M:%S")
time_diff = time1_obj - time2_obj
total_seconds = int(time_diff.total_seconds())

print(round(total_seconds / 15))
