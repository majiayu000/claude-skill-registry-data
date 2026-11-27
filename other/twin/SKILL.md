---
name: twin
description: "Use when a video needs yskills to say lines he did not record: his voice clone and his real face with only the mouth re-synced. Recording ask, laptop tool, Critic lines."
---

# Twin

yskills, 2026-10-12: train on his face and voice, build our own HeyGen. 2026-10-26: "it
should never look ai, my videos always high quality and not slop", and free only (no paid or rented tools). The twin is his **real** face
clip with only the mouth re-synced, plus his cloned voice. Nothing about him is generated from
scratch: that is what keeps it from looking AI.

## Hard rule

- A twin shot ships only after the Critic passed it (below). A twin shot that fails is never
  patched into the video: the video uses real footage instead (his own clip, voice-over on real
  footage, or an ask for a 10 s selfie take through the coordinator). [advisory]
- No generated faces, bodies, places or b-roll around it ([`social-team/xyskillsx-style.md`](../social-team/xyskillsx-style.md), Never).
- Twin face on screen in short bursts (one sentence, about 8 s at most), cut with real footage;
  voice-only over real footage is the safer first use.
- Labels and provenance: `social-team` SKILL.md, Posting (AI label). Chatterbox writes an inaudible
  PerTh watermark into every file; never strip it or any provenance data. [advisory]
- His raw recordings and `twin/` stay on the laptop, never in a repo, chat upload or cloud bucket. [advisory]

## What fits his account

His hits are his real face plus one ironic caption, 7-9 s ([`xyskillsx-style.md`](../social-team/xyskillsx-style.md)).
The twin does not replace that. It fills: voice-over for devlog and learning clips, a fixed or
added line in a clip he filmed, a short talking hook when he has no time to film. A meme or a
reaction stays real.

## Recording (once)

The exact ask, the drop folder and the reading script: [`record.md`](record.md). Files land in
`lib/footage/<date>-twin/source/` (under `STUDIO_ROOT`).

## The tool (laptop, RTX 4060 8 GB)

`scripts/twin.py`, stdlib only; the models run in their own venvs, one process after the other, so
8 GB RAM is enough. Setup: [`laptop-setup.md`](laptop-setup.md).

| Step | Command | Writes |
|---|---|---|
| 1 Check the raw files | `python twin.py check lib/footage/<date>-twin/source` | `CHECK OK` or one `PROBLEM` line each (sample rate, length, clipping, noise, vertical, resolution) |
| 2 Prepare, once | `python twin.py prep lib/footage/<date>-twin/source twin` | `twin/voice/*-ref.wav` (a clean ~12 s clip per mood), `twin/face/<mood>.mp4` (25 fps), `twin/twin.json` |
| 3 Say a script | `python twin.py say twin --text-file line.txt --mood talk --out out/<slug>` | `voice.wav`, `words.json`, `face.mp4`, `critic/`, `report.json` |
| Tools present | `python twin.py doctor` | ok or MISS per tool and the GPU line |

- Moods: `talk` (free-talk voice, talking clip), `calm`, `hyped`, `think`. `--voice-only` skips the face.
- `--engine musetalk` (default, MuseTalk 1.5) or `latentsync` (LatentSync 1.5 on 8 GB; 1.6
  needs ~18 GB and is not used).
- Voice: Chatterbox reads each sentence, faster-whisper listens back, a sentence with more than 8 %
  wrong words is made again (twice), then the run fails. No wrong word ships.
- A face shot over 8 s, or longer than the mood's face clip, stops with "real footage" (the hard rule); split the script or use `--voice-only`.
- Longer than ~10 minutes: run it through `scripts/laptop-job.mjs` (`docs/pc-claude-user.md`, Long laptop jobs).

Callers: `video-studio`'s Editor (a twin shot in a cut), the `social` app's daily lane through the
daily routine (a script from the feed, `say` on the laptop over Remote Control, the cut goes back
as a draft). The cloud has no GPU, so every call runs on the laptop.

Language: the word check in `voice.py` runs faster-whisper `small.en`, so it fits English scripts only; a German script needs another model first (`doctor` does not catch this).

## Critic (fresh agent, every twin shot)

The `video-studio` Critic ([`roles/critic.md`](../video-studio/roles/critic.md)) adds these lines; any fail means real footage:

| Line | Pass looks like | Evidence |
|---|---|---|
| Mouth | as sharp as the cheeks in the same frame; teeth separate, no smear, no seam at jaw or chin, no flicker at the mask edge | `critic/side-*.png` (base left, twin right) |
| Sync | lips fully closed on every b, p, m | `critic/closure-*.png` |
| Voice | every word right (`report.json` WER 0 on names), his pace, breaths between sentences, no flat robot read | `words.json`, transcript |
| Face | blinks and head moves are his (they come from the real clip), no frozen face, no loop jump | side frames |
| Length | twin face on screen 8 s at most per shot, cut with real footage | `report.json` seconds |
| Friend test | his friends would not notice; when in doubt, fail | all of the above |

Voice by ear is yskills' call in his first test (the plan's T3): "would a friend notice?" yes or no.

## Quality ceiling (2026-10-26)

8 GB VRAM caps lip-sync at 256 px mouth crops (MuseTalk 1.5, LatentSync 1.5); a face that fills the
frame can look soft at 1080p. yskills chose free only (2026-10-26): the answer to a soft mouth is a
smaller twin shot (a cut-in, the face not filling the frame), voice-only over real footage, or real
footage, never a paid or rented tool. Full avatars that generate the whole face (HeyGen,
InfiniteTalk) read more AI and are not used.
