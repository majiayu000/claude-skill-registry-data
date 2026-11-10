---
name: big-arrow
description: "Point at something on the human's screen (Windows, or Linux on X11) with a big arrow and a sign (\"Click Save: keeps your changes\") using the bigarrow CLI. Use whenever the human has to look at, click, type into or choose a specific spot, button, field, window, tab or menu: show me where, point to it, which button, where do I click, chỉ cho tôi chỗ nào, guide me through this UI, the human must approve or sign something, or you need the human's hand and they may not be looking at the terminal. Use it to teach when the human wants to learn how to do something in an app (Blender, Excel, Settings, ...): teach me, show me how, walk me through, dạy tôi, hướng dẫn tôi từng bước. Mandatory when it is time-critical: a code that expires, a login or payment page that times out, a build waiting on the human."
license: MIT
allowed-tools: Bash(bigarrow:*)
metadata:
  short-description: "Point at the screen with a big arrow and a sign"
---

# big-arrow

`bigarrow` (see-the-arrow) draws a click-through arrow with a sign, needs no permission and never
takes the focus. Point at the thing itself, a line in the terminal is easy to miss.

Two ways to use it:

- **Hand over one step.** You are doing a task and one click must be the human's: open the exact
  page or URL yourself, then point at the one control left. Do not walk them through menus.

  ```bash
  start ms-settings:privacy-webcam        # PowerShell: Start-Process ms-settings:privacy-webcam
  bigarrow start --element "Camera access" --app "Settings" --text "Switch this on: apps may use the camera" --say
  # watch for the result (page changed, job continued, file appeared), then:
  bigarrow stop
  ```

- **Teach.** The human wants to learn how: walk them through every step in the app, one arrow per
  step; they click, you look again. Do not open pages, run commands or click for them unless they
  ask: their hands are learning the way.

  ```bash
  bigarrow screenshot --window blender --png step.png --max-size 1280 --json   # look first
  bigarrow point --app blender --rect 318,64,36,25 --until-click --text "1. Click Add: new objects live here"
  bigarrow screenshot --window blender --no-raise --png step.png --max-size 1280 --json   # the menu is open now
  bigarrow point --app blender --no-raise --rect 318,95,204,22 --until-click --text "2. Then Mesh"
  ```

## Rules

- The sign is one full sentence naming the action ("Click Save", never "here"); start with the
  human's name only when you know it. When the click approves, grants, pays, signs, sends or
  deletes, add what happens: "Click Pay: 12 USD for the domain renewal". The human decides; the
  facts go on the sign, not only in the terminal.
- `--say` when the human may not be looking. Time-critical (code expires, page times out, job
  waits): `--color red --say` and say by when: "Enter the 2FA code now, it expires in 60 s".
- Something to paste (a command you may not run, a URL, a code): put it on the sign as
  `{{value}}`. The human sees the value on a copy button (no braces); one click copies all of it
  and the arrow stays. Point at where it goes: "Copy {{winget upgrade --all}} and paste it
  here", then check that it was pasted.
- One arrow per step; `bigarrow stop` the moment the step is done. Arrows also end alone: after
  300 s, when your session exits, when the human answers (hook below).
- A click on the sign or shaft, except a copy button, removes the arrow (target clicks pass
  through). A removed arrow was seen: check the result, do not redraw. Skip `--close-button`
  unless asked.
- A screenshot you read goes to your model provider. Capture only the window of the app you are
  pointing in (`--window "<App>"`), never the whole screen, and none at all while a password
  manager, a banking page or private messages are open.

## Teaching

- Look before every step: `bigarrow elements --app X` where the app names its controls,
  `bigarrow screenshot` where it does not. A click changes the screen (a menu opens, a dialog
  appears), so never point at step 2 from the picture you took before step 1.
- One `bigarrow point --until-click` per step. It returns when the human clicks the target
  (`dismissedReason: clicked` with `--json`); `timeout` or `closed` means they did not, so ask
  before going on. It waits up to 300 s: run it with a tool timeout of several minutes.
- Number the steps and keep each sign short: "2. Then Mesh". Add why when it helps them remember:
  "1. Click Add: new objects live here".
- A keyboard step has no button: point at where the keys act and name them: "3. Press Tab here:
  Edit Mode".
- Once the app is in front, pass `--no-raise` so bigarrow leaves its windows alone while a menu is
  open. If the next picture shows the menu closed (the human clicked elsewhere or switched
  windows), point at the step that opens it again.
- At the end, say what they did and the shortcut for next time, if there is one.

## Targets

| You know | Use |
|---|---|
| A label in a native, Electron or browser app | `--element "Allow" --app "Settings"` |
| An app or one of its windows | `--window "Notepad"` / `--window "Google Chrome:Inbox"` |
| A spot inside a browser tab | `--rect x,y,w,h --app "Google Chrome:<tab title>"` |
| A spot no label reaches (Blender, canvases, games) | `bigarrow screenshot --window "<App>" --png shot.png --max-size 1280 --json`, find it in the image, then `--rect` or `--at` with `--app "<App>"` |

Always pass `--app` (or `--window`) for a target inside an app: it is raised first and the arrow
hides while another app covers it. `App:title` matches a window title, else a tab. Apps match by
product name ("Google Chrome", "Settings") or executable ("chrome", "msedge"). Coordinates are
global top-left physical pixels, as UI Automation and `bigarrow screenshot` report them: image
pixel (x, y) is X = rect x + x * rect width / size width, Y likewise.
Roles: `button`, `textfield`, `checkbox`, `link`, `tab`, `menuitem`, `combobox`, ... Unsure?
`bigarrow elements --app X --match "allow"` or `--dry-run`.

## Errors

Exit 2 bad input, 3 target not found (the message lists what exists), 4 permission missing: run
`bigarrow doctor`. On Windows, 4 means the target app runs as administrator and bigarrow does
not: ask the human to restart that app normally, or to run your terminal as administrator. On
Linux it means a Wayland session or no accessibility bus; the message names the fix. If the app
cannot come to the front (Windows refuses to steal the focus), bigarrow warns, flashes its
taskbar button and shows the arrow once the window is visible.

More (settings pages, browser coordinates, look and timing flags): [reference.md](reference.md).

## Setup once

`~/.claude/settings.json`: `"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "bigarrow stop --hook"}]}]}`
