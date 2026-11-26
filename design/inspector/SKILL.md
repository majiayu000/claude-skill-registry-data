---
name: inspector
description: Read before checking or driving an app's window (one drawn natively, not in a web view) on one of the user's devices, to read its tree, tap, type, snap a picture or control its clock.
metadata:
  title: "Inspector"
  subtitle: "Your AI checks an app's screen"
  about: "Lets your AI read an app's screen on your devices as a test would, and tap, type and take pictures of it, to check it works."
  category: Developer tools
---

An app's window on a computer is drawn natively, and Inspector reads and drives it the way a test does: by
what's in it, not by pixels. It's faster and surer than Computer Use for these windows; use Computer Use for anything
else.

- `windows` lists the native windows open on your devices: each one's `device`, `window`, the `entrypoint` it shows
  (`notifications`), its size, and its clock. Every other tool takes `device` and `window` from there, and needs
  neither when only one is open.
- `tree` gives the semantic tree, each node's id, role, name, value, states, actions and `rect` (CSS pixels from the
  window's top left). `query` finds nodes by `role`, `name` (exact), `text` (words in the name), `key` or `node` (its
  id), with their rects and styles: start here rather than with a picture.
- `tap` presses a node by the same selector, or what's at `x` and `y`. Tapping a row's text presses the row. A tap on a
  node waits for it to be there, drawn, still and not under something else, a second unless `timeout` says, so tap
  what a press just opened at once, without a `settle` first.
- `type` types `text` into an input (by `role`, `name`, `key` or `node`), or the one with the keyboard. `key` presses
  `Enter`, `Escape`, `Tab`, `Backspace`, a letter.
- `settle` waits until the app has heard back from whatever it asked and its timers are done, and says what's still
  pending if its `deadline` passes first. Settle after an action before you read or snap.
- `close` closes the window as its system does (its close button, ⌘W or Alt-F4): what a person does to an app's
  window, which a launcher's put away instead.
- `snap` takes a PNG of the window. `clock` pauses, steps or seeks the app's clock, for what moves or waits on time.
- `profile` checks what moves, and what's slow: it pauses the clock, steps it to each time in `at` (ms from now, 0,
  80, 200 and 400 unless you say), and gives a picture of each frame there with what it cost: the JS `mutations`
  applied since the frame before, `layout_ms` and `paint_ms` (styling, layout and painting all told), GPU `draws`
  and the glyph `atlas`'s use. Tap what starts the motion, then profile at once. A frame where nothing changed costs
  nothing. The clock stays paused: resume it with `clock`.
- `replay` checks how a gesture moves: a press goes down on a node (or at `x`, `y`), moves along `moves` (each
  `{dx, dy, ms}`, one with neither holding still) and lifts, on the paused clock, every frame of a display `hz` (60,
  or 120) times a second drawn until it comes to rest, each with its cost, its GPU `work`, where `track` (a selector)
  was drawn and how far what scrolls shows scrolled, and how many went `over` their budget. A fling is a short quick
  move (300 px in 80 ms), a rubber band one past a list's end. `bun animation.js` in `clients/app/renderer/tests` of the One App's repo plays the same on
  a scene, with no window, and judges it against kinds of devices.
- `host` checks the device's host keeps the renderer's contract: a tick each display refresh, a frame presented each
  tick while something moves, nothing while still, and inputs with the device's own times. Move the pointer over the
  window while it runs (a second and a half).
- `record` gives every input the window gets for `ms` (5 s unless you say), each as it came (`touch`, `move`, `down`,
  `up`, `wheel` with a trackpad's phase and momentum, `key`), timed by the device: save its `events` as a JSON file
  beside a scene's and play them headless as a check's or a motion's `trace`. Someone uses the window as it runs.

A device is its person's: you inspect only theirs. Tapping and typing act as they would, so don't send, buy or delete
there unless they asked.
