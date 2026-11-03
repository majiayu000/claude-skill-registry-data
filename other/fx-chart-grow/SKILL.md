---
name: fx-chart-grow
description: Draw an animated growth chart on the wall behind a talking-head speaker — a minimal grid with day or month labels, a white line that draws itself left to right behind their head, then spikes up in glowing yellow with a gradient fill, dashed guide and a "SCALE ↗" pill. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user mentions growth, results, revenue, followers, views going up, "it took off", scaling, a before/after jump, wants a graph or stats animation behind them, or the chart grow effect, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Chart Grow — Claude Video FX 10/17

Faint vertical grid lines and labels (M T W T F S S) fade in across the top of the frame. A white line with small dots draws itself from left to right with a glowing tip, passing behind the speaker's head. At the take-off point it turns into a glowing yellow spike with a soft yellow gradient underneath, a dashed guide drops from a yellow pill (SCALE ↗) that pops in above it, and the end point pulses. The speaker is cut out and stays in front.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Results and growth: "my views tripled", "revenue took off in week 3".
- Before/after moments where a flat period turns into a jump.
- Any stat the speaker says out loud.

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
3. **Write the config** as `<video name> - chart-grow.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still chart-grow "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render chart-grow "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Chart Grow.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `labels` | `["M","T","W","T","F","S","S"]` | x-axis labels across the top, e.g. ["M","T","W","T","F","S","S"] or ["JAN","FEB","MAR","APR"] |
| `values` | `[0.14,0.17,0.21,0.25,0.33,0.64,1]` | one height per label, 0 = bottom of the chart, 1 = top (resampled if the count differs) |
| `highlightFrom` | `4` | index of the label where the line turns into the glowing spike (0 = first label) |
| `pill` | `"SCALE"` | label text in the pill at the take-off point ("SCALE", "+312%"); empty string = no pill |
| `arrow` | `true` | draw the ↗ arrow inside the pill |
| `pillInFront` | `true` | keep the pill in front of the speaker (true) or behind them like the line (false) |
| `at` | `0.2` | when the chart starts appearing (seconds or "@word") |
| `drawDuration` | `1.1` | seconds the line takes to draw from first to last point |
| `outAt` | `null` | optional: when the chart fades away (null = hold to the end; it also leaves automatically when an effect window ends early) |
| `accent` | `"#FFE14D"` | spike / pill colour |
| `lineColor` | `"#FFFFFF"` | colour of the line before the spike |
| `lineWidth` | `6` | line thickness in px (at 1080 wide) |
| `dim` | `0.22` | how much to darken the wall behind the chart so it reads (0-0.5) |
| `region` | `"auto"` | "auto" (fitted around the speaker's head) or [x0, y0, x1, y1] as 0-1 fractions: y0 = label row, y1 = chart bottom |

Run `node "$ENGINE/fx.mjs" info chart-grow` to print these with the full default config.

## Writing the config

- `labels`: the time axis the speaker implies — days (`M T W T F S S`), months (`JAN…JUN`), weeks (`W1…W6`) or milestones. 4–8 labels fit.
- `values`: one 0–1 height per label, flat-ish then a jump; the last value 1 for the peak. Match the story (a slow start then a spike).
- `highlightFrom`: the label index where things took off (the spike and pill start there).
- `pill`: the result in 1–2 words or a number ("SCALE", "+312%", "10x"); it is upper-cased. `""` hides it.
- `at`: start on the word that introduces the result ("@grew", "@revenue").

## Example

Line: "This new Opus model should be capable of doing three absolutely mind-blowing things."
```json
{
  "at": "@model",
  "labels": ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"],
  "values": [0.12, 0.15, 0.2, 0.28, 0.55, 1],
  "highlightFrom": 3,
  "pill": "10x",
  "captions": { "emphasis": ["Opus", "capable", "mind-blowing"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `pop`, centred at 72% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"pop"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.72` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- The chart is fitted above and around the head. If the speaker sits low in frame or you want a bigger chart, set `region` to `[0.08, 0.12, 0.92, 0.45]` (x0, label row, x1, chart bottom).
- The middle of the line hides behind the head by design; put the take-off (`highlightFrom`) on a side the viewer can see (usually the right third).
- On bright walls raise `dim` to 0.3 so the white line reads; on dark walls lower it to 0.1.
- `pillInFront: true` keeps the label readable even when it overlaps hair.
- Keep `drawDuration` around 0.8–1.4 s; slower feels like a slideshow.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
