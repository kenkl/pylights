#!/usr/bin/env python3
# A little ditty to simulate sunrise over time using Hue lights

from lightkit import *

# How many minutes should the "sunrise" take? 
minutes = 7
sleepInterval = (minutes * 60) / 254

# see lightlist.py for unit number(s)
#units = [21, 38]
#units = [16, 30, 31, 32, 33]
units = [16, 30, 31, 32, 33, 22, 23, 24, 25]

def doThing(lights, brightness):
    for light in lights:
        setlevel(light, brightness)
        
# First, turn the lights on, set the colour-temperature, and initial brightness...
for light in units:
    oneon(light)
    #setct(light, 400)  # "standard" warm-white colour-temperature
    setct(light, 330)  # "standard" cool-white colour-temperature
    setlevel(light, 0)

# ...and then bring them up.
for i in range(0, 255):
    doThing(units, i)
    sleep(sleepInterval)


    
