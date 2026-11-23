---
name: music-video
description: "Music-video editor: syncs every performance take to the master track, builds a performance 'multicam' of takes, intercuts narrative footage, cuts on downbeats and phrase changes (varying every beat / every 2nd / every bar), uses speed ramps and flashes on hits, applies a heavy stylised grade, and delivers the 16:9 master plus 9:16 hook clips and clean/explicit versions. Use when the user says: edit my music video, cut to the beat, performance edit, beat-synced montage, lip-sync takes to the song, visualiser with footage, make a music video from these clips. Default skin neon-orbit; any Video Studio skin works."
license: MIT
---

# Music Video

Every take locked to the song, cuts that breathe with the music, a look as loud as the track.

- **Best for:** artist music videos, performance videos, dance videos, beat-synced montages, visualisers with footage
- **Inputs:** the master song (licensed / the artist's), performance takes shot to playback, narrative/B-roll clips
- **Default skin:** `neon-orbit` · alternatives `y2k-chrome`, `chaos-stack`, `vhs-tape` (graphics are minimal; the skin mostly sets title styling)
- **Formats:** 16:9 1920x1080 master (or 4K source), 9:16 hook clips (15-30 s chorus), clean/explicit versions
- **Duration target:** the song (2.5-5 min); genre preset `music-video`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre music-video`.
- **Sync method:** every performance take must have the playback audible (or a slate clap at a known song second). Find each take's offset: the take second where song second 0 plays (`OFFSET_take`). Then a song moment T is at `OFFSET_take + T` in that take.
- Ask: explicit lyrics? (clean version needed), artist look references, credits.

## How a pro cuts this

| section | cutting | what happens |
| --- | --- | --- |
| intro | slow (bar or 2 bars) | establish the world, the artist's first look |
| verse | every 1-2 beats in performance, holds on narrative | story moves |
| pre-chorus | accelerating | build: closer shots, faster |
| chorus | on the beat, biggest shots, hero performance take | energy peak, best lip-sync |
| bridge | change: slow-mo, different look or location | contrast |
| final chorus | fastest, every half beat on hits, flashes | climax |
| outro | resolve on the last downbeat | final image |

- **Pacing:** ASL 0.8-3 s; vary between every beat, every 2nd beat and every bar; hold longer on the best performance moments.
- **Cut rules:** cut on downbeats and phrase changes (every 4/8 bars), right before strong beats; lip sync must be frame-accurate on the sung words (performance cuts happen on beats, not mid-syllable).
- **Intercut:** performance carries the chorus; narrative carries verses; cutaways on instrumental bars.
- **Transitions:** cuts; flash-white / glitch / zoom-blur overlays on hits only; speed ramps (0.4x into a hit, snap back) on the drop.
- **Audio:** the song is the soundtrack, untouched (no dialogue chain, no ducking). Diegetic sound only if the intro/outro has a scene.
- **Colour:** stylised: `music-video-neon` 0.9, `cross-process`, `cinestill-800t` + halation, `infrared` for surreal; consistent per section.
- **Captions:** none (use `lyric-video` for lyrics).
- **Client (artist) judges:** lip sync, rhythm matching the song, the artist looking iconic.
- **Common mistakes:** cutting on every beat for 3 minutes, out-of-sync mouths, the hero take buried, no change in the bridge, a grade that turns skin green unintentionally.

## Make the edit

Beat map first:

```bash
python CORE/scripts/beats.py song.wav --out mv/beats.json --peaks
```

Quick beat montage of narrative clips (auto-picks shots, every cut on a beat):

```bash
python CORE/scripts/timeline.py auto narrative/ --work mv_draft --mode montage --music song.wav --duration 200 \
  --beats-per-shot 2 --format 16:9 --dry-run      # edit mv_draft/timeline_spec.json
```

Performance cutting is a hand-written spec: each clip's `in` = `OFFSET_take + song second where the shot starts`, `out` = `OFFSET_take + song second where it ends` (shot boundaries from `beats.json` downbeats), `"audio": "mute"`, and the song as the spec music:

```json
{"format": "16:9", "fps": 30,
 "clips": [
   {"src": "perf_wide_t2.mp4", "in": 4.12, "out": 11.62, "audio": "mute"},
   {"src": "narr_street.mp4", "in": 20.0, "out": 23.75, "audio": "mute"},
   {"src": "perf_cu_t5.mp4", "in": 18.30, "out": 21.05, "audio": "mute",
    "speedRamp": [{"at": 20.4, "rate": 0.4, "ramp": 0.4}]}],
 "music": {"src": "song.wav", "volume": 1.0, "duck": false, "fadeOut": 0.1}}
```

(Speed-ramped performance shots lose lip sync; use them on instrumental bars.) Then:

```bash
python CORE/scripts/timeline.py build mv_spec.json --work mv --no-transcribe
python CORE/scripts/make_plan.py --work mv --style SKILLS/neon-orbit --genre music-video --format 16:9 --beats mv/beats.json --no-matte
python CORE/scripts/render.py mv/plan.json --frames 10,45,90,150
python CORE/scripts/render.py mv/plan.json
python CORE/scripts/finish.py mv/plan.json --platform youtube
```

If `make_plan.py` stops for missing words (no speech was transcribed), write `{"words": []}` to `mv/words.json` and run it again.

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Graphics:** keep `"elements"` to the title (`titlecard` artist / song on the first downbeat) and end credits; remove captions.
- **Hits:** `{"type": "flash", "times": "downbeats", "opacity": 0.35, "dur": 0.1}` only inside the final chorus window (or a hand list of times); `{"type": "transition", "kind": "zoom-blur", "at": 61.2, "dur": 0.3}` on the drop.
- **Beat pulse:** `"pulseOn": "downbeats"` on the title; `shake` with `decay` on the biggest hit.
- **Audio:** `"audio": {"voice": false}` so the song gets no dialogue processing; loudness is still normalised (-14 LUFS) - use `--platform` per delivery.
- **Look:** `"color": {"look": "music-video-neon", "intensity": 0.9}`, `"finish": {"grain": 8, "halation": 0.4, "aberration": 2}`.

## Deliver

```bash
python CORE/scripts/deliver.py mv/plan.json --to youtube,youtube-4k --out-dir mv/deliver --no-post
python CORE/scripts/qc.py mv/deliver/final_youtube.mp4 --plan mv/plan.json --platform youtube
```

- 9:16 hooks: rebuild a chorus-only spec with `"format": "9:16"` and `"reframe": "face"` on performance clips; deliver `reels,tiktok,shorts`.
- Clean version: same spec with the clean song file; check the visuals don't show explicit words.

## Check before delivering

- Lip sync checked at three chorus points (frame-accurate on hard consonants).
- Cuts land on beats; no section cut uniformly for > 30 s; bridge feels different.
- Song intact (no clicks at the start/end, ends on the last downbeat), loudness on target.
- `qc.py`: flash frames under the photosensitivity limit (< 3 flashes in any second).
- Tell the user: structure, takes used per section, look, files.

## Example requests

- "Edit my music video: performance takes + street scenes, cut to the beat, neon grade."
- "Make a beat-synced montage of these 40 clips on my track."
- "Cut 3 vertical chorus clips from the music video for Reels."
