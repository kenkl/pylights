#!/usr/bin/env python3

# Collecting groupings of lights into scenes/macros to abstract activities from client scripts

from lightkit import *

# Home Office (HO) scenes
def hoalloff():
    units = [3, 19, 18, 21, 37, 38]
    for light in units:
        oneoff(light)
    hofl("false")

def hofull(ct=CTWARM):
    units = [3, 19, 18, 21, 37, 38]
    on(units)
    setcts(units, ct)
    setlevels(units, bri=254)
    hofl("true",1)

def honormal(ct=CTWARM):
    # Monitor backlights
    mbl = [3, 19]
    for l in mbl:
        oneon(l)
        setct(l, ct)
        setlevel(l, 128)
    # Dragonfly Lamp
    oneon(18)
    # Swing arm
    sal = 21
    oneon(sal)
    setct(sal, ct)
    setlevel(sal)
    # Floor lamp
    fl = 38
    oneon(fl)
    setct(fl, ct)
    setlevel(fl)
    # Worklight
    oneoff(37)
    # NeoPixel strands
    if ct == CTWARM:
        hofl("colour")
    else:
        hofl("true")

def howltog():
    wl = 37
    toggle(wl)
    returnstate = {"toggleon": ison(wl)}
    return returnstate


def hohalf(bri=128):
    units = [3, 19, 21, 38]
    for light in units:
        oneon(light)
        setct(light, CTWARM)
        setlevel(light, bri)
    oneoff(37) # worklight
    hofl("false")

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
    hofl("false")

def homin47():
    oneoff(18)
    hohalf(47)
    hofl("orange",0.05)

def homin1():
    oneoff(18)
    hohalf(1)
    hofl("false")

def hosp2(force=False):
    units = [3, 19, 21, 38]
    if ison(21) or force:
        on(units) # Assuming that the key is off, but we got here by force
        off([18, 37])
        setsp2(units)
        hofl("red",0.03)

def hofl(callstring, bri=0.5):
    '''call the PICOW-based fairy-lights in HO - no returns'''
    picows = [picow2, picow3, picow8]
    for picow in picows:
        try:
            r = requests.get(f"{picow}/led?on={callstring}&bri={bri}")
        except Exception as e:
            print(f"Failed talking to {picow} - {e}")

# Living Room (LR) scenes
def lroff():
    units = [11, 12, 13, 14, 15, 17, 20, 28, 29, 39]
    off(units)
    lrdl(onstate=False)
    lrfl("false")

def lrtvbloff(): # If we're streaming to the TV backlights, this will be NOOP
    units = [28, 29, 39]
    off(units)

def lrtvblon(): # an unconditional activation of the TV backlights. For reasons. 
    units = [28, 29, 39]
    on(units)
    setlevel(28, b=8)
    setlevel(29, b=8)
    setlevel(39, b=30)
    setcts(units, 430)

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
            lrfl('colour',bri=1)
        else:
            lrdl(onstate=True, bri=127, ct=CTWARM)
            lrfl('colour')
    elif keylight['bri'] == 254:
        lrdl(onstate=True, bri=127, ct=CTWARM)
        lrfl('colour')
    elif keylight['bri'] == 127:
        lrdl(onstate=True, bri=254, ct=CTWARM)
        lrfl('colour',bri=1)
    else: # The key is on, but at an uncaught bri level.
        lrdl(onstate=True, bri=127, ct=CTWARM)
        lrfl('colour')

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
    lrfl('colour',bri=0.02)

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
    lrfl('colour',bri=0.01)

def lrsp2(force=False):
    ''' SP2 - Sleep Protocol 2 - a visual reminder/encouragement to go to bed at a reasonable hour '''
    # 2021-11-30: revising the behaviour of SP2 after moving lights around the room 
    units = [11, 12, 13, 14, 15, 28, 29, 39] # this probably isn't needed now
    if ison(12) or force: # keyed on the end-table lamp
        on([28,29]) # the two lower backlights should always be on here.
        setsp2(units)
        setlevels([28, 29], 16) # TV backlights should not be so bright
        off(39) # The play light strip is still a bit bright, so...
        #off([17, 20]) # Candleboxes off
        lrdl(False)
        # 2025-04-12: decouple brsp2() here.
        #brsp2()
        hosp2() # If I'm playing vidja games in my studio, trigger this one too.
        lrfl("red",0.03)

def lrcbon():
    '''An alternative to SP2 - candleboxes on, everything else off'''
    units = [11, 12, 13, 14, 15, 28, 29, 39]
    off(units)
    lrdl(onstate=False)
    on([17,20])
    lrfl('orange',bri=0.03)

def lrteevee2():
    ''' Alternate TV mode with everything dimmed, but downlights still active '''
    lrtvbloff()
    lrdfoff() # Tall dragonfly lamp off
    on([17,20]) # candleboxes on
    lrdl(True, bri=1, ct=CTWARM) # bring the downlights up to a minimal state
    onwithbri([11,12],True,b=55) # table lamps on dimly
    sethues([11,12], hue=8402, sat=143)
    lrfl('colour',bri=0.01)

def lrdfoff():
    ''' just turn off the three lights in the tall dragonfly lamp. for reasons. '''
    off([13,14,15])

def lrdfon():
    ''' just turn on the three lights in the tall dragonfly lamp. for reasons. '''
    on([13,14,15])

def lrread():
    ''' Stateful toggle, to full brightness, the lights for reading (a book) '''
    units = [13,14,15,23]
    state = False
    if not checkstate(23): # keyed on the downlight
        #no statefile found, so we're not in-progress...
        state = True
        for light in units:
            savestate(light)
        onwithbri(units,True,b=255)
        for light in units:
            sethue(light) # force warm white for these
    else: #key's in progress, so restore the state...
        for light in units:
            restorestate(light)
    returnstate = {"toggleon": state}
    return returnstate
            
def lrfl(callstring, bri=0.5):
    '''call the PICOW-based fairy-lights in LR - no returns'''
    picows = [picow6, picow7, picow9]
    for picow in picows:
        try:
            r = requests.get(f"{picow}/led?on={callstring}&bri={bri}")
        except Exception as e:
            print(f"Failed talking to {picow} - {e}")


# Bedroom (BR) scenes
def broff():
    units = [5, 9, 16, 36]
    off(units)
    brdl(onstate=False)
    brfl("false")

def brfull():
    units = [5, 9, 16, 36]
    on(units)
    setlevels(units)
    sethues(units)
    brdl(onstate=True, bri=254, ct=CTWARM)
    brfl("true", 1)

def brhalf():
    units = [5, 9, 16, 36]
    on(units)
    setlevels(units, bri=127)
    sethues(units)
    brdl(onstate=True, bri=127, ct=CTWARM)
    brfl("colour")

def brmin():
    units = [5, 9, 16]
    off(units)
    on(36)
    sethue(36, s=199)
    setlevel(36,38)
    brdl(onstate=True, bri=1, ct=CTWARM)
    brfl("colour",0.02)

def brsp2(force=False):
    units = [5, 9, 36]
    if ison(5) and not force:
        # 2025-04-12 - actually, if the reading light is on, don't bug me - I'M READING A BOOK!
        return 1
    if ison(16) or ison(36) or force: # keyed on the bedside table light
        on(16) # the key is off, but we got here by force
        off(units)
        setsp2(16, 16)
        brdl(False)
        brfl("red",0.03)
        return 0

def brread():
    '''Stateful toggle of the reading light'''
    unit = 5
    state = False # tracking the toggle-state for reporting back to the caller - did we toggle on?
    if checkstate(unit): 
        # statefile exists, so let's roll it back...
        restorestate(unit)
    else:
        # statefile doesn't exist. let's create one for a toggle and turn it on...
        savestate(unit)
        onwithbri(unit,on,b=254)
        sethue(unit) # force warm white for colour
        state = True
    returnstate = {"toggleon": state}
    return returnstate

def medtog():
    '''Toggle the lights in the meditation corner'''
    state = False
    units = [9, 33]
    if not checkstate(33): # use the downlight to see if we're in-progress
        # not in progress, so save states and turn them on
        for light in units:
            savestate(light)
        oneon(9)
        onwithbri(33, True, b=254)
        setct(33, ct=CTWARM)  # should this be CTWARM? 
        state = True
    else:
        # we're in-progress, so just restore states
        for light in units:
            restorestate(light)
    returnstate = {"toggleon": state}
    return returnstate

def brfl(callstring, bri=0.5):
    '''call the PICOW-based fairy-lights in BR - no returns'''
    picows = [picow4, picow5, picow10]
    for picow in picows:
        try:
            r = requests.get(f"{picow}/led?on={callstring}&bri={bri}")
        except Exception as e:
            print(f"Failed talking to {picow} - {e}")

# Kitchen (K) scenes
def kcstog():
    '''Kitchen Coffee Shop scene'''
    state = False
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
        state = True
    else:
        # statefile found, let's restore the previous state
        for light in units:
            restorestate(light)
    returnstate = {"toggleon": state}
    return returnstate

def knormal(): # An unconditional kitchen normal full lights on mode
    hueaccent(on=True)
    kdl()
    clearallstates()

def koff(): # Similarly, an unconditional "all off" for the kitchen
    hueaccent(on=False)
    kdl(False)
    espresso()
    clearallstates()
       
# Global (GL) scenes
# allalloff() already exists in lightkit, FYI

def servicemode(): # Time to water the houseplants
    hofull(CTCOOL)
    hueaccent(on=True)
    alldl()
    brfl('true')
    lrfl('true')

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
            clearstate(light)

def hatog():
    '''A toggle wrapper for the hueaccent() function with return for Siri/Shortcuts'''
    state = False
    units = [4, 26, 27, 34, 41]
    if not checkstate(4): #keying on the mission accent light's in-progress state
        for light in units:
            savestate(light)
        hueaccent(True)
        state = True
    else:
        for light in units:
            restorestate(light)
    returnstate = {"toggleon": state}
    return returnstate

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
    
def goodmorning():
    '''Turn on ALL the lights in the house'''
    # "Good morning, houseplants. Yes, it's wake-up time."
    
    # Living room:
    lrnormal()

    #Bedroom
    # Basically, a copy of brmin() without the downlights (to avoid the jarring flash when they come up)
    units = [5, 9, 16]
    off(units)
    on(36)
    sethue(36, s=199)
    setlevel(36,38)
    brfl("colour",0.02)
    
    # Everything else, including kitchen downlights and dangling statefiles
    hueaccent(True)
    onwithbri(35, True, 96) # Coffee station worklight
    on(41) # Kitchen fairy lights (coffee station)
    kdl() 
    homin47()
    clearallstates()
    
def fakesun():
    '''Simulated sunrise'''
    # How many minutes should the "sunrise" take? 
    minutes = 7
    sleepInterval = (minutes * 60) / 254
    sleepInterval *= 0.77  # Allow for some overhead in the network processing of these calls
    units = [22, 23, 24, 25, 30]

    # Get everyone turned on, at minimal brighness to start...
    onwithbri(units, True, b=0)
    #setlevels(units=units, bri=0)
    setcts(units, CTCOOL)
    # then, step (slowly) through them all to bring them up
    for level in range(0, 255):
        setlevels(units, level)
        sleep(sleepInterval)

def fakesunfl():
    '''Using fairy-lights as the fake-sun light source'''
    minutes = 7
    sleepInterval = (minutes * 60) / 100
    sleepInterval *= 0.77 # do we need this with the PICOWs?
    # then, step (slowly) through them all to bring them up
    for level in range(0, 100):
        bl = level / 100
        brfl('orange',bl)
        sleep(sleepInterval)
    brfl('mywhite',1) # the 'sun' is done rising; let's flip colour temperature to something less warm

def nightlight(): # A simple, unconditional one-shot to put all the lights into an overnight/nightlight state
    brsp2(force=True)
    rnl(on=True)
    lrcbon()
    kdl(False)
    hueaccent(on=True)
    hosp2()
    clearallstates()

def nltog(): # key off the random nightlight (10) to "toggle" the nightlight state
    state = False
    rnl = 10
    if ison(rnl):
        allalloff()
    else:
        nightlight()
        state = True
    returnstate = {"toggleon": state}
    return returnstate

def xmastree(on=True):
    xmastreehost = 'http://speck.kenkl.org:5000/'
    treeon = xmastreehost+'red'
    treeoff = xmastreehost+'treeoff'
    if on:
        r = requests.get(treeon)
    else:
        r = requests.get(treeoff)

def rgbflash(unit, loops=1):
    ''' just for fun - cycle a single unit through red, green, and blue, saving/restoring state along the way '''
    savestate(unit)
    onwithbri(unit, state=True, b=255)
    while loops > 0:
        sethue(unit, h=HRED)
        sleep(1)
        sethue(unit, h=HGREEN)
        sleep(1)
        sethue(unit, h=HBLUE)
        sleep(1)
        loops -= 1
    restorestate(unit)

# Outside scenes

def fpset(state=False, bri=255, ct=CTCOOL):
    ''' A simple, direct control for the front porch light '''
    unit = 42
    onwithbri(unit, state, bri)
    setct(unit, ct)

def fplast(state=False):
    ''' An even simpler control - on/off only, to retain the previous colour/brightness state '''
    unit = 42
    on(unit, state)

def bpset(state=False, bri=255, ct=CTCOOL):
    ''' A simple, direct control for the back porch light '''
    unit = 43
    onwithbri(unit, state, bri)
    setct(unit, ct)

def bplast(state=False):
    ''' An even simpler control - on/off only, to retain the previous colour/brightness state '''
    unit = 43
    on(unit, state)
    

# Other (O) (test) scenes


if __name__ == "__main__":
    print("A collection of scenes/macros to be used from calling scripts. To use:")
    print("from scenes import *")
