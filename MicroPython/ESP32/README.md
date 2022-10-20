# MicroPython on the Lolin/Wemos S2 Mini

MicroPython on the S2 Mini is a bit different from CircuitPython.
The main difference is that this port does not offer the convenience of a flash drive.
These examples were tested with MicroPython 1.19.1.

## Download MicroPython for the S2 Mini

[This page](https://micropython.org/download/LOLIN_S2_MINI/) contains the download and installation instructions.
When your S2 Mini came with a UF2 boot loader, you might use the UF2 images.
For a list of all supported devices, visit the [download overview](https://micropython.org/download/).
However, when the board already has been used with CircuitPython you might want to erase and do a full flash.

The `esptool.py` used for erasing and flashing can be installed with the command `pip3 install esptool`.

## Access the board

The 12-14 year old kids I teach Python on MicroControllers love full IDEs like [Mu Editor](https://codewith.mu/en/download) or [uPyCraft](https://github.com/DFRobot/uPyCraft).
You might give them a try.

However I do not like them, I rather prefer [rshell](https://github.com/dhylands/rshell).
It can be installed using `pip3 install rshell`.
This offers a FTP like interface for uploading and downloading files on the MicroPython device.
The Microcontroller board defaults to the "Mountpoint" `/pyboard`.
This can be changed, see the rshell documentation on GitHub.

### Listing all files

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM2 ls /pyboard
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Oct 20, 2022 08:23:03
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
boot.py    main.py    secrets.py
```

### Show the content of a file

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM2 cat /pyboard/secrets.py
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Oct 20, 2022 08:46:09
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
secrets = {
    'ssid' : 'your_ssid',
    'wpapsk' : 'T0p_S3cr37_PSK'
}
```

### Upload a file

```
mattias@barium:/tmp$ rshell -p /dev/ttyACM2 cp /home/mattias/main.py /pyboard/main.py
Using buffer-size of 32
Connecting to /dev/ttyACM2 (buffer-size 32)...
Trying to connect to REPL  connected
Retrieving sysname ... esp32
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /boot.py/ /main.py/ /secrets.py/
Setting time ... Oct 20, 2022 08:49:00
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
Copying '/home/mattias/main.py' to '/pyboard/main.py' ...
```

