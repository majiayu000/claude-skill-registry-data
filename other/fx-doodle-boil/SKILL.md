---
name: fx-doodle-boil
description: Add hand-drawn doodle animation to a talking-head video — a white chalk outline traces the speaker and "boils" like cel animation while doodles (heart, clapperboard, star, crown, frame, arrow, sparkle) draw themselves on next to their head with pink and yellow scribble fills. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants doodles, scribbles, sketch or chalk outlines, a hand-drawn/animated outline around themselves, "boiling lines", cartoon annotations, or a playful drawn-on look over their footage, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Doodle Boil — Claude Video FX 14/17

The footage plays untouched. A chunky white chalk line traces the speaker's silhouette a few pixels outside the body and re-wobbles every three frames, so it shimmers like hand-drawn animation. Doodles draw themselves on in the space beside and above the head (outline first, then a crayon scribble fill, then little spark lines) and boil along with the outline. A newer doodle in the same spot replaces the old one.

This effect cuts the speaker out of the background (person matte, cached after the first run), traces the speaker's outline. Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Light, personal or funny moments where a little cartoon energy helps.
- Pointing at ideas: a heart on "love", a clapperboard on "video", a crown on "the best", a star on "three things".
- Hook or outro beats where you want movement without covering the face.

## The engine

Every Claude Video FX skill renders through one local Remotion engine:

```bash
ENGINE="engines/video-fx/engine"
```

The first time in a session, run `node "$ENGINE/fx.mjs" doctor`. If any line shows ✖, stop and follow the setup steps in the `video-fx` skill (or tell the user to run the kit installer). Never edit files inside the engine to make a single video work; everything is controlled through the config JSON.

## Workflow

1. **Read the video.** `node "$ENGINE/fx.mjs" words "<video>"` prints a timestamped transcript of the whole file (cached); add `--detail` for every word's start → end. Pick the 3–12 second stretch the user means, or the one this effect suits best. Snap the range to speech: start ~0.1s before its first word, end ~0.2s after its last word, so nothing is clipped.
2. **Decide the deliverable.**
   - The clip *is* the moment → render that range and deliver the MP4.
   - A moment inside a longer video → render the moment's range, then put it back with `splice` (step 7) and deliver the full video (mention the segment file too). If the range ends before the video does, add `"window": [0, <range length − 0.4>]`: the effect has fully left by the window end, so keep that after the last word the graphics belong to. Captions must match the rest of the video: either caption everything (render the `captions` effect over the whole file with the same `"captions"` block as this config and splice into that render) or set `"captions": {"enabled": false}` here and splice into the original. The `video-fx` skill covers multi-effect videos.
3. **Write the config** as `<video name> - doodle-boil.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still doodle-boil "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render doodle-boil "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Doodle Boil.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `doodles` | `"auto"` | "auto" (a sequence timed to the emphasised words) or a list of doodles: {"type", "slot" or "x"/"y", "at", "until", "size", "color", "fill", "accent", "rotate"} |
| `doodles[].type` | `null` | heart, clapper, frame, square, star, arrow, sparkle, crown, swirl or circle |
| `doodles[].slot` | `null` | where it sits relative to the head: left, right, topLeft, topRight, aboveHead (a newer doodle in the same slot replaces the older one) |
| `doodles[].x / y` | `null` | instead of a slot: centre position as 0-1 fractions of the frame |
| `doodles[].at` | `null` | when it starts drawing (seconds or "@word") |
| `doodles[].until` | `null` | optional: when it disappears (otherwise it stays, or until replaced in its slot) |
| `doodles[].size` | `null` | width as a fraction of the frame width (default 0.15-0.2) |
| `doodles[].color` | `null` | line colour (default white chalk) |
| `doodles[].fill` | `null` | scribble fill colour, or null for no fill |
| `doodles[].accent` | `null` | colour of the spark lines / clapper stripes |
| `doodles[].rotate` | `null` | tilt in degrees |
| `minGap` | `0.9` | auto mode: minimum seconds between doodles |
| `drawFrames` | `10` | frames each doodle takes to draw on |
| `fillDelay` | `3` | frames between the outline finishing and the scribble fill starting |
| `boilEvery` | `3` | redraw the wobble every N frames (2 = fast boil, 4 = slow) |
| `chalk` | `true` | chalky, speckled line texture (false = clean lines) |
| `shadow` | `0.35` | opacity of the soft dark shadow under the lines (helps on bright walls) |
| `outline.enabled` | `null` | draw the outline around the speaker |
| `outline.color` | `null` | outline colour |
| `outline.width` | `null` | outline thickness in px (at 1080 wide) |
| `outline.offset` | `null` | gap between the body and the line in px |
| `outline.wobble` | `null` | how much the line wanders in px |
| `outline.double` | `null` | add a thinner second pass for a sketchy double stroke |
| `outline.drawOn` | `null` | trace the outline on at the start |
| `outline.at` | `null` | when the outline starts tracing |
| `outline.drawFrames` | `null` | frames the trace takes |
| `outline` | `{"enabled":true,"color":"#FFFFFF","width":10,"offset":10,…` |  |

Run `node "$ENGINE/fx.mjs" info doodle-boil` to print these with the full default config.

## Writing the config

- `"doodles": "auto"` drops a doodle on each emphasised word (heart → frame → clapperboard → square → star → sparkle → crown → swirl), at least `minGap` seconds apart. Good default.
- For meaning, list doodles that match the words: `{"type": "clapper", "slot": "left", "at": "@video"}`. Types: heart, clapper, frame, square, star, arrow, sparkle, crown, swirl, circle. Slots: left, right, topLeft, topRight, aboveHead (`crown` belongs `aboveHead`; `arrow` points at the head automatically).
- Use `fill` for the scribble colour (`#F58BB4` pink, `#FFE45C` yellow) or `null` for an empty outline; `accent` colours the spark lines.
- Use 3–5 doodles per 6 seconds; more gets busy. `until` removes one early.
- `outline.drawOn` traces the outline on at the start; set `"outline": {"enabled": false}` for doodles only.

## Example

Line: "This new Opus model should be capable of doing three absolutely mind-blowing things."
```json
{
  "doodles": [
    { "type": "star", "slot": "right", "at": "@three", "fill": "#FFE45C" },
    { "type": "crown", "slot": "aboveHead", "at": "@absolutely", "fill": "#FFE45C" },
    { "type": "arrow", "slot": "left", "at": "@mind" }
  ]
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `pop`, centred at 76% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"pop"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.76` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- Doodles are placed from the head position; on tight close-ups they sit in the top corners. If one covers something important, give it an explicit `"x"`/`"y"` (0–1 fractions) instead of a slot.
- On bright white walls the chalk line needs its shadow: keep `shadow` around 0.35 (raise to 0.5 if it still disappears).
- The outline follows the cut-out, so desks, mics or chairs the matte includes or excludes change where the line goes; that is expected.
- Slower boil (`"boilEvery": 4`) feels calmer; `2` feels frantic.
- If the effect runs inside a `window`, the outline traces on at the start and everything fades out over the last few frames.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
