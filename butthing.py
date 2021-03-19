#!/usr/bin/env python3

from gpiozero import LED
from gpiozero import Button
from signal import pause
from scenes import *

led1 = LED(16)
but1 = Button(26)
but2 = Button(21)
but3 = Button(20)

def dosomething(thing):
    led1.on()
    fullurl = baseurl+thing
    wr = urllib.request.urlopen(fullurl)
    led1.off()

def dobut1():
    led1.on()
    honormal()
    led1.off()

def dobut2():
    led1.on()
    howltog()
    led1.off()

def dobut3():
    led1.on()
    hoalloff()
    led1.off()

if __name__ == '__main__':
    # Let's blink the led a few times to signal that we're ready to go.
    for _ in range(0,3):
        led1.on()
        sleep(0.3)
        led1.off()
        sleep(0.3)

    but1.when_pressed = dobut1
    but2.when_pressed = dobut2
    but3.when_pressed = dobut3
    pause()

