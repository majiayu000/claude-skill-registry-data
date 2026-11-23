---
name: asmr-video
description: "ASMR video editor for Claude: turns long trigger recordings (tapping, whispering, brushing, crinkles, roleplay, cooking sounds) into a calm, long-take ASMR video with untouched trigger audio, slow dissolves, no music and a quiet master, plus short vertical teasers. Use when the user says 'edit my ASMR video', 'make an ASMR cut', 'keep the tingles', 'no music, no cuts', 'sleep video', 'ASMR shorts from this', or hands over a whisper or trigger recording. Runs on video-studio-core (timeline, colour, finish, deliver, QC). Not for talking-head content that needs tight jump cuts (use halo-cut or retention editing)."
license: MIT
---

# ASMR Video

Long, slow, quiet: the sound is the product and the edit's job is to stay out of the way.

- **Best for:** trigger videos (tapping, scratching, brushing, crinkles), whisper roleplay, soft-spoken tutorials, sleep videos, cooking and nature ASMR
- **Inputs:** one or more long takes with a good stereo or binaural mic track; optional close-up inserts
- **Default skin:** `loop-ambient` · alternatives `minimal-mono`, `soft-gradient`, `cinematic-phone`
- **Formats:** 16:9 master, 9:16 teasers (30-60 s)
- **Durations:** 10-60 min full video, teasers 30-60 s
- **Genre preset:** `--genre asmr-video` (see `python CORE/scripts/editor.py genre asmr-video`)

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- Ask: which triggers are the stars, anything to remove (a phone buzz, a cough, a dog), is the mic binaural (keep L/R
  exactly as recorded), and the target length.
- Keep the original files. Never re-record or "clean" the master audio in place.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| settle in | 10 | soft greeting or first gentle trigger, establishing frame, no surprises |
| triggers | 80 | trigger blocks of 2-8 min each, one trigger family per block, slow transitions between |
| wind down | 10 | slowest, quietest trigger, fade to black, no outro jingle or loud end screen |

**Pacing.** ASL 15-60 s. A cut is an event that can break relaxation, so cut only to change trigger, remove a
mistake, or move to a better angle. Never a pattern interrupt, never a zoom punch.

**Cut rules.**
- No autocut. Pauses are part of the experience: always run with `--no-cut`.
- Remove mistakes with explicit ranges (`--cut "312-318.5"`) or by leaving them out of the timeline spec.
- Join takes on silence or on the start of a trigger, never mid-sound. Crossfade audio 40-60 ms minimum.
- Keep binaural L/R as recorded: no mono fold, no panning, no stereo widening.

**Transition grammar.** Slow dissolves (1-2 s) between trigger blocks; one dip to black at the end. Nothing else.

**Music and sound.** No music, no SFX. The dialogue chain is the enemy here: noise reduction smears soft triggers and
compression lifts breaths into hiss. Turn denoise off (or the whole chain), keep a gentle high-pass at most.
Loudness: a quiet master around -20 LUFS / -3 dBTP (the genre preset). Do not brick-wall limit.

**Colour.** Soft and low-contrast: `faded` (preset) or `high-key` at low intensity for bright sets, `moody` for dark
sleep videos. Intensity 0.3-0.5. No grain (it reads as noise), no flicker, no light leaks.

**Captions.** None in the video. A small title card in the first seconds is optional. Upload `captions.srt` only for
whispered speech that matters (roleplay lines).

**What the client judges.** Audio fidelity (no hiss, no pumping, no clicks), calm pace, and that nothing jolts.

**Common mistakes.** Running autocut; denoising the triggers; loud intro sting; music under triggers; sudden
volume jumps between takes; normalising the whole video to -14 LUFS so whispers come out shouty.

## Make the edit

Single take:

```bash
python CORE/scripts/run.py session.mp4 --style SKILLS/loop-ambient --genre asmr-video --format 16:9 --no-cut --cut "312-318.5" --model base --work asmr --stop-after plan
python CORE/scripts/render.py asmr/plan.json --frames 5,120,600,1200
python CORE/scripts/render.py asmr/plan.json
python CORE/scripts/finish.py asmr/plan.json --lufs -20
```

Note: `--cut` ranges are source seconds; `--no-cut` keeps every pause but still removes your `--cut` ranges.

Several takes joined with slow dissolves: write `asmr/spec.json` by hand:

```json
{"format": "16:9", "fps": 30,
 "clips": [
   {"src": "tapping.mp4", "in": 4, "out": 410},
   {"src": "brushing.mp4", "in": 2, "out": 520, "transition": {"type": "dissolve", "dur": 1.5}},
   {"src": "whisper.mp4", "in": 0, "out": 380, "transition": {"type": "dissolve", "dur": 2.0}}
 ]}
```

```bash
python CORE/scripts/run.py - --timeline asmr/spec.json --style SKILLS/loop-ambient --genre asmr-video --format 16:9 --no-cut --model base --work asmr --stop-after plan
```

Teaser (9:16, 45 s): run the same with `--format 9:16`, a spec of the single best trigger block cut to 45 s,
`--work asmr-teaser`.

## Refine the plan

Edit `asmr/plan.json`:

- **Audio chain:** `"audio": {"platform": "youtube", "lufs": -20, "tp": -3, "voice": {"denoise": false, "deess": false, "compress": false, "hpf": 40}}`.
  For a fully untouched mix use `"voice": false` (no chain at all). A/B it: `python CORE/scripts/audio_chain.py voice in.wav out.wav --cfg '{"denoise": false, "compress": false}'`.
- **No room-tone fill** needed (nothing was autocut): leave `roomTone` unset.
- **No music, no sfx:** make sure `"music"` is absent or null and `"sfx": []`.
- **Remove creator captions:** delete the skin's `captions` element and any hook/headline elements.
- **Colour:** `"color": {"look": "faded", "intensity": 0.4}`; `"finish": {"grain": 0, "vignette": 0.2, "sharpen": false}`.
- **Optional title:** `{"type": "text", "text": "Slow tapping for sleep", "start": 1, "end": 6, "in": "blurIn", "out": "fade", "y": 900}`.
- Check `python CORE/scripts/editor.py review asmr/plan.json --genre asmr-video` but ignore pacing notes that ask for
  more interrupts; this genre is deliberately slow.

## Deliver

`deliver.py` re-normalises every web preset (youtube, web-h265, web-av1, reels...) to its own target, usually
-14 LUFS. For a quiet ASMR master use the finished `final.mp4` (already at -20 from `finish.py --lufs -20`) as the
upload file, and deliver the mezzanine untouched:

```bash
python CORE/scripts/deliver.py asmr/plan.json --to prores-422hq,audio-wav --out-dir asmr/deliver --burn no --no-post
python CORE/scripts/deliver.py asmr-teaser/plan.json --to shorts,reels,tiktok --out-dir asmr-teaser/deliver --burn no
python CORE/scripts/qc.py asmr/final.mp4 --plan asmr/plan.json --platform none
python CORE/scripts/qc.py asmr-teaser/deliver/final_shorts.mp4 --plan asmr-teaser/plan.json --platform shorts
```

If the user wants a -14 YouTube upload anyway, `--to youtube` does it; say that whispers will be louder.
Expect `qc.py` WARNs for long silences: in ASMR those are intended (say so in the report).

## Check before delivering

- Listen with headphones to the start, every join and the end: no clicks, no level jumps, L/R not swapped.
- Measure: `python CORE/scripts/audio_chain.py measure asmr/final.mp4` shows about -20 LUFS and TP at or under -3.
- Contact sheet: soft, even exposure; no text left from the skin; nothing flashes (`qc.py` flash check passes).
- Tell the user which ranges were removed, that no noise reduction was applied, and which file to upload.

## Example requests

- "Edit my 40-minute tapping session, don't cut the pauses, just remove the bit where my phone rang at 5:12."
- "Join these three trigger recordings with slow fades, no music, keep it quiet."
- "Make a 45-second vertical teaser of the best brushing part."
