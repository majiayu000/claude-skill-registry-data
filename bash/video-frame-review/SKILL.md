---
name: video-frame-review
description: "Use when reviewing a local video visually with systematic timestamped frame sampling, contact sheets, selected full-dimension frames, or dense inspection of a short interval."
---

# Video Frame Review

Use the local, offline CLI in scripts/video_frame_review.py for reproducible visual inspection. It samples decoded frames at about every 2 seconds by default, labels each thumbnail with the **actual presentation timestamp (PTS)** and requested time, and writes paginated contact sheets, a JSON manifest, and at least one full-dimension PNG. It does not edit the source video.

## Choose the route

- If Diffusion Studio is already available in the task environment, read its installed watch.md for the read-only footage workflow. Prefer its probe, filmstrip, and grab for ordinary editorial inspection. Grab chooses settled states from an automatic scan; it is not a guarantee of systematic every-2-second coverage. Its -S -q fullres supplies a separate full-resolution view. Use this CLI when offline/headless inspection, explicit PTS evidence, regular sampling, or dense intervals are needed. Do not invoke Diffusion listen or transcribe as part of this visual workflow.
- If using this CLI, verify ffmpeg, ffprobe, Python 3, and Pillow are available **in the current runtime**. Missing dependencies are a blocker; do not install packages or escape to a host runtime automatically. No PyAV is used.

## Run

Run these commands from the skill directory, or use the absolute path to its scripts directory.

~~~bash
python3 scripts/video_frame_review.py /path/to/local-video.mp4 --output /path/to/new-review-dir
python3 scripts/video_frame_review.py /path/to/local-video.mp4 --output /path/to/new-dense-review-dir --start 10 --end 18 --dense 12:14:0.25 --full 13.25
~~~

The output must be a new directory. Optional --interval changes the regular cadence; repeat --dense START:END:STEP and --full SECONDS to inspect transition windows and save selected full-dimension frames. The dense interval is end-exclusive and must lie inside the coverage window. The CLI rejects requests above 240 sample times, 12 contact-sheet pages, or 24 selected full-dimension frames; use narrower windows or separate runs rather than silently dropping coverage. Page size defaults to 20 and is capped at 40. Plan disk space for temporary decoded PNGs, especially with long 4K footage.

Read manifest.json before drawing conclusions: it records requested times, actual frame PTS, frame indices, covered interval, sheets, selected frames, and limitations. Review the whole contact sheets, then open relevant full/*.png at native decoded dimensions. A full PNG preserves pixel dimensions but is not the original compressed frame bitstream. If the chosen cadence misses a short event, rerun a **new output directory** with a dense interval or selected full times. Report what portion of the footage was sampled and what was inspected at full size.

This is visual evidence only: samples cannot establish events between frames or outside the requested window. The CLI notes whether an audio stream exists but does not listen, transcribe, or assess it. Use a separately authorized audio path if audio matters.

## Proof before adoption

On a runtime with the dependencies above, run python3 tests/prove_synthetic.py. It generates a local six-second clip, exercises 2-second and 0.2-second sampling, checks PTS mapping, three sheet pages, the full-dimension frame, and the audio limitation. For human visual inspection, run it with --pause, open the printed sheet and full-frame paths, then press Enter to remove the temporary fixture. Syntax checks or missing-dependency messages alone do not establish runtime or visual correctness.
