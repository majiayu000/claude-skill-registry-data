---
name: reaction-duet
description: "Reaction / duet / stitch editor: combines a source clip with the creator's facecam reaction in a picture-in-picture, split-screen or stitch layout, keeps the two in sync, ducks the source audio under the reactor's voice, freezes or zooms on the moment being reacted to, and delivers a 9:16 short with captions and an on-screen credit. Use when the user says: reaction video, react to this clip, duet, stitch, split screen with my face, commentary on a video, PiP facecam over a clip. Commentary must add something (fair use) and the source must be credited. Default skin split-proof."
license: MIT
---

# Reaction Duet

Source on one side, you on the other, perfectly in sync, the source politely ducking whenever you talk.

- **Best for:** reactions, commentary, duets, stitches, "expert reacts", breakdowns of someone else's clip
- **Inputs:** the source clip (`source.mp4`, yours to use or used under fair use with commentary), the facecam recording made while watching it, the source offset (where in the source your recording starts)
- **Default skin:** `split-proof` (facecam bottom half) · alternatives `halo-cut` (PiP), `bold-bounce`, `before-after`
- **Formats:** 9:16 1080x1920 with captions; `captions.srt`
- **Duration target:** 15-60 s Shorts, up to 3 min; genre preset `reaction-duet`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre reaction-duet`.
- **Sync first.** Record the facecam while the source plays, clap or say "go" on its first frame, and note the offset. Work out `OFFSET` = source second that plays at facecam second 0.
- **Ethics and rights:** credit the creator on screen for the whole clip, add real commentary (not just watching), never fake a reaction, use short excerpts. Ask the user if they have the creator's permission when the clip is long.

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| hook | 0-10 | the most surprising moment of the source + your strongest reaction, in the first 1.5 s |
| context | 10-20 | who / what this is, one line, credit on screen |
| source + reactions | 20-80 | play the source; pause (freeze) or zoom where you talk over it |
| verdict | 80-95 | your take: the value you add |
| CTA | last 2 s | follow / part 2 |

- **Sync is sacred:** do NOT run autocut on a reaction (`--no-cut`); every removed pause would desync your face from the source. Cut only whole sections with `--cut` ranges and move the source the same amount (a new clip element with its own `clipOffset`).
- **Pacing:** ASL 2-4 s; a change every 3 s: zoom on the source detail, freeze-frame + callout, a punch-in on your face.
- **Audio:** source audio plays as a bed ducked ~10 dB whenever you speak (the plan `music` block does this); your voice leads.
- **Transitions:** cuts only; flash on the reveal moment at most once.
- **Colour:** correct the facecam only (`color` affects the speaker video); leave the source as is.
- **Captions:** your words only (the source can carry its own), preset `boxed` or `hormozi`, in the band between the two panes.
- **Client judges:** is the reaction genuine, does the commentary add value, hold rate.
- **Common mistakes:** drifting sync, source louder than the reactor, no credit, reacting with nothing to say, captions over the source's own subtitles.

## Make the edit

```bash
python CORE/scripts/run.py facecam.mp4 --style SKILLS/split-proof --genre reaction-duet --no-cut \
  --clip source.mp4 --format 9:16 --work react --stop-after plan
python CORE/scripts/render.py react/plan.json --frames 1,4,8,14
```

`--clip source.mp4` makes the source available to elements as clip id `main`. Then wire the layout and the audio in the plan (next section), review and render:

```bash
python CORE/scripts/editor.py review react/plan.json --genre reaction-duet --fix
python CORE/scripts/render.py react/plan.json --frames 1,4,8,14      # LOOK: source visible, face visible, credit
python CORE/scripts/render.py react/plan.json
python CORE/scripts/finish.py react/plan.json --platform tiktok
```

## Refine the plan

- **Source pane (split, top half):** `{"type": "clip", "clip": "main", "clipOffset": OFFSET, "start": 0, "end": DUR, "x": 540, "y": 480, "w": 1080, "h": 960, "in": "none"}`. The facecam already fills the bottom half in `split-proof`.
- **PiP instead:** use `halo-cut` (face full frame) and a smaller source: `"w": 620, "h": 350, "x": 540, "y": 520, "className": "glass"`; or swap: source full (`w`/`h` = frame) and set `"speaker": {"mode": "panel", "rect": [700, 1300, 330, 440], "radius": 40}` for the face.
- **Source audio, ducked:** `"music": {"src": "../source.mp4", "start": OFFSET, "volume": 0.5, "duck": true, "duckDepth": 10, "fadeOut": 0.5}`. `start` is the source second at video 0, so it matches `clipOffset`.
- **Freeze on a moment:** end the playing clip element at T and add an `image` element (a still exported with `ffmpeg -ss <src time> -i source.mp4 -frames:v 1 freeze.png`) from T to T+2, then a new clip element with `clipOffset` = OFFSET + T + 2 (the source jumps past what was frozen; adjust `music.start` the same way only if you split the audio too).
- **Callouts:** `{"type": "callout", "point": [700, 420], "x": 300, "y": 180, "title": "watch his hand"}`, `scribble` circles on the detail.
- **Credit:** `{"type": "chip", "text": "Source: @creator", "start": 0, "end": DUR, "x": 60, "y": 120, "anchor": "top-left"}`.
- **Captions:** `{"type": "captions", "preset": "boxed", "y": 1000, "dodgeFace": false}` - place between panes.

## Deliver

```bash
python CORE/scripts/deliver.py react/plan.json --to tiktok,reels,shorts --out-dir react/deliver
python CORE/scripts/qc.py react/deliver/final_tiktok.mp4 --plan react/plan.json --platform tiktok
```

- Put the original link in `post.md`'s description. Platform-native duet/stitch features keep attribution automatically; this edit is for re-uploads with commentary.

## Check before delivering

- Lips and the source stay in sync at the start, middle and end (compare 3 stills).
- Reactor always intelligible; source audible in gaps; no clipping (`qc.py` -14 LUFS / -1 dBTP).
- Credit on screen the whole time; commentary present in every section.
- Captions don't cover the source's own text or the face.
- Tell the user: layout, offset used, length, file paths, and the rights caveat.

## Example requests

- "Make a reaction video: this clip on top, my face below, duck the clip when I talk."
- "Stitch-style: first 3 seconds of their video, then my answer."
- "PiP my facecam over this trailer, freeze when I explain the shot."
