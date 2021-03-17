#!/usr/bin/env python3

# Collecting groupings of lights into scenes/macros to abstract activities from client scripts

from lightkit import *

# Home Office (HO) scenes
def honormal():
    # Monitor backlights
    mbl = [3, 19]
    for l in mbl:
        oneon(l)
        setct(l, CTWARM)
        setlevel(l, 128)
    # Dragonfly Lamp
    oneon(18)
    # Swing arm
    sal = 21
    oneon(sal)
    setct(sal, CTWARM)
    setlevel(sal)
    # Floor lamp
    fl = 38
    oneon(fl)
    setct(fl, CTWARM)
    setlevel(fl)
    # Worklight
    oneoff(37)

def hoalloff():
    units = [3, 19, 18, 21, 37, 38]
    for light in units:
        oneoff(light)

def howltog():
    howl = 37
    toggle(howl)
    """
    if ison(howl):
        oneoff(howl)
    else:
        oneon(howl)
    """

def hohalf(bri=128):
    units = [3, 19, 21, 38]
    for light in units:
        oneon(light)
        setct(light, CTWARM)
        setlevel(light, bri)
    oneoff(37) # worklight

def hoh1():
    hohalf()
    oneon(18)

def hoh2():
    hohalf()
    oneoff(18)

def hogame():
    units = [3, 19, 21, 38]
    uoff = [18, 37]
    for light in uoff:
        oneoff(light)
    for light in units:
        oneon(light)
        sethue(light, 5262, 201)

def homin47():
    oneoff(18)
    hohalf(47)

def homin1():
    oneoff(18)
    hohalf(1)

# Living Room (LR) scenes


# Kitchen (K) scenes
def kcstog():
    '''Kitchen Coffee Shop scene'''
    units = [4, 6, 7, 8, 27, 34]
    if not checkstate(8): # keyed off the downlight at the far end; if it's in-progress, they all are
        # no statefile found. first, save states
        for light in units:
            savestate(light)
        # ...and then set the scene
        on(units)
        """
        for light in units:
            oneon(light)
            """
        sethue(4, 7676, 199)
        setlevel(4, 38)
        for dl in [6, 7, 8]:
            setct(dl, 400)
        setlevel(6, 127)
        setlevel(7, 254)
        setlevel(8, 127)
        setlevel(34, 38)
    else:
        # statefile found, let's restore the previous state
        for light in units:
            restorestate(light)
       

# Global (GL) scenes
# allalloff() already exists in lightkit, FYI
def hueaccent(on=True):
    '''Turn on/off the accent lights in the LR and Kitchen'''
    units = [4, 26, 27, 34]
    if on:
        for light in units:
            oneon(light)
        sethue(4, 7676, 199)
        setlevel(4, 38)
        setlevel(34, 38)
    else:
        for light in units:
            oneoff(light)

def dl(units, onstate=True, bri=254, ct=CTCOOL):
    '''Generic downlight(s) on/off, brightness, CT'''
    if isinstance(units, list):
        on(units, onstate)
        setlevels(units, bri)
        setcts(units, ct)
    elif isinstance(units, int):
        on(units, onstate)
        setlevel(units, bri)
        setct(units, ct)

def kdl(onstate=True, bri=254, ct=CTCOOL):
    '''Kitchen downlights on/off, brightness, CT'''
    units = [6, 7, 8]
    dl(units, onstate, bri, ct)

def lrdl(onstate=True, bri=254, ct=CTCOOL):
    '''Living room downlights on/off, brightness, CT'''
    units = [22, 23, 24, 25]
    dl(units, onstate, bri, ct)

def brdl(onstate=True, bri=254, ct=CTCOOL):
    '''Living room downlights on/off, brightness, CT'''
    units = [30, 31, 32, 33]
    dl(units, onstate, bri, ct)

def alldl(onstate=True, bri=254, ct=CTCOOL):
    kdl(onstate, bri, ct)
    lrdl(onstate, bri, ct)
    brdl(onstate, bri, ct)


def rnl(on=True):
    '''Random Night Light on/off'''
    rnl = 10
    if on:
        oneon(rnl)
        setlevel(rnl, 1)
        sethue(rnl, 0, 254)
    else:
        oneoff(rnl)


    

# Other (O) (test) scenes


if __name__ == "__main__":
    print("A collection of scenes/macros to be used from calling scripts. To use:")
    print("from scenes import *")
