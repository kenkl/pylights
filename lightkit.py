#!/usr/bin/env python3
  
import subprocess
import urllib.request
import json, time, os
from time import sleep, strftime
from datetime import datetime

# The Hue Bridge presents a self-signed cert, so let's skip the checks for that
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Useful globals
hostname='huehub.kenkl.org'
apikey='RPVo8wEXziF6OeLtCaCUqMdqWm28DrKqVQL7ftgG' # See (TODO: add reference) to get a Bridge API Key
baseurl="https://"+hostname+"/api/"+apikey
CTWARM = 400
CTCOOL = 330

def lighturl(i):
    '''From the provided ID, construct the URL to POST to for it'''
    url=baseurl+"/lights/"+str(i)
    return url

def statefilename(i):
    '''Returns the path for a state file name to use for saving/restoring state of a unit'''
    return f"/tmp/pylights.{i}.state"

def getstate(i):
    '''Returns the full JSON state of a single unit'''
    lights = getlights()
    unitid = lights[str(i)]
    state = unitid['state']
    return state

def savestate(i):
    '''Save current unit status to a file'''
    with open(statefilename(i), 'w') as statefile:
       statefile.write(json.dumps(getstate(i)))

def restorestate(i):
    '''Restore unit status from statefile'''
    sf = statefilename(i)
    if os.path.exists(sf):
        with open(sf) as statefile:
            state = bytearray(statefile.read(), 'utf-8')
        url = lighturl(i) + "/state"
        wr = urllib.request.Request(url, state, method='PUT')
        urllib.request.urlopen(wr, context=ctx)
        os.remove(sf)

def checkstate(i):
    '''Check whether the unit has a statefile (in progress)'''
    if os.path.exists(statefilename(i)):
        return True
    else:
        return False

def oneon(i):
    '''Simply turn on a single unit'''
    url=lighturl(i)+"/state"
    dothis=b'{"on": true}'
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def oneoff(i):
    '''Simply turn off a single unit'''
    url=lighturl(i)+"/state"
    dothis=b'{"on": false}'
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def getlights():
    '''Gets the complete state of the Bridge and returns the Lights node'''
    wr=urllib.request.urlopen(baseurl, context=ctx)
    wd=wr.read()
    resp=json.loads(wd)
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
        print(i,name,"  "+onoff+"  "+rs)

def allalloff():
    '''Turns off ALL the lights known to the Bridge'''
    lights=getlights()
    for i in lights.keys():
        oneoff(i)

def sethue(i, h, s=254):
    '''Set hue/saturation values for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"hue": '+str(h)+', "sat": '+str(s)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def setct(i, ct):
    '''Set colour-temperature value for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"ct": '+str(ct)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def setlevel(i, b=254):
    '''Set brightness level value for a single unit'''
    url=lighturl(i)+"/state"
    dothis='{"bri": '+str(b)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def toggle(i):
    '''Toggle the on state of a single unit'''
    if ison(i):
        oneoff(i)
    else:
        oneon(i)


if __name__ == '__main__':
    print()
    print("lightkit library -")
    print("from lightkit import *")
    print("to begin molesting the bridge/hub thingie.")
    print()

    
