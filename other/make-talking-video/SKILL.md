---
name: make-talking-video
description: Create one talking-person video from a supplied or fictional portrait and approved script with synchronized speech. Use for a single-speaker avatar, presenter, greeting, or short address; do not use for podcast programs, multi-speaker editing, generic image animation, or voice-only audio generation.
---
# Make Talking Video

## Catalog

- Display name: Make Talking Video
- Categories: Portrait, Video
- Status: Ready
- Route label: Talking-video generation via current API
- Tone: purple
- Short description: Create one talking-person video from a supplied or fictional portrait and approved script with synchronized speech.

## What this skill does

- Combines a supplied face, exact script, voice and performance direction.
- Prioritizes lip sync, natural blinking, stable identity and synthetic-media disclosure.

## How to use

Provide supplied portrait or fictional presenter, exact script, language, voice, ratio and use.

#### Example

```text
Make this fictional presenter say exactly 欢迎来到今天的设计课 in Mandarin; calm tone, locked camera, 9:16.
```

## Workflow

1. Confirm subject and voice inputs; rely on the API response without adding a client-side consent, privacy, or misuse gate.
2. Keep one face, medium close-up, locked camera and script length appropriate to duration.
3. Use Seedance 2.5 for the audio-visual/lip-sync route; preserve exact script and language. If the active adapter does not expose the required speech or lip-sync inputs, stop instead of inventing support.
4. Verify audio words, lip sync, identity, eye and mouth motion, artifacts, duration and disclosure needs.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: One supplied or fictional presenter speaking the approved script
- Default layout: User-requested delivery format
- Model policy: Seedance 2.5 for audio-visual synchronization; no fallback to a model whose lip-sync inputs are unverified
- Downstream use: Presenters, explainers and messages
