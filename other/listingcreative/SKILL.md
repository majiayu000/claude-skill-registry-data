---
name: listingCreative
description: Make a listing's photos as a scene, an action, a before and an after, in the composition of winning junk removal creatives, generate each frame once, then show them inside the iPhone Photos viewer with the town in the title and faces scribbled out in red. Use when the owner asks for new creatives, photos for a listing, a before/after, or to "put them in the camera roll".
---

# listingCreative

How a listing's photos are made. The words are `listingCopy`'s job; this is the
pictures. The research behind it is in the workspace's
`RESEARCH/JUNK_REMOVAL_CREATIVES/`: `creatives.jsonl` (58 winner frames, one per
line, from real Craigslist and Marketplace junk removal listings),
`CREATIVE_RUBRIC.md`, `subqReading.json` (what SubQ says a winner is) and
`spinOuts.jsonl`.

## Hard boundaries

- **The owner's concept comes first.** Never judge or replace the owner's creatives; build on
  them. Report what the winners show as data, never as a verdict on that work.
- **No text and no logos inside a generated image.** No letters, numbers, brand
  names, signs, number plates or printed paper. Every prompt says so and every
  avoid list repeats it.
- **No phone or interface words in a prompt.** "Shot on an iPhone" made the
  model draw a Photos app screen into the picture (Verizon, a clock, a date bar).
  Prompt the photo only; the phone around it is `photosViewer.html`.
- **No vehicles in any frame.** No car, truck, pickup, trailer or dumpster,
  parked in the background or part of the job (the owner, 2026-10-23: every made shot
  with a car in it came out wrong). The action is the crew carrying things out,
  a dolly at most. Every prompt says "no cars, trucks or trailers anywhere in the
  frame" and every avoid list repeats it.
- **Generate each frame once, then show the owner.** Never regenerate on your own
  judgement. Generation costs money (rule 41): ask before anything the owner didn't say.

## The rubric: scene, action, before, after

What SubQ read from the 58 winner frames (`subqReading.json`, 2026-10-23):

| | Winners |
|---|---|
| Scene | an interior room or a side yard along a fence, then a garage |
| Action | crew mid-job (99%); never a vehicle (below) |
| Before | a room's or a yard's worth of junk (95%), raw phone snapshot (95%) |
| After | the exact same spot and angle (99%), bare (88%) |
| People | a homeowner almost never in frame |

Per creative: one scene, then `before`, `action` and `after`. The action and the
after are edits of the before (it is the reference image), so the place and the
people match.

## Generating

`reapi.image-gen.gemini-3-pro-image` through treg ($0.034 an image at 2K,
`"size": "9:16"`, `"resolution": "2K"`). It answers with a task id; poll
`reapi.tasks.get` every 10 s. Reference images must be public HTTPS URLs, so
the before's own output URL is passed to its action and after (valid about 7
days). A photo only on this machine can't be a reference there.

The media lives in this repo, `media/listings/<creative>/`, in three folders:

| Folder | What's in it |
|---|---|
| `raw/` | the generated photos as they came back: `before.jpg`, `action.jpg`, `after.jpg` |
| `ios/` | each photo inside the iPhone Photos viewer, no scribble |
| `iosScribbled/` | the same, every face scribbled out in red |

Beside them, `images.jsonl` (one line per generated frame: prompt, avoid, task,
credits) and `viewer.json` (below). A new frame goes in `raw/`; `ios/` and
`iosScribbled/` are always rendered from it, never edited by hand.

## The phone: Photos viewer, place and scribbles

`python/creative/photosViewer.html` is the iOS 26 Photos viewer, matched to a
screenshot of the owner's phone: status bar, glass back button, the title pill
(the town, then date and time), the ••• button, the photo fitted to the width
on black, the filmstrip with the current photo larger, and the share, heart,
info, edit and trash controls. It renders at 1179 × 2556, a real iPhone
screenshot.

Each listing folder gets a `viewer.json`:

```json
{
  "place": "Bethlehem",
  "frames": {
    "before": { "when": "October 21  10:12 AM", "clock": "2:21", "battery": 72,
                "faces": [{ "x": 205, "y": 1266, "w": 225, "h": 225 }] }
  }
}
```

- `place` is the account's town, shown on every frame.
- `faces` are whole heads, hair to chin, in image pixels. Measure them on a
  zoomed crop with a pixel grid, never from a whole-image grid: rough boxes
  left faces showing.
- Every face is scribbled out in red (`#ff3b30`), messy like a hand with the
  Markup pen: three overlapping passes at different angles, an uneven oval, a
  stroke or two past the edge. They must cover the whole head.

```bash
C:\Python312\python.exe python/creative/renderListings.py
C:\Python312\python.exe python/creative/renderListings.py basementWoman
C:\Python312\python.exe python/creative/renderViewer.py <image> <out.jpg> --faces "[...]" --place Bethlehem --when "October 21  10:12 AM"
```

`renderListings.py` renders the `raw/` frames of every folder under
`media/listings` that has a `viewer.json` into its `ios/` and `iosScribbled/`
folders (JPEG, quality 92). The filmstrip is made from the listings' own frames, never
anyone else's photos. It drives the system Edge headless through Playwright,
so nothing is downloaded.

## Checking

Show the owner every frame (a sheet of all of them, plus one at full size), then
crop each scribble and look at it before saying the faces are covered. SubQ can
then score the made frames against the winners, the same way
`subqReading.json` was made.
