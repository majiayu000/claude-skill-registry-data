---
name: Create New Indicator
description: Use this skill when you need to add a new Python indicator to AERA.
---

# Create New Indicator (Python)

Use when adding a new indicator under the Strategy Lab `indicators/` workspace.

## Constraints (platform rules)

- Do NOT hardcode indicator id/name/kind in the frontend renderer.
- Keep the output generic via Plot API (v1 today).

## Steps

1) Create the script file
- Path: `server/indicators/<name>.py` (or subfolders under `server/indicators/`).
- Must export `calculate(inputs, settings=None)`.
- Optional: `initialize(ctx)` to declare Inputs UI (Manifest).

2) Produce Plot API v1 output (recommended)
- Return `{"plots": [...]}`.
- Prefer index-based coordinates (`index`, `from`/`to`) so the backend can align to candle `time`.
- Reference: `docs/public/plot-api-v1.md`.

3) No manual registration
- The backend scans `server/indicators/` automatically:
  - `server/src/services/indicatorFileService.js`
  - `server/src/indicatorRegistry/registry.js`
- The indicator id is the relative path including `.py` (example: `my_indicator.py` or `market_structure/pivots.py`).

4) Verify
- In the app: Strategy Lab -> save the file; Chart -> activate and run.
- Optional quick check: Debug -> terminal command `run indicator <id> --asset=CL1! --tf=M15 --len=1000`.
- Run standard validations: see `skills/verify_changes/SKILL.md`.

## Template

Start from `skills/create_new_indicator/template_indicator.py`.

