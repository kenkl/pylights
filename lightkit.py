#!/usr/bin/env python3
  
import requests
import json, time, os, smtplib
from pylsecrets import secrets
from time import sleep, strftime
from datetime import datetime

# The Hue Bridge presents a self-signed cert, so let's skip the checks for that. Calls to requests will still throw a warning with 'verify=False' - mute those with:
requests.packages.urllib3.disable_warnings()

# Useful globals
whitelist=secrets['whitelist']
aaoexclude=secrets['aaoexclude']
hostname=secrets['huehostname']
apikey=secrets['hueapikey']
baseurl="https://"+hostname+"/api/"+apikey
picow2="http://picow2.kenkl.org:8080"
picow3="http://picow3.kenkl.org:8080"
picow4="http://picow4.kenkl.org:8080"
picow5="http://picow5.kenkl.org:8080"
picow6="http://picow6.kenkl.org:8080"
picow7="http://picow7.kenkl.org:8080"
picow8="http://picow8.kenkl.org:8080"
picow9="http://picow9.kenkl.org:8080"
picow10="http://picow10.kenkl.org:8080"
allpicows=[picow2, picow3, picow4, picow5, picow6, picow7, picow8, picow9, picow10]
STATEFILEPATH = '/tmp' # Where to store statefiles 
CTWARM = 400
CTCOOL = 330
HRED = 0
HGREEN = 25500
HBLUE = 46920


def lighturl(i):
    '''From the provided ID, construct the URL to POST to for it'''
    url=baseurl+"/lights/"+str(i)
    return url

def statefilename(i):
    '''Returns the path for a state file name to use for saving/restoring state of a unit'''
    return f"{STATEFILEPATH}/pylights.{i}.state"

def getstate(i):
    '''Returns the full JSON state of a single unit'''
    lights = getlights()
    unitid = lights[str(i)]
    state = unitid['state']
    return state

def sanitizestate(state):
    '''Remove extra keys from state in preparation for replay/restore'''
    g = state.pop("effect", None)
    g = state.pop("alert", None)
    g = state.pop("mode", None)
    g = state.pop("reachable", None)
    return state

def savestate(i):
    '''Save current unit status to a file'''
    # Get the state, sanitize it, and strip unused colour-modes
    state = sanitizestate((getstate(i)))
    if 'colormode' in state:
        # let's preserve only the colour-state used for the current light condition
        if state['colormode'] == 'xy':
            g = state.pop("hue", None)
            g = state.pop("sat", None)
            g = state.pop("ct", None)
        if state['colormode'] == 'ct':
            g = state.pop("hue", None)
            g = state.pop("sat", None)
            g = state.pop("xy", None)
        if state['colormode'] == 'hs':
            g = state.pop("ct", None)
            g = state.pop("xy", None)
        g = state.pop('colormode', None)

    # Then, write it to a statefile for later restoration
    with open(statefilename(i), 'w') as statefile:
       statefile.write(json.dumps(state))

def restorestate(i, rmstatefile=True):
    '''Restore unit status from statefile'''
    sf = statefilename(i)
    if os.path.exists(sf):
        with open(sf) as statefile:
            state = bytearray(statefile.read(), 'utf-8')
        url = lighturl(i) + "/state"
        r = requests.put(url, state, verify=False)
        if rmstatefile:
            os.remove(sf)

def checkstate(i):
    '''Check whether the unit has a statefile (in progress)'''
    if os.path.exists(statefilename(i)):
        return True
    else:
        return False

def clearstate(i):
    '''drop the statefile for an individual light'''
    if checkstate(i):
        os.remove(statefilename(i))

def getstates():
    '''returns a list of lights that have a statefile (in progress)'''
    lightlist = []
    for light in getlights():
        if checkstate(light):
            lightlist.append(light)
    return lightlist

def clearallstates():
    '''drop statefiles for all lights'''
    for light in getstates():
        clearstate(light)

def saveallstates():
    '''save a statefile for every light'''
    for light in getlights():
        savestate(light)

def restoreallstates(dropstatefile=True):
    '''restore the state for every in-progress light'''
    for light in getstates():
        restorestate(light, dropstatefile)

def oneon(i):
    '''Simply turn on a single unit'''
    url=lighturl(i)+"/state"
    dothis=b'{"on": true}'
    r = requests.put(url, dothis, verify=False)

def oneoff(i):
    '''Simply turn off a single unit'''
    url=lighturl(i)+"/state"
    dothis=b'{"on": false}'
    r = requests.put(url, dothis, verify=False)

def on(units, state=True):
    '''Turn on (or off) a set of lights'''
    if isinstance(units, list):
        for light in units:
            if state:
                oneon(light)
            else:
                oneoff(light)
    elif isinstance(units, int):
        if state:
            oneon(units)
        else:
            oneoff(units)
    else:
        print("Fail. on() needs either an int with a single unit, or a list with multiple units. You provided:")
        print(type(units))

def onwithbri(units, state=True, b=0):
    '''Turn on/off unit(s) at a specific brightness'''
    # Lights will come on, by default/design at their last brightness level. This is meant to override that. 
    if isinstance(units, list):
        if not state:
            off(units)
        else:
            for unit in units:
                url=lighturl(unit)+"/state"
                dothis='{"on": true, "bri": ' + str(b) + '}'
                dothis=dothis.encode('utf-8')
                r = requests.put(url, dothis, verify=False)
    elif isinstance(units, int):
        if not state:
            off(units)
        else:
            url = lighturl(units)+"/state"
            dothis='{"on": true, "bri": ' + str(b) + '}'
            dothis=dothis.encode('utf-8')
            r = requests.put(url, dothis, verify=False)
    else:
        print("Fail. onwithbri() needs either an int with a single unit, or a list with multiple units. You provided:")
        print(type(units))




def off(units):
    '''Turn off a set of lights'''
    # This is only here to maintain symmetry with the on() call
    on(units, state=False)


def getlights():
    '''Returns the lights node from the Hue Bridge'''
    r = requests.get(baseurl, verify=False)
    resp = r.json()
    lights=resp['lights']
    return lights

def ison(i):
    '''Returns the on state of a single unit'''
    state = getstate(i)
    ison=state['on']
    return ison

def gethrstate(i):
    '''Displays the human-readable state for a single unit'''
    lights=getlights()
    unitid=lights[str(i)]
    man=unitid['manufacturername']
    prod=unitid['productname']
    state=unitid['state']
    name=unitid['name']
    ison=state['on']
    reachable=state['reachable']
    try:     # Not all lights have the same capabilities (HS vs. CT only vs. ON/OFF only). Play nice.
        bri=state['bri']
    except KeyError:
        bri="N/A"
    try:
        hue=state['hue']
    except KeyError:
        hue="N/A"
    try:
        sat=state['sat']
    except KeyError:
        sat="N/A"
    try:
        ct=state['ct']
    except KeyError:
        ct="N/A"
    try:
        cm=state['colormode']
    except KeyError:
        cm="N/A"

    print("Unit %i - %s:"%(i,name))
    print("On:", ison)
    print("Brightness:", bri)
    print("Hue:", hue)
    print("Saturation:", sat)
    print("Colour Temp:", ct)
    print("Colour Mode:", cm)
    print("Manufacturer Name:", man)
    print("Product Name:", prod)
    print("Reachable:", reachable)

def lightlist():
    '''Displays a list of all Lights units and each of their on: states'''
    lights=getlights()
    for i in lights.keys():
        unitid = lights[i]
        state = unitid['state']
        name = unitid['name']
        ison = state['on']
        reachable = state['reachable']
        if(ison == True):
            onoff="ON"
        else:
            onoff="OFF"
        if reachable:
            rs = ""
        else:
            rs = "*** UNREACHABLE ***"
        print(f"{rs}{i} {name}  {onoff}")

def allalloff(force=False):
    '''Turns off all the lights known to the Bridge, except those listed in aaoexclude'''
    print(f"force set to {force}")
    lights=getlights()
    for i in lights.keys():
        off = False
        if int(i) not in aaoexclude:
            off = True
        elif force:
            off = True
        if off:
            oneoff(i)
    for picow in allpicows:
        try:
            r = requests.get(picow+"/led?on=false")
        except Exception as e:
            print(f"Failed talking to {picow} - {e}")
            
    clearallstates()

def sethue(i, h=7676, s=143):
    '''Set hue/saturation values for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"hue": '+str(h)+', "sat": '+str(s)+'}'
    dothis=dothis.encode('utf-8')
    r = requests.put(url, dothis, verify=False)

def setct(i, ct):
    '''Set colour-temperature value for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"ct": '+str(ct)+'}'
    dothis=dothis.encode('utf-8')
    r = requests.put(url, dothis, verify=False)

def setcts(units, ct):
    '''set colour-temperature value for a set of lights'''
    for light in units:
        setct(light, ct)

def sethues(units, hue=7676, sat=143):
    '''Set hue/saturation values for a set of lights'''
    for light in units:
        sethue(light, hue, sat)

def setlevels(units, bri=254):
    '''Set brightness level value for a set of lights'''
    for light in units:
        setlevel(light, bri)

def setlevel(i, b=254):
    '''Set brightness level value for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"bri": '+str(b)+'}'
    dothis=dothis.encode('utf-8')
    r = requests.put(url, dothis, verify=False)

def setsp2(units, sp2bri=76):
    '''Set SP2 for named unit(s)'''
    # This is my standardised reminder to go to bed - Sleep Protocol, part 2
    sp2hue = 3771
    sp2sat = 240
    if isinstance(units, list):
        sethues(units, hue=sp2hue, sat=sp2sat)
        setlevels(units, bri=sp2bri)
    elif isinstance(units, int):
        sethue(units, h=sp2hue, s=sp2sat)
        setlevel(units, b=sp2bri)
    else:
        print("Fail. setsp2() needs an int or list. You provided:")
        print(type(units))


def toggle(i):
    '''Toggle the on state of a single unit'''
    if ison(i):
        oneoff(i)
    else:
        oneon(i)

def notify(message):
    '''send an email/text to destination(s) defined in secrets.py when something needs to alert'''
    try:
        myemail = secrets['myemail']
        password = secrets['email_password']
        host = secrets['email_host']
        port = secrets['email_port']
        email_dest = secrets['email_dest']

        with smtplib.SMTP(host, port=port) as connection:
            connection.starttls()
            connection.login(myemail, password)
            connection.sendmail(myemail, email_dest, msg=message)
    except Exception as e:
        print(f"Sending notification failed:")
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

def checkall():
    '''Detect whether any units have gone unreachable, and send a list via notify() if they have'''
    send_alert = False  # Flag whether we found any
    # from pylsecrets, whitelist is a list of str's that should never send alerts, e.g. whitelist = ['42', '43']
    message = 'Units UNREACHABLE\n'
    lights = getlights()
    for i in lights.keys():
        unitid = lights[i]
        state = unitid['state']
        name = unitid['name']
        reachable = state['reachable']
        if not reachable and int(i) not in whitelist:
            message += f"{i} - {name}\n"
            send_alert = True
    if send_alert:
        print(message)
        notify(message)
    return send_alert



if __name__ == '__main__':
    print()
    print("lightkit library -")
    print("from lightkit import *")
    print("to begin molesting the bridge/hub thingie.")
    print()

    
