---
name: platform-pack
description: "Platform pack for Claude: turns one finished master into every platform version in one pass: YouTube, Shorts, Reels, TikTok, LinkedIn, X, Facebook, Snapchat, Pinterest, WhatsApp status, podcast video, web H.265/AV1, ProRes and DNxHR masters, GIF/WebP previews and audio files, each with the right frame, face-aware reframe, safe zones, loudness, length limit, subtitles, chapters, thumbnails and a post pack, then QC on every file. Use when the user says 'export for all platforms', 'make vertical and square versions', 'post this everywhere', 'Reels and TikTok versions', 'LinkedIn version', 'what size for Shorts', 'deliverables for social'. Runs on video-studio-core (deliver, track, qc)."
license: MIT
---

# Platform Pack

One master in, a folder of correctly built uploads out, each one checked.

- **Best for:** any finished edit that needs to go to more than one place
- **Inputs:** a finished `W/plan.json` (+ `final.mp4`) or any finished video file
- **Outputs:** `final_<preset>.<ext>` per platform, `captions.srt/.vtt/.ttml`, `chapters.txt`, `thumb_*.png`,
  `post.md`, `deliver_report.md`, plus a `qc_report` per file

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder.
- First run on a machine: `python CORE/scripts/check_env.py`.
- See the live preset table: `python CORE/scripts/deliver.py --list`.
- Ask which platforms, whether captions should be burned in, and whether the vertical should be a real re-edit
  (better) or a reframe of the 16:9 (faster). Lock picture before you pack.

## Pick the presets

| preset | frame | max length | loudness | keep text out of |
| --- | --- | --- | --- | --- |
| youtube | 1920x1080 | 12 h | -14 / -1 | 5% title-safe |
| shorts | 1080x1920 | 3 min | -14 / -1 | top 13%, bottom 22%, right 14% |
| reels | 1080x1920 | 3 min (recommended) | -14 / -1 | top 12%, bottom 18%, right 6% |
| tiktok | 1080x1920 | 10 min (API) | -14 / -1 | top 6%, bottom 25%, right 14% |
| linkedin | 1080x1350 (4:5) | 10 min* | -14 / -1 | 5% |
| x | 1280x720 | 140 s (free tier) | -14 / -1 | 5% |
| facebook | 1080x1350 | 240 min | -14 / -1 | 5% |
| snapchat | 1080x1920 | 60 s* | -14 / -1 | top 10%, bottom 20% |
| pinterest | 1080x1920 | 60 s* | -14 / -1 | top 10%, bottom 25%, right 10% |
| whatsapp-status | 720x1280 | 60 s*, 16 MB* | -14 / -1 | as shorts |
| podcast-video | 1920x1080 | | -16 / -1 | 5% |
| web-h265 / web-av1 | source | | -14 / -1 | |
| prores-422hq / prores-4444 / dnxhr-hq | source | | mix untouched | masters for editors / archive |
| broadcast-xdcam | 1080i25 MXF | | -23 / -1 (EBU R128) | 5%; "XDCAM-like", not conformance-checked |
| gif / webp | 480 wide | 6 s | | previews |
| audio-wav / podcast-mp3 | | | untouched / -16 | |

`*` = third-party or contested figures: tell the user when a limit matters. Safe-zone percentages are different on
every app; one conservative rule for all verticals: keep text between 13% and 75% of the height and out of the right 14%.

## Make the pack

```bash
python CORE/scripts/deliver.py W/plan.json --to youtube,shorts,reels,tiktok,linkedin,x --out-dir W/deliver
python CORE/scripts/qc.py W/deliver/final_youtube.mp4 --plan W/plan.json --platform youtube --strict
python CORE/scripts/qc.py W/deliver/final_reels.mp4 --plan W/plan.json --platform reels --strict
python CORE/scripts/qc.py W/deliver/final_tiktok.mp4 --plan W/plan.json --platform tiktok --strict
```

> Tested: `qc.py --plan` compares a **reframed** output (e.g. 9:16 from a 16:9 plan) with the plan's own frame and
> overlay positions, so it reports false FAILs (`resolution_vs_plan`, `safe_zone_vertical`, `max_overlays_at_once`).
> For files whose aspect differs from the plan, run `qc.py FILE --platform NAME` without `--plan`, and check overlays on a still.

Run `qc.py` once per file with that file's platform (audio files too: `qc.py final_podcast-mp3.mp3 --platform podcast`). From a plain video instead of a plan:
`python CORE/scripts/deliver.py final.mp4 --to reels,tiktok --words W/words.json --out-dir out`.

### Reframing (aspect change)

`deliver.py` reframes when the preset's aspect differs from the master:
- **Face-follow crop** when it finds a face track: `W/track.json`, or pass one. Make it for the finished video:

```bash
python CORE/scripts/track.py analyze W/final.mp4 --work W --out W/track_final.json
python CORE/scripts/deliver.py W/plan.json --to shorts,reels,tiktok --track W/track_final.json --out-dir W/deliver
```

  A track whose width/height do not match the input is ignored (it falls back to the next mode).
- **Centre crop** for mild changes (aspect ratio within 0.8-1.25x of the master, e.g. 4:5 to 1:1).
- **Blurred fill** otherwise: the subject is never cut off, but a 9:16 master sent to YouTube becomes a blurred
  pillarbox, and 16:9 to 9:16 without a track becomes a small band in a blurred frame.
- **Best quality:** re-render the plan at the target size instead (`make_plan.py --format 9:16` or `run.py ... --format 9:16`
  on the same footage), so graphics are laid out for that frame, then deliver that plan to the vertical presets.

### Captions

- `--burn auto` (default) burns subtitles only on presets that autoplay muted (verticals, LinkedIn, Facebook) **and**
  only if the plan has no creator `captions` element. `--burn yes|no` overrides.
- Burn-in uses libass, or Pillow PNGs (`--burn-engine pillow`) if libass fails. FFmpeg drawtext is never used.
- YouTube: upload `captions.srt` as a sidecar instead of burning (searchable, translatable).
- Kids content: `--kids` (17 cps). Custom reading speed: `--cps 15`.

### Length, chapters, thumbnails, post text

- Too long for a preset: the report warns; `--trim` cuts to the platform maximum (better: make a real cutdown).
- Chapters: `--chapters "0:00 Intro; 1:20 Setup; 4:05 Results"`, else `plan.chapters`, else automatic.
  YouTube needs 00:00 first, >= 3 chapters, each >= 10 s.
- Thumbnails from the clean speaker video; headline override `--headline "3 Mistakes That Cost Me $10,000"`.
  `--no-thumbs` / `--no-post` skip them.
- `post.md` drafts titles, description, hashtags from the transcript only. Never add claims the video does not make.

## Name and hand over

Rename for the client: `client_project_v003_9x16_reels.mp4`, `..._16x9_youtube.mp4`, `..._4x5_linkedin.mp4`.
Hand over the files, `deliver_report.md`, every `qc` report, the sidecars and `post.md`.

## Check before delivering

- `deliver_report.md`: every preset `ok`, measured LUFS / dBTP next to the target, reframe mode per file, warnings read.
- Every `qc.py` run passes (or each WARN is explained): frame, fps, codec, faststart, loudness within +-1 LU, size and
  length inside limits, safe zones on verticals.
- Look at a still of each vertical: face not cropped, captions not under the platform buttons, no tiny pillarbox.
- Thumbnails readable at 160 px wide; YouTube thumbnail <= 2 MB (convert PNG to JPG q90 if bigger).
- Tell the user which versions were reframed (and how) versus re-rendered, and any trimmed or over-length file.

## Example requests

- "Export this for YouTube, Reels, TikTok and LinkedIn."
- "I need a WhatsApp status version under 16 MB and a GIF preview for the website."
- "Make the vertical versions follow my face, and burn captions only where it autoplays muted."
