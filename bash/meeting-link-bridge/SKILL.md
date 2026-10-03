---
name: meeting-link-bridge
description: Build or operate a macOS menu-bar bridge that turns the current meeting join link into a clean handoff for notes, chat, email, or a fast open action, with extra weight for Microsoft Teams and browser-based meeting flows.
---

# Meeting Link Bridge

Use this skill when the user wants a Mac menu-bar utility for taking the current meeting join link and handing it off cleanly without hunting through tabs, copied URLs, or half-written notes.

## Core Workflow

- Read the visible meeting link from the front supported browser tab, the clipboard, or an explicit pasted URL.
- Detect Microsoft Teams links first, while also supporting common Zoom, Google Meet, and Webex join URLs when they are already in the handoff path.
- Normalize the output into one compact meeting card with provider, title, join URL, and a ready-to-paste format for notes, chat, or email.
- Keep the interaction short: one primary copy or open action, plus one clear fallback format.
- Treat this as a pre-meeting bridge, not a calendar client or meeting intelligence system.

## Local Helper

Use `scripts/meeting_link_bridge.py` when a deterministic local read is useful:

```bash
python skills/meeting-link-bridge/scripts/meeting_link_bridge.py current --format json
python skills/meeting-link-bridge/scripts/meeting_link_bridge.py current --format note --copy
python skills/meeting-link-bridge/scripts/meeting_link_bridge.py clipboard --format email
python skills/meeting-link-bridge/scripts/meeting_link_bridge.py parse "https://teams.microsoft.com/l/meetup-join/..." --format markdown
python skills/meeting-link-bridge/scripts/meeting_link_bridge.py open "https://teams.microsoft.com/l/meetup-join/..."
```

The helper uses macOS `osascript`, `pbpaste`, `pbcopy`, and `open`. It reads only visible browser-tab metadata or text the user already copied or pasted. It does not call Microsoft 365, Outlook, Teams cloud APIs, or calendar services.

Supported front-browser reads:

- Safari
- Google Chrome
- Brave Browser
- Arc
- Microsoft Edge

## Guardrails

- Do not claim Outlook or Teams calendar sync, attendee lists, chat history, recordings, or transcript access.
- If the front tab is not a supported meeting URL, say so plainly and ask for a meeting tab or direct join link instead of guessing.
- Keep copied output short and destination-ready. Do not turn this into a full CRM or calendar sidebar.
- Treat clipboard and browser data as transient; do not persist join links unless the user explicitly asks for that behavior.

## Prototype

The SwiftUI starter in `prototype/` sketches a compact menu-bar shell with provider status, handoff formats, and one open-or-copy path. Use it as the top-level menu-bar layer for a real macOS target.
