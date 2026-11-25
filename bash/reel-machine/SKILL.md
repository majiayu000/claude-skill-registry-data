---
name: reel-machine
description: "Turn raw phone clips into scheduled vertical reels with no editor in the loop: iCloud Photos clips, word-level transcription (free local faster-whisper, or ElevenLabs Scribe with a key), segment picking across one or more clips, a drift-free precut, hook text with a logo or flag on frame 0, bare stat cards, full-screen cutaways for named places and products, captions above the app UI, a handle closer or a product CTA, natural voice EQ, VAD jump cuts with a pace gate, a face check on the first and last frames, a lip-sync check, written sensitivity rules, a second-model caption review, then a finished 9:16 file to post by hand, or Instagram Reels (plus a Story reshare), TikTok and YouTube Shorts scheduled through Buffer when a Buffer token is set. Runs free with no API keys. Use when someone wants their selfie or talking clips turned into finished, posted shorts, or wants a daily reel cadence run by an agent."
---

# reel-machine

Raw clips in, finished reels out. Runs free: no API key is required at any step. You make the editorial calls (which moment, which words,
which hook); the scripts do the cutting, drawing, rendering, checking and scheduling. A reel
is one JSON spec, so every render is reproducible and a fix is a one-line change.

**Done means:** the render exists, `finish.sh` passed (voice EQ, jump cuts, pace gate, face check),
`avsync.py` passed, the sensitivity pass and the second-model caption review both cleared, the owner approved anything on the show-first list, and the reel is handed over: the 9:16 file plus
its caption to post by hand, or, with Buffer set up, the three posts exist in Buffer (drafts until the owner arms them).

## Setup (once per machine)

Needs `ffmpeg`, `ffprobe` and Python 3. Any machine with those renders; no GPU. The pace gate
and jump cuts use Silero VAD through `faster-whisper` (CPU, about 2 MB model, downloaded with the
package); the face check uses OpenCV 4 (`opencv-python-headless<5`: OpenCV 5 dropped the Haar
cascades from the main package).

```bash
bash scripts/setup.sh        # Python deps, Funnel Display hook font (SIL OFL), work dirs, config file
```
Then edit `~/.config/reel-machine/config.env` (template: `config.example.env`): your handle,
language. Both keys are optional upgrades, never a reason to stop:
- No `ELEVENLABS_API_KEY`: transcription runs locally with faster-whisper (free). Tell the user in one line.
- No `BUFFER_TOKEN`: step 7 hands over the finished file and caption to post by hand.
If the user has a key, it stays in the environment (never in chat, a command argument or the config file).

For iCloud Photos as the clip source, install the `icloud-photos-bridge` skill and run its
setup. `selfie-picker` and `broll-picker` find the moments worth cutting; this skill starts
once you have clip UUIDs.

## The pipeline

### 1. Get clips
```bash
$PY $B/catalog.py --out catalog.jsonl --since <date> --kind video   # icloud-photos-bridge
bash scripts/fetch_clips.sh <UUID> [<UUID> ...]                       # -> $REEL_WORK/clips/
```
Clips from anywhere else: drop the files in `$REEL_WORK/clips/`.

### 2. Transcribe
```bash
python3 scripts/transcribe.py $REEL_WORK/clips/<clip>.mov     # or --watch; local + free unless ELEVENLABS_API_KEY is set
python3 scripts/words.py <clip>                                # sentences with times
python3 scripts/words.py <clip> 12-30                          # every word with start-end
```

### 3. Pick the segment(s)
Read the whole transcript before choosing. Rules, in order:
- **Story gate:** would a stranger send this to a friend? Utility, surprise, identity,
  aspiration or a strong opinion. A diary line ("wrote some code today") fails.
- **Strongest line first.** The first spoken words are a claim, a number or a stakes question.
  No greeting, no "so today". Move the best line to the front if it stands alone.
- **Cut filler, false starts and repetitions** at word boundaries from `words.py`. Keep a pause
  only when it carries personality. Length follows the payoff (most land at 15 to 60 s).
- Then run step 6's text pre-screen on the kept words before you invest in a render.

### 4. Write the spec
One JSON per reel, format in `references/spec-format.md`. Single clip:
```json
{"name": "second-opinion", "clip": "<clip stem>",
 "segments": [[0.26, 4.74], [5.16, 9.08], [10.28, 11.4]],
 "hook": "I made Claude ask ChatGPT\nfor a second opinion",
 "inline": {"Claude": "sig/claude.png", "ChatGPT": "sig/openai.png"},
 "cards": [{"image": "sig/card_5m.png", "at": [7.6, 8.62], "w": 520, "y": 380}],
 "cap_fix": {"like, ": ""}}
```
Several clips in one reel (the transcripts are laid end to end, so captions, cards, cutaways and
the ending rule work across clips; every time is `[clip_index, start, end]`):
```json
{"name": "picks-38", "clips": ["IMG_0412", "IMG_0415"],
 "segments": [[0, 0.0, 5.6], [0, 6.58, 10.95], [1, 23.66, 27.6], [1, 29.12, 35.28]],
 "hook": "Your agent picks the right\nskill 38% of the time",
 "cuts": [{"image": "sig/landmark.jpg", "title": "Golden Gate Bridge", "at": [1, 29.12, 31.6],
           "credit": "Author, CC BY-SA 4.0 (Wikimedia Commons)"}],
 "cta": {"text": "yourproduct.com", "logo": "sig/product.png"}}
```
**Cutaways for named things.** Whenever the speaker names a place, product or thing a stranger
may not picture, cut to it full screen while it is named (1.5 to 3 s, hard cut in and out,
captions stay on top). Photos come from Wikimedia Commons with their credit:
```bash
python3 scripts/commons.py sig landmark="File:Golden Gate Bridge as seen from Battery East.jpg"
python3 scripts/cutaway.py sig/c_landmark.png sig/landmark.jpg "Golden Gate Bridge" "San Francisco"
```
A cut with `"title"` builds the card in `mkreel.py`; a cut without it uses the image as a ready
1080x1920 card (a product screenshot card, for example). `mkreel.py` writes the credits of a
reel to `credits.txt`; they go in the post caption (`schedule_reel.py --credits`).

**Product reels.** `"cta": {"text": "yourproduct.com", "logo": "..."}` replaces the handle closer
with the logo and the landing page at the end; `"corner_logo"` keeps a small logo in the corner.
Put the same landing link in the post caption (`schedule_reel.py --link`).

The look (hook, signal, cards, captions, closer) is in `references/look.md`. Build the pieces:
```bash
python3 scripts/logo_png.py claude "#D97757" sig/claude.png     # brand mark (Simple Icons)
python3 scripts/emoji_png.py 🇺🇸 sig/us.png                       # flag as the place signal
python3 scripts/statcard.py sig/card_5m.png '$5M' 'raised'       # bare stat card
```

### 5. Bundle, curate captions, render
```bash
python3 scripts/mkreel.py spec.json              # bundle + drafted captions printed with times
# edit $REEL_WORK/bundles/<name>/caps.json if needed, then:
python3 scripts/make_caps.py check $REEL_WORK/bundles/<name>/caps.json
bash $REEL_WORK/bundles/<name>/job.sh            # render here, or:
bash scripts/remote_render.sh $REEL_WORK/bundles/<name>    # on REEL_REMOTE over ssh
```
`mkreel.py spec.json --render` does bundle + local render in one go. The precut seeks each
segment as its own input and concatenates audio and video together, so long multi-cut reels do
not drift. The render: optional grade, wind high-pass, -14 LUFS, 1.1x, hook for the first
seconds, cards and cutaways at their spoken words, captions (55 px, block ending at y~1425 of
1920, above the strip Instagram and TikTok cover with their UI), closer on the last second,
H.264 high profile, faststart.

**Ending rule:** the last segment ends on the last whole word of a sentence; the voice fades out
0.12 s after it while the footage keeps playing under the closer for up to `tail_max` (1.15 s),
so the reel lands on a face, not on a cut mid-breath. A warning prints if the last word is not
a sentence end.

### 5b. Finish: voice, pace, face
```bash
bash scripts/finish.sh $REEL_WORK/bundles/<name>     # -> $REEL_WORK/renders/reel_<name>.mp4
```
Runs in this order and stops at the first failed gate:
1. `voiceclean.py`: the real voice with a gentle EQ (high-pass 90 Hz, -3 dB at 220 Hz, +2 dB at
   3.3 kHz) and loudness normalisation (I=-15, TP=-2, LRA=7). Both are config
   (`REEL_VOICE_EQ`, `REEL_LOUDNORM`): tune them to your voice and mic. No voice isolation: model
   isolation made voices sound robotic (a robotic-voice detector scored raw phone audio 0.002,
   isolated audio 0.27 to 1.0).
2. `pcut.py`: jump cuts on speech found by voice activity detection. Every inner silence shrinks
   to about 0.1 s with 10 ms fades, the lead-in drops under 0.15 s. If the reel still runs under
   2.6 words per second it is sped up 1.1x to 1.15x (pitch kept). `--headfreeze 0.12` holds a
   later frame over a blink on frame 0.
3. `vadgaps.py`: the pace gate. FAIL on any pause over 0.35 s or more than 8% dead air. Use
   voice activity, not transcript word times: transcribers stretch words over pauses and hide them.
4. `facecheck.py`: the first 0.5 s (thumbnail) and the last 2 s. FAIL on closed eyes, a soft face
   or half a face in shot. It is a heuristic: always look at the `_face.jpg` strip it writes. Fix
   a fail by moving the cut to another word, `--headfreeze`, or a shorter `tail_max`.

### 6. Check before anyone sees it
1. **Lip sync:** `python3 scripts/avsync.py <source clip> <render>`. Only rows with frame
   similarity >= 0.85 count; PASS means the offset does not grow across the reel. A FAIL is
   a render bug: fix it, never ship it.
2. **Sensitivity:** `python3 scripts/sensitivity_scan.py <transcript> <caps.json> --text "<hook>" --text "<post caption>" --posted <date>`,
   then apply `references/sensitivity-rules.md` yourself, including the frame pass. Every
   flag gets a decision: cut, keep with a reason, or show the owner.
3. **Second-model caption review:** `python3 scripts/caption_review.py $REEL_WORK/bundles/<name> --hook "..." --post "..."`.
   With `REEL_REVIEW_CMD` set it asks another model (Codex, Claude, any CLI that reads stdin);
   apply its fixes, re-render if captions changed, and loop in the same session until it answers AGREED.
4. **Look at it:** one frame per second (`references/sensitivity-rules.md`, frame pass) plus
   the first frame, which is the thumbnail.

### 7. Hand over or schedule
No Buffer token: `schedule` writes `<reel>.post.txt` (caption, title, time) next to the reel and
schedules nothing. Give the user the file and the caption to post by hand. With Buffer:
```bash
python3 scripts/schedule_reel.py channels
python3 scripts/schedule_reel.py schedule --file renders/reel_<name>.mp4 \
    --at 2026-11-02T12:00:00-08:00 --caption "..." --title "YouTube title"          # drafts
# product reel: --link https://yourproduct.com ; cutaway credits: --credits bundles/<name>/credits.txt
# Instagram Story reshare 1 h after the reel: --story
# after the owner approves the exact file + caption: same command with --armed
python3 scripts/schedule_reel.py swap --caption-start "first words" --file renders/reel_<name>_v2.mp4 --title "..."
```
Buffer fetches media from a public https URL at publish time (no upload API), so the file must
stay hosted with byte-range support until the post fires. Instagram needs
`metadata.instagram = {type: "reel", shouldShareToFeed: true}`; YouTube needs a title and a
`categoryId`; the script sets both. `--story` adds an Instagram Story with the same video
`REEL_STORY_DELAY_MIN` (60) minutes after the reel (`metadata.instagram.type = "story"`), a second
push to followers who watch Stories but skip the feed. `--armed` runs the pace gate on the exact
file first and refuses a reel with dead air. Never two similar topics back to back; mix street, people,
work and product.

## Rules

- Drafts by default. Arm a post only after the owner approved that exact file and caption.
- Anyone clearly identifiable on camera needs consent. The owner's standing-consent list is the
  only exception.
- Never invent words in captions. The transcript is ground truth; fix only recognition errors.
- A failed check is a stop, not a note. Fix, re-render, re-check. Never loosen a gate to ship.
- Keep media private until it is scheduled: host renders at an unlisted URL.

## Files

- `scripts/`: `setup.sh`, `fetch_clips.sh`, `transcribe.py`, `words.py`, `mkreel.py`,
  `precut.py`, `build_reel.py`, `make_caps.py`, `fit_hook.py`, `hook_png.py`, `statcard.py`,
  `closer_png.py`, `cta_png.py`, `cutaway.py`, `commons.py`, `logo_png.py`, `emoji_png.py`,
  `remote_render.sh`, `finish.sh`, `voiceclean.py`, `pcut.py`, `vadgaps.py`, `facecheck.py`,
  `avsync.py`, `sensitivity_scan.py`, `caption_review.py`, `schedule_reel.py`, `rmconf.py` (config loader).
- `references/spec-format.md`, `references/look.md`, `references/sensitivity-rules.md`.
- `config.example.env`. No EVALS.md ships yet, so no measured benefit over an agent without
  the skill is claimed.
