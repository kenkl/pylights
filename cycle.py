#!/usr/bin/env python3

from lightkit import *

unit=21
sat=254
delay=0.25

for x in range(0,5):
    sethue(unit,0,sat)
    sleep(delay)
    sethue(unit,25500,sat)
    sleep(delay)
    sethue(unit,46920,sat)
    sleep(delay)
                                
#sethue(unit,7676,143)
setct(unit, 382)
