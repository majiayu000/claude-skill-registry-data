---
name: background-music
description: Pick background music from the assets/music/ library and configure auto-ducking (music dips automatically under speech) via meta.json audio.music for the Remotion assembly layer. Read when the brief/edit prompt has a "Nhạc nền" (background music) section set to auto, or when the user asks to add/adjust background music on a video.
---

# Background Music - music bed + auto-ducking

Background music is played by Remotion in the assembly layer (the `MusicTrack` component): the track loops, fades in over 0.5s at the start of the video, fades out over 1s at the end, and **auto-ducks** (smooth 0.4s volume dip) around every speech segment. Claude's job is to pick the track + generate the speech ranges + declare `audio.music` correctly in `meta.json` - everything else is deterministic inside Remotion.

## 1. Pick a track by mood

- Read `assets/music/library.json` - each entry has `file`, `tags` (mood: nang-luong, chill, cam-hung, cang-thang, vui-ve...), `durationMs`, `description`.
- Pick **ONE** track whose mood matches the video content (motivational video -> nang-luong/cam-hung; slow explainer -> chill...).
- A track shorter than the video is fine - `MusicTrack` loops it automatically, no need to concatenate files with ffmpeg.

## 2. Generate speech ranges from the transcript

Speech ranges = the segments that DO contain speech (in seconds, on the already-cut composition timeline) - these are the moments the music gets ducked.

1. Take the word timestamps from the transcript (already remapped if autoCut ran).
2. Merge adjacent words into one continuous range.
3. **Merge two ranges if the gap between them is < 0.6s** - a short breath between two sentences is not worth having the music swell back up and drop again.
4. Result: `[[startSec, endSec], ...]` - usually just a few ranges for a talking-head video (silent intro, body, outro).

## 3. Volume levels

| Context | volume | Notes |
|---|---|---|
| Speech present (`duckVolume`) | **0.10-0.15** | Music sits ~18-20dB below the voice - the voice is ALWAYS clearer than the music |
| No speech (`volume`): intro/outro/pauses | **0.30-0.40** | Music carries the emotion but does not bury the sfx |

Loud / bass-heavy tracks -> take the **lower bound** of both ranges (0.10 / 0.30).

## 4. Declare it in meta.json

**Copy the music file into the project's `assets/`** (same as sfx) so the project stays portable - NEVER point directly at the shared library:

```powershell
Copy-Item "assets/music/<file>" "video-projects/<id>/assets/music/<file>"
```

Then declare it (path relative to the project root):

```json
"audio": {
  "voice": "...",
  "sfx": [...],
  "music": {
    "file": "assets/music/<file>",
    "volume": 0.35,
    "duckVolume": 0.12,
    "speech": [[1.2, 14.8], [16.1, 42.5]]
  }
}
```

The server stages the file into the Remotion staging directory during assembly - nothing else to do.

## 5. Verify (mandatory before final)

1. Render a draft (assemble-draft) then **listen at 3 points**: start of the video (fade-in + intro level), middle of the video during speech (music must sit clearly under the voice), end of the video (clean fade-out).
2. The only standard: **the voice MUST be clearer than the music at every moment**. If you have to strain to make out the words -> lower `duckVolume`.
3. If in doubt about the levels, measure with `ffmpeg -i <draft.mp4> -af volumedetect -f null NUL` over a speech segment and a non-speech segment, and compare the two mean_volume values.

## Mistakes to avoid

- **Music louder than speech** - `duckVolume` is too high, or the speech ranges are missing a segment. Re-check transcript coverage: every spoken segment must fall inside a range.
- **Forgetting the final fade-out** - `MusicTrack` fades out over 1s based on `durationInFrames`; but if the composition's total duration is computed wrong, the music gets cut off abruptly. Verify the end point when listening to the draft.
- **Music with Vietnamese lyrics** - it fights the speech, the listener's brain cannot separate two layers of words. ONLY use instrumental music.
- **Downloading music from the internet** - FORBIDDEN (copyright). Only use the `assets/music/` library. If the library is empty -> skip background music and state that clearly in the report.
