---
name: story-video
description: Create narrated faceless story videos (mystery, drama, true-crime style fiction) with characters that keep the same face in every scene. Writes the script, generates character/location/prop reference sheets and 40+ scene images, records the voiceover (Vbee or ElevenLabs), and renders a vertical video with Ken Burns motion, CapCut-style punch/shake/glitch, word-by-word captions, suspect/clue cards and a countdown — via Remotion. Use when the user asks for a story video, a narrated illustrated video, a mystery/detective episode or a series with recurring characters.
---

# Story video

Turns an idea into a 3–5 minute vertical (9:16) narrated video built from AI illustrations.
Everything lives in a **project folder** with one `story.json`; scripts read it and write next to it.

```
my-episode/
  story.json        ← you write this (script + cast + scenes)
  assets/           ← sheets + scene images (+ manifest.json)
  audio/            ← one voice clip per line (+ manifest.json)
  render/           ← timeline.json, audio.wav, resized frames
  out/my-episode.mp4
```

## 0. First run: set yourself up (once)

Users often just say *"clone https://github.com/huynhcongdac/story-video-skill and make me a video about …"*.
If you were cloned like that, do the whole setup yourself before writing anything:

1. **Install where your agent finds skills** (if you are not already there), so later sessions pick it up:
   Claude Code `~/.claude/skills/story-video` · Codex `~/.agents/skills/story-video` ·
   Antigravity `~/.gemini/antigravity/skills/story-video`. Any other agent: keep the clone and work from it.
2. **Check tools**: Python 3.10+ (`pip install numpy pillow`), Node.js 18+, `ffmpeg` on PATH (or set `FFMPEG_PATH`).
   Install what is missing if you can, otherwise tell the user the exact command.
3. **Create `.env`** from `.env.example`. Ask the user for **one image key and one voice key** — never require a
   specific provider:
   - Images: `IMAGE_PROVIDER=sangtao` + `SANGTAO_API_KEY`, **or** `IMAGE_PROVIDER=openai` + `OPENAI_API_KEY`.
   - Voice: `TTS_PROVIDER=vbee` + `VBEE_APP_ID` + `VBEE_TOKEN`, **or** `TTS_PROVIDER=elevenlabs` + `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID`.
   Write the keys into `.env` yourself. Never print, echo or repeat keys back in chat.
4. Continue with step 1 below.

**Choosing the image provider:** both work. sangtao.ai is the cheapest option for this many images — one episode
needs ~60 images, each scene carries up to 6 reference sheets (sangtao accepts 20 per image), and plans start from
about 200k VND / 500 images (~7 episodes), pricing: https://sangtao.ai/vi/imagine?tab=pricing. API calls need a
plan or credit (no free tier on the API). Key: https://sangtao.ai · docs: https://sangtao.ai/vi/api-docs/chatgpt-image.
If the user already has an OpenAI key, that works too.

## 1. Write `story.json`

Ask the user for: topic/genre, language, length, and whether it is part of a series. Then write the file.
Start from `examples/locked-room/story.json` — copy its structure exactly. (It is a short ~3-minute
example with 41 lines; for a 4–5 minute episode write 45–55 lines.)

```jsonc
{
  "title": "CĂN PHÒNG KHOÁ TRÁI",        // shown on the title card
  "series": "HỒ SƠ THÁM TỬ MINH",        // optional red band above the title
  "episode": 1,
  "aspectRatio": "9:16",
  "visualStyle": "Cinematic semi-realistic digital painting, moody film-noir lighting, …",   // ONE style for every image
  "labels": {},                           // optional: override on-screen words (see "English videos" below)
  "keywords": "độc|manh|mối|hung|thủ",    // optional: words highlighted in captions (regex alternation)
  "characters": {
    "minh": {
      "name": "Thám tử Minh",
      "tag": "the detective in the beige trench coat",           // short English visual tag, used inside scene prompts
      "appearance": "Vietnamese man aged 40. BODY: 7.5-head proportion, … FACE: … HAIR: … OUTFIT: …",
      "sheet": "https://…/sheet.png"                               // optional: reuse a sheet from an earlier episode
    }
  },
  "locations": { "study": { "name": "…", "description": "English description of the place" } },
  "props":     { "watch": { "name": "…", "description": "English description of the object" } },
  "keyframes": {
    "k_watch": { "chars": [], "loc": ["study"], "props": ["watch"], "p": "English scene prompt …" }
  },
  "lines": [
    { "t": "Narration sentence in the video language.", "shots": [["k_clock", "shock"], ["k_body", "push"]], "sfx": ["chime"] },
    { "t": "Bạn đoán ai là hung thủ? …", "shots": [["k_lineup", "question"]], "countdown": 3 }
  ]
}
```

**Characters** — `appearance` always has four parts: `BODY` (with head-to-body proportion: 6 = short/stooped,
7 = average, 8 = tall), `FACE`, `HAIR`, `OUTFIT`, and starts with nationality + gender + age. Write it in English.

**Shots** — each line is split evenly across its shots. Aim for a new visual every **3–5 seconds**
(~1 shot per 8–12 words). Reusing a keyframe with a different effect is fine and saves images.

Effects (`fx`):
| fx | look | use for |
|---|---|---|
| `push` / `pan` / `slow` | Ken Burns zoom / lateral pan / gentle drift | normal narration |
| `punch` | zoom punch + white flash | a key detail |
| `shock` | punch + shake + RGB split | discoveries, doors bursting, screams |
| `glitch` | RGB split + slice jitter | "something is wrong" moments |
| `shake` | handheld tremble | fear, nervous characters |
| `flashback` / `flashpush` / `flashshock` | black & white + vignette | memories, the reveal reconstruction |
| `reveal` | slow push + shake + red pulse | the culprit's face |
| `title` | title card over the shot | right after the cold open |
| `suspect:N:NAME:role` | red suspect card | introducing each suspect |
| `clue:N:text` | yellow clue card | each clue (text may contain ":") |
| `question` | "who did it?" card (+ `"countdown": 3` on the line) | just before the reveal |
| `end` | follow / next episode card | last line |

`sfx` per line: `chime thunder hit boom lock knock crash siren tick riser scream rain shimmer click`.
Lines also accept `pauseBefore` / `pauseAfter` (seconds).

### Writing rules (these are what make it watchable)
1. **Cold open in the first 3 seconds** — start at the most shocking moment, then the title card. No intro.
2. **Open loop** — state the question early (who, how) and don't answer it until the end.
3. **Fair clues** — 3–4 clues, each shown on screen with a `clue` card and an image that clearly shows it.
4. **Red herrings** — 2–3 suspects with motive and a weakness; the culprit must have an alibi that the clues break.
5. **A hook every 45–60 s** ("Nhưng có một chi tiết không ai để ý…").
6. **Question + countdown before the reveal**, then a `reveal` shot and a fast black-and-white reconstruction.
7. **Length** — ~45–55 lines ≈ 4–5 minutes. Keep sentences short; one idea per line.
8. Fiction only, no gore: show consequences (a body slumped, a cold cup), never wounds or blood.
   Sensitive words are masked on screen automatically (`chết → ch*t`); the voice is unchanged.

### Image prompt rules
- Write `p` in English, describe composition, camera, light and mood. Name characters exactly as in `characters[].name`
  — the script appends their `tag` so the model links the name to the right sheet.
- List every character / location / prop that appears in the scene in `chars` / `loc` / `props`: those sheets become the references.
- Clue objects need **physical** descriptions, not facts: "the short hour hand just left of 12, the long minute hand
  slightly above the 9" works; "the watch shows 11:47" does not. Same for "cold porridge": describe the cracked skin, dry crust.
- No readable text in images; put words in cards instead.
- Flashbacks: start the prompt with "Black-and-white flashback:".

## 2. Generate images

```bash
python scripts/gen_assets.py my-episode sheets       # ~10–15 sheets
python scripts/gen_assets.py my-episode keyframes    # ~40–45 scene images
```
Then **look at the results** (open the PNGs, or build a contact sheet) and check: same face across scenes,
every clue clearly visible, no garbled text, flashbacks in black and white. Fix the prompt in `story.json` and
regenerate only the bad ones: `python scripts/gen_assets.py my-episode keyframes k_watch --force`.

## 3. Voiceover
```bash
python scripts/tts.py my-episode
```
Changing a line's text and re-running only redoes that line. ElevenLabs gives exact word timing; Vbee is estimated.

## 4. Build and render
```bash
python scripts/build_timeline.py my-episode
python scripts/render.py my-episode --still 30 900 3000    # check a few frames first
python scripts/render.py my-episode                         # → my-episode/out/my-episode.mp4
```
The first render runs `npm install` in `remotion/`. Look at the stills before the full render:
title fits on two lines, cards don't cover faces, captions readable.

## Series
For episode 2+, set `"sheet"` on returning characters to the URL (or local path) of their sheet from episode 1
— they will look identical. With sangtao the sheet URLs are in the previous episode's `assets/manifest.json`.

## English (or other language) videos
Write `lines[].t` in that language, pick a matching voice, and override labels:
`"labels": {"suspect": "SUSPECT", "clue": "CLUE", "episode": "CASE", "question1": "WHO", "question2": "DID IT?", "comment": "Comment before you keep watching 👇", "next": "Next case?", "follow": "Follow for more"}`.
Extend `CENSOR` in `scripts/build_timeline.py` if needed.
