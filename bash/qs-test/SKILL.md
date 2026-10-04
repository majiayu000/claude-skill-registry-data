---
name: qs-test
description: Live-test the user's running Quickshell (bidshell) like a real user - glide the real mouse, click and type, find items by QML id / type / text through Qt's QML debugger, check state, take cropped screenshots on both monitors, and read the logs of every step. Use this whenever you changed anything in the quickshell config and need to verify it, when the user asks to test / check / verify / "try it" / "see if it works" for the bar, sidebar, popups, notifications, OSD or any other shell UI, when hunting a UI bug, or before telling the user that a shell change works - even if they do not say "test".
---

# qs-test

Test the live shell the way the user uses it: real pointer and keyboard events, both monitors, every
state looked at, every log line read. The goal is to find bugs before the user does; a missed bug costs
far more than extra screenshots or tokens, so look at things instead of assuming.

Everything goes through `scripts/qstest.py` (run it with `python3`). `scripts/qmldbg.py` is its client
for Qt's QML debug protocol; you do not call it directly.

## How it works (so you can reason about failures)

- `start` restarts quickshell as `qs -d --debug 47777`. That debug port gives the full live object tree
  (QML ids, types, file:line) and lets JS run on any object. The shell itself contains no test code.
- The port listens on **every network interface**: anyone on the LAN could run code in the shell while it
  is open. So `end` restarts qs without it, and `start` arms a watchdog that does the same after 30 min.
  Always finish a session with `end`, also after a failure.
- The mouse moves like a hand (ease-out glide, ~0.5 s, real `ydotool` events), because instant jumps skip
  hover and motion events that real bugs depend on. Keys: `wtype` for text and Esc into shell surfaces,
  `ydotool` for Hyprland keybinds (wtype cannot trigger compositor binds).
- A guard stops any move if the cursor is not where the last move left it: the user took the mouse.
  Stop, tell the user, and wait for them before `start` again.
- `start` plays `assets/testing.mp3` (the user's chosen sound) to the end before anything moves, so the
  user knows to let go of the mouse (falls back to a notification if it cannot play).

## Session

```bash
# a function, not Q="python3 ...": zsh does not word-split variables
Q() { python3 /home/bida/dotfiles/.config/quickshell/.claude/skills/qs-test/scripts/qstest.py "$@"; }
Q start                        # sound, restart qs with the debug port, arm guard + watchdog
Q test "sidebar vpn row"       # one test = one behaviour; marks the log
...steps...
Q done                         # all log lines this test made
Q end                          # restart qs normally (closes the port)
```

Run the steps as a `batch` (one step per line, as you would type them after `Q`): one Bash call and one
process for a whole group of tests. A step takes about 50 ms plus its glide; the slow part is your own
turns between calls, so put as many steps as you can in one batch and look at one sheet:

```bash
Q batch --keep-going --sheet <<'STEPS'
test calendar popout
click type:ClockButton@DP-3
wait type:ClockButton@DP-3 calendar.visible
shot type:CalendarPanelContent@DP-3
key Escape
done
STEPS
```

A batch stops at the first FAIL, or goes on with `--keep-going`; it always stops when the guard stops it.
`--sheet` joins all shots of the batch into one labelled image and prints `SHEET path`; read that one image,
and crop a shot at full size when you need detail. `--open` also shows it on the user's screen - only when
they asked, since the viewer can take the focus the next steps need.

Get one case right before running a matrix: check it fully (look at its shots, fix what is wrong), then run
the other edges, monitors and settings. A matrix run on a broken case only multiplies the same failure.
Between tests, bring the UI back to a known state (Esc, close the sidebar) so a test never depends on
the previous one.

## Selectors

- `#fortiRow` - QML `id` (stable, unique; read the QML file to find ids). Ids come from the debugger's
  object tree, which does not hold items made by a `Repeater` / list delegate: reach those by type or text.
- `type:ToggleTile` - every on-screen item of that QML type, found in the visual tree, so list rows work too
  (inline components use their own name, e.g. `type:Tile`). `eval 'type:X' EXPR` runs on the first one.
- `Bluetooth` - text / `label` / `title` / `placeholderText` / tab name, exact; `~blue` = contains
- An optional index picks the Nth match: `click Bluetooth 1`
- `@SCREEN` limits a selector to one monitor: `click VPN@HDMI-A-1`, `eval '#sidebarWindow@HDMI-A-1' 'visible'`.
  Per-monitor components (`Variants`: bar, sidebar, notification popups) exist once per monitor with the
  same id; without `@SCREEN`, `eval` uses the visible instance and `find` lists all (with their monitor).

The pointer lands on sub-pixel positions (QML may see 1400.59 where `hyprctl cursorpos` says 1400), like
a real mouse: compare pixel sizes that come from pointer positions with a tolerance of 1 px.

Only items really on screen match: hidden, zero-size or scrolled out of a clipping parent do not.
Selectors look inside every visible shell window, whatever its type is called (`CalendarPopout`, `TrayMenu`).
Tooltips show after a delay (500 ms): `wait #vpnTooltip visible` before the shot.
Clicks and shots wait until the item stops moving (slide-in animations).

## Steps

| step | what |
|---|---|
| `click SEL [N] [--right]`, `hover SEL [N]` | glide to the item's center, click / only hover |
| `move X Y [--click]` | glide to global logical coordinates (same space as `hyprctl cursorpos`) |
| `wheel N` | scroll N steps where the pointer is (N > 0 up, N < 0 down) |
| `drag X1 Y1 X2 Y2` | press, glide holding the left button, release (selections, sliders, drag and drop) |
| `key Escape`, `type "text"` | keyboard into the focused shell surface |
| `bind super+space` | Hyprland keybind with real key events |
| `wait [#id] EXPR [--timeout=S]` | poll until the JS expression is truthy (use instead of `sleep`) |
| `expect [#id] EXPR` | check once; prints `FAIL ... <value>` |
| `see SEL` / `gone SEL` | wait until an item is / is not on screen |
| `eval [#id or type:T][@SCREEN] EXPR` | print any value, e.g. `eval 'Settings.sidebarSelectedTab'`, `eval 'type:SelectionWindow@DP-3' 'regionWidth'` |
| `shot SEL [N] [PAD]`, `shot-screen DP-3` | cropped / full screenshot, taken once the picture stops changing; prints the path - then Read it |
| `shot-rect X Y W H` | area in global logical coordinates, for popups and tooltips without a good selector |
| `find SEL` | list matches (x y w h) |
| `reload [FILE]` | after editing QML: wait until qs reloaded (touches FILE if not) |

JS runs with ShellRoot as scope (singletons such as `Settings`, `Notifications`, `Audio` work), or with
the object named by `#id` as scope (its own properties: `expanded`, `text`, `visible`...).
Focus sits on the innermost control: `InputField` is a wrapper, so `activeFocus` on it is false while its
inner TextField has focus - check `Window.activeFocusItem` or the inner field instead.

Every step prints the WARN / ERROR lines it caused (`LOG ...`), also when it fails. Read them: a step
that "worked" but logged a TypeError is a bug.

## Method

1. **Read the QML first** to know ids, types and what each state should look like.
2. **Every monitor.** Run `hyprctl monitors` first: each monitor has its own copy of the bar, sidebar
   and popups, so test on each (`@SCREEN` picks the copy). A monitor with a fractional scale (1.2, 1.5)
   finds its own bugs: blurred or 1 px off captures, sub-pixel positions. The sidebar opens on the
   focused monitor: `move` onto a monitor before `bind super+space`. In `hyprctl monitors`, x/y are
   logical but width/height are physical pixels: divide them by the scale.
3. **Screenshot every important state and look at each one** (open, expanded, each tab, each popup):
   clipping, overlap, wrong colors, wrong alignment, cut text only show in images. Text checks
   (`expect`, `wait`) add to screenshots; they never replace them.
4. **Check the state you cannot see** with `expect` / `eval` (selected tab, expanded, search text).
5. **Read `done` for every test**, not only warnings: wrong data (for example a brand lookup returning a
   wrong domain) shows up in INFO/DEBUG lines.
6. **Watch what the test does to the rest of the desktop.** Keys and clicks can reach the app under a
   closing popout (for example Esc leaving a video's fullscreen). Compare the windows (`hyprctl clients`)
   before and after, and report any change you did not ask for.
7. **Go for the edges**: long names, empty lists, many items, fast repeated open/close, Esc from a
   focused field, click outside, switching tabs back and forth, theme change while open.
8. Report every bug with the step, the screenshot path and the log lines.

## Do not

`click` refuses system toggles (quick-toggle tiles, power buttons, Connect / Disconnect / Clear All) unless
you add `--force`, which you only do when the user agreed. Text selectors are ambiguous: "Bluetooth" is
both the Bluetooth tile and the Bluetooth tab (`find` first, then pick the index / type).

- Type real passwords, or click Connect / Disconnect (Wi-Fi, VPN, Bluetooth), power actions (shutdown,
  reboot, logout, suspend), Clear All, or toggles that change the system (Wi-Fi, Bluetooth, airplane,
  HDR, DND, idle) without the user's OK. They change the user's machine, not only the UI.
- Lock the screen (you cannot unlock it).
- Judge animations: frames and feel need the user's eyes. List them for the user to check.

## Known limits

- Qt's `LIST_OBJECTS` answer is corrupt after reloads (it counts invalid child contexts but does not
  write them); the client only scans it for the ShellRoot id and gets everything else from `FETCH_OBJECT`.
- AT-SPI does not work: Quickshell exposes no windows on the accessibility bus.
- Layer windows (bar, popouts) cannot know where the compositor put them; positions come from the one
  `hyprctl layers` surface with the window's size. xdg popups (bar tooltips, `PopupWindow`) are not layers:
  their positions are only Qt's guess, so find them without `@SCREEN` and check them on a screenshot.
- Before switching workspaces in a test, look at what is on the target workspace: an app that grabs input
  (Remmina, a VM, a game) takes the keyboard and the pointer.
- State and screenshots live in `$XDG_RUNTIME_DIR/qstest/`; `start` clears the screenshots.
