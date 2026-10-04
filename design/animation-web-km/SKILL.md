---
name: animation-web_KM
description: >-
  Make browser-rendered animation videos: HTML/CSS/JS scenes, captions, overlays, transitions, and social-video compositions.
metadata:
  hermes:
    command_priority: 88
    tags: ['animation', 'web-video', 'captions', 'html']
---
# Animation Web

Use this for video compositions made like a tiny designed webpage: title cards, captions, overlays, image/video layers, audio-reactive moments, scene transitions, UI walkthroughs, and exportable MP4s.

Prefer `media-creative__hyperframes` for the actual composition/render pipeline, `media-creative__hyperframes-cli` for commands, and `media-creative__gsap` for motion timing. The user should not need to remember those names; this command is the plain-English front door.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
