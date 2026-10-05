---
name: mk:html-video
description: Render an HTML/CSS/JS template to a local MP4 video by capturing frames with headless Chromium (via Playwright) and encoding them with ffmpeg. Use when "render my animation as a video", "export HTML to MP4", "make a video from my web template", or "capture CSS animation as MP4". NOT for recording live browser interactions (use `agent-browser record start`); NOT for screen recording; NOT for AI video generation (use mk:multimodal).
keywords:
  - html-to-video
  - mp4-export
  - animation-render
  - css-animation
  - playwright-capture
  - ffmpeg-encode
  - frame-capture
  - html-canvas
when_to_use: Use to render a local HTML/CSS/JS file to an MP4 by capturing frames with Playwright and encoding with ffmpeg. NOT for live browser recording (agent-browser record) or AI video generation (mk:multimodal).
user-invocable: true
owner: utility
criticality: low
status: active
runtime: claude-code
requires_external_service: ["playwright", "ffmpeg"]
default_enabled: false
allowed-tools:
  - Bash
  - Read
  - Write
---

# HTML → MP4 Render Pipeline

Render a local HTML/CSS/JS animation to MP4 with Playwright frame capture and ffmpeg encoding.

## Route by Intent

- **Check dependencies or choose dimensions/fps:** load [render workflow](references/render-workflow.md).
- **Implement deterministic JavaScript, canvas, WebGL, or GSAP animation stepping:** load [template contract](references/html-template-contract.md).
- **Capture frames directly:** execute `node .claude/skills/html-video/scripts/capture-frames.mjs <html-file> <frame-dir> <fps> <duration-seconds> <width> <height> [background-color]`.
- **Render a complete MP4:** execute `bash .claude/skills/html-video/scripts/render-html-to-mp4.sh <html-file> <output.mp4> [fps] [duration-seconds] [width] [height] [background-color]`.
- **Resolve module, `file://`, codec, cleanup, or dimension failures:** load [troubleshooting](references/troubleshooting.md).

## Quick Start

```bash
bash .claude/skills/html-video/scripts/render-html-to-mp4.sh template.html output.mp4 30 5 1920 1080
```

The final optional argument supplies a background colour. The script captures `fps × duration` PNG frames, encodes H.264 MP4 with `yuv420p`, cleans its temporary frame directory, and prints the output path.

## Delivery

1. Verify `ffmpeg` and Playwright before rendering; install Chromium only when missing and only with user approval.
2. Use an even viewport width and height.
3. Prefer a `window.onFrame` hook for fast deterministic animation; otherwise capture runs at real time.
4. Verify the MP4 with the `ffprobe` command in [render workflow](references/render-workflow.md).

## Gotchas

- This is a skill, not an npm package: execute its bundled scripts directly.
- Do not use it for live browser recording, screen recording, or AI video generation.
- See [troubleshooting](references/troubleshooting.md) for cleanup and file-origin limitations.
