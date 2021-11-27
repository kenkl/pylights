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
    units = [11, 12, 13, 14, 15, 17, 20, 28, 29, 39]
    off(units)
    lrdl(onstate=False)

def lrtvbloff(): # If we're streaming to the TV backlights, this will be NOOP
    units = [28, 29, 39]
    off(units)

def lrnormal(fulldl=False):
    lrtvbloff()
    units = [11, 12, 13, 14, 15, 17, 20]
    on(units)
    setlevels(units)
    for light in units:
        sethue(light)
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
    lrdl(onstate=False)
    if ison(9): # If the bedroom is on, bring it down
        brmin()

def lrsp2(force=False):
    units = [11, 12, 13, 14, 15, 28, 29, 39]
    if ison(14) or force: # keyed on one of the bulbs in the big dragonfly floor lamp
        on(units) # assuming that the key is off, but we got here by force
        setsp2(units)
        setlevels([28, 29, 39], 16) # TV backlights should not be so bright
        off([17, 20]) # Candleboxes are off now
        lrdl(False)
        brsp2()
        hosp2() # If I'm playing vidja games in my studio, trigger this one too.

def lrcbon():
    '''An alternative to SP2 - candleboxes on, everything else off'''
    units = [11, 12, 13, 14, 15, 28, 29, 39]
    off(units)
    lrdl(onstate=False)
    on([17,20])

def lrteevee2():
    ''' Alternate TV mode with everything dimmed, but downlights still active '''
    lrdfoff() # Tall dragonfly lamp off
    on([17,20]) # candleboxes on
    lrdl(True, bri=1, ct=CTWARM) # bring the downlights up to a minimal state
    onwithbri([11,12],True,b=55) # table lamps on dimly

def lrdfoff():
    ''' just turn off the three lights in the tall dragonfly lamp. for reasons. '''
    off([13,14,15])

def lrdfon():
    ''' just turn on the three lights in the tall dragonfly lamp. for reasons. '''
    on([13,14,15])

def lrread():
    ''' Stateful toggle, to full brightness, the lights for reading (a book) '''
    units = [13,14,15,23]
    if not checkstate(23): # keyed on the downlight
        #no statefile found, so we're not in-progress...
        for light in units:
            savestate(light)
        onwithbri(units,True,b=255)
        for light in units:
            sethue(light) # force warm white for these
    else: #key's in progress, so restore the state...
        for light in units:
            restorestate(light)
            


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
    if ison(16) or ison(36) or force: # keyed on the bedside table light
        on(16) # the key is off, but we got here by force
        off(units)
        setsp2(16, 16)
        brdl(False)

def brread():
    '''Stateful toggle of the reading light'''
    unit = 5
    if checkstate(unit): 
        # statefile exists, so let's roll it back...
        restorestate(unit)
    else:
        # statefile doesn't exist. let's create one for a toggle and turn it on...
        savestate(unit)
        onwithbri(unit,on,b=254)
        sethue(unit) # force warm white for colour

# Kitchen (K) scenes
def kcstog():
    '''Kitchen Coffee Shop scene'''
    units = [4, 6, 7, 8, 27, 34, 41]
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
    units = [4, 26, 27, 34, 41]
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

def espresso(state=False):
    '''Turn the espresso machine on/off'''
    # Default to turning it off. Y'know, for safety's sake.
    em = 40 # The Espresso Machine's Hue ID presence
    on(em, state)
    onwithbri(35, state, 96) # The worklight follows the machine
    on(41) # Coffee station fairy lights
    
def goodmorning():
    '''Turn on ALL the lights in the house'''
    # "Good morning, houseplants. Yes, it's wake-up time."
    # The PHP version in Lights works really well. Let's ape that, with order and everything. First, all the table lamps and such, and THEN the downlights.
    
    # Living room:
    units = [11,12,13,14,15]
    on(units)
    sethues(units)
    setlevels(units)
    on([17,20]) # The candlebox lamps

    #Bedroom
    units = [5,16,36]
    on(units)
    sethues(units)
    setlevels(units, 127)
    on(9)
    
    # Everything else, including downlights and dangling statefiles
    hueaccent(True)
    onwithbri(35, True, 96) # Coffee station worklight
    on(41) # Kitchen fairy lights (coffee station)
    alldl()
    clearallstates()
    
def fakesun():
    '''Simulated sunrise'''
    # How many minutes should the "sunrise" take? 
    minutes = 7
    sleepInterval = (minutes * 60) / 254
    sleepInterval *= 0.77  # Allow for some overhead in the network processing of these calls
    units = [16, 30, 31, 32, 33, 22, 23, 24, 25]

    # Get everyone turned on, at minimal brighness to start...
    onwithbri(units, True, b=0)
    #setlevels(units=units, bri=0)
    setcts(units, CTCOOL)
    # then, step (slowly) through them all to bring them up
    for level in range(0, 255):
        setlevels(units, level)
        sleep(sleepInterval)

# Other (O) (test) scenes


if __name__ == "__main__":
    print("A collection of scenes/macros to be used from calling scripts. To use:")
    print("from scenes import *")
