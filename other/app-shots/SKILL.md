---
name: app-shots
description: Take screenshots of the Kaeri apps and run UI checks safely - Apple and Android shots scripts, scenes and fixture ids, emulator and Simulator rules, and click tests. Use when capturing screens, comparing with design boards or measuring frames.
---

# App screenshots and UI checks

## Apple

```bash
caffeinate -u apple/scripts/shots.sh <mac|iphone|ipad> [--landscape] [shot…]
```

- A shot is a scene and optionally a screen: `watching` (default), `fresh`, `sourceless`, then
  `:calendar`, `:seasonal`, `:search`, `:library`, `:downloads`, `:providers`, `:pluginStores`,
  `:settings`, or `title=<id>`, `query=<words>`, joined with `+` (`pane=`, `sheet=`,
  `showcase=`, `watched=<id>:<episodes>`). Player states: `player-playing`, `player-skip`,
  `player-up-next`, `player-picture-in-picture` and so on. Read the script's header for all.
- Output goes to `apple/.shots/` (git ignores it). Mac shots come out white while the display
  sleeps, hence `caffeinate -u`. `--landscape` and a clean 9:41 status bar are built in for iPad.
- `KAERI_SIMULATOR` picks the Simulator. Create your own and delete it after; never shut
  down others' (no `simctl shutdown all`).

## Android

```bash
android/scripts/shots.sh <phone|phone-37|tablet|fold> [shot…]
```

Same shot syntax: `watching`, `fresh`, or `app` (real AniList), then `:calendar`, `:seasonal`,
`title=<id>` and so on. Roborazzi JVM shots (`:ui` tests) cover most boards without an emulator.

## Fixture ids

Made-up titles only: 900001–900006 (the base fixtures), 920001–920014 (a 12-season franchise
with a film and an OVA). Never real shows.

## Rules

- Only the Fixtures app or a re-identified copy runs. Never launch `app.kaeri.app`; never post
  real notifications on the Mac.
- One emulator at a time, your own AVD name and port, selected by `-avd`/`-port` in any script
  (including `taskpolicy -b` throttling for phone-speed timing). Stop it when done.
- Anything that moves the pointer on the maintainer's Mac needs their go-ahead, must act only
  when our window is in front, and must restore their windows. The Mac player XCUITest runs in
  CI only.
- Measure frames on release-like builds (R8, not debuggable); debug builds mislead.
