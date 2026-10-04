---
name: living-codex-browser-builder
description: "Build and evolve an AI-native browser stack (Living Codex Browser / AetherBrowse) using existing SCBE infrastructure. Use when implementing browser architecture, headless research lanes, UI panels, agent routing, or browser reliability/performance upgrades across Electron, Playwright, and runtime APIs."
---

# Living Codex Browser Builder

## Overview

Execute browser development as a lifecycle, not ad hoc patches.
Prefer upgrading existing AetherBrowse systems over rebuilding from scratch.

## Default Architecture

Use **Infestation mode** by default:
- Keep Electron shell as primary product container.
- Keep FastAPI runtime as control plane.
- Keep Playwright worker as browser execution engine.
- Add headless research as a dedicated lane, not mixed with user-facing coding panels.

Only switch to alternate architecture if there is a hard blocker:
- Hive Mind mode (extension-first): use when shell work is minimal.
- Chrysalis mode (web app + browser split): use when strict isolation is required.

## Development Flow

Use this exact loop for every browser feature:

1. Plan
- Define feature goal, constraints, affected modules, and acceptance tests.

2. Architect
- Choose integration points across:
  - `aetherbrowse/electron/*`
  - `aetherbrowse/runtime/*`
  - `aetherbrowse/worker/*`
  - `src/api/*` when API surface changes are needed.

3. Evaluate
- Verify design for:
  - governance boundaries
  - headless vs visible path separation
  - performance and failure blast radius.

4. Implement
- Ship smallest useful slice.
- Keep patches scoped and reversible.

5. Test
- Run module compile/lint/unit/smoke checks.
- Run one real navigation task.

6. Fix
- Patch only verified failure points.

7. Test
- Re-run failed checks and smoke path.

8. Improve
- Optimize routing, reliability, or UX after stability.

9. Test
- Confirm no regressions after improvements.

10. Fix or Launch
- If risk remains: fix and loop.
- If green: launch.

11. Launch
- Publish release notes with changed files and verification results.

## Browser Lane Rules

Use dual browser engines intentionally:

- `playwriter`: preferred for signed-in existing-tab flows.
- `playwright`: preferred for isolated automation and deterministic headless runs.

Always route tasks first:
- `python scripts/system/browser_chain_dispatcher.py --domain <domain> --task <task> --engine playwriter|playwright`

## Definition of Done

- Feature works end-to-end in one real browser path.
- Logs are written to artifact lanes.
- Tests/smokes pass.
- No unrelated files are touched.
- Final output includes what changed, how verified, and next launch action.

## Output Contract

Return:
- `files_changed`
- `verification_run`
- `known_risks`
- `launch_state` (`hold` or `go`)
