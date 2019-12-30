#!/usr/bin/env python3
  
import subprocess
import urllib.request
import json
import time
from time import sleep, strftime
from datetime import datetime

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

hostname='huehub.kenkl.org'
apikey='RPVo8wEXziF6OeLtCaCUqMdqWm28DrKqVQL7ftgG'
baseurl="https://"+hostname+"/api/"+apikey

def lighturl(i):
    url=baseurl+"/lights/"+str(i)
    return url

def ison_nukeme(i):
    url=lighturl(i)
    wr=urllib.request.urlopen(url, context=ctx)
    wd=wr.read()
    resp=json.loads(wd)

    state=resp['state']
    ison=state['on']
    return ison

def oneon(i):
    url=lighturl(i)+"/state"
    dothis=b'{"on": true}'
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def oneoff(i):
    url=lighturl(i)+"/state"
    dothis=b'{"on": false}'
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def getlights():
    wr=urllib.request.urlopen(baseurl, context=ctx)
    wd=wr.read()
    resp=json.loads(wd)
    lights=resp['lights']
    return lights

def ison(i):
    lights=getlights()
    unitid=lights[str(i)]
    state=unitid['state']
    ison=state['on']
    return ison

def getstate(i):
    lights=getlights()
    unitid=lights[str(i)]
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

def lightlist():
    lights=getlights()
    for i in lights.keys():
        unitid = lights[i]
        state = unitid['state']
        name = unitid['name']
        ison = state['on']
        if(ison == True):
            onoff="ON"
        else:
            onoff="OFF"
        print(i,name,"  "+onoff)

def allalloff():
    lights=getlights()
    for i in lights.keys():
        oneoff(i)

def sethue(i, h, s=254):
    url=lighturl(i)+"/state"
    dothis='{"hue": '+str(h)+', "sat": '+str(s)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def setct(i, ct):
    url=lighturl(i)+"/state"
    dothis='{"ct": '+str(ct)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)

def setlevel(i, b=254):
    url=lighturl(i)+"/state"
    dothis='{"bri": '+str(b)+'}'
    dothis=dothis.encode('utf-8')
    wr=urllib.request.Request(url, data=dothis, method='PUT')
    urllib.request.urlopen(wr, context=ctx)


if __name__ == '__main__':
    print()
    print("lightkit library -")
    print("from lightkit import *")
    print("to begin molesting the bridge/hub thingie.")
    print()

    
