#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

import time
import pycom
from pysense import Pysense
import machine

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

########
from network import LoRa
import socket
import binascii
import struct
import time
import config
########
########
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26041C52'))[0]
nwk_swkey = binascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
app_swkey = binascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
for i in range(3, 16):
    lora.remove_channel(i)

lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)
s.setblocking(False)
#######################
pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pysense()

mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
print("MPL3115A2 temperature: " + str(mp.temperature()))
print("Altitude: " + str(mp.altitude()))
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("Pressure: " + str(mpp.pressure()))


si = SI7006A20(py)
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")
#s.send(str(si.temperature())+str(si.humidity())+"-")

lt = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

li = LIS2HH12(py)
#print("Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))
print("Acceleration: " + str(li.acceleration()))
s.send(str(si.temperature())+"|"+str(si.humidity())+"|"+str(li.acceleration())+"|"+str(mpp.pressure())+"|"+str(mp.altitude()))
#print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
#print("Pitch: " + str(li.yaw()))


print("Battery voltage: " + str(py.read_battery_voltage()))

time.sleep(3)
py.setup_sleep(10)
py.go_to_sleep()
