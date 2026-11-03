---
name: opendesigner-preflight
description: Checks anything visual before export or sharing (a video, page, deck or UI) for the silly mistakes that make it look cheap or wrong. Use before any render, export or publish.
license: MIT
compatibility: Python 3.10+ (standard library, no network) for the helper. ffmpeg and ffprobe for the video, frame and audio checks.
metadata:
  version: "0.1.0"
  homepage: "https://github.com/ckryptickunal/OpenDesigner"
---

# OpenDesigner: preflight

Passing a linter is not the same as looking good. A composition can pass every automated check and still read as cheap. This skill is the last look before anything leaves the building, and it starts one step earlier than most checklists: with the design system.

## 1. System first

Before judging the output, ask whether it was built on a design system **made for this artifact**.

- No system, or a look copied from one existing image? Stop and make one with the `opendesigner` skill (the 5-question sketch is enough), even for a video or a deck. A video is a surface like any other.
- Map the system to the medium instead of using UI sizes directly. Work out the viewing scale: a 1920 px frame watched 390 pt wide on a phone is shown at 390 / 1920 ≈ 0.2. Text that must be read needs about 11 pt there, so at least about 54 px in the frame (56 px or more for captions). Anything inside a scaled container, such as a canvas drawn at half size, shrinks with it. Take easing and durations from the motion tokens. Write the mapping down next to the artifact.
- Study real references before building (Mobbin, the taste poll, shipped products), not your memory of them. Note what the premium ones do that yours does not.

## 2. Run the helper

```
python3 scripts/preflight.py html index.html --medium web       # sizes (tokens and rem included), the token scale, tracking, fonts, small text, <br>
python3 scripts/preflight.py video out.mp4 --ignore 0-17          # frozen time (with timestamps), black frames, flashing, audio, length
python3 scripts/preflight.py frames out.mp4 --every 0.5 --out frames/   # full-size frames plus phone-size copies
python3 scripts/preflight.py audio audio/*.wav                    # clicks and noise bursts at clip edges
```

`--medium` sets the smallest text allowed: `web` 12 px for text people read (11 px warns, under 11 fails), `app` 11 pt, `watch` 12 pt (app and watch pages laid out at the device's width in points), `video` about 54 px in a 1920 px frame (under 40 fails). The `html` check reads the page's CSS, including linked token files, not the rendered page. It cannot see text over glass, photos or gradients, or text inside a scaled container: the checklist covers those.

The `video` check also measures flashing against WCAG 2.2 SC 2.3.1, the general flash threshold: no more than 25% of a 10-degree field may flash more than three times in a second. The field is worked out from the video's size for a 13-inch tablet at 25 cm, the closest likely viewing (`--flash-field phone`, or a size in px, for others). Over the limit is an error, and over 90% of it is a warning, to leave a margin for re-encoding. `--flash-where worst.png` saves the worst moment with the flashing pixels in magenta. It runs in ffmpeg, takes about 0.6 times the video's length on a 10-core Mac, and measures the whole video, ignored sections included. It does not measure red flashes (checklist item 49).

It exits 1 when it finds an error. It never edits anything and needs no network. Use `--ignore start-end` (seconds, repeatable) for a section that is deliberately bad, such as a "before" act, and say so in the report.

## 3. Look at full size

Thumbnails and contact sheets hide most of these mistakes. Open frames at 100% and crop type at 200%. Then open the phone-size copies (390 px wide) and read every label that carries meaning. Wherever text sits on glass, a photo or a gradient, measure its contrast against the rendered pixels (checklist item 11).

## 4. Walk the checklist

Go through `references/checklist.md`: type, layout, motion, truth, sound and process. `references/mistakes.md` explains each mistake: what it looked like when it really happened, why it happens, and how to catch it.

## 5. Report, fix, re-run

Report each finding with its time or place, the evidence (frame path or measurement), the rule it breaks and a severity:

- **S1, broken or wrong:** unreadable, clipped, false or contradicting itself. Fix before anyone sees it.
- **S2, reads as cheap:** monotony, imbalance, drift from the system, sync slips.
- **S3, polish.**

Fix, then run the helper and the checklist again. Say what you could not check.

When you find a mistake that is not on the list, add it to `references/mistakes.md` and `references/checklist.md` in this skill's source (`skills/opendesigner-preflight/` in the OpenDesigner repo), then run `python3 tools/sync_skills.py`.

If something in OpenDesigner itself was missing, wrong or confusing, record it with `engine.py feedback "..." --kind gap|bug|confusing|idea` (`references/improve.md` in the opendesigner skill). Nothing is posted without the person's OK.
