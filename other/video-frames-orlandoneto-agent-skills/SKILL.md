---
name: video-frames
description: >-
  Extract, sample, and annotate key frames for review, QC, and storyboarding. Use when the user asks for video frames, video, frames, or related AI video production workflows.
license: MIT
---

# Video Frames

## Goal

Extract, sample, and annotate key frames for review, QC, and storyboarding.

## Inputs

- Creative brief, script, or reference links
- Target aspect ratio, duration, and platform
- Brand assets / voice notes when available
- API keys only when the user provides them (never invent credentials)

## Instructions

1. Clarify the deliverable (length, format, platform, style) before generating.
2. Prefer official APIs, exports, and documented CLIs over scraping or invented results.
3. Draft a short shot list or edit plan the user can approve.
4. Execute with the user's tools/keys; pause before paid API calls when cost is non-trivial.
5. QC: check framing, audio sync, captions, and claim accuracy before final export notes.

## Output

Production plan + prompts/commands + QC checklist (and file paths when generated locally).

## Rules

- Do not invent API results, render outputs, rankings, or metrics you cannot see.
- Prefer official APIs/exports; document exact commands and providers used.
- Paid APIs (HeyGen, Veo, Runway, ElevenLabs, fal.ai, etc.) require the user's own keys and explicit OK before spend.
- No illegal deepfake or impersonation of real people without clear consent; disclose synthetic presenters.
- Respect copyright, platform ToS, and privacy; do not strip watermarks from content the user does not own.
