---
name: ztx3-visual-qa
description: "Visual QA & Self-Correction — select, implement, audit and test visual qa for production Codex frontend work, with responsive and accessibility checks."
---

# Visual QA & Self-Correction

Run production build, unit tests and visual browser matrices. Gate screenshot comparisons on fonts loaded and animations settled. Test RTL/LTR, 320px/400% zoom, safe areas, reduced motion, 3D fallback and realistic flow. Iterate from measured issues with minimal diffs and maintain a change log. Clearly separate executed tests from recommended tests.

## Workflow

1. Record explicit project requirements, business goal, content and accepted test budget.
2. Read `references/HANDBOOK.md` and pick precise technique Skill files, not the entire catalog.
3. Implement smallest meaningful working baseline, then add incremental enhancements.
4. Measure or inspect result with real devices and produce fallback.
5. Report verified/untested results. No MCP, no destructive overwrites.

## Core obligations

Build deterministic test fixtures with reduced animation, local fonts and stable mock data; run browser matrix.

Collect screenshots, errors and keyboard flow logs; rerun after each targeted fix.

## References

- `references/HANDBOOK.md` — full architecture and 10 deep techniques.
- Refer to `ztx3-<technique>` Skill for focused implementation and acceptance.
