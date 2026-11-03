---
name: fx-orbit
description: Make social-post cards orbit the speaker in 3D on a talking-head video. Thumbnails and posts circle their torso, slide behind their body and pass in front of it. Renders an MP4 for Reels, TikTok or Shorts with gold serif captions. Use this whenever the user wants cards, screenshots, thumbnails, testimonials or posts floating or circling around them, a 3D orbit or carousel around a person, social proof flying around the speaker, or "the orbit effect", even if they never mention Remotion.
---

# Orbit — Claude Video FX 01/17

Six small portrait cards circle the speaker's chest on a tilted ring: Reel thumbnails with a white title chip and a ▷ view count, plus white text posts. The speaker is cut out of the shot, so cards on the far side slide behind their body while near cards pass in front, bigger and brighter. Far cards are smaller, darker and slightly soft. The cards whip in at the start and settle into a slow spin. Captions show a small white setup line with the key word in gold italic serif with sparkles.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Social proof: past videos, results, testimonials, press mentions.
- Listing many things ("all these tools", "every platform") while the speaker talks.
- An eye-catching hook in the first two seconds.

## The engine

Every Claude Video FX skill renders through one local Remotion engine:

```bash
ENGINE="{{FX_ENGINE}}"
```

The first time in a session, run `node "$ENGINE/fx.mjs" doctor`. If any line shows ✖, stop and follow the setup steps in the `video-fx` skill (or tell the user to run the kit installer). Never edit files inside the engine to make a single video work; everything is controlled through the config JSON.

## Workflow

1. **Read the video.** `node "$ENGINE/fx.mjs" words "<video>"` prints a timestamped transcript of the whole file (cached); add `--detail` for every word's start → end. Pick the 3–12 second stretch the user means, or the one this effect suits best. Snap the range to speech: start ~0.1s before its first word, end ~0.2s after its last word, so nothing is clipped.
2. **Decide the deliverable.**
   - The clip *is* the moment → render that range and deliver the MP4.
   - A moment inside a longer video → render the moment's range, then put it back with `splice` (step 7) and deliver the full video (mention the segment file too). If the range ends before the video does, add `"window": [0, <range length − 0.4>]`: the effect has fully left by the window end, so keep that after the last word the graphics belong to. Captions must match the rest of the video: either caption everything (render the `captions` effect over the whole file with the same `"captions"` block as this config and splice into that render) or set `"captions": {"enabled": false}` here and splice into the original. The `video-fx` skill covers multi-effect videos.
3. **Write the config** as `<video name> - orbit.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still orbit "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render orbit "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Orbit.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `cards` | `"auto"` | "auto", or a list of cards: {"src": "path/to/image-or-video", "title": "chip text", "views": "1.2M", "style": "reel" \| "post"}. Every field is optional; a card without src shows a still of the clip |
| `count` | `6` | number of auto cards (3-9) |
| `titles` | `"auto"` | "auto" (phrases from the transcript), "none", or a list of title strings for the auto cards |
| `views` | `true` | true to show view counts on auto cards, false to hide them |
| `at` | `0` | when the cards fly in (seconds or "@word") |
| `outAt` | `null` | optional: when the cards fly away (null = stay; they leave automatically if the effect window ends before the clip) |
| `speed` | `0.16` | orbit speed in turns per second (0.16 = one lap every ~6s) |
| `direction` | `1` | 1 = counter-clockwise seen from above (front cards move right), -1 = the other way |
| `phase` | `0` | starting angle in radians (rotate the ring so a favourite card starts in front) |
| `radius` | `0.4` | horizontal radius of the orbit as a fraction of the frame width |
| `tilt` | `0.065` | vertical radius (how tilted the ring looks) as a fraction of the frame height |
| `height` | `0.42` | where the ring sits on the body: 0 = face, 1 = bottom of the person (0.42 ≈ chest) |
| `center` | `"auto"` | "auto" or [x, y] fractions to place the ring centre yourself |
| `cardSize` | `0.17` | card width as a fraction of the frame width (front cards) |
| `depthBlur` | `1.6` | blur in px on the farthest cards |
| `captionPlacement` | `"auto"` | "auto" (above the head if there is room, else below the ring) or "keep" (use captions.y) |

Run `node "$ENGINE/fx.mjs" info orbit` to print these with the full default config.

## Writing the config

- Best: real media. Put the user's screenshots, thumbnails or short clips in `cards` as file paths, e.g. `[{"src": "~/Desktop/thumb1.png", "title": "1M views", "views": "1.2M"}]`. Use 4–8 cards. Every field is optional.
- Without media, the auto cards show stills of the clip itself. Give them `titles` that say something (results, topics, hooks from the transcript), 2–5 words each.
- `speed` 0.1–0.2 turns per second. Slower reads better when the cards carry text.
- `height` moves the ring on the body: 0.3 is the shoulders, 0.6 is the waist. On a wide shot of a seated person, 0.5 matches the reference reel.
- Set `captions.emphasis` to the word that should turn gold. Only one gold word per phrase shows.

## Example

Line: "The video that you're currently watching was edited completely using Claude Code."
```json
{
  "count": 6,
  "titles": ["Edited with Claude Code", "No editor needed", "Raw clip to finished reel", "Auto captions", "Motion graphics", "Ready to post"],
  "speed": 0.14,
  "captions": { "emphasis": ["watching", "Claude"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `serif`, centred at 70% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"serif"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.7` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `64` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- In close-up framing, the back half of the ring hides behind the body. That's correct. For the classic look, use a wider shot where the person is smaller in frame.
- Cards briefly cross-fade at the sides of the ring, where they switch from behind to in front. A low `speed` makes that read as a smooth pass.
- Card text is small, so keep titles under about 25 characters.
- Captions place themselves above the head on wide shots and below the ring on close-ups. Set `"captionPlacement": "keep"` plus `captions.y` to force a position.
- If the effect window ends before the clip, the cards fly away on their own. Use `outAt` to send them off earlier.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
