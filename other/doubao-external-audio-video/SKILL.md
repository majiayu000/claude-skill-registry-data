---
name: doubao-external-audio-video
description: Use when opening or controlling Doubao through the shared visible Chrome/CDP profile to create a video from externally generated music, including audio and image uploads, prompt preparation, guarded paid submission, monitoring, download, soundtrack replacement, and reusable documentation.
---

# Doubao External-Audio Video

Use the real Doubao web UI in the existing visible browser. Do not substitute a
Doubao API unless the user explicitly requests it.

## Workflow

1. Reuse the configured Chrome profile, CDP endpoint, and noVNC desktop. Prove
   that the Doubao tab and visible browser share the same process/profile.
2. Bring Doubao to the front. If login is required, stop for visible user login.
3. Preserve the reviewed external song as the soundtrack authority. Probe its
   duration and audio stream before upload.
4. Prepare a path-free video prompt and one or more stable visual references.
5. Select video generation, upload the actual audio and image files, fill the
   prompt, and capture screenshot/DOM evidence.
6. Validate login, selected mode/model/duration/ratio, attachments, prompt, and
   visible cost. Do not submit if any paid-generation contract field is unclear.
7. Submit exactly once only after explicit approval. A queued/running state or
   changed credit balance means monitor, not retry.
8. Download the result and verify identity, duration, dimensions, video stream,
   and audio stream. If Doubao changes the song, mux the reviewed external audio
   back into the downloaded video.

Use the project controller when present:

```bash
python scripts/doubao_cdp_browser.py prepare \
  --prompt-file PROMPT.md --audio SONG.mp3 --image REFERENCE.png \
  --screenshot outputs/doubao/prepared.png
python scripts/doubao_cdp_browser.py submit --confirm-paid
python scripts/doubao_cdp_browser.py result --activate
python scripts/doubao_cdp_browser.py download --output Videos/result.mp4
```

If direct audio upload is unsupported, finalize with the project soundtrack
helper or equivalent FFmpeg mapping:

```bash
scripts/doubao_lock_soundtrack.sh \
  Videos/result.mp4 reviewed-song.mp3 Videos/result-song-locked.mp4 0
```

Never paste local paths into the creative prompt. Keep local paths only in a
private manifest or ignored local configuration.

Read `references/workflow.md` for recovery and validation details.
