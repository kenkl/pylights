#!/usr/bin/env python3
'''Take a call for scenes from the CLI and call it from here'''
import sys, scenes
from scenes import *

def usage():
    print("Usage: call [function]")
    print(f"where function is one of {dir(scenes)}")

def dothing(function):
    result = eval(function)
    print(result)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        dothing(sys.argv[1])
    else:
        usage()

