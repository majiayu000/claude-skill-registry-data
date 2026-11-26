---
name: iphone-simulator
description: Read before running an iPhone app for the user in Xcode's iOS Simulator, to install a simulator build, try a site in Safari on iOS, or look at and tap on an iPhone screen.
metadata:
  title: "iPhone Simulator"
  subtitle: "iPhones on your Mac"
  about: "Runs iPhones in Xcode's Simulator on your Mac, to try apps and sites on. Watch and use one live from any device, and let your AI tap through it."
  category: Agent tools
---

A simulator is an iPhone in Xcode's iOS Simulator, the newest iPhone Pro on the newest iOS the Mac's Xcode has, with
no window. `machines` lists the Macs that run them.

- `create` takes a `name` and what it's for (`description`), and boots it, which takes a minute or so. `list` shows
  yours, with each one's model, iOS version and state.
- `install` installs an app built for the simulator (`xcodebuild -sdk iphonesimulator`, not one for a real iPhone):
  its `.app`, zipped (`ditto -c -k --keepParent My.app My.zip`), uploaded (`app`) or from a `url`. `open_url` opens a
  URL in the app for it or Safari.
- A running one is a screen in Computer Use, called what the simulator is: look at it and tap on it there. A click
  is a tap, a right click a long press, a middle click the Home button, a drag a swipe, `scroll` swipes, and `type`
  types into what has the focus. Keys are as xdotool names them; super is ⌘.
- `stop` shuts it down: its apps and files stay, what was open doesn't. `remove` deletes it and everything on it.

A simulator is the Mac's own processes, run as the Mac's user, not a machine apart. It shares the Mac's network,
the Mac's 127.0.0.1 and every server on it among it, and an app in it can read what the Mac's user can: their files,
and the One App's own on that Mac. Nothing can stop either. Install only apps the user trusts, and never one to
test what an untrusted app does.

A simulator costs about 2 GB of memory while it runs. Stop it when you're done; one left running and unused for two
hours is shut down on the hour. Yours are yours: nobody else sees them but the network's owner.

A Mac runs simulators once its service is installed there: `install_service --app iphone-simulator --service
IphoneSimulator.Simulator --server <key>`. It needs Apple silicon, macOS 15, Xcode 26 with an iOS runtime, and uv,
and installs idb (Meta's iOS Simulator automation) the first time.
