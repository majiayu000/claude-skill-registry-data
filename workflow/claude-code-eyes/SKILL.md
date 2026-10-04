---
name: claude-code-eyes
description: Look at real hardware, screens, panels, and wiring on a desk or workbench through a camera, so Claude can SEE physical output that no unit test, log, or API can. Use whenever the user says "are you seeing this?", "olha isso", "look at this", "watch this", "can you see...", "check the camera", "look at the screen" / "look at the display", "is this wired right?", or "what's this part?"; asks to visually verify a rendered display, LCD, LED, or panel; wants a wiring, polarity, or voltage-rail check before power-on; or needs to confirm a font, layout, clipping, or on-screen value renders correctly instead of trusting green tests. Grabs the current camera frame(s) and reads them; supports a watch mode for an action in progress. Needs a snapshot-capable camera reachable over HTTP (Android IP Webcam app, Raspberry Pi camera-streamer, or any snapshot URL) set via CCE_CAM_URL.
---

# claude-code-eyes — let Claude look at the real world

Some outputs live where no test, log, or API can reach them: a display panel, an
LED, a breadboard, a rack of wires. This skill grabs the current camera frame and
lets you `Read` it, so you answer from what you actually see — not from what the
code *should* produce.

## How

1. Run: `bash <path-to-skill>/snap.sh` — it prints the path(s) of the captured
   JPEG/PNG. (It works from any directory.)
2. `Read` each printed path — the Read tool renders images visually.
3. Answer from the frame. Reference positions concretely: "the red wire on the
   left rail, third hole down", not "a wire near the top".

If a capture fails, read the error before retrying — it names the actual cause
and the fix. One case is worth knowing: Claude Code runs Bash in a sandbox that
blocks LAN addresses, so a camera your own terminal reaches fine can be
unreachable here. `snap.sh` detects that and prints the fix already filled in —
either approve Claude's offer to rerun the command outside the sandbox, or add the
printed `sandbox.excludedCommands` entry to `~/.claude/settings.json` (the network
allowlist does *not* cover private addresses). Frames are written under `./.claude-code-eyes/` in the working
directory, not `$TMPDIR`, because sandboxed commands and the Read tool resolve
`$TMPDIR` differently. See the README's Troubleshooting section.

**When you cannot read something, zoom instead of guessing.** If a label, marking,
or band is too small to resolve, do not report a guess and do not say the image is
too blurry — take another look:

```bash
bash <path-to-skill>/snap.sh --zoom 5    # then Read the new frame
bash <path-to-skill>/snap.sh --focus     # if it is soft rather than small
```

`--zoom` is a magnification from 1 to 10 and the previous zoom is restored
afterwards, so it is safe to reach for. Requires `CCE_CAM_TYPE=ipwebcam`; other
backends say so and still capture. Escalate deliberately: 1x to frame the scene,
then zoom to read the detail you actually need.

For **"watch this"** / an action in progress: `bash <path-to-skill>/snap.sh 3 2`
(3 frames, 2 s apart), then compare the frames and narrate what changed. Longer
processes: raise the count/interval.

## Visual-verify: catch what green tests cannot

A rendered screen is an output no unit test can see. This is the use case that
makes this more than a webcam grab.

**Workflow for any display/render change:**
1. **Before/after** — snap once before the change, once after, and diff the two
   frames.
2. **Against the source of truth** — take what the spec / API / expected string
   says the screen *should* show, and check the frame against it character by
   character, element by element.
3. **Report mismatches** — say exactly what differs, where.

**A small case library** (real bugs that every automated layer passed):
- **Font coverage / silently-dropped characters.** A 48 px clock font contained
  only `0-9 : . - a p m`; handed `~1h23min` it rendered **`1 24m`** — `~ h i n`
  were dropped *silently*. The bytes were valid ASCII and the test asserting ASCII
  passed; the narrow thing was the *font*. Only the camera caught it.
- **Text ↔ graphic collision.** With the text finally rendering in full, the tail
  of a number was drawn *underneath* a status icon sharing that row. It had
  already been misread as a pass once — look at the whole frame, not just the part
  you expected to change.
- **Clipping at a panel edge.** Text that runs past the usable width is truncated
  by the panel, not by your string — you only see it on the glass.
- **Stale vs live.** A frozen render can look identical to a live one. Confirm the
  screen reflects *now* (a value you just changed, a timestamp, a known-stale
  state that should read "offline"/grey rather than a frozen number).

Rule of thumb: **any change to a render path or a font is not "done" until a frame
confirms it.**

## Wiring-mentor: before you approve a power-on

When the question is "should I connect that?" / "is this right?", the frame is
checked against a plan, not eyeballed:

- **Check the frame against the build's wiring table** (the from-pin → to-pin
  contract). Call out **every** mismatch.
- **Wire-color discipline** helps a photo be checked against a plan (e.g.
  red = 3V3/5V, black = GND, other colors per signal).
- **Verify polarity and voltage rails before saying "power it on":** no 5 V on a
  3.3 V-only pin (many MCU GPIOs, e.g. ESP32, are NOT 5 V-tolerant); check battery
  / JST polarity (reversed connectors are a classic release-the-smoke gotcha).
- **Safety rails:** a relay/module switching **mains** → stop and involve a
  qualified human. Don't hot-plug camera ribbons or delicate connectors.
- **Too far or too blurry to read pin labels? SAY SO and ask for a closer aim.**
  Never guess a pin you cannot read.

## Know what your instrument can and cannot see

The camera is an instrument, and so is every other tool you trust. A blank result
is **not** a negative result until the instrument itself is proven working. Three
ways the same lesson bit in one session:

- **A tool that was never installed.** `tcpdump` returned empty because it wasn't
  on the box, and `2>/dev/null` turned "command not found" into a convincing clean
  capture — which became a confident, wrong root cause that had to be retracted.
- **A log for a code path that logged nothing.** Silence from a serial log read as
  "it didn't happen" when the path simply emitted no line.
- **A correct behavior invisible in the data.** A correct de-duplication leaves the
  database byte-identical to "nothing happened" — the only evidence was on the
  device and in the response, not in the store.

So: when a frame looks blank, empty, or unchanged, first ask whether the camera is
actually pointed, focused, and capturing — prove the instrument before you trust
its silence.

## Config

Set a camera endpoint (highest precedence first): exported env vars, then a
`.cce.env` in the current directory, then
`${XDG_CONFIG_HOME:-$HOME/.config}/claude-code-eyes/config`. Config files only
fill values you haven't already exported; they are read, never executed.

| Key | Meaning |
|---|---|
| `CCE_CAM_URL` | Camera URL (interpreted per `CCE_CAM_TYPE`) |
| `CCE_CAM_AUTH` | Optional HTTP basic auth `user:pass` |
| `CCE_CAM_TYPE` | `ipwebcam` \| `camera-streamer` \| `url` (default `url`) |

Backends:
- `ipwebcam` — Android **IP Webcam** app: `GET $CCE_CAM_URL/shot.jpg`.
- `camera-streamer` — Raspberry Pi camera-streamer: `GET $CCE_CAM_URL/snapshot`.
- `url` — **generic**: `GET $CCE_CAM_URL` exactly as given (any snapshot URL).

A local USB-webcam grab via `ffmpeg` is possible but **experimental / untested**
(it needs camera permission granted to your terminal); see the README. The
supported, portable path is a snapshot URL via one of the backends above.

## Troubleshooting

If nothing is reachable, `snap.sh` prints exactly which type + URL it tried. Common
causes: the phone app or Pi server isn't running, the IP or port changed, HTTP
basic auth is required (set `CCE_CAM_AUTH`), or you're not on the same network.
