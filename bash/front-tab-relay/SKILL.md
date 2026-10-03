---
name: front-tab-relay
description: Build or operate a macOS menu-bar relay that captures the front browser tab and formats it for prompts, notes, tickets, or chat handoffs.
---

# Front Tab Relay

Use this skill when the user wants a Mac menu-bar utility for taking the current browser tab and handing it off somewhere else without copying and cleaning it manually.

## Core Workflow

- Read the frontmost supported browser and capture the visible tab title and URL.
- Show one compact relay card with the browser, domain, and output presets.
- Prefer one-tap formats that are already useful in the next destination: markdown, prompt context, ticket bullet, or plain text.
- Keep the interaction short enough to feel like a real top-bar utility instead of a browser replacement.
- Treat the relay as a handoff step, not a history tool or a tab manager.

## Local Helper

Use `scripts/front_tab_relay.py` when a deterministic local read is useful:

```bash
python skills/front-tab-relay/scripts/front_tab_relay.py current --format json
python skills/front-tab-relay/scripts/front_tab_relay.py current --format markdown
python skills/front-tab-relay/scripts/front_tab_relay.py copy --format prompt
```

The helper uses macOS `osascript` and supports Safari, Google Chrome, Brave Browser, Arc, and Microsoft Edge. It reads only the front visible tab of the chosen browser and does not use network access.

## Guardrails

- Do not claim full browser history, hidden tabs, or page contents; this skill is about the visible active tab metadata only.
- If macOS automation permission is blocked, explain the permission path instead of inventing browser state.
- If the frontmost app is unsupported, ask for a supported browser or a direct URL instead of guessing.
- Keep the relay formats short and destination-ready; do not turn this into a large bookmark manager.

## Prototype

The SwiftUI starter in `prototype/` sketches a small status-item shell: current tab card, output presets, recent relays, and one primary copy action. Use it as the top-level menu-bar layer for a real macOS target.
