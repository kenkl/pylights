#!/usr/bin/env python3
from tkinter import *
from lightkit import *

FONT="Ariel"
NORMAL="normal"
SIZE=14
W="W"


# Button handlers

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
    if ison(howl):
        oneoff(howl)
    else:
        oneon(howl)

def hohalf():
    units = [3, 19, 21, 38]
    for light in units:
        oneon(light)
        setct(light, CTWARM)
        setlevel(light, 128)
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

# UI setup
window = Tk()
window.title("HO Lights")
window.config(padx=10, pady=10)

title_label = Label(text="HO Lights", font=("Ariel", 24, "bold"))
title_label.grid(column=1, row=0, sticky=W)

but1 = Button(text="Normal", command=honormal)
but1.grid(column=0, row=1, sticky=W)

but1_label = Label(text="Normal full bright", font=(FONT, SIZE, NORMAL))
but1_label.grid(column=1, row=1, sticky=W)

but2 = Button(text="Half 1", command=hoh1)
but2.grid(column=0, row=2, sticky=W)

but2_label = Label(text="Half bright, with dragonfly", font=(FONT, SIZE, NORMAL))
but2_label.grid(column=1, row=2, sticky=W)

but3 = Button(text="Half 2", command=hoh2)
but3.grid(column=0, row=3, sticky=W)

but3_label = Label(text="Half bright, without dragonfly", font=(FONT, SIZE, NORMAL))
but3_label.grid(column=1, row=3, sticky=W)

but4 = Button(text="Worklight", command=howltog)
but4.grid(column=0, row=4, sticky=W)

but4_label = Label(text="Work light toggle", font=(FONT, SIZE, NORMAL))
but4_label.grid(column=1, row=4, sticky=W)

but5 = Button(text="Game", command=hogame)
but5.grid(column=0, row=5, sticky=W)

but5_label = Label(text="Game mode", font=(FONT, SIZE, NORMAL))
but5_label.grid(column=1, row=5, sticky=W)

but6 = Button(text="OFF", command=hoalloff)
but6.grid(column=0, row=6, sticky=W)

but6_label = Label(text="All lights off", font=(FONT, SIZE, NORMAL))
but6_label.grid(column=1, row=6, sticky=W)

window.mainloop()
