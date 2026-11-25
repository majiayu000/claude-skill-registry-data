---
name: record-mac-demo
description: Record a real screen-recorded demo on a Mac that your agent drives by itself, with zero manual clicks, on your own Mac (for example overnight) or on a second Mac without touching your screen. Use when you need authentic footage of an app or website actually running on macOS rather than a mocked-up animation, such as a product launch video, a custom demo for one specific customer or prospect, an install walkthrough, feature b-roll or a bug repro. Covers connecting over Screen Sharing (VNC) to the same or another Mac, clicking and typing, starting and stopping the macOS recorder, a timestamped action log that becomes the captions, clean-frame setup and pulling the files back.
---

# Record a real Mac demo

Your agent sits at a Mac and records itself using a product: it opens the app, clicks, types and
scrolls, and macOS records the screen at 60 fps. Nobody touches the mouse. Every action is written
to a log with its second in the video, so the captions for the edit are already done when the
recording stops.

Two setups, same scripts:

- **Your own Mac, while you are away.** The agent connects to your Mac's own Screen Sharing over
  `127.0.0.1`. Start it before bed or lunch; the takes are waiting when you are back.
- **A second Mac** (a Mac mini, a spare laptop). The agent drives it remotely and nothing appears
  on your screen, so you keep working.

What people record with it: launch demos, **a custom demo per customer** (their website, their
use case, their name in the prompt, one script run per prospect), install guides, and bug repros.

Real footage beats a rebuilt animation for one reason: viewers can tell. Use this whenever the
claim is "this works", and use motion graphics only for what a screen cannot show.

## What you need

- **Screen Sharing** on for the Mac that will be recorded (System Settings, General, Sharing).
  Its user is logged in at the console.
- **Same Mac:** run everything locally with `MACVNC_HOST=127.0.0.1`. Save your login password
  once for it, typed at the prompt so it never lands in your shell history:
  `security add-internet-password -s 127.0.0.1 -a "$USER" -w`
- **Second Mac:** **Remote Login** on too, reachable from where the agent runs (Tailscale or the
  same LAN), and an SSH login with passwordless `sudo` for `launchctl` (for `scripts/gui.sh`).
- The Screen Sharing password, saved once in your login keychain by connecting manually with
  Screen Sharing, or injected as `MACVNC_PASSWORD` into the controller's environment only.
  Never put it in a command line, a prompt or a log.
- `pip install vncdotool pillow` on the machine that runs the controller. `ffmpeg` anywhere you
  want check frames.

## Workflow

### 1. Attach and prove the screen exists (hard gate)

A Mac with no monitor has **no framebuffer** until a VNC client connects. Before that,
`screencapture` fails with `could not create image from display` and `caffeinate -u` does not
help. Start the controller first; its connection is the framebuffer.

```bash
MACVNC_HOST=100.64.0.5 MACVNC_USER=alice python3 scripts/macvnc.py &
curl -s 'http://127.0.0.1:8765/shot?out=/tmp/probe.png'   # must give a real 1920x1080 image
```

Look at the probe image yourself. If it is black, a login window or a lock screen, stop: logging
in at the console is a human step. Do not guess a password.

Do not use a Screen Sharing window on your own Mac to watch or drive the target. It takes your
mouse and focus, and it stops updating when covered or minimized.

**Same Mac, unattended:** the screen must stay awake and unlocked for the whole run, because a
locked screen blocks clicks and recording. Keep it awake for exactly the run and no longer:

```bash
caffeinate -dimsu -t 7200 &            # 2 hours; pick the length of the script
MACVNC_HOST=127.0.0.1 MACVNC_USER=$USER python3 scripts/macvnc.py &
```

Your own apps and windows are on camera, so close or hide everything private first, and do not
leave the Mac unattended in a place where an unlocked screen is a risk.

### 2. Set a clean frame

See `references/framing.md`. In short: one app window, about 85% of the screen, wallpaper visible
around it, every other app hidden, banners and popups closed, private sidebars collapsed, the app
in the language your audience reads. Take a `/shot` and check it before recording.

### 3. Record

The macOS recorder gives 60 fps, full resolution, and needs no permissions for your agent:

```bash
curl -s 'http://127.0.0.1:8765/key?k=super-shift-5'      # recorder toolbar
curl -s 'http://127.0.0.1:8765/shot?out=/tmp/bar.png'     # find the Record button, then click it
curl -s 'http://127.0.0.1:8765/click?x=<x>&y=<y>'
curl -s 'http://127.0.0.1:8765/log?path=/tmp/actions.tsv' # start the clock right after the click
```

Drive the demo, logging each step just before you do it:

```bash
a() { curl -s "http://127.0.0.1:8765/act?label=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$1")" >/dev/null; }
a "click: Copy setup link";      curl -s 'http://127.0.0.1:8765/click?x=1172&y=609'
a "type a goal";                 curl -s 'http://127.0.0.1:8765/type?t=Make%20a%20pitch%20deck'
a "press Enter";                 curl -s 'http://127.0.0.1:8765/key?k=enter'
```

Stop with `/key?k=super-ctrl-esc`. The file lands in the GUI user's recording folder (on macOS
26 `~/Recordings`, older versions the Desktop or the folder chosen in the toolbar's Options).

Write the whole take as one script with fixed `sleep`s between steps (see `references/framing.md`
for pacing), so a retake is one command and the log matches every retake.

### 4. Pull the file and check it

```bash
MAC_SSH="ssh me@100.64.0.5" GUI_USER=alice scripts/gui.sh 'ls -t ~alice/Recordings | head -3'
ssh me@100.64.0.5 'sudo -n cat "/Users/alice/Recordings/<file>.mov"' > take.mov
```

The file belongs to the GUI user, so read it through `sudo` or `chmod 644` it first. Extract a few
frames (`ffmpeg -ss 5 -i take.mov -frames:v 1 f5.png`) and look at them: right window, nothing
private, no stray dialogs. The `.mov` is H.264 and plays in a browser as is.

### 5. Leave the Mac as you found it

Delete the recordings and temp files you made, restore windows you moved, sign out of nothing,
quit nothing that was running before you came, and stop the controller. On a shared machine,
leftovers are the owner's problem; do not create them.

## Rules

- **Never fake footage.** If the gate fails or the product breaks on camera, report it. A retake
  is fine; a staged result is not.
- **Respect a shared machine.** If its owner is using it (recent console input, another Screen
  Sharing session), wait. Do not quit their apps, change system settings, or reboot. Do not touch
  the VPN or remote-access service that carries your own connection.
- **Mask secrets before anything leaves the machine.** API keys, account names and emails that
  appear on screen are blurred in the edit and checked frame by frame; any key shown in a demo is
  a throwaway that gets revoked when the video is published.
- **Hand over a link, not a file dump.** Upload takes somewhere your reviewer can stream them.

Driving gotchas are in `references/gotchas.md`. Read it before the first take; each item cost a
failed take.
