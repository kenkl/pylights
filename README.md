# pylights
### A Python frontend for Philips Hue Bridge

Experiments with using Python3 to replicate some of the behaviours that [Lights](https://github.com/kenkl/lights) has. In an ideal world, we'd maintain parity between lightkit.py and functions.php, but that's not especially critical right onow.

One conscious/deliberate difference is function naming. Although I generally follow the convention for [camelCase](https://en.wikipedia.org/wiki/Camel_case) in functions.php over there, I'm not doing that here with lightkit.py. As a general rule, I like to avoid [Bucky bits](https://en.wikipedia.org/wiki/Bucky_bit) at the CLI whenever possible. Lazy? Probably.

2021-03-02: Added fakesun.py - inspired by the inaugural issue of [Remotely Interesting](https://ckarchive.com/b/8kuqhohn5mnz%20), I wanted to make a couple lights in the bedroom (or wherever) do a simulated sunrise sequence - brightening over the course of a few minutes. That lead to the question "how long does a sunrise take?" - the answer is [complicated](https://astronomy.stackexchange.com/questions/12824/how-long-does-a-sunrise-or-sunset-take). Adjust to taste, I guess.

Because of the network traffic generated to the Hue Bridge, and the responsiveness of the Hue bulbs (they take ~400ms to transition state/brightness by default), the sunrise interval defined in the script tends to run a little long. During my testing, a 5-minute interval actually takes roughly 6 minutes, while a test at 1 minute took just over 2 to complete. For a long-running script, it's probably not important, but it's not a bug - it's a feature.


