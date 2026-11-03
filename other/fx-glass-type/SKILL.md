---
name: fx-glass-type
description: Put a giant 3D glass word on the wall behind a talking-head speaker at head height — thick clear glass letters in perspective that bend and magnify the room like a lens, with bright rims, a glossy highlight, dark inner edges and a wall shadow, fading in with a light sweep while the speaker stays in front. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants 3D text, glass or chrome text, a big word on the wall behind them, text behind the person, a premium or Apple-style title in their room, or the glass type effect, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Glass Type — Claude Video FX 17/17

One big word made of thick clear glass stands on the wall behind the speaker at head height, turned in perspective so it recedes to one side and spans most of the frame width. The letters are tall and condensed with a visible extruded body of bright edges. Their faces bend and magnify the room behind them like a lens (strongest at the rims), with a glossy highlight band, dark inner edges that give thickness, bright specular rims and a soft shadow on the wall. The word fades in from a blur, a light sweep glides across it, and it sways a few degrees while it holds. The speaker is cut out and covers the lower part of the middle letters.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Naming the one idea of the video ("DESIGN", "FOCUS", "AI").
- Brand or product reveals in a premium, tech look.
- Any "text behind the person" moment that should feel more 3D than a flat title.

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
3. **Write the config** as `<video name> - glass-type.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still glass-type "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render glass-type "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Glass Type.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `word` | `"DESIGN"` | the word made of glass (one word, 4-8 letters reads best) |
| `font` | `"black"` | letter style: "black" (heavy grotesk, reference look), "sans" (Inter Black), "serif" (Playfair) or "didone" (Bodoni) |
| `at` | `0.15` | when the letters fade in (seconds or "@word") |
| `fadeDuration` | `0.6` | seconds the fade/blur-in takes |
| `sweepDuration` | `1.1` | seconds the light sweep takes to cross the word |
| `outAt` | `null` | optional: when the letters fade away (null = hold to the end; they also leave automatically when an effect window ends early) |
| `widthFraction` | `0.95` | how much of the frame width the word spans after the perspective turn (0.95 = edge to edge) |
| `size` | `1` | extra size multiplier on top of the automatic fit (1 = fit to widthFraction) |
| `condense` | `0.66` | horizontal squeeze of the letters (0.66 = tall condensed glass letters like the reference, 1 = the font's normal width) |
| `y` | `"auto"` | "auto" (placed from the head) or a 0-1 fraction for the top of the letters |
| `x` | `0` | horizontal nudge as a fraction of the frame (-0.1 = left) |
| `overlap` | `0.5` | how much of the letter height the head covers, 0-1 (0.5 = lower half of the middle letters hidden; keep ≤ 0.55 so the word stays readable) |
| `rotateY` | `30` | perspective turn in degrees (positive = word recedes to the right, negative = to the left) |
| `rotateX` | `5` | tilt in degrees (positive = top leans back) |
| `sway` | `3` | degrees of slow turn while it holds (0 = static) |
| `depth` | `44` | thickness of the glass in px |
| `refraction` | `0.22` | how strongly the glass bends and magnifies the room (0.1 = subtle, 0.22 = thick glass, 0.35 = heavy lens) |
| `brightness` | `1.1` | brightness of the room seen through the glass (1.0-1.4) |
| `tint` | `"#FFFFFF"` | glass tint colour (white = clear glass) |
| `letterSpacing` | `0.03` | letter spacing in em |
| `shadow` | `0.5` | strength of the soft shadow the letters cast on the wall (0-0.8) |

Run `node "$ENGINE/fx.mjs" info glass-type` to print these with the full default config.

## Writing the config

- `word`: one word, 4–8 letters, upper-cased automatically. Take it from the key noun the speaker stresses.
- `at`: start a beat before the word is spoken ("@design-0.2") or 0.1–0.3 s in.
- Size and placement are automatic: the word is fitted to `widthFraction` of the frame after the perspective turn, set at head height with `overlap` of the letter height behind the head, and shrunk if needed so at least the top half of every letter stays visible. Short words or a head near the top of the frame therefore come out narrower.
- `font`: `black` (heavy grotesk, reference look) suits most words; `serif` or `didone` for fashion/editorial topics. `condense` 0.6–0.75 gives the tall glass-letter look; 1 uses the font's own width.
- `rotateY`: positive recedes to the right (reference), negative to the left. Point it away from the side with more empty wall.
- Glass shows what is behind it: shelves, windows, plants and lights bend visibly through the letters; on a plain wall it reads as clear acrylic with bright edges.

## Example

Line: "But the truth is I don't have to do that anymore thanks to this new Claude Code AI video editor."
```json
{
  "word": "CLAUDE",
  "at": "@truth",
  "captions": { "emphasis": ["truth", "anymore", "Claude"] }
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

- If the word looks too small, the speaker's head is probably high in frame (the readability cap shrinks it). Lower `overlap` (0.35), or set `y` (e.g. 0.06) to place it yourself; with `y` set, `widthFraction` decides the size.
- For wide shots with lots of wall, set `y` (0.15–0.25) and `overlap` 0.2 so the whole word sits on the wall above the head.
- Raise `refraction` (0.3) for a heavier lens; lower `depth` (25) for thinner glass; raise `shadow` (0.7) if the letters don't separate from a pale wall.
- Very dark rooms: set `tint` to a light colour such as `#DDEBFF` so the glass doesn't disappear.
- Only the person is cut out; a microphone in front of the wall area will show the letters over it.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
