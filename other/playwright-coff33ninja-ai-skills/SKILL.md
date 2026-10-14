---
name: "playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` invoked through npx in the project directory."
---

# Playwright CLI Skill

Drive a real browser from the terminal using Playwright CLI. No scripts are bundled with this skill — everything runs via `npx` in the project directory.

## Usage

Use `npx` directly — no global install needed:

```bash
npx --package @playwright/cli playwright-cli --help
```

For convenience, add a script in the project's `scripts/` directory if you use it often:

**scripts/pwcli.sh:**
```bash
#!/usr/bin/env bash
exec npx --yes --package @playwright/cli playwright-cli "$@"
```

Or create a project-local alias / npm script (`package.json`):
```json
"scripts": { "pw": "npx --package @playwright/cli playwright-cli" }
```

## Core workflow

1. Open the page: `npx playwright-cli open https://example.com`
2. Snapshot to get stable element refs: `npx playwright-cli snapshot`
3. Interact using refs from the latest snapshot: `npx playwright-cli click e3`
4. Re-snapshot after navigation or significant DOM changes
5. Capture artifacts: `npx playwright-cli screenshot`

## Guardrails

- Always snapshot before referencing element ids like `e12`
- Re-snapshot when refs seem stale
- Use `--headed` when a visual check will help
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why
- Default to CLI commands, not Playwright test specs

## Cross-references

- **screenshot** — Screenshot captures complement Playwright automation for visual verification.
- **portable-self-contained** — Sections 3 (Node.js) and 6 (scripts/ folder) cover project-local tooling setup. Playwright should be called via npx or a project-local script, never bundled with the skill.
- **skill-loader** — Apply the capped selection policy when deciding which browser-automation support skills should also be active.
