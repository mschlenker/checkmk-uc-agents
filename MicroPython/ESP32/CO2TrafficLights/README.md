# A Checkmk compatible CO2 traffic light

This small project aims to create a CO2 traffic lights based on ESP32.
The component choice was done in a way that it can be completely assembled on a 17x10 "third size" breadboard.
That design allows for easy translation to a 40x50mm² "perma proto" PCB board.

Since Checkmk is a Python company is was important to use a Python compatible platform.
Feel free to streamline ... blah 

## Components used

It is inspired by Watterott CO2 Ampel, but uses different components:

* ESP32 of course as µC – ESP8266 might work (but requires changing I²C wiring)
* 128x32px² I²C SSD1306 OLED display 
* SGP30 TVOC eCO2 air quality sensor
* BME280/BMP280/BMP180 air pressure, temperature (and maybe humidity) sensor
* Two (or more WS2812B or compatible design) LEDs

## Libraries used

* SGP30 https://github.com/mschlenker/micropython-sgp30
* BME280 https://github.com/robert-hh/BME280
* SSD1306 https://github.com/stlehmann/micropython-ssd1306
* Neopixel is included in Micropython base libraries

## Schematics

Wiring was done with with having in mind to be easily read.
Thus ESP32 was chosen despite being a bit more expensive that ESP8266.
With ESP32 the hardware I²C can be routed to arbitary GPIOs which makes wiring easier.
Keep this in mind when adjsusting for ESP8266.




