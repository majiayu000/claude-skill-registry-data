---
name: android-emulator
description: Read before running an Android app or an Android phone for the user, to install an APK, try a site on Android's Chrome, or look at and tap on an Android screen.
metadata:
  title: "Android Emulator"
  subtitle: "Android phones on your own machines"
  about: "Runs Android phones in Google's emulator on your own computers, to try apps and sites on. Watch and use one live from any device, and let your AI tap through it."
  category: Agent tools
---

An emulator is an Android phone (Android 16 with Google Play, a Pixel 8's screen) in Google's Android Emulator, on
one of the user's machines, with no window. `machines` lists the machines that run them.

- `create` takes a `name` and what it's for (`description`), and starts it, which takes a minute or two (longer the
  first time on a machine, which may install the Android SDK first), with Chrome's first-run prompts already answered. `list` shows yours and their state.
- `install` installs an APK, uploaded (`apk`) or from a `url`, granting what it asks for. `open_url` opens a URL in
  the app for it or Chrome. `shell` runs a command in the phone (adb shell): `logcat -d -t 200` is its log.
- A running one is a screen in Computer Use, called what the emulator is: look at it and tap on it there. A click is
  a tap, a right click a long press, a drag a swipe, `scroll` swipes, and the key `Escape` is Back. `type` types
  into what has the focus, ASCII only.
- `stop` saves what it was doing, and `start` carries on from there in seconds. `remove` deletes it and everything
  on it.

On Linux a phone has a network of its own: it reaches the internet but nothing on its machine, not even its
127.0.0.1. On a Mac the emulator's own network gives its apps the Mac's 127.0.0.1 at 10.0.2.2, and nothing can stop
that: install only apps the user trusts there.

An emulator costs about 2 GB of memory and a CPU or two while it runs. Stop it when you're done; one left running and
unused for two hours is stopped on the hour. Yours are yours: nobody else sees them but the network's owner.

A machine runs emulators once its service is installed there: `install_service --app android-emulator --service
AndroidEmulator.Emulator --server <key>`. It needs KVM and pasta on Linux, or a Mac, and Java.
