---
name: pb-launch-video
description: >-
  Turn a live app or landing page into a short launch video: composition
  brief, render in Hyperframes or Remotion, an ffprobe check per format,
  publish hand-off only after GO. Use for "launch video", "make a video of
  the shipped app", "promo clip for the landing page".
category: media-eventtech
kind: playbook
trigger: ["launch video", "video of the shipped app", "promo clip for the landing page"]
inputs: [url, project, length, formats, render_tool]
requires:
  skills: [brag, remotion, "hyperframes (external)", "ffprobe (external)"]
  agents: []
  mcps: []
  store: []
go_points: [publish]
outputs: ["renders/<project>/launch_<fmt>.mp4", "renders/<project>/publish.md", "production_artifacts/pb-launch-video-<date>.md"]
verify: "ffprobe shows the asked WxH and duration per file"
difficulty: intermediate
est_time: 30-90 min
---

# Launch video of a shipped app
What you get: a short launch video per format, checked with ffprobe, handed off for publishing after your GO.

## Inputs
- url — the live URL of the shipped app or landing page (for example from pb-landing-page)
- project — a slug for `renders/<project>/`
- length — target duration in seconds
- formats — for example 16:9 (1920x1080) and 9:16 (1080x1920)
- render_tool — `hyperframes` or `remotion` (remotion needs an existing Remotion project)

## Steps
1. Preflight — ask render_tool first; then `command -v ffprobe` and, for hyperframes, `test -f ~/.claude/skills/hyperframes/SKILL.md`. ffprobe missing → stop with "Missing tool: ffprobe. Install ffmpeg and rerun." Hyperframes missing → stop with "Missing skill: hyperframes (installed locally only, not shipped by AOS). Install it, or rerun with render_tool = remotion and the path of an existing Remotion project." Remotion chosen without an existing project → stop and ask for its path. Write nothing except the run log on a stop — all probes answered
2. Ask — url, project slug, length, formats, render_tool → run log and `renders/<project>/` — all answered; `curl -sI <url>` returns 200
3. brag — url → composition brief in `renders/<project>/brief.md` (scenes, copy lines, length, formats; brag's brief stage only, the render choice stays with render_tool) — stops for approval
4. Render — either way one file per format:
   - hyperframes: brag with hyperframes → `renders/<project>/launch_<fmt>.mp4`
   - remotion: from the Remotion project dir, `npx remotion render <Composition> <out>` per format (network/npm on first run needs approval)
5. ffprobe — per file: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration -of json <file>` → WxH and duration in the run log — equals the asked WxH, duration within 1 s of length; on a mismatch stop with "export <format> has WxH, expected ...", do not publish, invent no conversion command; then the clips stop for approval (taste review)
6. [GO] publish — destination and the full file list shown. The run stops here until the human types GO. No publish MCP or CLI exists on this machine, so the GO releases the hand-off: the files plus the caption in `renders/<project>/publish.md`; upload is manual unless the human named a tool in step 2 — hand-off file written

Run log: `production_artifacts/pb-launch-video-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
