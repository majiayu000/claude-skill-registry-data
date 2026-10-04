---
name: aetherbrowser-notion-nav
description: "Navigate Notion workspace pages in AetherBrowser for knowledge retrieval and workspace coordination tasks. Use when locating pages, databases, or section paths in browser mode before API operations."
---

# AetherBrowser Notion Nav

## Workflow

1. Route the browser task.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain notion.so --task navigate --engine playwriter`

2. Open workspace target.
- Root: `https://www.notion.so`
- Known page: `https://www.notion.so/<slug-or-page-id>`

3. Confirm route and workspace identity.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title`

4. Snapshot for structure-aware follow-up.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot`

## Rules

- Use browser navigation for discovery; use Notion API for deterministic writes.
- Keep captured evidence concise and task-scoped.
- Re-route through fallback engine if extension session is unavailable.
