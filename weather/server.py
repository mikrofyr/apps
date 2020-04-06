#!/usr/bin/env python3

from prometheus_client import start_http_server
from prometheus_client import Gauge
import random
import time
from weatherstation import WeatherStation

MAC_ADDR = "A4:4A:38:A7:90:34"
GAUGE_T0 = Gauge('weather_temp_0', 'Temperature, Celcius')
GAUGE_T1 = Gauge('weather_temp_1', 'Temperature, Celcius')
GAUGE_H0 = Gauge('weather_humid_0', 'Humidity, percent')
GAUGE_H1 = Gauge('weather_humid_1', 'Humidity, percent')

# Start up the server to expose the metrics.
start_http_server(8000)

# 
# Generate some requests.
while True:
  try:
    ws = WeatherStation(MAC_ADDR)
    if ws.monitorWeatherStation() is not None:
      ws.disconnect()
      data = []
      data.append(ws.getIndoorTemp())
      data.append(ws.getOutdoorTemp())
      data.append(ws.getHumidity0())
      data.append(ws.getHumidity1())
      for item in data:
        if item == None:
          raise Exception('None value detected, skipping gague update ...')
     
      print("Setting gauges")
      GAUGE_T0.set(ws.getIndoorTemp())
      GAUGE_T1.set(ws.getOutdoorTemp())
      GAUGE_H0.set(ws.getHumidity0())
      GAUGE_H1.set(ws.getHumidity1())
  except Exception as err:
    print(err)
    
  # Sleep before next cycle
  time.sleep(90)
