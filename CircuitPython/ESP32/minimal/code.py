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
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

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
    led.value = True
    print("Request from " + str(addr[0]) + ", port " + str(addr[1]))
    conn.settimeout(TIMEOUT)
    conn.send(output)
    print("Served request, closing...")
    conn.close()
    led.value = False
