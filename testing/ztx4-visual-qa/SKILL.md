---
name: ztx4-visual-qa
description: "Deep implementation master for Visual QA & Self-Correction with 18 targeted Codex skills, code, tests and no MCP. Additive to all existing Perfect_AI versions."
---

# Visual QA & Self-Correction

Close the loop between rendered UI evidence, detected defects and verified fixes.

## Mandatory sequence
1. Establish test fixtures, seeded content, font readiness, stable animation clock and expected baselines.
2. Run a viewport × theme × direction × motion × interaction matrix, including 320px and 400% zoom.
3. Detect overflow, clipped content, failing actions, console errors, accessibility violations and animation state drift.
4. Generate annotated diff reports and rank issues by user impact, not only pixel count.
5. Fix then rerun targeted + regression tests; record what was actually executed.

## Skill routing
Choose only technique files needed for this project from `DEEP-IMPLEMENTATION-v2/references/visual-qa.md`. Never indiscriminately load all 300+ skills into context.

## Runbook
Inputs: page URL/fixtures, responsive matrix, snapshots, deterministic font/time and expected functional assertions.

Implementation: Playwright screenshots and DOM checks, keyboard flows, console/network errors, pixel-diff triage and fix verification loop.

Tests: one failing regression intentionally detected, 8 viewports, reduced motion, RTL/LTR, JS errors, focus and no horizontal overflow.

## Acceptance gates
1. Both regression failures and successful controls are recorded with screenshots.
2. Test matrix includes 320/390/768/1440 and RTL/reduced motion.
3. Never describe skipped tests as passed.

## Runnable assets
`extensions/DEEP-IMPLEMENTATION-v2/examples` and `tools` (installed main package). See `RUNBOOK-FA.md`.

## Sources
- [playwright](https://playwright.dev/docs/test-snapshots)
- [wcag](https://www.w3.org/TR/WCAG22/)
