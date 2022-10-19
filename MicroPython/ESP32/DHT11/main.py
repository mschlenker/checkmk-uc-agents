#!/usr/bin/python3
# encoding: utf-8
# Shebang and encoding just for the editor
#
# Copyright (C) 2022 Mattias Schlenker for tribe29 GmbH
# License: GNU General Public License v2

import network
import socket
import machine
import dht
import time
from secrets import secrets

TIMEOUT = None
PORT = 6556
# thresholds for temperature and humidity
tsteps = [ 13, 17, 22, 26 ]
hsteps = [ 30, 40, 65, 75 ]

# Prepare a minimal static agent output:
output = """<<<check_mk_agent>>>
AgentOS: MicroPython
<<<cmk_dht_plugin>>>
temp %d
humidity %d
<<<local>>>
0 "Dummy MicroPython" - This is OK.
"""

# Initialize the board LED to show activity
led = machine.Pin(15, machine.Pin.OUT)

# Initialize the DHT sensor, measure once
d = dht.DHT11(machine.Pin(16))
d.measure

# Initialize the WiFi interface in station mode
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan() # Scan for available access points
print("Trying to connect to: " + secrets["ssid"])
sta_if.connect(secrets["ssid"], secrets["wpapsk"])
sta_if.isconnected()
print("My IP is " + sta_if.ifconfig()[0])

# Start a listening server on the Checkmk agent port:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', PORT))
s.listen(2)

while True:
    # On connect, print the IP address:
    conn, addr = s.accept()
    led.on()
    print("Request from " + str(addr[0]) + ", port " + str(addr[1]))
    conn.settimeout(TIMEOUT)
    d.measure()
    temp = d.temperature()
    humidity = d.humidity()
    print("Temperature: " + str(temp) + "°C")
    print("Humidity: " + str(humidity) + "%")
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
    led.off()
