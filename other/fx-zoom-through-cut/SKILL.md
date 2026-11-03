---
name: fx-zoom-through-cut
description: Join two talking-head shots with a whip "zoom-through" transition — the first shot rushes in toward the speaker with a radial zoom blur and a little spin, hard-cuts at the peak, and the second shot bursts out from extremely close and settles, each with its own caption style. Works with two clips or by splitting one clip. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants a zoom transition, whip zoom, punch-through, "zoom into the next clip", a smooth transition between two takes or locations, or to hide a jump cut, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Zoom-Through Cut — Claude Video FX 09/17

Over the last ~9 frames of shot A the frame accelerates toward the speaker's chest, smearing into a radial zoom blur with a slight clockwise spin, and A's caption blurs away with it. Hard cut. Shot B starts about 3.4× zoomed in, blurred and tilted, then decelerates out to normal framing over ~12 frames, and its caption fades in. By default A's captions use the gold serif style and B's use wide-tracked small caps, like the reference.

This effect can take a second clip (`--second`). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Moving between two takes, outfits or locations ("…or you can get the…").
- Hiding a jump cut inside one long take (single-clip mode with `cutAt`).
- A "but wait" or contrast beat where the second shot should feel like a reveal.

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
3. **Write the config** as `<video name> - zoom-through-cut.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still zoom-through-cut "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript; after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render zoom-through-cut "<video>" --start <s> --end <s> --config "<config.json>" [--second "<other video>" --second-start a --second-end b] --out "<folder>/<video name> - Zoom-Through Cut.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `cutAt` | `"auto"` | single-clip mode: where the cut happens (seconds or "@word"; "auto" = a word boundary near the middle). Ignored with --second (the cut is where clip A ends) |
| `pushFrames` | `9` | frames shot A spends rushing in before the cut (8-10 feels like the reference) |
| `pullFrames` | `12` | frames shot B takes to settle after the cut (10-14) |
| `pushScale` | `4` | how far shot A zooms in by the cut (4 = 4x) |
| `pullScale` | `3.4` | how zoomed-in shot B starts (3.5 = 3.5x) |
| `blur` | `0.55` | strength of the radial zoom blur (0 = none, 0.6 = strong) |
| `samples` | `12` | blur quality: copies used for the blur (6-9) |
| `rotate` | `7` | degrees of spin across the transition (0 = straight zoom) |
| `focus` | `"chest"` | where shot A zooms: "chest" (default), "face", or [x, y] as 0-1 fractions |
| `focusB` | `null` | where shot B zooms out from (defaults to focus) |
| `captionsA` | `{}` | caption overrides for shot A, e.g. {"style": "serif"} |
| `captionsB` | `{"style":"tracked"}` | caption overrides for shot B, e.g. {"style": "tracked"} |

Run `node "$ENGINE/fx.mjs" info zoom-through-cut` to print these with the full default config.

## Writing the config

- Two clips: render with `--second "<clip B>" --second-start s --second-end s`; the cut is where clip A ends, so trim clip A to end right after a phrase.
- One clip: `cutAt` picks the cut, e.g. `"@absolutely"` (the cut lands as that word starts). `"auto"` picks a word boundary near the middle.
- `captionsA` / `captionsB` override the caption look per shot, e.g. `{"emphasis": ["Claude"]}` for the gold word in shot A, or `{"style": "pop"}` in shot B.
- Faster and harder: `pushFrames` 7, `pullFrames` 10, `blur` 0.65. Calmer: `rotate` 0 and `blur` 0.35.
- `focus` sets where the zoom goes (`"chest"`, `"face"` or `[x, y]`); use `"face"` for tight close-ups.

## Example

Shot A line: "…edited completely using Claude code." Shot B line: "Meaning that if you wanted to build your own course selling platform…"
```json
{
  "captionsA": { "emphasis": ["Claude"] }
}
```
Rendered with `--start 0 --end 5.6 --second "<shot B>.mp4" --second-start 21 --second-end 27`.

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `serif`, centred at 60% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"serif"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.6` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `72` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- End shot A on a finished phrase; the push eats the last ~0.3s, so a word that runs into the cut gets blurred away.
- The blur is built from stacked copies of the frame; at the peak you may see faint rings in a paused frame, which read as motion blur at full speed. Raise `samples` (12–16) for cleaner stills, at some render cost.
- Two very different exposures cut harder; that is often the point, but match brightness if you want it seamless.
- Without a cut-out the zoom aims at the centre-chest of a typical framing; if the speaker sits off-centre, set `focus` to `[x, y]`.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
