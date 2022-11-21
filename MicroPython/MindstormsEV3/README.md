# MicroPython on the LEGO Mindstorms EV3

MicroPython for EV3 is actually a bootable EV3DEV based Linux image that also includes the MicroPython interpreter.

## Download MicroPython for the S2 Mini

The card image is distributed as Zip file, unpack it and use `dd` to write it to a 4–32GB TF card. 
https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3

## Access the board

I suggest using WiFi with an adapter like Edimax EW-7811Un or similar adapters (most N150 that are advertised as Raspberry Pi compatible will do.
You can then SSH to the brick (user: robot, pass: maker) and use `vim.basic` to edit files directly on the board.
