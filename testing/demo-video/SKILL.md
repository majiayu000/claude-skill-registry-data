---
name: demo-video
layer: stack
description: Record a WebM demo video of a UI flow with shot-scraper video — a YAML storyboard drives the browser (click, type, scroll, wait) with an animated cursor overlay, so a reviewer can watch the feature instead of driving it. Use to attach motion evidence to a UI sign-off (#307), to turn an issue's "How to test" steps into a watchable clip, or when asked to "record a demo", "make a video of this flow", "show me it working".
allowed-tools: Bash, Read, Write, Grep, Glob, SendUserFile
---

# Demo Video — storyboard-recorded WebM demos

Records a **watchable demo** of a UI flow using
[`shot-scraper video`](https://shot-scraper.datasette.io/en/stable/video.html)
(Simon Willison, Apache-2.0, Playwright-based): a declarative YAML storyboard
opens the app, clicks, types, scrolls and waits — with an injected **animated
cursor + click-ring overlay** so the recording reads like a human demo, not a
ghost session.

**What this is:** evidence capture — the motion analog of `scripts/app-shots.mjs`.
**What this is NOT:** assertion testing. The e2e harness (`/e2e-smoke`) remains
the correctness gate; Playwright's own `video: 'on'` test artifacts (#356) remain
the *test-run* recordings. This skill is for *narratable* demos a reviewer watches.

## When to use

- **UI sign-off (#307/#590)**: alongside the staging preview URL, attach a clip
  of the flow under review — richer than a PNG, cheaper than the reviewer
  driving it themselves.
- **`## 🧪 How to test`**: a storyboard is an executable version of those
  numbered steps; the video is the before/after evidence.
- **POC demos**: show a `pocs/*` feature working without deploying.
- On ask: "record a demo", "video of this flow", "show me it working".

## Setup (once per session)

```bash
bash scripts/demo-video-setup.sh
```

Idempotent. Installs `shot-scraper` via pip and makes sure Playwright's expected
chromium exists — downloading it where possible, or (in the egress-blocked web
harness) **symlink-shimming** the expected build dirs onto the pre-installed
`/opt/pw-browsers` browsers. Don't hand-roll the shim; don't conclude "no
browser" from a failed `playwright install` (see CLAUDE.md's headless-browser
note — same trap).

## Recording

1. Copy `example-storyboard.yml` (next to this file) and adapt it. The
   storyboard can boot the app itself via `server:` (e.g. `pnpm dev`), or point
   `url:` at an already-running server / local HTML file.
2. Output path: **`screenshots/<name>.webm`** — same HARD-GATE location rule as
   screenshots; `*.webm`/`*.mp4` are gitignored so recordings stay out of commits.
3. Run it:

```bash
shot-scraper video storyboard.yml            # → WebM
shot-scraper video storyboard.yml --mp4      # + MP4 (needs a real system ffmpeg)
```

### Storyboard essentials

```yaml
output: screenshots/feature-demo.webm
url: http://localhost:3000/        # or omit and use `open:` in the first scene
server: pnpm dev                   # optional: runs while recording, killed after
viewport: {width: 1280, height: 720}
cursor: true                       # the demo-polish switch — keep it on
wait_for: "text=Dashboard"         # recording starts AFTER this settles
scenes:
- name: Create a thing
  do:
  - click: "#new-thing"
  - type: {into: "input[name=title]", text: "Demo item", delay_ms: 40}
  - press: Enter
  - wait_for: "text=Demo item"     # doubles as a weak smoke assertion
  - screenshot: screenshots/feature-demo-result.png   # stills mid-recording
  - pause: 1
```

Actions: `click`, `type` (visible keystrokes) / `fill` (instant), `press`,
`scroll` (eased, or `to:` a selector), `pause`, `wait_for`, `wait_for_url`,
`open`, `js`, `screenshot`, `sh`, `python`. Full syntax: the `video.py` pydantic
models in the shot-scraper source, or `shot-scraper video --help`.

**Authed apps:** log in once with `shot-scraper auth <url> auth.json`, then
record with `shot-scraper video storyboard.yml -a auth.json`. Never commit
`auth.json`.

## Delivering the video

GitHub's API can't attach binary media to comments, so pick by context:

- **Interactive session** → send the `.webm` to the user directly (SendUserFile).
- **PR evidence** → upload as a CI artifact (like the #356 e2e reports) and link
  it from the PR comment; or drag-and-drop manually — a human gesture, not an
  agent one.
- WebM plays in every modern browser; only convert to MP4 (`--mp4`, needs
  system ffmpeg with libx264) when the audience needs QuickTime/Slack inline.

## Gotchas

- `type` vs `fill`: use `type` with `delay_ms: 25–50` for anything on camera —
  `fill` is instant and reads as a glitch.
- Recording starts *after* the top-level `wait`/`wait_for`, so open on a settled
  page; add a trailing `pause: 1` so the last state is visible.
- A failed `wait_for`/selector aborts the recording with a Playwright timeout —
  that's a feature (broken flow ⇒ no misleading demo), but keep storyboards
  short and re-runnable.
- `sh:`/`python:`/`server:` in a storyboard are arbitrary code execution — treat
  third-party storyboards like shell scripts.
- Videos are viewport-size at 25fps VP8; bigger viewports = bigger files. 1280×720
  is the sweet spot.
