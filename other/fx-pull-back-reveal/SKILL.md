---
name: fx-pull-back-reveal
description: Make a talking-head shot pull back to reveal it's playing inside an editor app that is rendering it — agent panel ticking through steps, render bar with waveform and frame counter, a big serif % counter rolling to 100% and a green "done" state. Renders an MP4 for Reels, TikTok or Shorts with captions inside the window. Use this whenever the user wants a pull-back or zoom-out reveal, "it was edited by AI the whole time", a behind-the-scenes rendering moment, a progress / percentage counter over their video, or to show their video being processed by a tool, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Pull-back Reveal — Claude Video FX 11/17

The full-frame footage smoothly shrinks into an editor window on a cream desk (title bar with the file name, the video keeps playing inside with its captions). A white agent panel slides in on the left and ticks through its steps with spinners and green checks; under the video a render bar with a waveform fills while a frame counter climbs. Near the end a big black serif number rolls up to 100 with a blue % badge, then the window border, bar and badge flip to green.

This effect works on the footage as-is (no cut-out needed), so it prepares quickly. Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- The reveal that the video itself was made by an AI tool or skill.
- Showing a process completing ("it transcribes, cuts, captions and renders").
- Ending a video on a satisfying "done" beat.

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
3. **Write the config** as `<video name> - pull-back-reveal.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still pull-back-reveal "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript; after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render pull-back-reveal "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Pull-back Reveal.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `pullAt` | `0.1` | when the pull-back starts (seconds or "@word") |
| `pullDuration` | `0.75` | seconds the pull-back takes |
| `doneAt` | `"auto"` | "auto" (about 0.7s before the end) or when the render completes and turns green |
| `counterAt` | `"auto"` | "auto" (about 0.9s before done) or when the % counter starts rolling |
| `returnAt` | `null` | optional: when to zoom back to full frame (null = stay in the window; it returns automatically if the effect window ends before the clip) |
| `filename` | `"final-cut.mp4"` | file name in the window's title bar |
| `tab` | `"Assistant"` | label on the right of the title bar |
| `workingLabel` | `"Working on"` | panel header text |
| `skill` | `"edit"` | pill next to the panel header (the skill / command name) |
| `steps` | `["Transcribed 1 clip","Picked the take","Cut 3 shots","Ca…` | list of step labels that tick off in order; {frames} is replaced by the frame count |
| `frames` | `"auto"` | "auto" (the clip's frame count) or a number for the render counter |
| `accent` | `"#3E6AE1"` | colour of the progress fill, skill pill and dots |
| `background` | `"#F1EEE6"` | desk colour around the window |
| `windowX` | `0.29` | left edge of the window, 0-1 of the width |
| `windowWidth` | `0.6` | window width, 0-1 of the width |
| `videoAspect` | `0.64` | width/height of the video area inside the window (0.5625 shows the full 9:16 frame) |
| `panelX` | `0.045` | left edge of the agent panel, 0-1 of the width |

Run `node "$ENGINE/fx.mjs" info pull-back-reveal` to print these with the full default config.

## Writing the config

- `steps`: 3–6 short past-tense steps describing what the tool did (≤ ~24 characters each); `{frames}` inserts the render frame count.
- `filename` and `skill` should name the user's real file and tool/command.
- `pullAt` a beat before the reveal line ("@edited-0.2"); keep at least ~2.5s after it so the steps and counter can play out. `doneAt` defaults to ~0.7s before the end.
- Add `returnAt` (e.g. -0.6) to zoom back to full frame before the clip ends; it also returns automatically when the effect window ends early.

## Example

Line: "The video that you're currently watching was edited completely using Claude Code. I didn't have to hire an expensive editor."
```json
{
  "pullAt": 0.3,
  "filename": "daily-update.mp4",
  "skill": "video-editor",
  "steps": ["Transcribed the take", "Cut the pauses", "Added captions", "Graded the colour", "Rendered {frames} frames"],
  "returnAt": -0.5
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

- Under ~3s of window time the beats feel rushed; give it 4–7s.
- Step labels longer than the panel are truncated with an ellipsis — shorten them.
- Captions render inside the window, scaled down with the video; keep `captions.y` around 0.7 so they stay inside the cropped area.
- `videoAspect` 0.5625 shows the whole 9:16 frame in the window (taller window); the default 0.64 crops a little top and bottom like the reference.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
