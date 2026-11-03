---
name: fx-checklist
description: Add an animated checklist overlay to a talking-head video — a frosted dark-glass card ("ALL YOU NEED TO DO", "0 of 3" — the counter follows however many steps you give it) whose steps type in as they are said and tick off with a yellow check, counter and progress bar. Renders an MP4 for Reels, TikTok or Shorts with word-by-word captions. Use this whenever the user wants a checklist, to-do list, step-by-step list, "3 steps", "all you need to do is", a numbered how-to or a tick-off list on screen while they talk, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Checklist — Claude Video FX 07/17

A dark frosted-glass card with a slight 3D tilt springs in above the speaker's head (or over the chest on close-ups). The header reads ALL YOU NEED TO DO with a "0 of N" counter (N = number of steps) and a segmented yellow progress bar; the rows start as grey skeleton bars. When a step is spoken its text types in with a caret, then its circle fills yellow with a check and a little burst, the counter ticks up and that bar segment fills.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- "All you need to do is…", "three steps", "here's the process" moments.
- Listing requirements, features or a recipe while talking to camera.
- Recapping what was just covered at the end of a video.

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
3. **Write the config** as `<video name> - checklist.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still checklist "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render checklist "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Checklist.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `title` | `"ALL YOU NEED TO DO"` | small header text on the card |
| `items` | `"auto"` | "auto" (3 short steps pulled from the transcript) or a list. Each item is a string, or {"text": "Drop your clips", "at": "@drop", "doneAt": "@trigger"}. "at" = when it types in (default: when its first key word is spoken), "doneAt" = when it ticks (default: checkAfter seconds after typing finishes). |
| `count` | `3` | how many items to generate when items is "auto" |
| `inAt` | `0.1` | when the card appears (seconds or "@word"); it always appears a moment before the first item |
| `outAt` | `null` | optional: when the card flies away (null = stays to the end) |
| `checkAfter` | `0.3` | seconds between an item finishing typing and its tick |
| `typeSpeed` | `32` | typing speed in characters per second |
| `position` | `"auto"` | "auto" (above the head if there is room, else over the chest), "top", "bottom", or a 0-1 fraction for the card's top edge |
| `width` | `0.84` | card width as a fraction of the frame width |
| `accent` | `"#F5E15A"` | colour of the ticks, progress bar and glow |
| `doneTextColor` | `"#F1E7A6"` | text colour of finished items |
| `tilt` | `6` | 3D tilt of the card in degrees (0 = flat) |
| `captionsAvoid` | `true` | move the captions above/below the card if they would overlap it |

Run `node "$ENGINE/fx.mjs" info checklist` to print these with the full default config.

## Writing the config

- `items`: 2–5 short steps, 2–4 words each, written as commands ("Drop your clips", "Trigger the skill"). Take them from what the speaker actually says, tightened. Leave `"auto"` only as a fallback (it pulls rough phrases from the transcript).
- Give each item an `at` on the word where that step is said ("@drop"); items always type one after another, so close timings are safe. Use `doneAt` only if the tick must land on a specific word.
- `title` is the small header; keep it under ~22 characters, uppercase reads best.
- `position` is automatic: above the head when there's room (wide shots), over the chest on close-ups, and captions move out of the way. Force `"top"` / `"bottom"` only if it covers something important.
- Set `outAt` if the list should leave before the clip ends (it also leaves automatically when the effect window ends early).

## Example

Line: "This new Opus model should be capable of doing three absolutely mind-blowing things."
```json
{
  "title": "WHAT OPUS CAN DO",
  "items": [
    { "text": "Run an agent swarm", "at": "@three" },
    { "text": "Rebuild any website", "at": "@absolutely" },
    { "text": "Generate images", "at": "@mind" }
  ],
  "outAt": -0.4
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

- Long step text shrinks to fit the row; past ~24 characters it gets small, so shorten the wording instead.
- If two steps are said within a second, the second waits for the first to finish typing; raise `typeSpeed` (e.g. 45) for rapid-fire lists.
- On very busy backgrounds raise contrast by darkening the footage a touch elsewhere, or keep the card over a plain wall with `position: "top"`.
- The card needs the cut-out pass only to find the head; if the speaker is off-centre and the card lands on the face, set `position` to a number (0–1 of the height).
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
