#!/usr/bin/python3
# encoding: utf-8
# Shebang and encoding just for the editor
#
# Copyright (C) 2022 Mattias Schlenker for tribe29 GmbH
# License: GNU General Public License v2

import wifi
import socketpool
import board
import digitalio
import time
import adafruit_dht
from secrets import secrets

TIMEOUT = None
PORT = 6556
# thresholds for temperature and humidity
tsteps = [ 13, 17, 22, 26 ]
hsteps = [ 30, 40, 65, 75 ]

# Prepare a minimal static agent output:
output = """<<<check_mk_agent>>>
AgentOS: CircuitPython
<<<cmk_dht_plugin>>>
temp %d
humidity %d
<<<local>>>
0 "Dummy CircuitPython" - This is OK.
"""

# Initialize the board LED to show activity
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Initialize the DHT sensor
dht = adafruit_dht.DHT11(board.IO16)
dht.temperature

# Initialize the WiFi interface in station mode
print("Trying to connect to: " + secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["wpapsk"])
print("My IP is " + str(wifi.radio.ipv4_address))

# Start a listening server on the Checkmk agent port:
pool = socketpool.SocketPool(wifi.radio)
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
s.settimeout(TIMEOUT)
s.bind(('0.0.0.0', PORT))
s.listen(2)

while True:
    # On connect, print the IP address:
    conn, addr = s.accept()
    temp = dht.temperature
    humidity = dht.humidity
    led.value = True
    print("Request from " + str(addr[0]) + ", port " + str(addr[1]))
    conn.settimeout(TIMEOUT)
    conn.send(output % (temp, humidity))
    # Create a local check for temperature
    if temp < tsteps[0]:
        conn.send("2 \"DHT temperature\" temperature=%d Temperature is critical low.\n" % temp)
    elif temp < tsteps[1]:
        conn.send("1 \"DHT temperature\" temperature=%d Temperature is low.\n" % temp)
    elif temp > tsteps[3]:
        conn.send("2 \"DHT temperature\" temperature=%d Temperature is critical high.\n" % temp)
    elif temp > tsteps[2]:
        conn.send("1 \"DHT temperature\" temperature=%d Temperature is high.\n" % temp)
    else:
        conn.send("0 \"DHT temperature\" humidity=%d Temperature is OK.\n" % temp)
    # Create a local check for humidity
    if humidity < hsteps[0]:
        conn.send("2 \"DHT humidity\" humidity=%d Humidity is critical low.\n" % humidity)
    elif humidity < hsteps[1]:
        conn.send("1 \"DHT humidity\" humidity=%d Humidity is low.\n" % humidity)
    elif humidity > hsteps[3]:
        conn.send("2 \"DHT humidity\" humidity=%d Humidity is critical high.\n" % humidity)
    elif humidity > hsteps[2]:
        conn.send("1 \"DHT humidity\" humidity=%d Humidity is high.\n" % humidity)
    else:
        conn.send("0 \"DHT humidity\" humidity=%d Humidity is OK.\n" % humidity)
    print("Served request, closing...")
    conn.close()
    led.value = False
