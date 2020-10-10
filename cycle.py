#!/usr/bin/env python3

from lightkit import *

unit=11
units=[11,12,13,14,15]
sat=254
delay=1.25
loops=17

for x in range(0,loops):

    # RED
    for unit in units:
        sethue(unit,0,sat)
    sleep(delay)

    # GREEN 
    for unit in units:
        sethue(unit,25500,sat)
    sleep(delay)
    
    # BLUE
    for unit in units:
        sethue(unit,46920,sat)
    sleep(delay)
    
                                
#sethue(unit,7676,143)
for unit in units:
    setct(unit, 382)
