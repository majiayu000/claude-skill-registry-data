---
name: claude-video-parser
description: Use when the user has a screen recording, screen capture, Loom, .mp4/.mov/.webm/.mkv/.gif, or CI test video of a UI flow that is broken, and wants it turned into a written bug report. Triggers on "QA sent me a video", "here's a recording of the bug", "watch this screen capture", "a customer sent a screen recording", "turn this video into a ticket", "what breaks in this recording". Do NOT use when the app is running locally and reproducible — drive the browser directly instead.
license: MIT
---

# Flow Recording → Bug Report

Turn a screen recording of a broken UI flow into a structured, evidence-bounded bug report.

## When NOT to use this

Say so and stop, rather than proceeding, if any of these hold:

- **The user can reproduce the bug locally.** A browser automation tool (Playwright MCP, Chrome DevTools MCP, Puppeteer) beats a recording on every axis: it sees the DOM, console, and network, and it can retry. A video is pixels. Recommend that instead.
- **A Playwright/Cypress trace exists.** `trace.zip`, `.har`, or a Cypress `screenshots/` + `videos/` pair ships with structured data. Read the trace. The video is the fallback, not the primary.
- **The recording is longer than ~10 minutes** and the user has not said where in it the bug occurs. Ask for a timestamp range first. Analysing 10 minutes of pixels to find a 4-second bug is waste.

Being upfront about this is more useful than producing a mediocre report from a bad input.

## Workflow

### 1. Locate the video and confirm scope

Confirm the file exists and get its duration before anything else:

```bash
ffprobe -v error -show_entries format=duration:stream=width,height -of default=nw=1 <video>
```

The extractor also accepts a **direct http(s) video URL** (a link that serves the actual
`.mp4`/`.webm` file) — it downloads to a temp file first and records the `source_url` in
the manifest. Player-page links (YouTube, Loom share, Google Drive, Vimeo) are rejected
with guidance: ask the user for the site's direct-download link instead. For a URL, skip
the ffprobe pre-check and pass the URL straight to the extractor.

The extractor also checks for richer sibling artifacts (a `trace.zip`, any `.har`, a
Cypress `screenshots/` directory beside the video) and reports them in its output and in
the manifest's `richer_artifacts` field. **If any are found, stop and tell the user** — a
trace carries the DOM, network, and console this recording cannot show; the video is the
fallback, not the primary.

If the user has not said what *should* have happened, ask now — one question. A bug report without an expected-behaviour statement is a description, not a report. If they are unavailable, proceed and mark the expected behaviour as `NOT PROVIDED` in the output.

### 2. Extract keyframes

```bash
python3 scripts/extract_keyframes.py <video> -o <outdir>
```

This writes `<outdir>/` containing `frame-NN.jpg`, `contact-sheet.jpg`, and `manifest.json`.
Stdlib Python + ffmpeg only. No API keys, no model downloads, no MCP server.

Useful flags:

| Flag | When to reach for it |
|---|---|
| `--max-frames N` | Default 14. Raise for a long multi-page flow, lower for a 10s clip. |
| `--threshold X` | Default `0.0015`. Raise to `0.01` if a noisy recording (video content, animated background) yields junk frames. Lower to `0.0005` if a genuinely subtle change was missed. |
| `--min-gap S` | Default 0.5s. Raise to 1.5 if one long animation dominates the selection. |
| `--long-edge N` | Default 1024 (~800 visual tokens/frame). Raise to 1568 only when on-screen text is unreadable. |
| `--no-cursor` | Skip cursor/click estimation (see below) if it misbehaves on an exotic recording. |
| `--cursor-window S` | Default 1.5s of pre-transition motion inspected for the pointer. |
| `--no-ocr` | Skip the OCR pass. It only runs when `tesseract` is on PATH anyway. |
| `--ocr-lang L` | Tesseract language(s), default `eng`. Use e.g. `eng+deu` for mixed UIs. |
| `--roi X,Y,W,H` | Score scene changes on this region only (frames still extracted full-size). The fix for recordings where a video player / canvas / animated background floods selection — when the extractor detects that, it prints the exact `--roi` to retry with. Validated: 76 candidates → 2, with the real UI change scored cleanly. |

**Cursor / click estimation.** For each scene-change frame the extractor also inspects the
seconds *before* the transition at low resolution: a moving pointer is a small compact blob
of inter-frame change, and the UI reacts where the motion stopped. When the evidence is
good enough, the frame's manifest entry carries
`"cursor": {"x", "y", "norm_x", "norm_y", "detected_at_t", "confidence"}` — the estimated
pointer position in source-video pixels just before that transition, i.e. *where the user
most likely clicked*. `"cursor": null` means **no reliable estimate** (keyboard-driven or
app-driven transition, pointer already resting on the target, no visible pointer) — it does
not mean no click happened. Spinners, blinking carets and typing are recognised and never
reported as a pointer. This is inferred, not observed: cite it as `[INFERRED]`, never as
fact (validated on real recordings: located clicks land within ~1–50px; wrong claims were
eliminated in favour of abstention).

**Why these defaults matter.** ffmpeg's conventional scene threshold is `0.3`, tuned for film cuts. Measured UI transitions in screen recordings score **0.002–0.05** — a toast appearing changes maybe 4% of the frame. At `0.3` a screen recording returns zero scene changes, which is why most video tooling gives up and samples at a fixed fps instead. This script seeds low and then applies temporal non-maximum suppression, so a 400ms spinner animation contributes one frame rather than twelve.

**OCR pass.** When `tesseract` is on PATH, each frame's manifest entry also carries
`ocr_text` — machine-read text from that frame (frames are upscaled 2x first; this is what
makes 14px error banners readable). Grep it for error strings *before* viewing any frame:
an exact error string found in `ocr_text` tells you which single frame to view. OCR output
can contain recognition errors — before quoting a string as `[OBSERVED]`, confirm it
against the frame itself; low-contrast colored-on-colored text (a red toast on a dark red
card) may be missed entirely, so absence of `ocr_text` never means absence of text. When
tesseract is absent, `ocr_text` is null everywhere and the workflow is unchanged.

### 3. Read the contact sheet FIRST

Before that, if OCR ran, skim the manifest's `ocr_text` fields — an error string there
points you at the exact frame and costs zero visual tokens.

View `contact-sheet.jpg` before any individual frame. It is one image (~1–1.5k visual tokens) showing every keyframe with its index and timestamp. For most bugs it is sufficient on its own.

Only then pull individual full-resolution frames, and only the ones you need — typically the frame before the divergence and the frame after it. Do not view all frames by default. Read `manifest.json` for exact timestamps and per-frame token cost.

If text in the contact sheet is unreadable, re-run with `--long-edge 1568 --sheet-tile 640` rather than opening every frame.

### 4. Write the report

Use `references/report-template.md` verbatim as the structure. Fill every section; write `Not determinable from video` rather than deleting a section — the absences are diagnostic.

Before writing, read `references/evidence-rules.md`. It is short and it is the part of this skill that matters most. A confident, wrong bug report costs a developer more time than no bug report.

### 5. Deliver

Write the report to `<outdir>/BUG-REPORT.md` and hand the user:

- the report path,
- the contact sheet path,
- the frame indices that carry the evidence.

Offer, in one line, to file it as a GitHub issue via `gh issue create` — do not do it unprompted.

## Composition

If the `claude-video-vision` MCP server is available in the session, prefer its
`video_analyze` / `video_detail` tools for **drill-down into a specific moment** — it has
per-segment variable-fps extraction and audio transcription, which this skill deliberately
does not. Use this skill's extractor for the initial pass and its report contract for the
output. The two are complementary: that plugin is a perception layer, this is a reporting
contract.
