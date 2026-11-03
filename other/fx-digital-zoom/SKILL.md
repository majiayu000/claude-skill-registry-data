---
name: fx-digital-zoom
description: Add punch-in "digital zoom" cuts with a radial zoom blur to a talking-head video, timed to the key words, the way short-form editors fake a second camera angle. Renders an MP4 for Reels, TikTok or Shorts with word-by-word captions. Use this whenever the user asks for punch-ins, zoom cuts, jump zooms, "digital zoom", zoom on emphasis, a more dynamic or more edited talking head, or wants a static clip to feel less flat, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Digital Zoom — Claude Video FX 05/17

The frame snaps 25–35% closer on an emphasised word, with a 4–6 frame radial zoom blur that sells the move, then holds. On the next emphasised word it snaps back out (or further in). Captions pop on word by word in white bold, with the key word in yellow.

This effect works on the footage as-is (no cut-out needed), so it prepares quickly. Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- A one-take talking head that needs energy without b-roll.
- Landing a punchline or the key noun of a sentence ("video *editing*").
- Faking a second camera angle between sentences.

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
3. **Write the config** as `<video name> - digital-zoom.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still digital-zoom "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript; after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render digital-zoom "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Digital Zoom.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `punches` | `"auto"` | "auto", or a list like [{"at": "@video", "scale": 1.3}, {"at": "@editing", "scale": 1.0}]. "at" takes seconds or "@word". |
| `scale` | `1.3` | zoom level for auto punch-ins (1.3 = 30% closer) |
| `rest` | `1` | zoom level between punches (1.0 = original framing) |
| `minGap` | `1.1` | seconds between auto punches |
| `transitionFrames` | `5` | frames the snap takes (3-6 feels like a punch) |
| `blur` | `true` | radial zoom blur during the snap (true/false) |
| `focus` | `"face"` | "face" to zoom toward the face, or [x, y] as 0-1 fractions of the frame |

Run `node "$ENGINE/fx.mjs" info digital-zoom` to print these with the full default config.

## Writing the config

- `punches: "auto"` punches on the words the captions highlight (the strongest noun per phrase), alternating in and out, never closer than `minGap` seconds. Good default.
- For control, list punches: `[{"at": "@editing", "scale": 1.3}, {"at": "@thousands", "scale": 1.0}]`. Use the word the speaker stresses, not filler.
- Keep `scale` between 1.15 and 1.4; above 1.4 footage goes soft. Keep at least ~1s between punches.
- Set `captions.emphasis` to the same words you punch on so the yellow word and the zoom land together.

## Example

Line: "I didn't have to spend thousands of dollars on video editing courses."
```json
{
  "punches": [
    { "at": "@thousands", "scale": 1.28 },
    { "at": "@editing", "scale": 1.0 }
  ],
  "captions": { "emphasis": ["thousands", "editing"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `pop`, centred at 60% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"pop"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.6` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- Punch on the stressed syllable's word start ("@word"), not on a pause, or it reads as a glitch.
- If the face drifts out of frame at high zoom, lower `scale` or set `focus` to `[0.5, 0.3]` (x, y fractions).
- Turn `blur` off for a cleaner, more corporate cut.
- Footage below 1080p will look soft when punched; keep scale ≤1.2 there.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
