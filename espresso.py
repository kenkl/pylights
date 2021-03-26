#!/usr/bin/env python3
# A shim into lightkit to turn the Espresso machine on/off or get its current state for scripting/crontab
import sys
from lightkit import *

em = 40 # The Espresso Machine's Hue ID presence

def usage():
    print("\nUsage:\n  espresso.py <command>\n\nCommands:")
    print("    on     Turn the machine on\n   off     Turn the machine off")
    print("  stat     Get the current state (on/off) of the machine.\n\n")

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        usage()
    else:
        if sys.argv[1].upper() == "ON":
            on(em)
        elif sys.argv[1].upper() == "OFF":
            off(em)
        elif sys.argv[1].upper() == "STAT":
            state = "OFF"
            if ison(em):
                state = "ON"
            print(f"The machine is {state}.")
        else:
            usage()
