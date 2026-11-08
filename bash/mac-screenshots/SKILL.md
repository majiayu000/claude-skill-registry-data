---
name: mac-screenshots
description: Take screenshots and screen recordings on a Mac from the shell — full screen, one display, a region, one window without its shadow, silently — then resize, convert or PDF them with sips. Use when you say "screenshot my screen", "grab that window", "record the screen for 10 seconds", "make this image smaller", "convert HEIC to JPG", "turn these PNGs into a PDF", "why is my screenshot black". Covers screencapture flags, getting a window id, the locked-screen and permission tells, and sips recipes.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: screencapture, sips, osascript (JXA). No network. Capturing other apps' windows needs the Screen Recording permission.
metadata:
  grounded: "2026-11-03 — capture, sips resize/convert/PDF run live on macOS 26.6; region/window capture hit the locked-screen failure described below"
---

# Screenshots and image conversion

## Capture

```bash
screencapture -x out.png                  # whole main display, no shutter sound
screencapture -x -D 2 out.png             # second display (-D 1 is main)
screencapture -x -t jpg out.jpg           # format: png (default), jpg, pdf, tiff, heic
screencapture -x -R 0,0,1280,800 r.png    # region x,y,w,h in points from top-left
screencapture -x -o -l <windowid> w.png   # one window, -o = no drop shadow
screencapture -x -T 3 out.png             # 3 s delay
screencapture -c                          # to the clipboard instead of a file
screencapture -i out.png                  # interactive: a human drags a box (blocks)
screencapture -v -V 10 rec.mov            # record 10 s of screen video
```

- **Always pass `-x`** in scripts; otherwise the shutter sound plays on the user's speakers.
- Output is in **pixels**, regions are in **points**. On a Retina display a full grab is
  2x the point size (a 1728x1117-point screen gives 3456x2234 px).
- `-D 2` on a one-display Mac fails with `Invalid display specified. Only 1 display` and
  writes nothing; check the exit code.
- `-i` and `-w` wait for a human. Never use them unattended.

## Get a window id for `-l`

```bash
osascript -l JavaScript -e 'ObjC.import("CoreGraphics");
var l = ObjC.castRefToObject($.CGWindowListCopyWindowInfo(1|16, 0)), o = [];
for (var i = 0; i < l.count; i++) { var w = l.objectAtIndex(i);
  if (w.objectForKey("kCGWindowLayer").js == 0)
    o.push(w.objectForKey("kCGWindowNumber").js + "\t" + w.objectForKey("kCGWindowOwnerName").js); }
o.join("\n")'
```

Layer 0 = normal app windows, frontmost first. Window *titles* are only present when the
responsible app holds Screen Recording.

## When the image is wrong

| Result | Cause |
|---|---|
| Solid **black** full-screen image (exit 0) and `could not create image from rect` / `from window` for `-R` / `-l` | **The screen is locked or the display is asleep.** Verified on a Mac whose terminal did hold Screen Recording. Check `ioreg -n Root -d1 -a \| grep -A1 CGSSessionScreenIsLocked`. Wait for the user, or keep the display awake while they're present (`caffeinate -d`). |
| Desktop wallpaper and menu bar, but no app windows | The responsible app lacks Screen Recording. See `mac-permissions`. |
| Captures fine in Terminal, black from a LaunchAgent | The agent's binary lacks Screen Recording, or it ran while locked. |

Look at a small copy before trusting a capture: `sips -Z 300 out.png --out thumb.png`.

## sips: resize, convert, PDF

```bash
sips -g pixelWidth -g pixelHeight in.png               # dimensions
sips -Z 800 in.png --out out.png                       # longest side to 800 px, keeps ratio
sips --resampleWidth 1200 in.png --out out.png
sips -s format jpeg -s formatOptions 70 in.png --out out.jpg   # quality 0-100
sips -s format jpeg in.heic --out out.jpg              # HEIC to JPEG
sips -s format pdf in.png --out out.pdf                # one image -> one-page PDF
sips -r 90 in.jpg --out rotated.jpg
for f in *.heic; do sips -s format jpeg "$f" --out "${f%.heic}.jpg"; done
```

- Without `--out`, **sips overwrites the input in place**. Always pass `--out`.
- `Warning: x not a valid file - skipping` means the input doesn't exist or is empty
  (often an earlier capture that failed). sips still exits 0 here; check the output file.
- Several images into one multi-page PDF: sips can't. Convert each to PDF, then join with
  the tool macOS ships inside an Automator action (present and working on macOS 26):

  ```bash
  J="/System/Library/Automator/Combine PDF Pages.action/Contents/MacOS/join"
  for f in *.png; do sips -s format pdf "$f" --out "${f%.png}.pdf" >/dev/null; done
  "$J" -o combined.pdf page1.pdf page2.pdf page3.pdf
  ```
