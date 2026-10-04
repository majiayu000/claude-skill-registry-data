---
name: profit-autopilot
description: Run a fact-checked monetization pipeline that upgrades the landing page, builds Shopify launch assets, validates storefront/admin state, and optionally publishes products live with evidence reports. Use when the user asks for money progress, product launch automation, website-to-store pipelines, or end-to-end sell-from-terminal execution.
---

# Profit Autopilot

## Overview
Use this skill when the goal is measurable monetization progress from terminal, not brainstorming. It enforces a fact gate first, then runs launch automation, then outputs artifact reports with blockers.

## When To Trigger
Trigger this skill when requests include:
- "make money", "ship products", "post to Shopify", "launch offers"
- "automate full flow" from website to checkout delivery
- "progress now" where the expected output is a run report and concrete next action

Do not use this skill for pure narrative writing or non-monetization coding.

## Workflow
1. Run fact gate before live publish:
   - Required files exist (`product-landing.html`, `scripts/system/shopify_store_launch_pack.py`, `scripts/shopify_bridge.py`).
   - Landing page contains conversion sections and store links.
2. Run launch pack:
   - Generate product media + scoring report.
   - Run Shopify both-side smoke test (admin + storefront status).
3. Optional live publish:
   - Only when tokens are available and user wants live sync.
4. Emit evidence:
   - Save JSON + markdown report under `artifacts/profit-autopilot/<timestamp>/`.
   - Surface blockers explicitly (for example missing token, storefront password gate).

## Commands
From repo root:

```powershell
pwsh -ExecutionPolicy Bypass -File scripts/system/run_profit_autopilot.ps1
```

Live publish attempt:

```powershell
pwsh -ExecutionPolicy Bypass -File scripts/system/run_profit_autopilot.ps1 -PublishLive
```

Direct Python mode:

```powershell
python scripts/system/profit_autopilot.py --publish-live
```

## Resource Usage
- Script runner: `scripts/run_profit_autopilot.ps1`
- Repo pipeline: `C:/Users/issda/SCBE-AETHERMOORE/scripts/system/profit_autopilot.py`
- Launch pack dependency: `C:/Users/issda/SCBE-AETHERMOORE/scripts/system/shopify_store_launch_pack.py`

## Execution Rules
- Prefer dry-run/fact gate first when environment is uncertain.
- Never claim publish success without reading generated report JSON.
- If live sync fails, return exact blocker and the one command needed next.
- Keep runs deterministic and artifact-backed.
