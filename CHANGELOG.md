# pylights changelog

2021-03-02: 

- Added fakesun.py - inspired by the inaugural issue of [Remotely Interesting](https://ckarchive.com/b/8kuqhohn5mnz%20), I wanted to make a couple lights in the bedroom (or wherever) do a simulated sunrise sequence - brightening over the course of a few minutes. That lead to the question "how long does a sunrise take?" - the answer is [complicated](https://astronomy.stackexchange.com/questions/12824/how-long-does-a-sunrise-or-sunset-take). Adjust to taste, I guess. Because of the network traffic generated to the Hue Bridge, and the responsiveness of the Hue bulbs (they take ~400ms to transition state/brightness by default), the sunrise interval defined in the script tends to run a little long. During my testing, a 5-minute interval actually takes roughly 6 minutes, while a test at 1 minute took just over 2 to complete. For a long-running script, it's probably not important, but it's not a bug - it's a feature.

2021-03-06:

- Update fakesun.py to include the bedroom downlights, _and_ get everyone using a cooler colour-temperature via setct(). It's a WIP, but I think the brighter, cooler light will more closely simulate a sunrise and wake me up a little better. As mentioned the other day - "adjust to taste" - here we are.


