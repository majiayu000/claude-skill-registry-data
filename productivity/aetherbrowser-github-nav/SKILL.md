---
name: aetherbrowser-github-nav
description: "Navigate GitHub repositories, pull requests, issues, and settings through AetherBrowser tentacle routing. Use when tasks require browser-based GitHub movement, page evidence capture, or coordinated lane assignment with playwriter or playwright."
---

# AetherBrowser GitHub Nav

## Workflow

1. Route the task through the browser dispatcher.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain github.com --task navigate --engine playwriter`

2. Reuse active browser session (if extension connected).
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --url https://github.com --task navigate`

3. Move to target surface.
- Repo page: `https://github.com/<owner>/<repo>`
- PR page: `https://github.com/<owner>/<repo>/pull/<number>`
- Issues page: `https://github.com/<owner>/<repo>/issues`

4. Capture proof.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot`

## Rules

- Prefer `playwriter` for signed-in GitHub flows.
- If extension is disconnected, fallback to existing Playwright/AetherBrowse path.
- Log every assignment and execution via JSONL artifacts.

## GitLab note

When the task is actually on GitLab (not GitHub), prefer `aetherbrowser-operator` or a domain-routed browser chain (`--domain gitlab.com`) instead of forcing GitHub-specific assumptions.
