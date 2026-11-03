---
name: fx-frame-break
description: Shrink a talking-head shot into a floating Instagram Reels or TikTok phone frame and have the speaker pop out of it. Their head breaks over the top edge and their hands reach past the sides, in 3D, with like / comment / share chrome, username and caption. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants a pop-out or out-of-frame effect, a "breaking out of the phone" or "3D pop out" look, their video shown as a Reel or TikTok inside the video, a frame break, or a social-feed mockup of their own clip, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Frame Break — Claude Video FX 04/17

The full-screen shot springs down into a phone-shaped Reels window floating on a dark, blurred copy of the footage. The window crops the shot just above the speaker's eyes, but the cut-out speaker is layered on top. Their cap and forehead break out over the top edge, and their hands reach past the sides. Once the window settles, the feed chrome fades in: heart, comment, share and more icons with counts, a round avatar, the username, a Follow pill, a one-line caption and a progress bar. Captions sit below the phone.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Talking about posting, going viral, or "this exact video".
- A hook that makes a plain talking head feel 3D in the first second.
- Showing the clip as it will look in the feed.

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
3. **Write the config** as `<video name> - frame-break.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still frame-break "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render frame-break "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Frame Break.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `at` | `0.1` | when the shot starts shrinking into the window (seconds or "@word") |
| `outAt` | `null` | optional: when it springs back to full screen (null = stays; it springs back automatically if the effect window ends before the clip) |
| `platform` | `"reels"` | "reels" (Instagram) or "tiktok" — which feed chrome to draw |
| `username` | `"yourhandle"` | handle shown under the video (no @ needed) |
| `caption` | `"auto"` | "auto" (first words of the transcript) or your own one-line caption |
| `likes` | `"48.2K"` | like count under the heart ("" to hide) |
| `comments` | `"1,204"` | comment count under the bubble ("" to hide) |
| `likeAt` | `null` | optional: when the heart turns red (seconds or "@word"), null = never |
| `ui` | `true` | true to draw the feed chrome, false for a clean window |
| `frameWidth` | `0.6` | window width as a fraction of the frame width (0.5-0.75) |
| `frameY` | `0.46` | vertical centre of the window, 0-1 of the frame height |
| `breakDepth` | `0.5` | where the window's top edge cuts the head: 0 = top of the head (little pops out), 1 = middle of the face (more pops out) |
| `sideBreak` | `1.1` | how much wider than the window the footage is (1.0 = no side break, 1.12 = hands reach past the sides) |
| `cornerRadius` | `40` | window corner radius in px at 1080 wide |
| `backdrop` | `"blur"` | "blur" (dark blurred copy of the footage), "dark" (charcoal gradient) or any CSS colour/gradient |
| `shadow` | `true` | soft drop shadow under the popped-out speaker (true/false) |
| `sideFade` | `0.08` | 0-0.15: fades the cut-out near the footage's left/right edges so a speaker who fills the frame doesn't end in a hard vertical line outside the window (0 = off) |

Run `node "$ENGINE/fx.mjs" info frame-break` to print these with the full default config.

## Writing the config

- `username`: the creator's handle without @. Always ask for it or take it from context; never leave "yourhandle" in a final render.
- `caption`: one short line (under ~45 characters), or "auto" to use the first words spoken.
- `platform`: "reels" (default) or "tiktok" if they talk about TikTok.
- `likeAt`: put it on a payoff word ("@viral") to turn the heart red at that moment.
- `at`: when the shrink starts. 0.1s works for an opener; for a mid-video moment use a word anchor.
- `breakDepth` sets how much of the head pops out: 0.3 is a little, 0.7 is the whole face. `sideBreak` 1.0 turns off the side pop-out.

## Example

Line: "But the truth is I don't have to do that anymore thanks to this new Claude Code AI video editor."
```json
{
  "username": "alexbuilds",
  "caption": "Claude edited this whole reel",
  "likes": "12.8K",
  "comments": "342",
  "likeAt": "@anymore",
  "captions": { "emphasis": ["truth", "anymore", "Claude"] }
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `pop`, centred at 89% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"pop"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.885` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"auto"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `64` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- The pop-out needs headroom. If the speaker's head is cut off by the top of the source frame, there is nothing above the window to break out. Lower `breakDepth` or accept a smaller pop.
- A speaker who fills the frame edge to edge gets a straight cut where the footage ends; `sideFade` (default 0.08) softens it. Raise it to 0.12 if you still see a vertical line beside the window.
- Feed text is drawn small at window scale, so keep `caption` short and the counts realistic ("12.8K", "342").
- With an effect window that ends early, the shot springs back to full screen on its own. Use `outAt` to control when.
- Turn `ui` off for a clean floating window (good for non-social topics).
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
