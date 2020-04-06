#!/usr/bin/env python3
# Connect to Oregon Scientific BLE Weather Station
# https://www.instructables.com/id/Connect-Raspberry-Pi-to-Oregon-Scientific-BLE-Weat/
# License: Released under an MIT license: http://opensource.org/licenses/MIT
import sys
import logging
import time
from bluepy.btle import *

# uncomment the following line to get debug information
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)

WEATHERSTATION_NAME = "IDTW218H" # IDTW213R for RAR218HG

class WeatherStation:
  def __init__(self, mac):
    self._data = {}
    try:
      self.p = Peripheral(mac, ADDR_TYPE_RANDOM)
      self.p.setDelegate(NotificationDelegate())
      logging.debug('WeatherStation connected !')
    except BTLEException:
      self.p = 0
      logging.debug('Connection to WeatherStation failed !')
      raise
      
  def _enableNotification(self):
    try:
      # Enable all notification or indication
      self.p.writeCharacteristic(0x000c, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x000f, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x0012, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x0015, bytearray(b'\x01\x00'))
      self.p.writeCharacteristic(0x0018, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x001b, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x001e, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x0021, bytearray(b'\x02\x00'))
      self.p.writeCharacteristic(0x0032, bytearray(b'\x01\x00'))
      logging.debug('Notifications enabled')
    
    except Exception as err:
      logging.debug(err)
      self.p.disconnect()
  
  def monitorWeatherStation(self):
    try:
      # Enable notification
      self._enableNotification()
      # Wait for notifications
      while self.p.waitForNotifications(2.0):
        # handleNotification() was called
        continue
      logging.debug('Notification timeout')
    except:
      return None
    
    regs = self.p.delegate.getData()
    if regs is not None:
      # expand INDOOR_AND_CH1_TO_3_TH_DATA_TYPE0
      self._data['index0_temperature'] = regs['data_type0'][4:6]   + regs['data_type0'][2:4]
      self._data['index1_temperature'] = regs['data_type0'][8:10]  + regs['data_type0'][6:8]
      self._data['index2_temperature'] = regs['data_type0'][12:14] + regs['data_type0'][10:12]
      self._data['index3_temperature'] = regs['data_type0'][16:18] + regs['data_type0'][14:16]
      self._data['index0_humidity'] = regs['data_type0'][18:20]
      self._data['index1_humidity'] = regs['data_type0'][20:22]
      self._data['index2_humidity'] = regs['data_type0'][22:24]
      self._data['index3_humidity'] = regs['data_type0'][24:26]
      self._data['temperature_trend'] = regs['data_type0'][26:28]
      self._data['humidity_trend'] = regs['data_type0'][28:30]
      self._data['index0_humidity_max'] = regs['data_type0'][30:32]
      self._data['index0_humidity_min'] = regs['data_type0'][32:34]
      self._data['index1_humidity_max'] = regs['data_type0'][34:36]
      self._data['index1_humidity_min'] = regs['data_type0'][36:38]
      self._data['index2_humidity_max'] = regs['data_type0'][38:40]
      # expand INDOOR_AND_CH1_TO_3_TH_DATA_TYPE1
      #self._data['index2_humidity_min'] = regs['data_type1'][2:4]
      #self._data['index3_humidity_max'] = regs['data_type1'][4:6]
      #self._data['index3_humidity_min'] = regs['data_type1'][6:8]
      #self._data['index0_temperature_max'] = b''.join(regs['data_type1'][10:12] + regs['data_type1'][8:10])
      #self._data['index0_temperature_min'] = b''.join(regs['data_type1'][14:16] + regs['data_type1'][12:14])
      #self._data['index1_temperature_max'] = b''.join(regs['data_type1'][18:20] + regs['data_type1'][16:18])
      #self._data['index1_temperature_min'] = b''.join(regs['data_type1'][22:24] + regs['data_type1'][20:22])
      #self._data['index2_temperature_max'] = b''.join(regs['data_type1'][26:28] + regs['data_type1'][24:26])
      #self._data['index2_temperature_min'] = b''.join(regs['data_type1'][30:32] + regs['data_type1'][28:30])
      #self._data['index3_temperature_max'] = b''.join(regs['data_type1'][34:36] + regs['data_type1'][32:34])
      #self._data['index3_temperature_min'] = b''.join(regs['data_type1'][38:40] + regs['data_type1'][36:38])
      return True
    else:
      return None
      
  def getValue(self, indexstr):
    val = int(self._data[indexstr], 16)
    if val >= 0x8000:
      val = ((val + 0x8000) & 0xFFFF) - 0x8000
    return val
  
  def getIndoorTemp(self):
    if 'index0_temperature' in self._data:
      temp = self.getValue('index0_temperature') / 10.0
      max = 0 #self.getValue('index0_temperature_max') / 10.0
      min = 0 #self.getValue('index0_temperature_min') / 10.0
      logging.debug('Indoor temp : %.1f°C, max : %.1f°C, min : %.1f°C', temp, max, min)
      return temp
    else:
      return None
  
  def getOutdoorTemp(self):
    if 'index1_temperature' in self._data:
      temp = self.getValue('index1_temperature') / 10.0
      max = 0 #self.getValue('index1_temperature_max') / 10.0
      min = 0 #self.getValue('index1_temperature_min') / 10.0
      logging.debug('Outdoor temp : %.1f°C, max : %.1f°C, min : %.1f°C', temp, max, min)
      return temp
    else:
      return None
      
  def getHumidity0(self):
    if 'index0_humidity' in self._data:
      hum = self.getValue('index0_humidity')
      logging.debug('Humidity0: {}'.format(hum))
      return hum
    else:
      return None

  def getHumidity1(self):
    if 'index1_humidity' in self._data:
      hum = self.getValue('index1_humidity')
      logging.debug('Humidity1: {}'.format(hum))
      return hum
    else:
      return None

  def disconnect(self):
    self.p.disconnect()
    
class NotificationDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)
    self._indoorAndOutdoorTemp_type0 = None
    self._indoorAndOutdoorTemp_type1 = None
    
  def handleNotification(self, cHandle, data):
    formatedData = binascii.b2a_hex(data)
    if cHandle == 0x0017:
      # indoorAndOutdoorTemp indication received
      #FIXME
      if str(formatedData)[2] == '8':
        # Type1 data packet received
        self._indoorAndOutdoorTemp_type1 = formatedData
        logging.debug('indoorAndOutdoorTemp_type1 = %s', formatedData)
      else:
        # Type0 data packet received
        self._indoorAndOutdoorTemp_type0 = formatedData
        logging.debug('indoorAndOutdoorTemp_type0 = %s', formatedData)
    else:
      # skip other indications/notifications
      logging.debug('handle %x = %s', cHandle, formatedData)
  
  def getData(self):
      if self._indoorAndOutdoorTemp_type0 is not None:
        # return sensors data
        return {'data_type0':self._indoorAndOutdoorTemp_type0, 'data_type1':self._indoorAndOutdoorTemp_type1}
      else:
        return None

class ScanDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)
    
  def handleDiscovery(self, dev, isNewDev, isNewData):
    global weatherStationMacAddr
    if dev.getValueText(9) == WEATHERSTATION_NAME:
      # Weather Station in range, saving Mac address for future connection
      logging.debug('WeatherStation found')
      weatherStationMacAddr = dev.addr


#if __name__=="__main__":
#
#  weatherStationMacAddr = None
#  
#  if len(sys.argv) < 2:
#    # No MAC address passed as argument
#    try:
#      # Scanning to see if Weather Station in range
#      scanner = Scanner().withDelegate(ScanDelegate())
#      devices = scanner.scan(2.0)
#    except Exception as err:
#      print(err)
#      print('Scanning required root privilege, so do not forget to run the script with sudo.')
#  else:
#    # Weather Station MAC address passed as argument, will attempt to connect with this address
#    weatherStationMacAddr = sys.argv[1]
#  
#  if weatherStationMacAddr is None:
#    logging.debug('No WeatherStation in range !')
#  else:
#weatherStationMacAddr="C4:43:38:A7:90:34"
#try:
#  # Attempting to connect to device with MAC address "weatherStationMacAddr"
#  weatherStation = WeatherStation(weatherStationMacAddr)
#  
#  if weatherStation.monitorWeatherStation() is not None:
#    # WeatherStation data received
#    indoor = weatherStation.getIndoorTemp()
#    outdoor = weatherStation.getOutdoorTemp()
#  else:
#    logging.debug('No data received from WeatherStation')
#  
#  weatherStation.disconnect()
#
#except KeyboardInterrupt:
#  logging.debug('Program stopped by user')
#

