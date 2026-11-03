---
name: fx-phone-mockup
description: Float a realistic iPhone next to the speaker in a talking-head video, with an app conversation that plays itself out — message, typing dots, a recommendation card, a finger tap on "Approve" and a reply — or your own screenshot/screen recording on the screen. Renders an MP4 for Reels, TikTok or Shorts with captions. Use this whenever the user wants a phone mockup, an app demo beside them, "show the app on a phone", a floating iPhone, a chat or notification on a phone screen, or to put a screen recording in a phone frame, even if they never mention Remotion.
---

> **Video Studio:** run every command from the Video Studio folder; `ENGINE` is `engines/video-fx/engine` (set up already: `node "engines/video-fx/engine/fx.mjs" doctor` should be all ✔). These lines win over the steps below where they differ:
> - **Footage from a studio job:** the source is `jobs/<id>/source.*`. Put configs and renders in `jobs/<id>/fx/` (`<effect>.json`, `<Effect>.mp4`), never next to the original.
> - **Never transcribe again.** Before the first still or render of a range: `node studio/words-convert.mjs video-fx projects/<id>/transcript/words.json jobs/<id>/fx/words-<start>-<end>.json <start> <end>`, then add `--words jobs/<id>/fx/words-<start>-<end>.json` (same `--start/--end`) to every `still`/`render` of that range. To pick moments, read `projects/<id>/transcript/words.json` instead of `fx.mjs words`. Use `words` (Whisper small on CPU) only for a video that isn't a studio job.
> - **Brand:** captions use the brand purple, not gold/yellow: every config gets `"captions": {"accent": "#C4B5FD"}` (plus any style/y settings), the same block in every segment of one video. Graphics that take a colour use `styles/brand.json` (accent #8B5CF6, accentLight #C4B5FD, accentDeep #4C1D95).
> - **Content:** headlines, checklist items, chart labels and phone messages come from what Bryan actually says or the Content OS script's cue tags; real numbers only. Generic app mockups only, never posing as a real company's product.
> - **Deliver:** the spliced full video goes to `jobs/<id>/preview.mp4` (review) or `final.mp4` (approved); log each effect with its time range in `edits.json` so the review page can take notes on it. Sounds: these renders have none; add them after with `studio/sfx.mjs` like any style.
> - **If doctor shows ✖:** in `engines/video-fx/engine`: `npm install`; `uv venv .venv --python 3.12` + `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`; the matting model into `models/` (URL in `engines/video-fx/install.mjs`); `node fx.mjs browser`. Don't run `install.mjs` (it copies these skills into ~/.claude/skills).
> - **Licences:** Remotion is free for companies of up to 3 people; the cut-out model (Robust Video Matting) is GPL-3.0 and is downloaded, never committed.

# Phone Mockup — Claude Video FX 06/17

A titanium iPhone (dynamic island, status bar, home indicator) springs in from the side beside the speaker's head with a slight 3D tilt, soft shadow and gentle float, while the footage pans a little the other way to keep the face clear. On screen, a dark chat-assistant app plays out: header with avatar, a message, typing dots, a recommendation card with stat tiles, then a touch indicator taps the white button, which turns green with a check and a reply bubble pops in.

This effect cuts the speaker out of the background (person matte, cached after the first run). Output: 1080×1920, 30 fps H.264 MP4 with the original audio.

## When to use it

- Showing what an app, bot or automation does while explaining it.
- "It just sends me a message and I hit approve" moments.
- Putting a real screenshot or screen recording into a phone frame (`screen`).

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
3. **Write the config** as `<video name> - phone-mockup.json` next to the video (or in the folder the user names). The engine never modifies the source video; every output is a new file. Repair misheard names with `"fixes"` (e.g. `{"cloud code": "Claude Code"}`).
4. **Check one frame** before the full render:
   `node "$ENGINE/fx.mjs" still phone-mockup "<video>" --start <s> --end <s> --config "<config.json>" --at <seconds into the clip> --out "<folder>/check.png"`
   then look at the PNG. The first still or render of a new range also makes the transcript and the cut-out (about 1s of processing per 9 frames, cached per exact --start/--end, so settle the range first); after that, it's fast. The CLI prints where every `"@word"` lands — fix any line marked `!` (word not found, default time used).
5. **Render:**
   `node "$ENGINE/fx.mjs" render phone-mockup "<video>" --start <s> --end <s> --config "<config.json>" --out "<folder>/<video name> - Phone Mockup.mp4"`
6. **Review:** `node "$ENGINE/fx.mjs" sheet "<output.mp4>" --fps 4` writes `<output>-sheet.png` next to the MP4 (use `--fps 2` for clips over 10s, `--from/--to` to zoom into a moment). For small text, grab a full-size frame: `node "$ENGINE/fx.mjs" frame "<output.mp4>" --at <s>`. Re-render if anything is off.
7. **Splice (moments inside a longer video):** `node "$ENGINE/fx.mjs" splice "<video>" --segments "<segment.mp4>@<start s>" --out "<folder>/<video name> - edited.mp4"`. It re-encodes the whole video to high-quality H.264 under the original (first) audio track.
8. Tell the user the output path(s), the time range used and what the effect shows.

`--start/--end` cut the source down to that range (times in seconds of the original file); everything in the config is relative to the start of that range. `"window": [from, to]` (seconds into the range) runs the effect for only part of it, with untouched footage outside. Add `--draft` for a quick half-resolution preview.

## Options

| Option | Default | What it does |
|---|---|---|
| `side` | `"auto"` | "auto" (the side with more room), "left" or "right" |
| `size` | `0.33` | phone width as a fraction of the frame width (0.3-0.4) |
| `y` | `"auto"` | "auto" (level with the head) or a 0-1 fraction for the phone's top edge |
| `tilt` | `12` | 3D tilt in degrees (0 = flat facing camera) |
| `nudge` | `"auto"` | "auto" pans the footage away from the phone so the face isn't covered, or a 0-0.12 fraction of the frame width (0 = no pan) |
| `app.name` | `null` | app name in the header |
| `app.status` | `null` | line under the app name (e.g. Online) |
| `app.avatarColor` | `null` | avatar / accent colour |
| `message` | `"Found one fix for you."` | the assistant's first message |
| `card.label` | `null` | small tracked label on the card |
| `card.title` | `null` | the card's headline (1-2 short lines) |
| `card.tiles` | `null` | up to 3 stat tiles: [{"label": "Ad 1", "value": 0.9, "color": "#6FD38A"}] (value 0-1 = bar fill); [] hides them |
| `button` | `"Approve"` | primary button label that gets tapped |
| `secondary` | `"Not now"` | secondary text next to the button ("" hides it) |
| `approvedLabel` | `"Approved"` | button label after the tap |
| `reply` | `"Done. Budget moved to Ad 1."` | reply bubble that appears after the tap ("" for none) |
| `screen` | `null` | optional image or video file shown on the screen instead of the chat UI |
| `inAt` | `0.05` | when the phone flies in (seconds or "@word") |
| `messageAt` | `"auto"` | "auto" or when the first message appears |
| `cardAt` | `"auto"` | "auto" (about 30% in) or when the card appears |
| `tapAt` | `"auto"` | "auto" (on words like approve/click/tap/done, else ~65% in) or when the button is tapped |
| `outAt` | `null` | optional: when the phone flies back out (null = stays) |
| `app` | `{"name":"Ads Assistant","status":"Online","avatarColor":"…` |  |
| `card` | `{"label":"RECOMMENDATION","title":"Pause Ad 3, move the b…` |  |

Run `node "$ENGINE/fx.mjs" info phone-mockup` to print these with the full default config.

## Writing the config

- Rewrite the chat for the user's product: `app.name`, `message` (the bot's first line), `card.title` (the key recommendation/result, ≤ ~40 characters), `button` / `approvedLabel`, and `reply`.
- `card.tiles` are 3 mini stats (label + 0–1 bar value); make them match the story or set `[]` to hide them.
- Time it to speech: `cardAt` when the speaker introduces the result, `tapAt` on the action word ("@approve", "@download", "@post"). `"auto"` puts the tap on words like approve/click/tap/done, else ~65% in.
- For a real app, pass `screen` with a screenshot or vertical screen recording path; the chat UI is replaced and the phone frame stays.
- `side` defaults to the side with more room; use `size` 0.3 for tight close-ups, 0.38 for wide shots.

## Example

Line: "If you wanted to build your own course selling platform, all you have to do is download this GitHub repo."
```json
{
  "side": "left",
  "app": { "name": "Repo Scout", "status": "Watching GitHub", "avatarColor": "#8AB4FF" },
  "message": "Found an open-source course platform.",
  "card": {
    "label": "NEW REPO",
    "title": "Gumroad is now fully open source",
    "tiles": [
      { "label": "Stars", "value": 0.95, "color": "#8AB4FF" },
      { "label": "Forks", "value": 0.6, "color": "#8AB4FF" },
      { "label": "Issues", "value": 0.25, "color": "#E5706B" }
    ]
  },
  "button": "Download",
  "secondary": "Later",
  "approvedLabel": "Cloned",
  "reply": "Cloned to ~/course-platform",
  "cardAt": "@course-0.3",
  "tapAt": "@download"
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

- On tight close-ups the phone may touch the cheek; lower `size` to 0.3 or raise `nudge` to 0.12 (pans the footage further away).
- Keep `card.title` to two lines; longer text pushes the buttons down.
- A screen recording in `screen` should be vertical (9:16-ish); landscape media gets cropped to fill.
- Leave at least ~0.8s after `tapAt` so the approved state and reply are seen.
- The cut-out follows the person. Things in front of them (a mic, a hand passing over the mic) can partly stay or partly vanish for a few frames; pick a range where the hands are clear if it matters.
- If the render fails, read the error: "Video not found" means a bad path; "Matting model missing" or Python errors mean the install is incomplete (run doctor); a timeout usually means the machine is overloaded, so render again with fewer apps open.
