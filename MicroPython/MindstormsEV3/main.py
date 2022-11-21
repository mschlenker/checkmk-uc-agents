#!/usr/bin/env pybricks-micropython
#
# This script uses the ultrasonic sensor of the EV3 to create an agent that
# monitors coffee levels using a local check. The thresholds are hardcoded:
#
# Less than 150mm from the sensor: CRIT
# Less than 100mm from the sensor: WARN
 

from pybricks import ev3brick as brick
from pybricks.ev3devices import UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import print, wait, StopWatch

# import network
import socket
import time

TIMEOUT = 300
PORT = 6556

# Prepare a minimal static agent output:
output = """<<<check_mk_agent>>>
AgentOS: MindstormsEV3
<<<local>>>
0 "Dummy MicroPython" - This is OK.
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', PORT))
s.listen(2)

brick.display.clear()
u = UltrasonicSensor(Port.S1)
while True:
  conn, addr = s.accept()
  conn.settimeout(TIMEOUT)
  brick.display.clear()
  d = u.distance()
  print("Distance: ", d)
  brick.display.text(str(d), (20,20)) 
  if d > 150:
    o = output + "2 \"EV3 coffee\" level=%d Level is critically low!\n" % d
  elif d > 100:
    o = output + "1 \"EV3 coffee\" level=%d Level is low.\n" % d
  else:
    o = output + "0 \"EV3 coffee\" level=%d Level is good.\n" % d
  conn.send(o)
  conn.close()
  wait(100)

