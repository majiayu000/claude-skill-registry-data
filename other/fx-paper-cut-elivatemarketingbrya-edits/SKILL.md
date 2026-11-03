---
name: fx-paper-cut
description: Turn a talking-head shot into a handmade scrapbook collage — the speaker becomes a paper sticker with a torn white border over crayon scribbles, torn yellow paper and X marks, while ransom-note letters thunk in one by one, get circled in red marker and a second word pops in underneath. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants a paper cut-out, scrapbook, collage, zine, ransom-note or "cut out from a magazine" look, a sticker version of themselves, crafty/handmade text, or a stat like "100%" called out in cut-out letters, even if they never mention Remotion.
---

# Paper Cut — Claude Video FX 13/17

The background is swapped for off-white paper with a faint grid, a big blue crayon scribble across the top, a torn yellow strip with navy scribbles and red ticks, pink scribbles, X marks and loop doodles. The speaker, still talking, is cut out as a paper sticker with a thick, slightly ragged white border and a drop shadow, slapping into place. Ransom-note letters on mixed chips (blue, white, black, yellow; serif, slab, typewriter) land one by one, a red marker ring draws itself around them, then a smaller word pops in below. All the scribbles boil on threes like stop-motion.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Calling out a number or claim: "100%", "3X", "$0", "FREE".
- A playful, creator-diary or "behind the scenes" moment that should feel handmade.
- A 2–5 second beat in the middle of a talk to reset attention (use `window`).

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
3. **Write the config** as `<video name> - paper-cut.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still paper-cut "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render paper-cut "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Paper Cut.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `headline` | `"auto"` | the ransom-note word or number, e.g. "100%", "3X", "FREE" ("auto" = a number from the transcript, else the strongest word) |
| `subline` | `"auto"` | smaller second word under the ring, e.g. "EDITED" ("auto" = the next strong word, "" = none) |
| `headlineAt` | `0.35` | when the first letter lands (seconds or "@word") |
| `sublineAt` | `null` | when the subline starts (null = right after the ring) |
| `stagger` | `4` | frames between letters |
| `circle` | `true` | draw the red marker ring around the headline (true/false) |
| `headlineX` | `0.07` | left edge of the headline as a 0-1 fraction of the width (when headlineAlign is left) |
| `headlineY` | `0.145` | vertical centre of the headline, 0-1 of the height |
| `headlineAlign` | `"left"` | "left" or "center" |
| `headlineSize` | `118` | maximum letter size in px at 1080 wide (long words shrink to fit) |
| `headlineWidth` | `0.8` | maximum headline width as a fraction of the frame |
| `sublineScale` | `0.62` | subline letter size relative to the headline |
| `stickerScale` | `"auto"` | "auto" (fits the head to headTopTarget) or a number like 0.75 |
| `headTopTarget` | `0.34` | auto scale: where the top of the head should land, 0-1 of the height |
| `stickerX` | `0.44` | horizontal centre of the sticker, 0-1 of the width |
| `stickerRotate` | `-1.5` | sticker tilt in degrees |
| `borderWidth` | `15` | white sticker border thickness in px |
| `tornEdge` | `12` | how ragged the border edge is (0 = clean) |
| `boilEvery` | `3` | re-jitter the scribbles every N frames |
| `elements` | `{"grid":true,"blueScribble":true,"tornPaper":true,"pinkSc…` | turn collage pieces on/off: {"grid", "blueScribble", "tornPaper", "pinkScribble", "marks", "loops"} |
| `colors` | `{"paper":"#F1EEE6","grid":"#C3CEDA","blue":"#8C9EDA","blu…` | palette: paper, grid, blue, blueDark, yellow, navy, pink, red, ring, border |

Run `node "$ENGINE/fx.mjs" info paper-cut` to print these with the full default config.

## Writing the config

- `headline`: 1–6 characters reads best (a number, %, or one short word). Take it from what the speaker says ("one hundred percent" → "100%"). Words up to ~8 letters shrink to fit.
- `subline`: one short word that completes the thought ("EDITED", "FREE", "DONE"), or `""` for none.
- `headlineAt`: anchor to the spoken word, e.g. `"@percent"` or `"@course-0.1"`, so the letters land as it is said. The ring and subline follow automatically.
- The collage replaces the whole background, so use it for a beat, not a whole video: pass `"window": [start, end]` (seconds in the clip) for a hard cut in and a quick fade back to the footage.
- Captions are off by default (the letters are the text). Turn them on with `"captions": {"enabled": true}`; the `box` style suits the look.
- Nudge the sticker with `stickerScale` (0.6–0.9), `stickerX` and `headTopTarget` if the head collides with the letters.

## Example

Line: "If you wanted to build your own course selling platform, all you have to do is download this GitHub repo."
```json
{
  "headline": "100%",
  "subline": "FREE",
  "headlineAt": "@course",
  "captions": { "enabled": false }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `box`, centred at 88% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `false` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"box"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.88` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- If the head overlaps the ring, lower the sticker (`"headTopTarget": 0.4`) or move the letters up (`"headlineY": 0.12`).
- Fast hand moves leave soft, semi-transparent edges in the cut-out; that reads fine as paper, but keep the beat short if hands fly around a lot.
- People sitting at a desk get cut where the desk is; the white border makes that edge look like a deliberate scissor cut.
- `"auto"` text picks a number from the transcript, otherwise the strongest word — always replace it with something meaningful when you know the topic.
- Turn collage pieces off with `"elements": {"loops": false, "marks": false}` for a cleaner page; change the palette under `colors` for brand colours.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
