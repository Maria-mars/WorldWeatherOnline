import json
import urllib.request
from datetime import datetime
import psycopg2
BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/'
ApiKey = 'BJLWM6CCCBCRKX6B3WUVQZSVX'
UnitGroup = 'metric'
Locations = 'Minsk,BY'
QueryType = 'FORECAST'
AggregateHours = '24'
StartDate = '2019-10-01'
EndDate = '2020-12-01'
if QueryType == 'FORECAST':
    print(' - Fetching forecast data')
    QueryParams = 'forecast?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&shortColumnNames=true'
else:
    print(' - Fetching history for date: ', QueryType)
    QueryParams = 'history?aggregateHours=' + AggregateHours + '&unitGroup=' + UnitGroup + '&startDateTime=' + StartDate + \
                  'T00%3A00%3A00&endDateTime=' + EndDate + 'T00%3A00%3A00'
Locations = '&locations=' + Locations
ApiKey = '&key=' + ApiKey
URL = BaseURL + QueryParams + Locations + ApiKey + "&contentType=json"
print(' - Running query URL: ', URL)
print()
response = urllib.request.urlopen(URL)
data = response.read()
weatherData = json.loads(data.decode('utf-8'))
errorCode = weatherData["errorCode"] if 'errorCode' in weatherData else 0
if (errorCode > 0):
    print("An error occurred retrieving the data:" + weatherData["message"])
    exit("Script terminated")
print("Connecting to mysql database")
cnx = psycopg2.connect(database="weather_data",
                       user="postgres",
                       password="postgres",
                       host="127.0.0.1",
                       port="5432")

cursor = cnx.cursor()

delete_weather_data=("""TRUNCATE TABLE weather_data""")
cursor.execute(delete_weather_data)
cnx.commit()

# Create an insert statement for inserting rows of data
insert_weather_data = ("""INSERT INTO weather_data
                       (address,latitude,longitude,datetime,maxt,mint,temp,precip,wspd,wdir,wgust,pressure)
                       VALUES (%(address)s, %(latitude)s, %(longitude)s, %(datetime)s, %(maxt)s,%(mint)s, %(temp)s,
                        %(precip)s, %(wspd)s, %(wdir)s, %(wgust)s, %(pressure)s)""")

# Iterate through the locations
locations = weatherData["locations"]
for locationid in locations:
    location = locations[locationid]
    # Iterate through the values (values are the time periods in the weather data)
    for value in location["values"]:
        data_wx = {
            'address': location["address"],
            'latitude': location["latitude"],
            'longitude': location["longitude"],
            'datetime': datetime.utcfromtimestamp(value["datetime"] / 1000.),
            'maxt': value["maxt"] if 'maxt' in value else 0,
            'mint': value["mint"] if 'mint' in value else 0,
            'temp': value["temp"],
            'precip': value["precip"],
            'wspd': value["wspd"],
            'wdir': value["wdir"],
            'wgust': value["wgust"],
            'pressure': value["sealevelpressure"]
        }
        cursor.execute(insert_weather_data, data_wx)
        cnx.commit()

cursor.close()
cnx.close()
print("Database connection closed")

print("Done")
