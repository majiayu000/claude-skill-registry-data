---
name: lyric-video
description: "Lyric-video editor: times every lyric line to the sung vocal (Whisper word timestamps, optionally on a Demucs vocal stem), shows each line with a karaoke fill as it is sung and the next line dimmed, over artwork, footage or a beat-reactive background, and delivers a 16:9 lyric video, a 9:16 chorus clip and an .srt of the lyrics. Use when the user says: lyric video, put the lyrics on screen, karaoke video, sing-along video, animated lyrics, lyrics for my song, visualiser with lyrics. Lyrics must be the artist's approved text. Default skin neon-orbit."
license: MIT
---

# Lyric Video

The words land exactly when they are sung, readable on any background, in the artist's look.

- **Best for:** song releases, sing-alongs, devotional and worship lyrics, karaoke versions
- **Inputs:** the song (master), the approved lyrics text, cover art / background footage
- **Default skin:** `neon-orbit` (use `--no-matte`) · alternatives `paper-cut`, `swiss-poster` (`--no-matte`), `minimal-mono`
- **Formats:** 16:9 1920x1080, 9:16 chorus clip (15-30 s), lyrics `.srt`
- **Duration target:** the song; genre preset `lyric-video`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = `video-studio-core`, `SKILLS` = the folder holding both.
- First time: `python CORE/scripts/check_env.py`. Preset: `python CORE/scripts/editor.py genre lyric-video`.
- Get the lyrics as text, exactly as the artist writes them (spelling, line breaks, censoring). Whisper only supplies *timing*; the words on screen come from the approved text.
- Vocal stem (optional, much better timing on dense mixes): `pip install demucs`.

## How a pro cuts this

| section | what happens |
| --- | --- |
| intro | title + artist on the artwork until the first sung word |
| verses | one line at a time, low-to-mid frame, calm motion |
| chorus | bigger type or a different layout; the same design each chorus so it feels like a hook |
| bridge | a visual change (colour, background) |
| outro | title card again, credits |

- **Timing:** each line appears 0.1-0.2 s before its first sung word and leaves 0.2 s after the last; words fill as sung. No line on screen < 1 s.
- **Line length:** <= 42 characters (16:9), <= 26 (9:16); split long lines at the singer's breath.
- **Readability:** contrast over any background (shadow/box/dim the background with `vignette`); avoid the face if footage has a singer.
- **Motion:** gentle (`maskUp`, `fade`); beat pulses on the chorus only; never shake text people must read.
- **Audio:** the song untouched (`"audio": {"voice": false}`), normalised to -14 LUFS.
- **Colour:** follow the cover art; a look on footage only (`music-video-neon`, `dreamy`, `vintage-70s`).
- **Client (artist) judges:** sync, readability, matches the release artwork.
- **Common mistakes:** lyrics typed from Whisper (wrong words), lines late by half a second, two lines changing at once, tiny type, text over the singer's mouth.

## Make the edit

1. A background video carrying the song (artwork still; or footage cut to the song with `timeline.py` / the `music-video` skill):

```bash
ffmpeg -loop 1 -i cover.jpg -i song.wav -r 30 -pix_fmt yuv420p -c:v libx264 -tune stillimage -c:a aac -shortest lyr_src.mp4
```

2. Plan with word timing from the song:

```bash
python CORE/scripts/run.py lyr_src.mp4 --style SKILLS/neon-orbit --genre lyric-video --no-cut --no-matte --format 16:9 \
  --model small --prompt "distinct words from the lyrics" --work lyr --stop-after plan
```

3. If the timing is poor (busy mix), time the vocal stem instead, in its own folder, and use its words for timing:

```bash
python CORE/scripts/stems.py song.wav --out lyr_vox/stems
ffmpeg -loop 1 -i cover.jpg -i lyr_vox/stems/vocals.wav -r 30 -pix_fmt yuv420p -c:v libx264 -c:a aac -shortest lyr_vox/vox.mp4
python CORE/scripts/prep.py lyr_vox/vox.mp4 --work lyr_vox && python CORE/scripts/transcribe.py --work lyr_vox --model small
#  read lyr_vox/transcript.json for line start/end times (song time = video time, both start at 0)
```

4. Write the `lyric` element from the approved text + those times (next section), then:

```bash
python CORE/scripts/render.py lyr/plan.json --frames 10,30,60,90
python CORE/scripts/render.py lyr/plan.json
python CORE/scripts/finish.py lyr/plan.json --platform youtube
```

Always pass `--format` matching the project: run.py and make_plan.py otherwise use the skin's own format (many skins default to 9:16).

## Refine the plan

- **Remove** the skin's `captions` element.
- **Lyric element:** `{"type": "lyric", "start": 0, "end": 212.0, "y": 760, "w": 1500, "lines": [{"text": "Seek it anywhere", "start": 31.6, "end": 33.0}, {"text": "you will find me there", "start": 33.2, "end": 35.4}]}` - text from the approved lyrics, times from the transcript (start 0.1 s early).
- **Per-word fill:** give a line its own `words` (`[{"w": "Seek", "start": 31.6, "end": 31.9}, ...]`) copied from the transcript but spelled as in the lyrics.
- **Title / credits:** `titlecard` with artist and song at 0 s until the first line; credits at the end.
- **Chorus emphasis:** a second `lyric` element for chorus ranges with a bigger `style` (`{"fontSize": "96px"}`) and `"pulseOn": "beats"` (add `"beats"` from `beats.py song.wav --out lyr/beats.json` via `make_plan.py --beats`).
- **Background:** `vignette` (`"strength": 0.7`) for contrast; `lightleak` (`"intensity": 0.3`) in the bridge.
- **Audio:** `"audio": {"voice": false}`; no `music` block (the song is the source audio).
- **SRT of lyrics:** put the approved words with their times into `plan.words` so `deliver.py` writes `captions.srt` from them.

## Deliver

```bash
python CORE/scripts/deliver.py lyr/plan.json --to youtube --burn no --out-dir lyr/deliver --no-post
python CORE/scripts/qc.py lyr/deliver/final_youtube.mp4 --plan lyr/plan.json --platform youtube
```

- 9:16 chorus clip: a new work folder with `--format 9:16` on the chorus range (`prep.py lyr_src.mp4 --work chorus --start 58 --end 84`, then `run.py chorus/source.mp4 ... --format 9:16`), lines <= 26 characters.
- Give the artist `captions.srt` (also usable as synced lyrics on platforms that accept SRT).

## Check before delivering

- Every word matches the approved lyrics (diff your `lines` against the lyric sheet).
- Sync checked at the first line, each chorus start and the last line (+-0.1 s).
- Readable on the darkest and brightest background moments; inside safe areas.
- Song audio intact and on loudness target.
- Tell the user: line count, any lines you split, files.

## Example requests

- "Make a lyric video for my song with this cover art, karaoke-style highlight."
- "Lyrics on screen over my performance footage, bigger text on the chorus."
- "A 9:16 chorus lyric clip for Reels."
