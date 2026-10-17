---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: song-recognition
repo: remorses/opencode-config
description: >
  Identify songs from audio files using ShazamIO. Use when the user asks to
  recognize a song, identify music from an audio file, find what song is
  playing, or Shazam an audio clip.
---

# Song Recognition

Identify songs from audio files using ShazamIO (reverse-engineered Shazam API).
Free, unlimited, no API key needed. Uses the full Shazam catalog.

## Usage

Run the bundled script with `uv run`:

```bash
uv run --with shazamio ~/.config/opencode/skills/song-recognition/recognize.py /path/to/audio.mp3
```

The script tries multiple offsets through the file (every 5 seconds) because
Shazam often fails on intros, quiet sections, or ambient parts. It stops at
the first match.

## Notes

- Shazam returns **one result per request**, not a ranked list.
- Short clips (under 5s) may not match. The script uses 15s clips.
- If no offset matches, the song may not be in Shazam's catalog,
  or it could be a cover/remix that fingerprints differently.
- Results include title, artist, genre, and a Shazam URL.
