---
name: memorial-tribute
description: "Memorial and tribute video editor: arranges a life's photos and clips in a family-approved chronological arc (opening portrait, childhood, young adult, family, later years, closing portrait with dates), 4-7 s per photo with slow push-ins, gentle dissolves on musical phrases, a quiet licensed song, names and dates checked three times, and a glitch-free 16:9 master plus a loopable version for the venue. Use when the user says: memorial video, tribute video, funeral slideshow, celebration of life video, photo slideshow for my grandmother, remembrance video, anniversary or retirement tribute. Default skin paper-cut; any calm Video Studio skin works."
license: MIT
---

# Memorial Tribute

A life told with dignity: the right photos, in the right order, at a pace that lets people remember.

- **Best for:** funerals and celebrations of life, remembrance days, milestone tributes (retirement, anniversary)
- **Inputs:** photos (scanned / phone copies) in the family's order, optional short clips and voice recordings, one song the family chose (licensed for the use), names, dates, a closing line
- **Default skin:** `paper-cut` · alternatives `soft-gradient`, `minimal-mono`, `cinematic-phone`
- **Formats:** 16:9 1920x1080 master (venue screen / TV), a looping version for the reception, optional 9:16 for family sharing
- **Duration target:** 3-10 min (about 12-15 photos per song minute at 4-5 s each); genre preset `memorial-tribute`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre memorial-tribute`.
- **Ask the family** for: the exact spelling of every name, birth and death dates, the order (or approval of yours), any photo that must or must not appear, the song, and the venue's screen (16:9? sound system?). There is no second chance on the day: deliver early and test on the venue's player.
- Name photo files in the approved order (`001_baby.jpg`, `002_school.jpg`...).

## How a pro cuts this

| beat | % | what happens |
| --- | --- | --- |
| opening portrait + name | 0-8 | the best-loved portrait, name and dates |
| childhood | 8-28 | earliest photos, family of origin |
| young adult | 28-48 | school, work, friends, wedding |
| family | 48-73 | children, grandchildren, homes, celebrations |
| later years | 73-90 | recent joy, the face people remember |
| closing portrait + dates | 90-100 | a final portrait and a short line ("Forever in our hearts") |

- **Pacing:** 4-7 s per photo (longer for group photos: more faces need more time), ASL varies with the music; never uniform.
- **Cut rules:** change photos on musical phrases (every 2 or 4 bars), not on every beat. Group by era or event; keep siblings and partners near each other.
- **Motion:** slow push-in (Ken Burns) on photos; never so tight that heads are cut; static for small/low-resolution scans.
- **Transitions:** dissolves 0.8-1.2 s (the one place they belong); dip to black between eras if the music pauses. No flashy effects.
- **Music:** gentle, leads the piece; one or two songs; end on the song's real ending (fade only at a phrase end). Under a recorded voice or speech, duck it.
- **Colour:** keep photos natural; a soft unifying look (`dreamy` 0.4 or `vintage-70s` 0.3) only if the family likes it; black-and-white photos stay black-and-white.
- **Text:** names and dates only, plus era titles if wanted; large, high-contrast, on screen >= 3 s.
- **Client (family) judges:** dignity, accuracy, everyone included, no glitches.
- **Common mistakes:** a wrong name or date, someone left out, faces cropped by the 16:9 frame, rushed pace, an upbeat song cut mid-phrase, glitch effects, a file that doesn't play on the venue's laptop.

## Make the edit

1. Beat map of the song (cut points on phrases): `python CORE/scripts/beats.py song.mp3 --out mem/beats.json`.
2. Draft spec on the music, then hand-tune it:

```bash
python CORE/scripts/timeline.py auto photos/ --work mem --mode montage --music song.mp3 --duration 240 \
  --format 16:9 --transition fade --beats-per-shot 8 --dry-run
```

`--beats-per-shot 8` gives 4 s shots at 120 BPM (use `60 / bpm x N` to pick N for 4-6 s). Choose `--duration` = number of photos x shot length, or the montage will repeat photos to fill it. Then edit `mem/timeline_spec.json`: put clips in the family's order, each photo **once**, vary `dur` (4-7 s, on bar lengths), set `"transition": {"type": "fade", "dur": 1.0}`, add `"fit": "contain"` for portrait or group photos that `cover` would crop, add a `"fadeOut": 3` to the spec `music`, delete `beatGrid`. Clips with sound: `"audio": "keep"` and the music `"duck": true`.

3. Build and plan (no transcription: there is no speech):

```bash
python CORE/scripts/timeline.py build mem/timeline_spec.json --work mem --no-transcribe
python CORE/scripts/make_plan.py --work mem --style SKILLS/paper-cut --genre memorial-tribute --format 16:9 --beats mem/beats.json
python CORE/scripts/editor.py review mem/plan.json --genre memorial-tribute
python CORE/scripts/render.py mem/plan.json --frames 2,30,90,200          # LOOK: faces whole, text readable
python CORE/scripts/render.py mem/plan.json
python CORE/scripts/finish.py mem/plan.json --platform youtube
```

**Narrated tribute** (a eulogy or a family member's voice as the soundtrack): put the recording in the spec's `music`
with `"voiceover": true` (`"music": {"src": "../eulogy.wav", "volume": 1.0, "voiceover": true}`) and build without
`--no-transcribe`: `timeline.py` transcribes it, so `words.json` has word times for gentle captions. Fallback: transcribe
the recording on its own (`transcribe.py --work vo --audio eulogy.wav`) and copy its words into the plan.

Pass `--format 16:9` to make_plan: otherwise the skin's own format (9:16 for paper-cut) is used even though the timeline is 16:9. Ignore review's "cut scores / mid-thought" lines (there are no words to cut by) and the "uniform shot lengths" note only if you deliberately kept a steady rhythm.

## Refine the plan

- **Replace the skin's placeholder elements** (e.g. a "Your title here" text) with: `{"type": "titlecard", "kicker": "In loving memory", "title": "Asha Verma", "subtitle": "1941 - 2026", "start": 0, "end": 4.5, "in": "fade", "out": "fade", "inDur": 0.8, "outDur": 0.8}`.
- **Era titles (optional):** a quiet `text` "The early years" 3 s at each era start, `in: fade`.
- **Closing:** `{"type": "text", "text": "Forever in our hearts", "start": END-4, "end": END, "y": 960, "in": "fade", "inDur": 1.0, "style": {"textShadow": "0 2px 12px rgba(0,0,0,.8)"}}` - keep readable over bright photos.
- **No captions, no SFX, no flashes.** Remove any the skin added.
- **Audio:** `"audio": {"voice": false}` (music only; no dialogue processing). With a recorded eulogy clip, keep the voice chain on and duck the music.
- **Look:** `"color": {"look": "dreamy", "intensity": 0.4}` or `"color": {"auto": true}` only; `"finish": {"grain": 3, "vignette": 0.3}`.
- **Faces:** the automatic push-in aims at the centre. If a face sits near an edge, set that clip to `"kenburns": false` or `"fit": "contain"` in the spec and rebuild.

## Deliver

```bash
python CORE/scripts/deliver.py mem/plan.json --to youtube --burn no --no-post --out-dir mem/deliver
python CORE/scripts/qc.py mem/deliver/final_youtube.mp4 --plan mem/plan.json --platform youtube
```

- **Loop for the reception:** `ffmpeg -stream_loop 9 -i mem/final.mp4 -c copy mem/deliver/loop_x10.mp4` (or set the venue player to repeat).
- Give the venue two copies (USB + link) and a backup on a second device; test on their player before the day.
- 9:16 for family sharing: `deliver.py ... --to whatsapp-status` makes a small file (blurred-fill vertical).

## Check before delivering

- Every name and date checked three times against the family's written list.
- Everyone the family named appears; nobody they excluded does; order approved in writing.
- No cropped heads, no upside-down or low-res stretched scans; black-and-white photos untouched.
- Song ends on its real ending; no glitches; `qc.py` passes (no black gaps, no flashes).
- Watch the whole video once before sending. Tell the family: length, song, order summary, files, and how to play it.

## Example requests

- "Make a memorial slideshow for my grandmother with these 60 photos and this song, about 5 minutes."
- "Celebration of life video: childhood to now, her name and dates at the start, gentle dissolves."
- "A tribute video for my dad's retirement from these photos and two short clips."
