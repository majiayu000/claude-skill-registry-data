---
name: gsap-refactor
description: Orchestrate safe GSAP improvements for existing pages or components. Use when the page already exists and needs better animation quality, cleanup, performance fixes, accessibility hardening, or a more coherent motion system. Read current code and .gsap artifacts first, audit the current motion system, build a refactor plan, apply safe improvements, then update artifacts.
---

# GSAP Refactor

Use this workflow for existing pages/components that already have code and may already have motion.

## Sequence

1. Read `.gsap` artifacts first.
2. Read the actual implementation files.
3. Run internal discovery, audit, and scan helpers.
4. Detect framework, packages, routes, current motion libraries, and matched page files.
5. Identify what to preserve, remove, simplify, or improve.
6. Update `.gsap/audit-report.md`, `.gsap/animation-plan.md`, `.gsap/tasks/<page>.tasks.md`, and `.gsap/phases/<page>/*.md`.
7. Split the refactor into phased sections instead of sweeping the full page at once.
8. Apply safe changes to the active phase only unless the user asks for a broader pass.
9. Update page artifact statuses and notes.

## Internal Helper

Use:

```bash
python scripts/gsap_workflow.py gsap-refactor --path "<project>" --page "<page>"
```

This command should gather current workflow state, inspect the project structure, detect current motion systems, write audit/refactor notes, and prepare implementation state. It is the only public helper command for this mode.

## Refactor Rules

- preserve good motion when possible
- remove noisy or redundant effects
- add reduced-motion handling where missing
- reduce mobile-heavy patterns before adding more spectacle
- do not change the motion direction without updating `.gsap` artifacts

## Completion

Before finishing, ensure:

- `.gsap/audit-report.md` records major findings and fixes
- `.gsap/animation-plan.md` reflects the refactor priorities
- `.gsap/tasks/<page>.tasks.md` reflects the current queue and active phase
- `.gsap/phases/<page>/` reflects the refactor section breakdown
- `.gsap/pages/<page>.animation.md` reflects the final status
