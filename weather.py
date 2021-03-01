import requests

url = "https://visual-crossing-weather.p.rapidapi.com/history"

querystring = {"startDateTime":"2020-01-01T00:00:00","aggregateHours":"24","location":"Minsk,BY","endDateTime":"2020-01-10T00:00:00","unitGroup":"us","dayStartTime":"01:00:00","contentType":"json","dayEndTime":"23:00:00","shortColumnNames":"0"}

headers = {
    'x-rapidapi-key': "10276cc884msh9938e545cadf1e9p11fd4bjsna0e5eecf279d",
    'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)