#!/usr/bin/env python3
from tkinter import *
from scenes import *

FONT="Ariel"
NORMAL="normal"
SIZE=14
W="W"


# Button handlers moved to scenes. What could possibly go wrong?

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
