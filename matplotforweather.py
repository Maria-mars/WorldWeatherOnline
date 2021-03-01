from datetime import datetime
import json
import matplotlib.pyplot as plt
from meteostat import Stations, Daily
stations = Stations(lat = 53.9, lon = 27.5667, daily = datetime(2019, 1, 1))
#data = Daily(station, start = datetime(2018, 1, 1), end = datetime(2018, 12, 31))
station = stations.fetch(1)
data = Daily(station, start = datetime(2019, 11, 1), end = datetime(2020, 11, 30))
data = data.fetch()
print(data)
data.plot(kind='scatter',x='snow',y='tmin')
plt.show()
#data.to_csv('wlastyear.csv', encoding='utf-8', date_format='%Y/%m/%d',na_rep='NULL')