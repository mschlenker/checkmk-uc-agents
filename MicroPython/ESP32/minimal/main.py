#!/usr/bin/python3
# encoding: utf-8
# Shebang and encoding just for the editor
#
# Copyright (C) 2022 Mattias Schlenker for tribe29 GmbH
# License: GNU General Public License v2

import network
import socket
import machine
import time
from secrets import secrets

TIMEOUT = None
PORT = 6556

# Prepare a minimal static agent output:
output = """<<<check_mk_agent>>>
AgentOS: MicroPython
<<<local>>>
0 "Dummy MicroPython" - This is OK.
"""

# Initialize the board LED to show activity
led = machine.Pin(15, machine.Pin.OUT)

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
    conn.send(output)
    print("Served request, closing...")
    conn.close()
    led.off()
