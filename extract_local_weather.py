from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

source = urllib.request.urlopen('https://www.weersverwachting.nl/wereldweer/europa/nederland/nieuw-lekkerland').read()
soup = BeautifulSoup(source,'lxml')
table = soup.find('table',{'class':'weather_forecast'})

TableRows = table.find_all('tr')

CleanTableRows = TableRows[2:]

days = []
min_temp = []
max_temp = []
wind_force = []
wind_direction = []
dirty_rain = []
sun_chance = []

for tr in CleanTableRows:
    td = tr.find_all('td')
    rows = [item.text for item in td]

    col1 = rows[0]
    days.append(col1)

    col3 = rows[2]
    min_temp.append(col3)

    col4 = rows[3]
    max_temp.append(col4)

    col5 = rows[4]
    wind_force.append(col5)

    col6 = rows[5]
    wind_direction.append(col6)

    col7 = rows[6]
    dirty_rain.append(col7)

    col8 = rows[8]
    sun_chance.append(col8)

rain_chance = [data[1:] for data in dirty_rain]

weather = []

for image in CleanTableRows:
    col2 = image.find('img').get('title')
    weather.append(col2)

WeatherData = pd.DataFrame({
        'dag': days,
        'weersvoorspelling': weather,
        'minimum temperatuur': min_temp,
        'maximum temperatuur': max_temp,
        'windkracht': wind_force,
        'windrichting': wind_direction,
        'neerslagkans': rain_chance,
        'zonkans': sun_chance,
    })

WeatherData.to_csv('weather-forcast.csv')
