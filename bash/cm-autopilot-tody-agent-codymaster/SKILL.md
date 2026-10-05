---
name: cm-autopilot
description: Easy-to-use conversational CLI (Claude Code style) for non-technical users to spawn parallel AI tasks supervised by a visual web dashboard.
---

# CM AutoPilot CLI — Conversational Task Supervisor

> **Just talk to it. It plans, splits, and watches parallel tasks for you.**

## What it does
- Provides a conversational CLI interface using `rich` and `prompt_toolkit`.
- Translates user intent into multiple parallel tasks.
- Integrates with `cm-content-factory`'s Dashboard (`localhost:5050`) for a visual way to track multi-threading.
- Allows non-technical users to utilize the Cody Master skill set effortlessly.

## Requirements
- Python 3.9+
- `rich`
- `prompt_toolkit`

## How to run

1. Launch the conversational CLI:
   ```bash
   python3 skills/cm-autopilot/scripts/autopilot.py
   ```
2. The CLI will ask what you want to do. Explain your complex request (e.g., "Dịch 10 bài báo sang tiếng anh", "Research 5 competitors").
3. The AutoPilot will generate tasks and push them into the Queue.
4. AutoPilot will automatically start the visual Dashboard at `http://localhost:5050` so you can watch your jobs execute in parallel.
