---
name: fx-couch-wall
description: Fill the room behind a talking-head speaker with a wall of short-form video thumbnails — portrait tiles with ▷ view counts and headline stickers pop in around them while they stay in front, like a creator's grid of past reels. Renders an MP4 for Reels, TikTok or Shorts with two-tier captions. Use this whenever the user wants a "wall of videos" or "wall of thumbnails" behind them, social proof of their content, a creator-portfolio or "all my reels" moment, a collage behind the person, or the couch wall effect, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Couch Wall — Claude Video FX 02/17

A masonry wall of 9:16-style thumbnails (rounded tiles, thin gaps) pops in tile by tile outward from the speaker's head in about half a second, covering the room behind them. Most tiles carry a white "▷ 1.07M" view-count badge, a few carry white headline stickers ("6 ways to make money with AI this week"). The speaker is cut out and stays in front; the wall drifts in very slowly while it holds. Captions are two-tier: a small setup line over one huge word ("selling a / COURSE").

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Social proof: "I've posted hundreds of videos", "this got millions of views".
- Talking about content, courses, a channel or a body of work.
- A punchy visual reset in the middle of a one-take talking head.

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
3. **Write the config** as `<video name> - couch-wall.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still couch-wall "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render couch-wall "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Couch Wall.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `at` | `0.15` | when the tiles start popping in (seconds or "@word") |
| `fillDuration` | `0.55` | seconds from first to last tile (0.4-0.8 feels snappy) |
| `outAt` | `null` | optional: when the wall pops away (null = holds to the end; it also leaves automatically when an effect window ends early) |
| `media` | `[]` | optional list of image/video file paths for the tiles (your real thumbnails/clips); they repeat if there are fewer than tiles. Empty = stills of this clip |
| `labels` | `["6 ways to make money with AI this week","Can you tell??"]` | white headline stickers placed on a few tiles, e.g. ["6 ways to make money with AI", "Can you tell??"]. Empty list = none |
| `views` | `null` | optional list of view-count strings ("1.07M", "534K"); null = plausible random counts |
| `showViews` | `true` | show the ▷ view-count badge on most tiles |
| `columns` | `3` | number of tile columns (3 = reference look, 4 = denser) |
| `gap` | `8` | gap between tiles in px (at 1080 wide) |
| `radius` | `10` | tile corner radius in px |
| `wallBottom` | `"auto"` | "auto" (from the speaker's head) or a 0-1 fraction: how far down the frame the wall reaches |
| `drift` | `0.035` | slow push-in of the wall while it holds (0 = static, 0.04 = subtle) |

Run `node "$ENGINE/fx.mjs" info couch-wall` to print these with the full default config.

## Writing the config

- `at`: land the wall on the word that names the content ("@course", "@videos"), or 0.1–0.3s in.
- `media`: if the user has real thumbnails or clips, list their file paths; that's the most convincing look. With nothing given, tiles are stills of the clip itself at different moments, crops and grades — fine for a demo, but say so to the user.
- `labels`: 1–3 short hooks that sound like real video titles from the user's niche (≤ 7 words each). Use `[]` for none.
- `views`: optional; give real numbers if the user has them, otherwise leave `null` for plausible counts.
- `captions.emphasis`: the single word that should go huge in the two-tier caption ("course", "platform"). Two-tier captions read best when the emphasis word ends the phrase.

## Example

Line: "If you wanted to build your own course selling platform, all you have to do is download this GitHub repo."
```json
{
  "at": "@build",
  "labels": ["How I sell my course", "Can you tell??", "My $0 tech stack"],
  "views": ["1.07M", "534K", "133K", "5,488", "15.3K", "2.2M", "847K", "61K"],
  "captions": { "style": "twoTier", "emphasis": ["course", "platform", "GitHub"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `twoTier`, centred at 62% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"twoTier"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.62` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- Only the person is cut out. Props in front of them (a microphone on an arm, a desk lamp) are treated as background and disappear under the tiles; warn the user if their mic sits in front of the wall area.
- If the speaker's head is very high or low in frame, set `wallBottom` (0.45–0.7) so the wall stops around shoulder height.
- `columns: 4` makes smaller, denser tiles for close-up framing; `3` matches the reference.
- Keep the effect window short (2–5 s). Use `"window": [start, end]` or `outAt` so the wall pops away before the clip ends if the video continues.
- Two-tier captions with an emphasis word mid-phrase can read oddly; pick emphasis words that end a phrase, or switch `captions.style` to `"pop"`.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
