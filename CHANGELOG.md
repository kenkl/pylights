# pylights changelog

2021-03-02: 

- Added fakesun.py - inspired by the inaugural issue of [Remotely Interesting](https://ckarchive.com/b/8kuqhohn5mnz%20), I wanted to make a couple lights in the bedroom (or wherever) do a simulated sunrise sequence - brightening over the course of a few minutes. That lead to the question "how long does a sunrise take?" - the answer is [complicated](https://astronomy.stackexchange.com/questions/12824/how-long-does-a-sunrise-or-sunset-take). Adjust to taste, I guess. Because of the network traffic generated to the Hue Bridge, and the responsiveness of the Hue bulbs (they take ~400ms to transition state/brightness by default), the sunrise interval defined in the script tends to run a little long. During my testing, a 5-minute interval actually takes roughly 6 minutes, while a test at 1 minute took just over 2 to complete. For a long-running script, it's probably not important, but it's not a bug - it's a feature.

2021-03-06:

- Update fakesun.py to include the bedroom downlights, _and_ get everyone using a cooler colour-temperature via setct(). It's a WIP, but I think the brighter, cooler light will more closely simulate a sunrise and wake me up a little better. As mentioned the other day - "adjust to taste" - here we are.

2021-03-08:

- Made holights.py - a "control panel" thing for my home-office/studio lights, as a proof-of-concept, with Tkinter. It largely echoes what [Lights](https://github.com/kenkl/lights) does for the room lights. I did leave the minimal scenes out, as I rarely use them. Along the way, added CTWARM and CTCOOL globals to lightkit.py; I'm already having ideas how they'll be useful for some other things.

2021-03-09:

- holights got me thinking - if I could plug a frontend in for lightkit so easily, it'd be handy to capture scenes and macros in one place, so that I could use whatever client, so long as it can import the module, to drive the lighting. Ultimately, Django/Flask/whatever could use that to create a unified web frontend. So, I've created scenes.py to do just that, and refactored holights.py to use it. 

2021-03-10:

- Add Docstrings to the functions in lightkit for self-documentation.
- Additional functions added to lightkit (toggle, statefilename, sp2_on, etc.).
- Refactor scenes a little to take advantage of new things in lightkit.
- Added kcstog() to scenes, and discovered A Thing. I _think_ I'm putting the bulbs in an error state for a moment (they'll flash when restorestate() runs) before settling in to what I'm pushing to them. I think I know what I need to do... to be continued...

2021-03-11:

- After some research, I think the flash I mentioned yesterday (with colour, depending on the bulb) is happening because I'm shoving _all_ the state keys, even the read-only ones. There's a precedence with XY, CT, and HS colour modes as well; I'm probably violating that by shoving all of them like this. I've a clever plan to clean all that up _before_ writing the statefile, but that's gonna take a little more time than I have just this minute. Just wanted to make a note of it. To be continued... (again)
- Added an indicator to lightlist() when a unit is unreachable for some reason, as an FYI. Having the idea that I could have a periodic poll somewhere that would send an alert/notification/whatever if the poll catches units that have gone 'missing'. 

2021-03-12:

The theme today is getting stateful toggling supported with a number of functions -

- Enhanced savestate() to only save the colour-mode currently in use for later restore. This fixed the flashing noted earlier.
- restorestate() can now be flagged to keep the statefile
- Add clearstate() to drop a previous statefile
- Add clearallstates() to iterate through the lights and clear all the dangling statefiles for them
- Add optional flag to restorestate() to allow preservation of the statefile
- Add saveallstates() and restoreallstates() for some reason (I don't know when this'll be useful, but...)

- Add 'Hue Accents' group scene on/off

2021-03-16:

- Added/refined functions in lightkit.py and scenes.py to support goodmorning.py
- Add goodmorning.py - to bring all the lights up to full brightness, as a way to 'kick-start' the morning wake-up routine. 

2021-03-17:

- Refactor lightkit.py to use requests instead of urllib3. The idea is to make PyLights portable to the [CircuitPython](https://circuitpython.org/) platform, which uses [adafruit_requests](https://circuitpython.readthedocs.io/projects/requests/en/latest/), which is very similar (for .get() and .put() calls at least).
- With [CircuitPython](https://circuitpython.org/) in mind, add a CONST for the statefile location.
- Implement secrets.py to keep API keys, credentials, and other stuff that doesn't belong in a public repo. Edit/rename secrets_sample.py to use.
- With the switch to using requests, PyLights will require the addition of that module (maybe others in the future). For completeness, I've run 'pip freeze' to create requirements.txt for building a target platform.

2021-03-19:

- Spent a bit of time with a [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) equipped with an [AirLift breakout](https://www.adafruit.com/product/4201) to get it on WiFi and running [CircuitPython](https://circuitpython.org/). Got "this close" to having it working, but ran into problems with adafruit_request.get() communicating with the Hue Bridge - was getting 0-byte responses (which json.dumps() didn't like _at all_) instead of the ~105KB that my Bridge serves up normally. I'm still investigating why it's doing that - test calls to other REST endpoints (that don't push back quite as much data) seem to work just fine.
- Putting the Pico on the side for a bit, I turned my attention to a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) instead. It has no trouble at all hosting pylights, so I wired up a few buttons to trigger calls into scenes.py. The new code here is in butthing.py (button thing) - it does require [gpiozero](https://gpiozero.readthedocs.io/en/stable/), but that's installed by default on recent/current versions of [Raspbian](https://www.raspbian.org/). 
