---
name: computer-use
description: Read before looking at or acting on a screen (a desktop, an app, a person's own Mac, Linux or Windows desktop or Android phone, anything that isn't only a web page), by screenshot, click, type, scroll and keys, or when a Mac's or a phone's screen says Accessibility isn't on.
metadata:
  title: "Computer Use"
  subtitle: "Your AI uses a screen"
  about: "Lets your AI see a screen and use it with clicks, typing and keys, for any app, not only web pages. You can watch what it does."
  category: Agent tools
---

Computer Use is how you see a screen and act on it like a person: take a screenshot, then click, type, scroll or
press keys at what you see. Its person watches in the Computer Use app.

- `screens` lists the screens you can use: each one's name, what it is, its size, and what it was last used for.
  A person's own computer is one (below), so is their Android phone (below), and other apps bring more: a container made from the image `desktop` is one
  (Containers' `create`). If you have none, make one first. Two of the same name, from two apps, are named `app/name`. An app that
  couldn't list its screens (its machine is asleep, say) is in `failed`, with why, and the rest are still listed, as is
  a computer whose own screen didn't answer (`computer-use/<its name>`): each computer's screen is its own.
- `screenshot` shows the screen. x and y in every other tool are pixels of that picture, from its top left.
- `click` (button left, right or middle), `double_click`, `move`, `drag` (a path of points), `scroll` (up, down,
  left or right, by steps), `type` (text where the focus is), `key` (`ctrl+l`, `Return`, `ctrl+shift+t`; several,
  space between) act on it, and answer in a few words, not with a picture: take a `screenshot` to see what changed.
  `wait` waits up to 10 seconds, for a page to load, and gives a screenshot.
- Say what you're doing in `doing` ("Booking the 3pm train"): it's what your person sees you using it for.

Each step costs a screenshot, about a thousand tokens and a second or two, so it's slow and costly next to a tool
that reads. Use Computer Use for what isn't a web page, or a site that blocks automation. For a web page, the
Chrome app reads the page's text and clicks things by name: faster and cheaper. Press keys over hunting with the
pointer (`ctrl+l` then type a URL and `Return`, not clicking the address bar), and look again after anything that
loads.

A screen is its owner's: you use only your person's, and whatever is signed in on it is theirs. Don't sign in,
buy, send or delete there without them asking for it.

## A person's own computer

Each Mac, Linux or Windows desktop running Computer Use's service is a screen, called what the computer is called: its main
display, the one with the menu bar, with everything on it, signed in as its person. You act as them, so do only what
they asked.

Its person is likely using it as you work, so work in the background, on one app's window, and leave their screen,
pointer and keyboard to them. Use the whole display (the tools without `pid`, `window_id` or `element_token`, with their
own pointer and keyboard) only when a task truly needs it or they're away. These tools are Cua Driver's, by its names:

- `windows` lists windows (`app` or `pid` narrows it): each one's `window_id`, `pid`, `app_name`, `title`, `bounds`.
  Open the app you need in the background yourself rather than bringing one forward.
- `elements` (`pid`, `window_id`) reads a window's elements through accessibility, as rows `[N]`; the element's
  `element_token` is `<snapshot_id>:N`. `query` narrows a large window. A new read of the window replaces its tokens.
- `screenshot` with `pid` and `window_id` is a picture of that window alone, as it is behind whatever is in front.
  Windows can't picture a minimized window: read it with `elements` instead.
- `click`, `double_click`, `scroll`, `type` and `key` with an `element_token`, or with `pid` and `window_id` (x and y
  then in that window's own screenshot), act in the background: the window stays behind, and the person's pointer
  doesn't move. `set_value` sets a field, slider or pop-up menu's value by its `element_token`. Prefer an element to a
  point; a point is for what has no element (a canvas, a video).
- An action answers with Cua Driver's `effect` where it has one: `confirmed`, `unverifiable` or `suspected_noop`, and
  an `escalation` when it recommends another way. Check what it did on the next `elements` or window `screenshot`.
  Not every background input lands (a key press or a click in a text, in some apps; Chromium and Electron web
  content): prefer `type` and `set_value` with an `element_token`, and use the whole display only when nothing else
  does it.

Never act on a window the person didn't ask you to use. On Linux, background work needs X11 (or XWayland): on Wayland
itself one window can't be aimed at.

- Never type a password or a code (a one-time code, a passkey's PIN). Ask the person to type it themselves. On a Mac
  `type` refuses while a password field has the focus.
- A screenshot is the display scaled down to what a model sees unshrunk (at most 1568 pixels on its long side and
  about 1.15 megapixels). On a large display text is small: zoom in the app you're using (⌘+ in a browser) rather
  than guessing.
- A drag is a straight line: its `path` is two points, where it starts and where it ends.
- On a Mac, `ctrl` with a letter, digit or punctuation is ⌘, as a shortcut means there (`ctrl+l`, `ctrl+c`,
  `ctrl+t`), and with anything else ⌃ (`ctrl+Tab`). `super`, `cmd` and `meta` are ⌘, `alt` is ⌥, and `control` is
  always ⌃ (`control+c` in Terminal).
- A computer's own screen is live video too (`stream`, for a person's app). A Mac's goes through its helper, which
  macOS may ask about once more, to let it capture the screen directly.
- Windows and elements are a computer's own screen's only: another screen is used whole.

Only the computer's person, the user its server is for, and the network's owner may use it. A computer gets it with
`install_service --app computer-use --service ComputerUse.Desktop --server <key>`. The service runs Cua Driver
(trycua/cua) in its person's session: on a Mac a launchd agent, on Linux a systemd user unit that starts with their
desktop (an X11 or XWayland one), on Windows a scheduled task of theirs that starts as they log on. Until they're
signed in to it, `screens` says Cua Driver isn't running there. On Windows it runs as their limited user, as their
server does, so it can't use a window of a program run as administrator.

On a Mac it runs inside a small app, Computer Use for the One App, which macOS lets see the screen only with Screen
Recording and use the mouse and keyboard only with Accessibility, which only the Mac's person can allow. `screens`
says in the Mac's description which is missing, asking macOS nothing. The first time an action needs one, System
Settings opens on the Mac where it's turned on, and the action says what's missing, with the link that opens it there.
They allow it in System Settings → Privacy & Security → Screen & System Audio Recording, and → Accessibility, by
turning on Computer Use for the One App in each. macOS keeps that
through the app's updates and Cua Driver's, and asks again now and then for Screen Recording, as it does of every
app that records the screen.

## A person's own phone

Each Android phone or TV whose the One App has answered is a screen, called what its person called it as they signed it in:
its whole screen, as its person sees it. A phone runs no server, so its app does each action, through Android's accessibility service,
which only its person turns on: Settings → Accessibility → the One App. Until they have, `screens` says so in the
phone's description, and an action fails saying so while the phone tells its person how to turn it on. On Android 13
and later, an app that didn't come from a store is a restricted setting there: its person allows it first, under ⋮ in
the One App's App Info. Computer Use on a phone needs Android 11 or later.

- A tap is `click`, a long press is `click` with `button` `right`, and `double_click` is a double tap. A phone has no
  pointer: `move` refuses.
- `drag` is a finger down at its first point, through the rest, and up at the last: a swipe. `scroll` swipes the other
  way from where it scrolls, and stops where it ends.
- `type` puts text into the field that has the focus, where its selection is: tap the field first. It refuses a
  password field: ask the person to type it.
- `key` has only what Android gives: `Back` (or `Escape`), `Home`, `Recents`, `Notifications`; `Up`, `Down`, `Left`
  and `Right`, which move the focus as a D-pad does and say where it went; and `Return`, which is Return in a field and
  presses what has the focus anywhere else. Anything else refuses.
- An Android TV is driven as its remote drives it: move with `key` Up, Down, Left and Right, and press with Return.
  It has no touchscreen, so `click` moves the focus to what's there and presses it (`right` holds it), `scroll`
  scrolls what's there a page at a time, and `drag` refuses. In a web view's page (the One App's own pages too), a TV's
  WebView takes the focus but not the press: open what's focused there by asking its person to press OK.
- A phone whose app isn't running is still listed, saying so, and is woken by a push as it's used, which takes a few
  seconds; one that doesn't wake (off, offline, or notifications not allowed for the One App) says so. Only the
  phone's person and the network's owner use it, and you act as them, with their apps and accounts.

## Other apps' screens

An app with screens hooks into `computer-use.screens`: its hook's description (offers, in its code) says what it
answers and what its tool is called with.
