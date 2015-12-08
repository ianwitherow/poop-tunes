PoopTunes
=========

![Screenshot](http://i.imgur.com/hDNlauN.gif)

What is it?
-----------
Is your bathroom at work too quiet? It's weird, right? **PoopTunes** solves that age-old problem by playing some music when the lights turn on.

How do I use it?
----------------
* Grab a photoresistor. I found mine on [Amazon](http://www.amazon.com/Sensitive-Resistor-Photoresistor-Optoresistor-GM5539/dp/B00AQVYWA2), but they're also on [SparkFun](https://www.sparkfun.com/products/9088) or probably lots of other places.
* Wire it up - I used this site as a guide: [https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading](https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading)
* Make sure you have [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) installed
* Install either MPG123 or MPG321. The script uses MPG123, so if you're using the other one then you'll have to get in there and change it.
* Clone this repo somewhere and throw some songs in the music/ folder. PoopTunes shuffles through them.
* (Optional) Check the readings for the light levels.
  * Run the script with the --lighting flag, or -l. This will give you the light reading - find a number between the lowest and highest for the 'threshold'. This is the cutoff where the program decides if the light is on or off. For example, if you turn off the light and the reading is at 4000, then you turn on the light and it's at 200, pick somewhere inbetween like 500 or 1000.
* Run the script with `python poop-tunes.py --threshold [number]`
  * Threshold is optional (default is 2000). Use this if it's not accurately detecting whether the light is on or off.

Dependencies
------------
* Python 2.x
* RPi.GPIO
* mpg123 or mpg321 (script uses 123, so if you use 321 you'll have to change that)

