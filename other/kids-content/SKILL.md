---
name: kids-content
description: "Children's video editor for Claude: turns kids' songs, stories, simple lessons and family-channel footage into bright, simply cut 2-10 min videos and short clips with big sing-along captions at slow reading speed, repetition, friendly sound effects and safe, age-appropriate graphics. Use when the user says 'edit a kids video', 'nursery rhyme video', 'educational video for children', 'toddler learning video', 'sing-along captions', 'family channel video', or 'made for kids'. Handles COPPA 'made for kids' and consent duties. Runs on video-studio-core (transcribe, captions, motion graphics, deliver with --kids, QC)."
license: MIT
---

# Kids Content

Simple, bright, repeated and safe: a child can follow it and a parent can trust it.

- **Best for:** nursery rhymes, sing-alongs, alphabet/number lessons, storytime, family-friendly science, toy-free play ideas
- **Inputs:** host or song recording, simple B-roll or drawings, the lyrics or script, images for flash-card moments
- **Default skin:** `sticker-pop` · alternatives `comic-panel`, `paper-cut`, `bold-bounce`
- **Formats:** 16:9 episode, 9:16 short clips
- **Durations:** 2-10 min episodes, 30-60 s clips
- **Genre preset:** `--genre kids-content`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- **Consent:** any child on camera needs a parent's or guardian's written consent; no full names, school, or location
  of a child on screen or in the post text.
- **COPPA / YouTube:** content aimed at children must be set "made for kids" at upload (the uploader does this; the
  engine can't). That turns off comments and personalised ads; tell the user.
- **No dark patterns:** no "subscribe or...", no fake prizes, no pressure to buy, no scary surprises, no product
  placement aimed at children without disclosure. Check flashing (`qc.py` photosensitivity) carefully.

## How a pro cuts this

**Structure (% of episode)**

| beat | % | what goes here |
| --- | --- | --- |
| hello song / hook | 8 | the same friendly opening every episode, the topic in one picture |
| lesson / story | 70 | one idea at a time, each shown, said and written |
| repeat / sing-along | 15 | repeat the key words or chorus with the captions filling as they are sung |
| goodbye | 7 | the same goodbye each episode, calm ending |

**Pacing.** ASL 2-4 s; visual change every 3 s but never frantic. Repetition is a feature: show a new word, say it,
show it again. Hold flash-card images >= 2 s.

**Cut rules.**
- Simple straight cuts; keep the host's face visible when they talk to the child.
- Remove fillers and long pauses but keep a beat after a question so the child can answer.
- Every word on screen is spelled right and matches what is said.

**Transition grammar.** Cuts and a soft `pop`/`zoomIn` on graphics; one playful transition kind (wipe or iris).
No glitch, flash bursts or fast strobing.

**Music and sound.** Gentle bed ~-24 dB under speech; songs lead. SFX high but soft (~15/min): `pop`, `boing`,
`sparkle`, `ding` on correct answers; gains 0.3-0.4; nothing scary or loud.

**Colour.** Bright and soft: `pastel` or `high-key` at 0.5-0.7; never neon or harsh contrast.

**Captions.** Big sing-along words, 1-4 at a time, uppercase or clear sentence case, <= 12-13 cps for young readers
(`"cpsMax": 12`); `"mode": "fill"` or the `lyric` element for songs.

**What the client judges.** Safety, age-appropriateness, kids keep watching.

**Common mistakes.** Captions too fast; tiny text; flashing; loud SFX; inconsistent intro; a child's personal
details on screen; manipulative CTAs; spelling mistakes in a learning video.

## Make the edit

```bash
python CORE/scripts/run.py episode.mp4 --style SKILLS/sticker-pop --genre kids-content --format 16:9 --smart-cuts --retakes --title "Count to 10!" --work kc --stop-after plan
python CORE/scripts/render.py kc/plan.json --frames 2,20,60,120,180
python CORE/scripts/render.py kc/plan.json
python CORE/scripts/finish.py kc/plan.json --platform youtube
```

Song with lyrics: transcribe the vocal, then replace `words` with the correct lyrics (keep the times), or use
`lyric` lines with your own start/end. With a music track behind the vocal, separate it first if the licence allows:
`python CORE/scripts/stems.py song.wav --out kc/stems` (needs `pip install demucs`) and transcribe `vocals.wav`
with `python CORE/scripts/transcribe.py --work kc --audio kc/stems/vocals.wav --model base`.
Short clip: same source, `--format 9:16 --duration 45` in a new work folder.

## Refine the plan

- **Captions:** `{"type": "captions", "maxWords": 4, "uppercase": true, "cpsMax": 12, "mode": "fill", "y": 860}`; key
  learning words in `keywords`.
- **Sing-along:** `{"type": "lyric", "lines": [{"text": "one, two, buckle my shoe", "start": 31.6, "end": 34.0}]}`.
- **Flash cards:** `{"type": "image", "image": "apple.png", "start": 12, "end": 15, "in": "springPop", "w": 520}` with a
  `text` word under it; `{"type": "sticker", "text": "A", "in": "bounce"}`.
- **Counting:** `{"type": "counter", "from": 0, "to": 10, "countDur": 8, "start": 40, "end": 49}` matched to the host's
  counting (check make_plan's auto counters for junk labels).
- **Celebration:** `{"type": "shape", "kind": "confetti", "start": 50, "end": 52}` or `burst` with friendly emoji.
- **SFX:** `"sfx": [{"t": 12.0, "kind": "pop", "gain": 0.3}, {"t": 49.2, "kind": "success-chime", "gain": 0.35}]`.
- **Audio:** `"music": {"src": "bed.wav", "under": 22, "duck": "speech-aware"}`; voice `{"eq": "clear", "deess": true}`.
- **Colour:** `"color": {"look": "pastel", "intensity": 0.6}`.
- Remove any `chip` "Subscribe" the skin adds if it pressures children; a plain end card is enough.
- `python CORE/scripts/editor.py review kc/plan.json --genre kids-content`.
- **Other children:** a child without consent in the frame gets a blur or the shot goes: `"blurs": [{"x": 1500, "y": 380, "w": 220, "h": 260, "start": 40.0, "end": 44.0}]` (output pixels, top-left box). Also blur school logos and name tags.

## Deliver

```bash
python CORE/scripts/deliver.py kc/plan.json --to youtube --out-dir kc/deliver --kids --burn no
python CORE/scripts/deliver.py kc45/plan.json --to shorts,reels --out-dir kc45/deliver --kids
python CORE/scripts/qc.py kc/deliver/final_youtube.mp4 --plan kc/plan.json --platform youtube --kids --strict
```

`--kids` sets sidecar subtitles to 17 cps (the broadcast children's limit); the on-screen sing-along captions use
your `cpsMax` (12). Remind the user to tick "made for kids" when uploading.

## Check before delivering

- Every word on screen spelled right and matching the audio; captions slow enough to read along.
- `qc.py --kids` passes photosensitivity and loudness; no sudden loud sounds.
- No child's personal details; consent on file; no manipulative CTA; disclosures present.
- Same hello/goodbye and look as the channel's other episodes.

## Example requests

- "Edit this counting song for toddlers with big sing-along words."
- "Make a 5-minute alphabet video with picture cards for each letter."
- "Cut a 45-second short from the episode, kid-safe and captioned."
