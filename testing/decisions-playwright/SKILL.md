---
name: decisions-playwright
description: Use Playwright inside DecisionsAI — Hermes playwright_browser tool, workflow playwright steps, and local Chromium from bin/setup.py.
---

# Decisions Playwright

DecisionsAI ships Playwright in its Python venv and installs Chromium during `bin/setup.py`.

## When to use

- Hermes workflow steps with `tool: playwright` or `playwright_browser`
- Ticket polish / ship loops that need screenshots or DOM checks
- Fallback when browser-use is unavailable

## Commands

```bash
# From Decisions venv (after bin/setup.py)
python -m playwright install chromium
```

## Workflow

1. Prefer the Hermes `playwright_browser` tool when the Decisions server is running.
2. For scripted checks, pair with ECC skills `browser-qa`, `webapp-testing`, or `e2e-testing`.
3. Attach screenshot paths or console excerpts in the workflow result packet.

## Related skills

- `browser-qa`, `webapp-testing`, `e2e-testing`
- `decisions-browser-stack` (full browser/content index)
