#!/usr/bin/env python3

# Collecting groupings of lights into scenes/macros to abstract activities from client scripts

from lightkit import *

# Home Office (HO) scenes
def hoalloff():
    units = [3, 19, 18, 21, 37, 38]
    for light in units:
        oneoff(light)

def hofull():
    units = [3, 19, 18, 21, 37, 38]
    on(units)
    setcts(units, CTWARM)
    setlevels(units, bri=254)

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

def howltog():
    toggle(37)

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

def hosp2(force=False):
    units = [3, 19, 21, 38]
    if ison(21) or force:
        on(units) # Assuming that the key is off, but we got here by force
        off([18, 37])
        setsp2(units)

# Living Room (LR) scenes
def lroff():
    units = [11, 12, 13, 14, 15, 17, 20, 35, 28, 29, 39]
    off(units)
    lrdl(onstate=False)

def lrtvbloff(): # If we're streaming to the TV backlights, this will be NOOP
    units = [28, 29, 39]
    off(units)

def lrnormal(fulldl=False):
    units = [11, 12, 13, 14, 15, 17, 20]
    on(units)
    setlevels(units)
    for light in units:
        sethue(light)
    # The edison bulb is a special case.
    on(35)
    setlevel(35, 73)
    # In Lights, we do a conditional - if we're already on, toggle the brightness of the DLs. I kinda like that, so...
    keylight = getstate(25)  # let's key off the far corner DL...
    if not keylight['on']:
        if fulldl:
            lrdl(onstate=True, bri=254, ct=CTWARM)
        else:
            lrdl(onstate=True, bri=127, ct=CTWARM)
    elif keylight['bri'] == 254:
        lrdl(onstate=True, bri=127, ct=CTWARM)
    elif keylight['bri'] == 127:
        lrdl(onstate=True, bri=254, ct=CTWARM)
    else: # The key is on, but at an uncaught bri level.
        lrdl(onstate=True, bri=127, ct=CTWARM)

def lrteevee():
    lrtvbloff()
    units = [11, 12, 13, 14, 15, 17, 20]
    on(units)
    setlevels(units, bri=154)
    sethues(units, hue=8402, sat=143)
    # The edison bulb is a special case.
    on(35)
    setlevel(35, 1)
    lrdl(onstate=True, bri=1, ct=CTWARM)
    if ison(9): # If the bedroom is on, bring it down
        brmin()

def lrcinema():
    lrtvbloff()
    units = [11, 12, 13, 14, 15, 17, 20]
    on(units)
    setlevels(units, bri=39)
    sethues(units, hue=8402, sat=140)
    # The edison bulb is a special case.
    off(35)
    lrdl(onstate=False)
    if ison(9): # If the bedroom is on, bring it down
        brmin()

def lrsp2(force=False):
    units = [11, 12, 13, 14, 15, 28, 29, 39]
    if ison(14) or force: # keyed on one of the bulbs in the big dragonfly floor lamp
        on(units) # assuming that the key is off, but we got here by force
        setsp2(units)
        setlevels([28, 29, 39], 16) # TV backlights should not be so bright
        off([17, 20, 35]) # Candleboxes and Edison bulb are off now
        lrdl(False)
        brsp2()
        hosp2() # If I'm playing vidja games in my studio, trigger this one too.

# Bedroom (BR) scenes
def broff():
    units = [5, 9, 16, 36]
    off(units)
    brdl(onstate=False)

def brfull():
    units = [5, 9, 16, 36]
    on(units)
    setlevels(units)
    sethues(units)
    brdl(onstate=True, bri=254, ct=CTWARM)

def brhalf():
    units = [5, 9, 16, 36]
    on(units)
    setlevels(units, bri=127)
    sethues(units)
    brdl(onstate=True, bri=127, ct=CTWARM)

def brmin():
    units = [5, 9, 16]
    off(units)
    on(36)
    sethue(36, s=199)
    setlevel(36,38)
    brdl(onstate=True, bri=1, ct=CTWARM)

def brsp2(force=False):
    units = [5, 9, 36]
    if ison(16) or force: # keyed on the bedside table light
        on(16) # the key is off, but we got here by force
        off(units)
        setsp2(16, 16)
        brdl(False)

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