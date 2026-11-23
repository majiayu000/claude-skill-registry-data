---
name: concert-multicam
description: "Concert and live-music multicam editor for Claude: lines up 2-4 camera angles of a gig, switches angles to follow the music, lays the board mix (or the best camera audio) under the picture, and delivers the full show, per-song files and vertical clips. Use when the user says 'edit my concert footage', 'multicam the gig', 'cut our live set', 'band live session video', 'recital video from two cameras', 'festival set', 'make clips from the show', or hands over several camera files from one performance. Runs on video-studio-core (multicam, timeline, beats, colour, deliver, QC)."
license: MIT
---

# Concert Multicam

A live show cut so the picture follows the music: the singer on the line, the guitarist on the solo, the crowd on
the drop, and the band's mix underneath.

- **Best for:** band gigs, live sessions, recitals, classical and devotional concerts, DJ sets, school shows
- **Inputs:** 2-4 camera files of the same performance (each with its own audio), optional board-mix WAV, set list
- **Default skin:** `event-promo` · alternatives `minimal-mono`, `neon-orbit` (add `--no-matte`), `vhs-tape`
- **Formats:** 16:9 full show and per-song files, 9:16 clips
- **Durations:** song = song length; full show as played (trim tuning and long talk); clips 15-60 s
- **Genre preset:** `--genre concert-multicam` (`python CORE/scripts/editor.py genre concert-multicam`)

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- Ask for: band / artist names and spelling, the set list with song titles, which camera is which (wide, stage-left,
  close), whether a board mix exists, and rights: posting a cover song or a venue recording may need permission.
- Never write into the camera folders; copy first.

## How a pro cuts this

**Structure (% of the show)**

| beat | % | what goes here |
| --- | --- | --- |
| walk-on / crowd | 5 | crowd noise, lights, the band walking on, first chord |
| songs | 88 | each song: wide to establish, then follow the music |
| encore / bow | 7 | applause, the bow, crowd wide, title + date |

**Angle grammar.** Wide at the start of each song and every 30-60 s as a reset; the lead vocal on verses; the soloist on
the solo (this is what the client judges); the drummer on fills and the build; the crowd on the drop or a sing-along.
Change angle on downbeats and phrase changes, not mid-word of a lyric. ASL 2-6 s: shorter on fast songs, 6-10 s holds on
ballads. Never cut to a camera that is refocusing or panning.

**Sync.** Lip and finger sync is everything. The picture must match the mix to the frame; check hard hits (snare,
plosives) at the start, middle and end of each song.

**Transition grammar.** Hard cuts on the beat. Dissolves only on ballads (0.5-1 s). Dip to black between songs in the
full-show file. No whips, no glitch.

**Sound.** The performance is the audio: board mix blended with an audience / camera mic for room and applause. No music
bed, no SFX, no ducking. Keep the master's own dynamics.

**Colour.** Stage light is extreme: `cinestill-800t` with a little `halation` for night shows, `music-video-neon` for
clubs, `documentary-natural` for recitals. Match cameras first (`color.match`), then the look.

**Captions.** None on the performance. Titles only: artist, venue, date, song titles as small lower thirds.

**What the client judges.** Angles that follow the music, sound, energy, the band looking good, sync.

**Common mistakes.** Cutting on every beat (seasick); missing the solo; out-of-sync picture; using the camera mic's
distorted audio; a lower third on every song; crushed blacks hiding the drummer.

## Make the edit

`multicam.py` switches to whichever camera's own mic is loudest (minimum shot `--min-shot`), uses `--wide` when several
are loud or nobody is, and takes the final sound from `--audio`. It does **not** sync cameras by waveform: every file
must start at the same moment. Align them first:

1. Find each camera's offset to the reference (a clap, a snare hit or the first chord): open the clips' waveforms or
   frames around the hit and note the time of the same hit in each file.
2. Trim each camera so it starts at that hit: `prep.py camB.mp4 --work syncB --start 3.42` writes `syncB/source.mp4`
   (constant 30 fps). Do the same for every camera and the wide.
3. Trim the board-mix WAV to the same hit with FFmpeg (`ffmpeg -ss 1.10 -i board.wav board_sync.wav`).

```bash
python CORE/scripts/prep.py camA.mp4 --work syncA --start 0.00
python CORE/scripts/prep.py camB.mp4 --work syncB --start 3.42
python CORE/scripts/prep.py wide.mp4 --work syncW --start 1.87
python CORE/scripts/multicam.py syncA/source.mp4 syncB/source.mp4 --wide syncW/source.mp4 --audio board_sync.wav --min-shot 3 --out show/multicam.mp4
python CORE/scripts/run.py show/multicam.mp4 --style SKILLS/event-promo --genre concert-multicam --format 16:9 --no-cut --model base --work show --stop-after plan
python CORE/scripts/render.py show/plan.json --frames 5,40,90,150,200
python CORE/scripts/render.py show/plan.json
python CORE/scripts/finish.py show/plan.json --platform youtube
```

Read `show/multicam.mp4.json` (the shot list) to see which angle won where. Loudest-mic switching suits bands where each
camera sits near a different player; for one PA mix on every camera it switches poorly. In that case build the edit
by hand: a timeline spec with each angle's `in`/`out` per section (all on the same synced files, `"audio": "mute"`),
then mux the board mix with `"music": {"src": "board_sync.wav", "volume": 1.0, "duck": false}` in the spec.

Per-song files: `run.py show/multicam.mp4 ... --stop-after plan` once, then cut songs with a spec per song
(`{"src": "show/multicam.mp4", "in": 312.4, "out": 538.0}`) or `prep.py show/multicam.mp4 --work song3 --start 312.4 --end 538.0`.

Vertical clips: `python CORE/scripts/track.py reframe song3/source.mp4 --out song3/clip_9x16.mp4 --format 9:16 --follow primary --mode smooth`
(MediaPipe needs a visible, fairly frontal face; with dark stages and small faces it centre-crops).

## Refine the plan

- **Delete the `captions` element** (lyrics transcription of a live mix is unreliable) and clear `words`.
- **Audio is the performance:** `"audio": {"platform": "youtube", "voice": false}` so the dialogue chain does not
  compress the mix; no `music`, no `sfx`.
- **Colour:** `"color": {"look": "cinestill-800t", "intensity": 0.7, "halation": 0.3, "match": "camA_hero.png"}`;
  `"finish": {"grain": 5, "vignette": 0.3}`.
- **Titles:** `{"type": "lowerthird", "name": "Song Title", "role": "Artist - Venue, 2026", "start": 4, "end": 9}` at the
  start of each song, nothing else on screen. End card: `titlecard` with artist and date.
- Fix bad switches in the shot list by rebuilding as a timeline spec; extend `--min-shot` (3-4 s) if it feels jumpy.
- **Angle clean-up (before multicam.py):** audience phone angles: `python CORE/scripts/prep.py cam3.mp4 --work fix/cam3 --stabilize --denoise light` and use `fix/cam3/source.mp4` (same length, so sync holds). Don't `--deflicker` stage lighting: strobes and chases are the show.

## Deliver

```bash
python CORE/scripts/deliver.py show/plan.json --to youtube,prores-422hq,audio-wav --out-dir show/deliver --burn no --no-post
python CORE/scripts/deliver.py song3/plan.json --to reels,tiktok,shorts --out-dir song3/deliver --burn no
python CORE/scripts/qc.py show/deliver/final_youtube.mp4 --plan show/plan.json --platform youtube --strict
```

`audio-wav` is the untouched 48 kHz / 24-bit mix for the band. Name files `band_venue_2026_song03_v001_16x9.mp4`.

## Check before delivering

- Sync on hard hits (snare, kick, plosives) at the start, middle and end of each song; drift means a camera's frame
  rate differed: re-prep it.
- The solo is on the soloist; the wide reset appears regularly; no shot on a focusing / panning camera.
- Strobes: `qc.py` photosensitivity check (>= 3 flashes in 1 s) often fires on concert light; warn the client, add a
  warning card at the start if it stays.
- Loudness at -14 LUFS without squashing the mix; no clipping on the drops.
- Tell the user which angles were used, the sync offsets, and that waveform auto-sync is not done by the engine.

## Example requests

- "I have three cameras and the desk recording from our gig, cut the whole set."
- "Make a vertical clip of the guitar solo in song 4."
- "Multicam my daughter's piano recital, two phones, keep it simple."
