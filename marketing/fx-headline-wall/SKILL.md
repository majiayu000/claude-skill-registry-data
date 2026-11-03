---
name: fx-headline-wall
description: Slap a collage of headlines, tweets, search bars and POV cards onto the wall behind a talking-head speaker — press-style paper headlines in bold serif, italic quotes, tweet cards, Google-style search pills and black POV cards pin up one after another, then a big hero headline lands with a yellow highlighter swipe. Renders an MP4 for Reels, TikTok or Shorts. Use this whenever the user wants headlines or news behind them, "everyone is talking about this", press/hype/social-proof moments, tweets or screenshots on the wall, a buzz or trend montage behind the person, or the headline wall effect, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Headline Wall — Claude Video FX 08/17

Cream paper headline notes (bold black serif, tiny uppercase kicker), italic quote cards, white tweet cards with avatar and action icons, a search pill with a blinking caret, black "POV:" cards, chat bubbles and a notification pop onto the wall behind the speaker, every 2–3 frames, each with a quick overshoot, slight tilt and a soft shadow. A larger hero card lands last and a yellow highlighter swipes across its key word. The speaker is cut out and stays in front of the whole collage.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- "Everyone is talking about X" / "X just changed everything" moments.
- Hype, news or trend videos: a new tool, launch, controversy.
- Social proof without real screenshots.

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
3. **Write the config** as `<video name> - headline-wall.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still headline-wall "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render headline-wall "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Headline Wall.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `cards` | `"auto"` | "auto" (written from the transcript) or a list of cards. Each card: {"type": "note" \| "quote" \| "tweet" \| "search" \| "pov" \| "bubble" \| "notify", "text": "..."} plus optional "kicker" (small caps line on notes), "name" / "handle" (tweet author, quote byline, notification app), "highlight" (word to mark yellow), "hero": true (the big card that lands last). Order = order they appear; the first cards get the most visible spots |
| `count` | `11` | how many cards auto mode writes (8-12 fills the wall) |
| `at` | `0.1` | when the first card lands (seconds or "@word") |
| `stagger` | `3` | frames between cards (2-4 = rapid-fire, 6+ = one by one) |
| `heroDelay` | `6` | extra frames before the hero card lands |
| `outAt` | `null` | optional: when the cards pop off (null = hold to the end; they also leave automatically when an effect window ends early) |
| `columns` | `3` | card columns across the wall (3 = reference look, 4 = smaller, denser cards) |
| `cardScale` | `1` | card size multiplier (0.85-1.15) |
| `wallBottom` | `"auto"` | "auto" (from the speaker's head) or a 0-1 fraction: how far down the cards reach |
| `accent` | `"#FFE14D"` | highlighter colour |
| `dim` | `0.12` | darken the room behind the cards a little so they pop (0 = off, 0.25 = subtle) |

Run `node "$ENGINE/fx.mjs" info headline-wall` to print these with the full default config.

## Writing the config

- Write `cards` yourself from the video's topic — 8 to 12 cards, short and punchy (headlines ≤ 7 words, tweets ≤ 12 words, search pills ≤ 6 words, lowercase like real queries). Mix types: 3–4 `note`, 2 `tweet`, 1–2 `pov`, 1–2 `quote`, 1 `search`, 1 `bubble` or `notify`.
- The first cards in the list get the most visible spots (beside and above the head); cards placed behind the head are mostly hidden, so put the strongest lines first.
- Exactly one card should be the hero: add `"hero": true` and `"highlight": "<word>"` (the topic word, e.g. the product name). It lands last, bigger, with the yellow marker.
- `at`: start on the word that introduces the hype ("@everyone", "@watching").
- Leave `cards: "auto"` only for a quick demo; auto text is cut from the transcript and reads generic.

## Example

Line: "The video that you're currently watching was edited completely using Claude Code. I didn't have to hire an expensive editor."
```json
{
  "at": "@watching",
  "cards": [
    { "type": "note", "kicker": "Creator briefing", "text": "Claude edits everyone's videos now" },
    { "type": "search", "text": "can claude edit videos" },
    { "type": "tweet", "name": "Agency owner", "handle": "@agencyowner", "text": "Dropped my clips in. Claude did the edit." },
    { "type": "pov", "text": "Claude edits your reel" },
    { "type": "quote", "text": "Claude cut my whole reel.", "name": "@founder" },
    { "type": "bubble", "text": "wait, Claude edits videos??" },
    { "type": "note", "kicker": "Weekly digest", "text": "Editors are worried about Claude" },
    { "type": "notify", "name": "Claude", "text": "Your video is ready to post" },
    { "type": "pov", "text": "you never hire an editor again" },
    { "type": "quote", "text": "Your next video editor is Claude.", "name": "@makesreels" },
    { "type": "note", "kicker": "Tech newsletter", "text": "Claude can edit your videos now", "highlight": "Claude", "hero": true }
  ],
  "captions": { "emphasis": ["Claude", "editor"] }
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

- Close-up framing leaves little wall: cards fill the top band and the sides of the head. Use `columns: 4` and `cardScale: 0.9` for tight shots, or `wallBottom` to let cards reach lower.
- Only the person is cut out; a microphone or lamp in front of the wall goes behind the cards.
- `stagger` 2–3 = rapid-fire flurry (reference); 5–6 if the user wants each card to be readable.
- If the room is bright and cards wash out, raise `dim` to 0.2–0.3.
- Don't invent real people's names or real publications on cards; use roles ("Agency owner") and generic kickers.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
