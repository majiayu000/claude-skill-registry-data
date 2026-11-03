---
name: teaser-video
description: Make a short product teaser with no narration (a feature announcement, a social clip, a hype video, about 10-30 s) from real screenshots of the product, as a HyperFrames composition (HTML and GSAP, rendered with npx). One slow camera move per scene, rows cut from the captures that land in place, a page tipped back in 3D, two- or three-word captions, a brand end card, and cuts on the hits of a music track. Use when someone wants a teaser, motion graphic, or launch clip without a voiceover; for a narrated demo use narrated-video instead.
---

# Teaser video

A teaser shows one feature in a few beats, each with one clear focus, set to music. Every screen is a real
screenshot of the product; the motion comes from the camera, from rows cut out of those screenshots landing in their
own places, and from the cuts falling on the music. The whole video is code (one HTML page and one timing table,
rendered by HyperFrames), so a new capture, a changed caption, or a different music clip is a re-run.

The person directs taste and will iterate several times. Show contact sheets before full renders, keep every render,
and write down what changed and why. Start from the defaults in [references/taste.md](references/taste.md): they
are what a first round of reviews converged on.

## Setup

- Node 22+ with npx (HyperFrames runs through `npx hyperframes@0.8.62`; nothing to install), ffmpeg on PATH (HyperFrames
  needs it for snapshots and renders too), `uv` (the Python tools declare their own dependencies), and Playwright with
  Chromium in the product's project for captures. Renders load GSAP and the Inter font from a CDN, so they need a
  network connection.
- `SK=<this skill's directory>/scripts`.
- Work in a folder outside any repository's tracked files (a gitignored `.logs/<video>/`, or a scratch folder):

```
<work>/
  assets/<theme>/    captures and boxes.json, per capture pass
  capture/           the capture scripts for this product
  video/             index.html and timeline.js (copied from the example); assets/ holds the captures, brand icon, music
  NOTES.md           every version and why it changed, rebuild commands
```

## 1. Brief

Confirm in one short exchange, offering defaults:

- Length: 10 s unless asked otherwise. Under a hard cap, cut beats, never speed motion up.
- The beats: three or four, each one job on one screen (enter a URL, review what was found, see the result, the
  brand). Each beat gets a caption of two or three words, with no numbers.
- Example data that reads at a glance: a well-known site, so the results (competitor names, favicons) are recognisable.
- Look: the product's own theme tokens (dark mode is a good default for a teaser) and its real brand icon, taken from
  its live website, not a mark you draw.
- Music: the file, and whether any 10 s will do (see step 5).
- Which branch or worktree has the newest UI for each screen. Check whether it is behind its remote before capturing.

## 2. Capture

Real screenshots at 1440x900, 2x, with `$SK/capture.mjs` (the same helper as narrated-video): typing frames for
anything typed, tall captures (2400 px) for anything the camera pans down, measured boxes for every element a scene
frames, cuts rows from, or clicks. Pass `{ colorScheme: 'dark' }` to `cap.page()` for dark mode. Never draw UI or
edit pixels. Details, including frozen-animation frames and capturing a loading state without paying for the request:
[references/capture.md](references/capture.md). Look at every capture before using it.

## 3. Compose

Copy [examples/openseo-ai-visibility/video](examples/openseo-ai-visibility/video) (`index.html`, `timeline.js`) into
the work folder, put the captures, brand icon, and music in `video/assets/`, and rewrite `timeline.js`: the timing
table, captions, palette, capture paths and heights, the measured boxes, each scene's camera keys, and the pointer.
`index.html` builds every scene from that file: rows are cut from their capture using the measured boxes. How the
pieces work and the numbers that matter: [references/composition.md](references/composition.md).

## 4. Draft and look

```sh
cd video
npx --yes hyperframes@0.8.62 lint                                           # must report 0 errors
npx --yes hyperframes@0.8.62 snapshot --at 0,1.2,2.4,2.6,3.4,4.4,6.0,8.2,9.5 --no-end   # into snapshots/
```

Snapshots take seconds, so use them instead of draft renders. Snapshot every scene start, click, caption entry, and
the middle of every dissolve, and look at them (each run also writes contact sheets): one focus per frame and
centred, the caption clear of the thing in focus, no blank page edge while the page is flat, no row still missing at
the end of a reveal. Then check a full-resolution frame of each scene for crisp text.

## 5. Music

```sh
uv run $SK/beats.py song.mp3                     # tempo, loudness per second, every hit
uv run $SK/beats.py song.mp3 --window 51.9 10    # a candidate clip's hits in video time
```

Pick the clip, write its start into the `<audio>` element in `index.html` and its hit times into the timing table,
and move the cuts onto them: the main click on the drop,
each scene change on a hit, the logo on the strongest hit. Choosing the clip and mapping it:
[references/music-sync.md](references/music-sync.md).

## 6. Render and verify

```sh
npx --yes hyperframes@0.8.62 render -o renders/<video>-vN.mp4 --fps 60 --crf 14 \
  --video-frame-format png --experimental-fast-capture=false            # about 15 s for 10 s of video
uv run $SK/verify-sync.py renders/<video>-vN.mp4 <planned hit times...>   # every hit within a frame; exits 1 if not
uv run $SK/sheet.py renders/<video>-vN.mp4 renders/sheet-vN.png <times...>
```

Name renders by version and keep them all; the person compares. A still for sharing (a social image, a thumbnail) is a
4K snapshot of a chosen moment: `npx --yes hyperframes@0.8.62 snapshot --at 7.3 --no-end --zoom 0,0,1920,1080
--zoom-scale 2 -o stills` writes a 3840x2160 PNG.

## 7. Review and iterate

Give the mp4 path (and how to open it), the beats and their times, and anything that differs from the request.
Record each round in `NOTES.md`. The first version of the worked example took seven rounds; what changed in each is in
[examples/openseo-ai-visibility/NOTES.md](examples/openseo-ai-visibility/NOTES.md).

## Hard rules

- Real screens only. A row reveal may briefly cover rows with the table's own background (sampled from the capture)
  while the real rows land on top; once they have landed, the frame is the capture.
- Check captures for secrets and personal data (keys, emails, other people's names, localhost URLs) before rendering.
- The music and captures stay on the person's machine; publish nothing without being asked.
- Restore any tracked file that building or previewing the product regenerates in its repository.

The mistakes that cost the most time are in [references/gotchas.md](references/gotchas.md).
