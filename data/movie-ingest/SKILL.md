---
name: movie-ingest
description: >
  Locate NZBGeek releases with subtitle-rich movie files, auto-tag rage/anger/humor
  cues, and emit PersonaPlex-ready JSON for Horus Theory-of-Mind benchmarks.
triggers:
  - movie ingest
  - ingest movie
  - nzb search
  - movie subtitles
  - persona plex movie
allowed-tools:
  - Bash
  - Python
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins:
        - uv
        - ffmpeg
        - whisper
        - requests
---

Use this skill whenever we need cinematic emotional exemplars (respect, humor, regret, anger, rage, etc.) for PersonaPlex.

It enforces a **subtitle-first** workflow:

1. **Search** NZBGeek for scene releases that already include `.srt`/`.sup` files with stage directions.
2. **Map** rage/anger windows from the subtitle text or tags (no decoding needed yet).
3. **Clip + Transcribe** targeted scenes, marry them with the subtitle cues, and emit Persona-ready JSON.

## Commands

### `run.sh search "<title>"`

- Calls NZBGeek’s API (requires `NZBD_GEEK_API_KEY`) and prints size/date/link.
- Use this to locate releases that explicitly mention `subs`, `CC`, or `SDH`.

### `run.sh scenes find --subtitle <file.srt> (--query "text" | --tag laugh)`

- Quick TUI view of subtitle windows that match free text or cue tags (`rage`, `shout`, `laugh`, etc.).
- Pass `--video movie.mkv` to see ready-to-copy `ffmpeg -ss ... -to ...` snippets.
- Designed for “project agent wants a specific sequence” moments.

### `run.sh scenes extract --subtitle <file.srt> --tag rage --video movie.mkv --clip-dir ./clips`

- Writes a PersonaPlex-ready manifest that lists each candidate scene, cue tags, inferred emotion, and clip timing.
- Optional `--clip-dir` automatically runs `ffmpeg` to produce numbered `.mkv` clips plus `.srt` subtitle snippets per match.
- Use this when we need every rage/anger sequence from a film—no guessing or manual scrubbing.

### `run.sh transcribe movie_clip.mkv --emotion rage --scene "..."`

- Extracts mono WAV via `ffmpeg`, runs Whisper (default `medium`), and joins the output with the matching `.srt`.
- Produces `*_persona.json` containing:
  - Stable `video_id`, movie title, scene notes, ISO timestamp.
  - Segment-by-segment tags (`laugh`, `rage`, `whisper_candidate`, etc.).
  - Rhythm metrics (WPM, pause count, duration).
- Pipe straight into `horus_lore_ingest.py emotion --input <dir> --emotion rage`.

> **Do we still need the movie if we have subtitles?**  
> Yes for PersonaPlex: subtitles help us *find* the right windows, but Whisper + rhythm features require the actual audio to model tone, pacing, and breath. Use `scenes extract --subtitle-only` when scouting, then transcribe once the clip is cut.

## Environment

| Variable | Purpose |
|----------|---------|
| `NZB_GEEK_API_KEY` (or `NZBD_GEEK_API_KEY`) | Auth for NZBGeek search |
| `NZB_GEEK_BASE_URL` (or `NZBD_GEEK_BASE_URL`) | Override for private Usenet proxies |
| `WHISPER_BIN` | Path to Whisper CLI (defaults to `~/.local/bin/whisper`) |
| `FFMPEG_BIN` | Path to ffmpeg (defaults to `/usr/bin/ffmpeg`) |
| `AUDIO_RMS_THRESHOLD` | Base RMS threshold for audio intensity tags (default `0.2`) |
| `AUDIO_RMS_WINDOW_SEC` | Window size in seconds for RMS scanning (default `0.5`) |

> Audio intensity tagging automatically installs `numpy` + `soundfile` via `uv`. If either import ever fails, the CLI logs a warning and continues without those tags so ingestion still works.

## Workflow Example

```bash
# 1. Find a release that ships with SDH subtitles
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/movie-ingest
./run.sh search "There Will Be Blood"

# 2. Extract rage windows from the downloaded subtitles
./run.sh scenes extract \
  --subtitle "/home/graham/Downloads/media/movies/There Will Be Blood (2007)/blood.en.srt" \
  --tag rage \
  --video "/home/graham/Downloads/media/movies/There Will Be Blood (2007)/There.Will.Be.Blood.2007.PROPER.1080p.BluRay.x264-ELBOWDOWN.mkv" \
  --clip-dir "./clips/there_will_be_blood_rage" \
  --output-json "./clips/there_will_be_blood_rage/scenes.json"

# 3. Transcribe one of the clips with subtitles + metadata baked in
./run.sh transcribe ./clips/there_will_be_blood_rage/clip_01.mkv \
  --subtitle ./clips/there_will_be_blood_rage/clip_01.srt \
  --emotion rage \
  --movie-title "There Will Be Blood" \
  --scene "Most explosive confrontation" \
  --characters "Daniel Plainview,Eli Sunday"
```

## Sanity

```bash
./sanity.sh   # Verifies Typer CLI + scenes helpers load
```
