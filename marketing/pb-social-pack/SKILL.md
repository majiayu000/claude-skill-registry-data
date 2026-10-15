---
name: pb-social-pack
description: >-
  Turn a release or ship recap into a social pack: posts per platform where
  every claim traces to a facts file, clip cut-downs per aspect ratio cut with
  ffmpeg and checked with ffprobe, hand-off for publishing only after GO. Use
  for "social pack for the release", "posts and clips for this launch",
  "announce the release".
category: media-eventtech
kind: playbook
trigger: ["social pack for the release", "posts and clips for this launch", "announce the release"]
inputs: [recap, platforms, "launch_video?", "formats?"]
requires:
  skills: [copywriting, quick-recap, pb-ship, pb-launch-video, "ffmpeg (external)", "ffprobe (external)"]
  agents: []
  mcps: []
  store: [content-engine]
go_points: [publish]
outputs: ["social/<slug>/facts.md", "social/<slug>/posts.md", "social/<slug>/clips/", "social/<slug>/publish.md", "production_artifacts/pb-social-pack-<date>.md"]
verify: "every post claim cites facts.md; ffprobe shows the asked WxH per clip"
difficulty: intermediate
est_time: 30-60 min
---

# Release social pack
Part of pb-content-studio (step f: social pack).
What you get: posts per platform and clip cut-downs from your release recap, every claim traceable to a fact, handed off for publishing after your GO.

## Inputs
- recap — release notes, or a pb-ship / pb-release-aos run log
- platforms — for example LinkedIn, X, Instagram, YouTube Shorts
- launch_video (optional) — an mp4 from pb-launch-video; without it the pack is posts only and step 4 is skipped; pb-launch-video renders with hyperframes when installed, else with the remotion skill
- formats (optional) — default 9:16 (1080x1920), 1:1 (1080x1080) and 16:9 (1920x1080)

## Steps
1. Preflight — `test -d ~/.claude/skills/content-engine`; absent → log "content-engine not installed: copywriting fallback" and continue. With launch_video: `command -v ffmpeg` and `command -v ffprobe`; either missing → stop with "Missing tool: <name>. Install ffmpeg and rerun." and write nothing except the run log — probes answered
2. Ask — recap path, platforms, slug, launch_video, formats → run log — all answered, recap file exists
3. quick-recap — recap → `social/<slug>/facts.md`, one numbered fact per line with its source line in the recap; no fact without a source — file written
4. content-engine (if present) or copywriting — facts.md → `social/<slug>/posts.md` per platform, each claim tagged `[F<n>]` — every claim has a tag that exists in facts.md — stops for approval
5. ffmpeg — launch_video → `social/<slug>/clips/<name>_<WxH>.mp4` per format and per requested cut, for example `ffmpeg -ss <start> -t <seconds> -i <video> -vf "scale=<W>:<H>:force_original_aspect_ratio=increase,crop=<W>:<H>" -c:a copy <out>`, then `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 <out>` — ffprobe equals the asked WxH for every clip; on a mismatch stop with "clip <file> has WxH, expected ...", do not publish
6. [GO] publish — platforms, post texts and the full clip list shown. The run stops here until the human types GO. No publish MCP exists, so the GO releases the hand-off: posts, clips and captions in `social/<slug>/publish.md`; upload is manual unless the human named a tool in step 2 — hand-off file written

Run log: `production_artifacts/pb-social-pack-<date>.md` in the start directory, never committed

## Optional silence-cut step: auto-editor

- **auto-editor** (https://github.com/WyattBlue/auto-editor) cuts silent sections from a clip automatically — useful before scale/crop when the launch video is a talking-head recording.
- **Preflight probe:** `auto-editor --version`. If the binary is missing or errors, log "auto-editor not installed: silence-cut skipped" and continue — the step never fails the run.
- **Usage when present:** `auto-editor <launch_video> -o <out.mp4>` before the ffmpeg cut-downs in step 5; the cut-downs then take the silence-cut file as input.
- Installing auto-editor (`pip install auto-editor`) is a manual opt-in step for the user — never pip-install it as part of this playbook.

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
