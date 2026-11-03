---
name: fx-green-screen
description: Put a talking-head speaker on a new background without a green screen. The person is cut out and set into an animated app UI (focus timer, task list, chat input with a typing cursor, a big serif line behind their head), or onto any image, video or gradient. Renders an MP4 for Reels, TikTok or Shorts with boxed word captions. Use this whenever the user wants to replace or remove their background, a virtual or fake green screen, to stand in front of an app, website, product or screenshot, a "me in front of the UI" shot, or background removal on video, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Green Screen — Claude Video FX 12/17

The room dissolves away while the speaker glides down into the lower centre of the frame. They are cut out and stay there at a smaller size. By default they stand in front of an animated productivity app with a purple band on top. The cream app window holds a black FOCUS bar with a ticking countdown, and a task list whose first task ticks off with a red NOW pill. A big serif line ("Everything else waits.") sits behind their head. A chat input below gets clicked by a cursor and typed into, over a blue band. Captions are word chips: white on black, with the key word on yellow.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Talking about an app, tool, workflow or product: put the speaker in front of it.
- Replacing a messy or boring room with a branded image or gradient.
- A "focus / productivity / do this one thing" message (the default UI says exactly that).

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
3. **Write the config** as `<video name> - green-screen.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still green-screen "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render green-screen "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Green Screen.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `background` | `{"type":"ui"}` | {"type": "ui"} (animated app, default); {"type": "image", "src": "path.png", "fit": "cover" \| "contain", "position": "50% 50%", "blur": 0, "brightness": 1}; {"type": "video", "src": "path.mp4", same fit/position}; or {"type": "gradient", "css": "linear-gradient(...)"}. "cover" fills the frame and crops (a landscape image keeps only its middle third — use "position" like "30% 50%" to choose which part), "contain" shows the whole image over a blurred fill. For ui: optional "topColor" and "bottomColor" as [from, to] colour pairs |
| `headline` | `"Everything else waits."` | big serif line near the speaker's head ("" for none). On the app UI it sits behind the head like the reference; keep it to 2-4 short words there. On image/video/gradient backgrounds it sits just above the head, so up to ~24 characters fits |
| `headlineColor` | `"#FFFFFF"` | headline colour on image/video/gradient backgrounds (the app UI always uses dark ink) |
| `headlineOffset` | `"auto"` | "auto" (behind the head on the UI, just above the head elsewhere) or a number: how far above the speaker's face centre the line sits, as a fraction of frame height (re-tune it if you change subject.scale) |
| `app` | `"Claude"` | app name in the window's title bar |
| `timer` | `"49:57"` | starting time of the FOCUS countdown, "mm:ss" |
| `task` | `"Write the sales page"` | task shown next to the timer |
| `tasks` | `["Write the sales page","Record 2 reels","Send the newsle…` | three task-list rows; the first one is the active task (ticked, NOW pill), the rest are locked |
| `input` | `"What should I work on next?"` | text the cursor types into the chat input |
| `cursorAt` | `1.1` | when the cursor appears and heads to the input (seconds or "@word"); it clicks ~0.6s later and starts typing |
| `accent` | `"#C9472F"` | accent colour (burst icon, active task, NOW pill, send button) |
| `subject` | `{"y":0.57,"x":0.5,"scale":"auto"}` | where the speaker lands: {"y": 0.57 (face height, 0-1), "x": 0.5, "scale": "auto" or a number}. "auto" picks the smallest scale that keeps the bottom of the shot on the bottom edge (about 0.5-0.7). A number is the size relative to the original footage (1 = unchanged) and drops that bottom anchoring. Seated-at-a-desk footage: use about {"y": 0.56, "scale": 0.8} so the desk edge and arm cut-offs fall below the frame |
| `at` | `0` | when the switch to the new background starts (seconds or "@word") |
| `outAt` | `null` | optional: when it switches back to the real room (null = stays; it switches back automatically if the effect window ends before the clip) |
| `intro` | `"morph"` | "morph" (the real room dissolves while the speaker glides into place, so the room is visible for the first few frames) or "cut" (instant switch; use it when the room must never show) |
| `sideFade` | `0.08` | 0-0.15: fades the cut-out near the footage's left/right edges (hides the straight edge of a speaker who fills the frame) |
| `bottomFade` | `0.5` | 0-0.9: fades the lower body into the background, measured as a share of the face-to-bottom distance (hides the diagonal cut a desk leaves). 0 = off. On light backgrounds keep it at or below ~0.55 or the torso turns to fog |
| `shadow` | `true` | soft shadow behind the speaker (true/false) |
| `captionPlacement` | `"auto"` | "auto" (just above the headline) or "keep" (use captions.y) |
| `headlineSize` | `84` | headline font size in px at 1080 wide (84 default; 60-70 for longer lines) |

Run `node "$ENGINE/fx.mjs" info green-screen` to print these with the full default config.

## Writing the config

- Default UI: rewrite `task`, `tasks` (3 rows, first is active), `timer`, `input` (what gets typed) and `headline` to match what the speaker says. Keep `app` as the tool being discussed.
- `headline` on the default app UI sits behind the head (like the reference) — 18–26 characters, and expect the middle to be covered. On image, video and gradient backgrounds it is placed just above the head and stays readable; up to ~24 characters, or lower `headlineSize` for longer lines.
- Own media: `"background": {"type": "image", "src": "path.png"}` or `{"type": "video", "src": "path.mp4"}` (add `"blur": 12, "brightness": 0.7` to push it back). `"fit": "cover"` (default) fills the frame and crops — a landscape 16:9 image keeps only its middle third, so pick the part with `"position": "30% 50%"`; `"fit": "contain"` shows the whole image over a blurred fill. Set `headlineColor` for contrast on light images.
- "Replace my room" requests: use `"intro": "cut"`, otherwise the real room shows for the first few frames while it dissolves.
- `subject`: `y` moves the face height (0.5 = higher, 0.62 = lower). `scale: "auto"` keeps the bottom of the shot on the bottom edge (about 0.5–0.7 of the original size). **Seated at a desk** (the usual talking-head setup): use `{"y": 0.56, "scale": 0.8}` so the desk edge and the arm cut by the frame edge drop out of view; auto scale leaves them visible.
- `cursorAt`: anchor the cursor click to the word where the speaker says what to do.

## Example

Line: "The video that you're currently watching was edited completely using Claude Code."
```json
{
  "headline": "Editing handles itself.",
  "timer": "24:59",
  "task": "Edit today's reel",
  "tasks": ["Edit today's reel", "Write the caption", "Schedule the post"],
  "input": "Cut the pauses and add captions",
  "cursorAt": "@edited",
  "captions": { "emphasis": ["currently", "Claude"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `box`, centred at 70% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"box"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.7` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `70` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- Desks cut people diagonally. The reliable fix is a numeric `subject.scale` (~0.8) that pushes the desk below the frame; `bottomFade` (default 0.5) then softens what's left. On light backgrounds keep `bottomFade` ≤ 0.55 or the torso turns to fog.
- Speakers who fill the frame edge to edge get straight side edges once scaled down. `sideFade` softens them.
- The cut-out is only as good as the matte. Busy backgrounds and motion-blurred hands can leave soft edges; that reads fine at this scale.
- White headlines vanish on light images. Set `headlineColor` (e.g. "#111111").
- A numeric `headlineOffset` is measured from the face, so re-tune it whenever you change `subject.scale`; leave it on "auto" unless you need a specific spot.
- If the effect window ends early, the room dissolves back in. Use `"intro": "cut"` for an instant switch both ways.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
