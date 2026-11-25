---
name: sk-render
description: Renders a short to mp4 with Remotion, normalises loudness, and re-encodes it to the platform upload spec (yuv420p limited range, BT.709 tags, 48 kHz audio, faststart), then verifies each file with ffprobe and by looking at frames. Use when the user says "render the video", "export it", "make the final mp4", "fix the loudness", "it's too quiet", "colours look washed out after upload", "the file won't play", or reports a truncated or broken output. Steps 10, 12 and 13 of sk-pipeline.
---

# sk-render: render, normalize, encode

**Announce:** "Using sk-render for <id>."

Rules: §8 audio (`docs/soul/06-audio.md`), §11 encode spec
(`docs/soul/08-cover-and-handoff.md`), §13 files. The § wins over this file.

## Before rendering

- `bun run lint <id>` 0 errors, `bun run check` clean, stills reviewed (`sk-scene`).
- `voice.json` is newer than `narration.json`; otherwise run `bun run tts <id>` first.

## Steps

1. **Render:**
   ```bash
   bun run render <id>        # → out/<id>/<id>.mp4
   ```
   Remotion bundles the source when the render starts. Editing files during a
   render changes nothing in that render; if a fix is missing from the output,
   compare the file's modification time with the render start before debugging code.
2. **Check the render is whole.** Exit 0 is not proof. Duration should match
   `voice.json` duration plus `outroHold`:
   ```bash
   ffprobe -v error -show_entries format=duration -of default=nw=1 out/<id>/<id>.mp4
   ```
3. **Look at frames from the mp4 itself**, not from the studio: the first frame,
   a frame per scene, the last frame.
   ```bash
   ffmpeg -v error -ss <seconds> -i out/<id>/<id>.mp4 -frames:v 1 out/<id>/check-<seconds>.png
   ```
   Open them. Delete the `check-*.png` files when done.
4. **Normalize loudness:**
   ```bash
   bun run normalize <id>     # → out/<id>/<id>-loud.mp4, target loudnessLUFS (default -13)
   ```
   Then listen: music must stay below the voice by at least `musicUnderVoiceDb`
   (§8), fade to zero, and the last 3 to 4 seconds hold the final frame.
5. **Encode for upload:**
   ```bash
   bun run encode <id>        # → out/<id>/<id>-upload.mp4
   ```
   Why this step exists: Remotion's default output can be full-range `yuvj420p`
   with an unusual sample rate and no faststart. Platforms re-encode assuming
   limited range, so colour comes out crushed or washed out, and nothing errors.
6. **Verify the upload file:**
   ```bash
   ffprobe -v error -select_streams v:0 \
     -show_entries stream=pix_fmt,color_range,color_primaries,color_transfer,color_space \
     -of default=nw=1 out/<id>/<id>-upload.mp4
   ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate \
     -of default=nw=1 out/<id>/<id>-upload.mp4
   ```
   Expect `yuv420p`, `tv`, `bt709` on all three colour axes, `48000`.
7. **Re-measure loudness on the final file**, because encoding touches audio:
   ```bash
   ffmpeg -i out/<id>/<id>-upload.mp4 -af ebur128 -f null - 2>&1 | grep -A3 Summary
   ```

## Traps

- **Never pipe a long ffmpeg command into `head`.** ffmpeg gets SIGPIPE and leaves
  an mp4 without a `moov` atom, still exiting 0.
- `ffmpeg -ss` *before* `-i` seeks to a keyframe; for sample-accurate audio checks
  use `-af "atrim=start=A:end=B,volumedetect"`. `volumedetect` logs at info level,
  so do not pass `-v error` or the numbers vanish.
- Keep every output inside `out/<id>/` (§13). No loose files at the root of `out/`.
- Render order and file names stay stable: the hand-off reads exact paths.

## Verify

- [ ] `out/<id>/<id>.mp4` duration matches the voice + outro hold
- [ ] frames pulled from the mp4 and opened
- [ ] `<id>-loud.mp4` at target loudness, no clipping, music under the voice floor
- [ ] `<id>-upload.mp4` passes the ffprobe checks above

Next: `sk-handoff` (cover can be done before or after encode).
