---
name: fx-ui-world
description: Turn the top of a talking-head video into a living chat-app UI — clip thumbnails fly into a "Drop files here" zone, a RAW CLIPS tape label sticks on and a slash command types itself out — while the speaker sits in the bottom panel and breaks out over the app. Renders an MP4 for Reels, TikTok or Shorts with bold captions. Use this whenever the user wants to show a prompt or command being typed, an AI chat interface, "drop your clips into Claude", an app UI above them, a split screen with software, or a UI-world / interface intro, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# UI World — Claude Video FX 03/17

A cream chat app slides in over the top ~60% of the frame: orange starburst logo and app name, and a dashed "Drop files here" box. Video thumbnails (frames of your clip) fly in on arcs, drop into the box and it becomes a message composer; a yellow tape label sticks on, then a slash command types in with a caret and the orange send button gets pressed. The footage slides down into the bottom panel and the speaker is cut out so their head pokes up over the app background. Captions are white bold caps low on the speaker.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Explaining a workflow that starts in an AI chat ("drop your clips in, trigger the skill").
- Showing the exact prompt or command to type.
- Any "here's the tool" moment where the software should feel like the set.

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
3. **Write the config** as `<video name> - ui-world.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still ui-world "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render ui-world "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - UI World.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `appName` | `"Claude"` | name next to the logo |
| `accent` | `"#D97757"` | logo / send-button colour |
| `background` | `"#F5F2EA"` | app background colour |
| `clips` | `5` | how many clip thumbnails fly in (1-6) |
| `thumbs` | `[]` | optional list of image/video files for the thumbnails (default: frames from your clip) |
| `label` | `"RAW CLIPS"` | text on the yellow tape label ("" to hide) |
| `placeholder` | `"How can I help you today?"` | composer placeholder before typing |
| `command` | `"/video-editor"` | what gets typed into the composer (e.g. /video-editor) |
| `typeSpeed` | `20` | typing speed in characters per second |
| `inAt` | `0` | when the UI slides in (seconds or "@word") |
| `intro` | `"slide"` | "slide" (app drops in from the top) or "cut" (appears instantly) |
| `dropAt` | `"auto"` | "auto" (on drop/upload/clip/file/video) or when the clips start flying in |
| `labelAt` | `"auto"` | "auto" (right after the clips land) or when the tape label sticks on |
| `typeAt` | `"auto"` | "auto" (on trigger/run/skill/command..., else halfway) or when typing starts |
| `sendAt` | `"auto"` | "auto" (just after typing ends) or when the send button is pressed |
| `outAt` | `null` | optional: when the app slides away and the footage returns to full frame (null = stays) |
| `split` | `0.62` | where the app background ends and the video panel starts, 0-1 of the height |
| `shift` | `"auto"` | "auto" (move the footage so the head sits under the composer) or a 0-1 fraction of the height to move it down |

Run `node "$ENGINE/fx.mjs" info ui-world` to print these with the full default config.

## Writing the config

- `command`: what gets typed — the real command or prompt (keep it under ~28 characters so it fits on one line).
- `label`: 1–2 words describing what was dropped ("RAW CLIPS", "PDF NOTES", "SCREENSHOTS").
- `dropAt` on the word that describes adding files ("@drop"), `typeAt` on the action word ("@trigger", "@type", "@run"). `"auto"` looks for those words and otherwise spreads the beats across the clip.
- `appName` / `accent` can rebrand the app; default is a Claude-style look.
- `thumbs` takes your own images/clips for the flying thumbnails; by default they're frames from the clip.
- Use a `window` (e.g. `[0.4, 5.6]`) to run it in the middle of a longer clip — the app slides in and out.

## Example

Line: "If you wanted to build your own course selling platform, all you have to do is download this GitHub repo."
```json
{
  "command": "/clone-repo gumroad",
  "label": "COURSE PLATFORM",
  "clips": 4,
  "dropAt": "@build",
  "typeAt": "@download",
  "window": [0.4, 5.6]
}
```

## Captions

Captions are on by default, word by word, timed from the transcript. Put caption settings under `"captions"` in the config. This effect's defaults: style `caps`, centred at 83% of the frame height.

| Option | Default | What it does |
|---|---|---|
| `enabled` | `true` | `false` hides captions (or pass `--no-captions`) |
| `style` | `"caps"` | `pop` white bold words with a coloured key word · `caps` ALL CAPS · `twoTier` small line + one huge key word · `serif` small line + big gold italic serif word with sparkles · `tracked` small wide-spaced caps · `box` words on black chips, key word on a yellow chip |
| `y` | `0.83` | vertical centre of the caption, 0 = top, 1 = bottom |
| `emphasis` | `"none"` | `"auto"` highlights the strongest word per phrase, `"none"`, or a list like `["course", "editing"]` |
| `accent` | `"#FFE14D"` | colour of highlighted words |
| `size` | `70` | font size in px at 1080 wide |
| `maxWords` / `maxChars` | `4` / `22` | how much text one caption phrase holds |
| `uppercase` | `false` | force capitals |

## Timing references

Any option that takes a time accepts seconds from the start of the range (`1.5`), seconds before the end (`-1`), or a spoken word: `"@course"` (first time it is said in the range), `"@course#2"` (second time), `"@course+0.3"` / `"@course-0.2"` (offset), `"@course:end"` (when it finishes), `"@build_your_own"` (a phrase; underscores for spaces). Matching ignores case and punctuation, runs after `fixes`, and falls back to "starts with" ("@edit" finds "editing"). Words are counted within the rendered range only. A word that isn't found silently uses the effect's default time, so read the timing lines the CLI prints.

## Getting it right

- Leave ~1s after `typeAt` for the command to finish typing before the window or clip ends (typing runs at `typeSpeed`, 20 chars/s by default).
- The footage moves down so the head sits under the composer; on very wide shots set `shift` to 0 to keep it in place.
- Captions default to `y` 0.83 so they sit on the chest under the face; move them with `captions.y`.
- Needs the cut-out pass for the head breakout; it runs automatically the first time (about 4 seconds per second of video).
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
