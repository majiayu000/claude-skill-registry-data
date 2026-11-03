---
name: fx-vertigo
description: Add a Hitchcock dolly-zoom ("vertigo" effect) to a talking-head video. The speaker stays locked in place at the same size while the room behind them zooms in or falls away, built from a clean background plate so there is no ghosting. Renders an MP4 for Reels, TikTok or Shorts with bold all-caps captions. Use this whenever the user wants a dolly zoom, vertigo shot, Hitchcock zoom, Jaws zoom, a "background zooms but I don't" moment, a dramatic realisation beat, or a cinematic push on a single line, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Vertigo — Claude Video FX 15/17

The speaker is cut out and held perfectly still at one size while the room behind them steadily zooms. With "push" the wall, lights and plants swell toward the camera; with "pull" they fall away. The move is a single eased 1–2.5 second beat, then it holds. Captions are white, bold, all caps, with the key word in yellow, sitting just below the face.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- A realisation or reveal line ("…and then it hit me").
- Emphasising one dramatic sentence in an otherwise static talking head.
- A cinematic opener on a wide shot where the room is visible.

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
3. **Write the config** as `<video name> - vertigo.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still vertigo "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render vertigo "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Vertigo.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `direction` | `"push"` | "push" = the room grows toward the camera (like the reference); "pull" = the room falls away behind the speaker |
| `intensity` | `0.26` | how far the room zooms, 0.1-0.35 (0.22 = 22%). The speaker is held at 1 + intensity the whole time |
| `at` | `0.1` | when the zoom starts (seconds or "@word") |
| `duration` | `2.2` | seconds the zoom takes; null = until the end of the clip/window. 1-2.5s feels like a dramatic beat |
| `easing` | `"inOut"` | "inOut" (smooth start and stop), "out" (fast start, soft landing) or "linear" (constant, most Hitchcock) |
| `anchor` | `"face"` | "face" to zoom around the speaker's face, or [x, y] as 0-1 fractions of the frame |
| `entry` | `"auto"` | "auto" (quick punch-in when the effect starts mid-clip, and an ease back out if it ends before the clip does), "punch" (always punch in) or "cut" (never; hard cut in and out) |
| `background` | `"plate"` | "plate" (clean room, no ghost; static) or "video" (live footage; tiny ghost slivers possible on big gestures) |
| `vignette` | `0` | 0-0.6, darkens the frame edges as the zoom runs (0 = off) |

Run `node "$ENGINE/fx.mjs" info vertigo` to print these with the full default config.

## Writing the config

- `at`: start the zoom just before the key word, e.g. `"@course-0.3"`. `duration` 1.5–2.2s is the sweet spot; null runs it to the end.
- `direction`: "push" (the room approaches, like the reference) or "pull" (the room recedes, more unsettling).
- `intensity` 0.2–0.3. The speaker is shown punched in by this much the whole time. Higher values crop the face on close-ups.
- `easing`: "linear" is the most Hitchcock; "inOut" is smoother for social.
- Put the key word in `captions.emphasis` so the yellow word lands with the move.

## Example

Line: "If you wanted to build your own course selling platform, all you have to do is download this GitHub repo."
```json
{
  "direction": "push",
  "intensity": 0.28,
  "at": "@course-0.3",
  "duration": 1.8,
  "captions": { "emphasis": ["course", "download"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `caps`, centred at 62% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"caps"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.62` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `66` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `16` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- The effect is only as visible as the room. On tight close-ups with a plain wall it is subtle; it shines on medium and wide shots with depth (windows, shelves, lamps).
- The background is a still "clean plate" made from the clip, so moving things behind the speaker (screens, people) freeze during the effect. Use `"background": "video"` to keep them live, at the cost of possible faint slivers on big gestures.
- Objects the cut-out leaves out (a microphone in front of the face) move with the room. Keep `intensity` modest if a mic sits in front of the speaker.
- The first prep of a clip builds the plate (a few seconds); later renders reuse it.
- If the effect starts mid-clip it punches in over 6 frames, and if it ends early it eases back to the original framing. Set `entry` to "cut" for hard cuts.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
