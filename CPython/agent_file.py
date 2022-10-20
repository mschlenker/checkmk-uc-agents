#!/usr/bin/python3
# encoding: utf-8
#
# Copyright (C) 2022 Mattias Schlenker for tribe29 GmbH
# License: GNU General Public License v2
#
# A minimal agent implemented using regular Python 3 
# serving the content of a text file (as in spool directory only).
#
# Replace everything starting from "file = open()" to "file.close()"
# with your code to create monitoring data.

import socket
import sys

PORT = 6556

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', PORT)
print('Starting Checkmk Python agent on %s port %s...' % server_address)
sock.bind(server_address)
sock.listen(1)

while True:
    print('Waiting for Checkmk site to connect...')
    connection, client_address = sock.accept()
    try:
        print('Connection from ', client_address)
        file = open('dummy.txt', 'r')
        while True:
            line = file.readline()
            if not line:
                break
            connection.sendall(line.encode())
        file.close()
        connection.close()
    finally:
        print("Done!")
