# -*- coding: utf-8 -*-


from __future__ import print_function
import sys
import json
import pandas as pd
#from aiml.constants import *
import pyowm

eNcOdiNG = 'utf-8'

def read_from_csv():
    df = pd.read_csv('cities.csv')
    #print (df['name'][:])
    encity = dict(zip(df['subcountry'][:], df['country'][:]))
    return encity

def querylocation(term):
    if term in read_from_csv():
        return term,read_from_csv()[term]
    else:
        print("cannot find place")
    return

def  queryrealtimeWeatherinfo(code):
    owm = pyowm.OWM('1197f60eb5f25e5e65359a2031142a12')
    observation = owm.weather_at_place(str(code))
    w = observation.get_weather()
    status = str(w)
    temperature = w.get_temperature('celsius')
    tomorrow = pyowm.timeutils.tomorrow()
    wind = w.get_wind()
    status_split = (status.split('status='))

    weather = {}
    weather['status'] = (status_split[1].strip('>'))
    weather['temprature'] = (temperature['temp'])

    return weather

def showrealtimeWeatherinfo(weather_info):
    template = u"weather facts: {status}, The temperature is {temprature}°c"
    # template = u"{name} {last_update} Weather facts: temperature {temperature}°c, {text}"
    #  print(template.format(**info))
    response = template.format(**weather_info).encode(eNcOdiNG)
    #response = response.encode(eNcOdiNG) if type(response) == str else response.decode('utf-8')
    print(response)

showrealtimeWeatherinfo(queryrealtimeWeatherinfo("lagos"))

def main():
    assert len(sys.argv) >= 3
    function = sys.argv[1]
    #function = 'realtime'
    term = ''.join(sys.argv[2:])
    #term = 'ondo'
    if function == 'realtime':
        #location = querylocation(term)
        location = True
        if location:
            showrealtimeWeatherinfo(queryrealtimeWeatherinfo(term))

if __name__ == '__main__':
    main()