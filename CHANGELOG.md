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

2021-03-20:

- Tweak fakesun.py to include _even more_ downlights in the group. 

2021-03-26:

- Add espresso.py - a shim into lightkit to turn the espresso machine on/off or get its current state for scripting/crontab. The target is a [Philips Hue Smart Plug](https://www.amazon.com/gp/product/B07XD578LD) that, like the [INNR Smart Plug](https://www.amazon.com/Zigbee-Philips-SmartThings-Google-Required/dp/B07SQGG8Z7), only supports ON/OFF. It's a minor QoL thing that probably doesn't deserve this much commentary, but here we are. ☕️

2021-03-27:

- See the commit diff for details - added scene presets for living room, home office, and bedroom, including SP2, to mimic what we've got in [Lights](https://github.com/kenkl/lights).
- Add call and call.py to shim calls into scenes.py (and lightkit.py) from the command-line, making it possible to script/cronjob functions contained therein without dedicated scripts.

2021-04-11:

- Added listener and listener.py as a Flask-powered remote interface to scenes (and lightkit, by extension). At present, it runs on the same RaspberryPI that I've got butthing.py running on, serving as a shim to the Hue ecosystem, much like [Lights](https://github.com/kenkl/lights) does. 
- Updated requirements.txt to reflect the addition of Flask to the project.

2021-04-15:

- Add goodmorning() macro to scenes.py 
- Move espresso() macro to scenes.py
- Move fakesun() macro to scenes.py
- Remove the external versions of goodmorning, espresso, fakesun, and lightlist; with the call/call.py functionality, they aren't needed any more.
- One of the annoying things that fakesun has revealed - the light will come on to the last brightness used if not overriden during the state change. onwithbri() is added to lightkit to address this. I _may_ circle back to refactor on(), oneon(), off(), etc. to use it, but that's not a high priority right this minute...

2021-04-16:

- Add a mutiplier to fakesun() to reduce the sleep interval on the iterations through its loop for increasing brightness. It's a really squishy number; the delay is variable based on the number of lights, the length of the run, whatever processing the bridge has to do, how quickly the lights respond, etc. etc. etc. For my 7-minute cycle with 9 lights, I was actually seeing fakesun() take as much as 14 minutes. This helps a bit. Reducing sleepInterval further runs up against hard limits/race conditions, so.

2021-05-04:

- Moved the light (#35) from the end-table to the coffee station. Update scenes accordingly...

2021-05-15:

- add checkall() to sweep through all known units and report any that have gone unreachable.
- add notify() to support checkall() (and future capabilities) to send email/text/whatever as appropriate.
- document/add new entries to secrets.py to support notify()

2021-10-08:

- change @app.route('/api') to return a page from /templates instead of a simple call echo. This enables building a simple .html page that calls API endpoints and will 'force' the browser back a page (with window.history.back() in the body tag) to streamline the behaviour a little when calling from a browser.

2021-10-09:

- Now that API calls don't "strand" the browser, assembled a simple prototype page to make the calls from the browser and serve that up at @app.route('/'). It's crude, but works well enough to get more ideas.
- Update requirements.txt to quiet GitHub hollering at me about urllib3's vulnerabilities (older version)
- Other little bugfixes

2021-11-01:

- As an alternate to SP2 mode in the living room, created 'lrcbon()' to turn off everything except the two candlebox units

2021-11-21:

- Add lrteevee2() - an alternate to TV mode that's a bit darker, but not as much as cinema mode.

2021-11-22:

- Add simple routine for turning off/on the tall dragonfly (with 3 lights). Because...
- Refactor lrteevee2() to use lrdfoff() to be a smoother transition
- Update listener top.html to include calls to these new functions

2021-11-23:

- bugfix for lrteevee2() - let's turn on the candleboxes too...
- add lrread() - reading lights in the living room
- add brread() - bedroom reading light

2021-11-26:

- bugfix for brsp2() - it wasn't checking the right lights for the conditional transition
- Upgrade the bedroom reading light (5) to a proper stateful toggle
- allalloff() should clear all dangling statefiles. It does now.
- Update listener's top.html to reflect the stateful toggle
- Add a 'clearallstates()' call in top.html utilities
- Upgrade lrread() to be a stateful toggle
- add a call to kcstog() in top.html utilities

2021-11-27:

- Add a simple xmastree() call in scenes.py to turn the Xmas tree on/off. Tis the season!
- ...and add an entry in top.html utilities to manage it...

2021-11-30:

- After rearranging the living room, the SP2 event needs minor revision, so let's do that.

2021-12-09:

- Bugfixes for lrsp2() - set the colour temperature and turn off the TV backlight.

2021-12-14:

- Add colour-temperature argument-parsing to hofull() and honormal().
- Add corresponding entries to top.html for use from the Flask listener.

2022-01-19:

- Remove the bedroom lights from fakesun(). Even at 0 brightness, these come on bright enough to be jarring.
- Add .DS_Store to .gitignore (not sure why that wasn't already there).

2022-03-10:

- Add just _one_ of the bedroom downlights (33) to fakesun(). Having no bedroom lights involved is less effective than I'd like.

2022-03-21:

- Further experimentation with the bedroom downlights in fakesun().

2022-04-03:

- Even more refinement of fakesun() behaviour. 

2022-04-15:

- Add medtog() - a stateful toggle of lights in the meditation corner. TODO: in Lights, this is a 2-stage toggle cycling between CTWARM and CTCOOL. Should that be A Thing here, as well? For now, it's only CTCOOL.

2022-04-23:

- Add the coffee station worklight (35) to Kitchen Coffee Shop (kcstog). 

2022-05-01:

- Construct an '/api2' app.route to return JSON states of calls instead of a browser-friendly return. I've been using [Apple Shortcuts](https://support.apple.com/guide/shortcuts/welcome/ios) to enable Siri to call into pylights to initiate an action, and had the idea that I could make Siri announce, in the shortcut, what the state of the call's return is. Problem is, '/api' doesn't return any useful data; just flipping the browser back to top.html. This is very much a WIP and may or may not develop further.
- Update brread() to return a value (dict), indicating whether we've toggled on (or off) that light. That way, '/api2' has _something_ to pass on to Siri

2022-05-02:

- The '/api2' app.route addition has been an unqualified success. Yesterday's upgrade of brread() gave Siri (via Shortcuts) the intended awareness of toggle state for that light. So, I'm inspired to add the return state functionality to a few more scenes: howltog(), lrread(), medtog(), and kcstog().

2022-05-07:

- Add hatog() wrapper for the accent group, providing a stateful toggle with return so that Siri/Shortcuts are simplified a bit.
- Add logging to listener.py to capture calls to '/api' and '/api2' to a simple logfile for diagnostics/history. 

2022-06-21:

- Yet another tweak to fakesun()

2022-08-14:

- Discovered, with some sadness, that the Hue Sync Box was interferring with the AirPlay functionality on the ATV4K in my AV stack, so I've taken it offline. I still want the TV backlights to do _something_, so I've added lrtvblon() to give it a nice unobtrusive level/colour-temperature for TV-watching sessions. Exact levels are subject to change, of course.
- Add a new global utility call - a whole-house nightlight setting, collecting low-light-level calls from the rooms to create the scene - nightlight(). Also, adding nltog() to add a simple toggle (non-stateful) for the scene.
- Add knormal() and koff() for a non-coffee-shop variant of the lights in the kitchen
- Expose lrtvblon() and nltog() to the web interface via top.html.

2022-10-15:

- I replaced the light on my front porch with the [Econic fixture](https://smile.amazon.com/gp/product/B07NDF3VPH), so it gets a few utility routines in scenes.py - fpset() and fplast()
- Updated top.html to include (what I think will be) commonly-used calls to these
- Although it does get caught in allalloff(), the porch light should (I think) go off when SP2 gets called, so add that.
- As a goof/for fun, added rgbflash() - to cycle red, green, and blue on a single unit/light. I mostly added it to play with the new porch light for a minute, to "prove" that it's healthy. I can't promise not to expand/enhance it later, but for now it's just a simple little test rig.
- _Another_ tweak to fakesun(). For reasons.

2022-10-20:

- Add whitelist capability to checkall() - units that are expected to be unreachable at times (back porch), but _shouldn't_ send alerts. Reminder to future-me: the unit ids need to be STRs in that list.
- Rework the front porch control in top.html. Also, added a back porch button.
- Add a couple of functions for the new back porch light. Copy/paste is my friend.

2022-11-24:

- Remove the front porch light from lrsp2(). It only gets called if lrsp2() passes the key-check (or is forced), so I already have a "safety" call in the crontab "just in case" anyway. That seems more appropriate/sane anyway.
- Speaking of lrsp2(). I've long been annoyed that it drops the candlebox lights, so let's stop doing that.
- I'd intended the porchlights to be managed/controlled with local wall switches, but in practice that's not really A Thing™, so let's take them out of the whitelist for checkall(). It would actually be useful to have a reminder if either of them has been turned off manually for some reason.

2023-01-08:

- Removed the fairy-lights (41) management from espresso() - they're handled in hueaccent() anyway, plus my call in espresso() was bugged; not passing the proper state to it anyway, causing some... _confusing_ behaviour, especially with koff() - it would turn off the fairylights with hueaccent(False), but then they'd come right back on with espresso(). Oops. Very minor bug, but one that bothered me. 
- Related: kcstog() has been toggling the coffee station work light (35), but the more I use that, the less "correct" it seems. Removed.

2023-01-09:

- VSC/Pylance has informed me that using secrets.py is overriding stdlib functions in Python. Although I'm not using any of that (right now), I can envision having a frustrating moment at some point in the future if I needed to use something from the standard library. So... secrets.py has been renamed to pylsecrets.py and references in lightkit updated.
- Move the whitelist for checkall() to pylsecrets.py. I'm planning to move a couple lights around, or even retire them from service, and it occurred to me that it would be good to not have to update the code (with associated commits on GitHub) for each one. Because the Hue Bridge returns the unit numbers as strings, whitelist needs to be a list of strings as well.

2023-02-05:

- Change the whitelist used by checkall() to be INTs. It was an amateur-hour move to force them to be strings just 'cos the Bridge returns them that way. 
- Add an aaoexclude list to pylsecrets to be used by allalloff(). Units listed here (as INTs) will be skipped during that call. This lets me schedule a unit (Nixie-tube clock) separately from the global lights-out behaviour.
- Add an optional argument to allalloff() to override the exclusion list as needed. 

2023-02-15:

- I've started using [Adafruit NeoPixel 50-pixel strands](https://www.adafruit.com/product/4560) with [Raspberry Pi PICO W](https://www.adafruit.com/product/5526)s to add even _more_ fairy-lights to my space. It didn't take long before I felt the desire to fold them into scenes in rooms that they're decorating. I've added picow2 and picow3 in my home-office/studio as a start. More are planned to follow. TODO: post a version of the CircuitPython I'm using on the PICOWs to respond to these calls. 

2023-02-16:

- Cleaning up the calls in HO for the NeoPixel strands - wrapping them in hofl() instead. It's not a performance boost or anything, but the code looks nicer.
- Add a few utility links in top.html for the listener to provide control.