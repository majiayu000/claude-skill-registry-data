---
name: tester
description: Run end-to-end web quality audits with Playwright and Lighthouse using existing project scripts first. Use when the user says /tester, e2e test, smoke test, Playwright audit, Lighthouse audit, performance audit, accessibility audit, dark mode audit, mobile audit, or asks for 100/100 Lighthouse improvement guidance.
---

# E2E Playwright + Lighthouse Tester

Use this skill to run reproducible e2e and Lighthouse checks across a target web repo, with discovery-first command selection and clear reporting.

## Workflow

1. **Discover first**
   - Run:
     - `python3 .cursor/skills/tester/scripts/discover_audit_targets.py .`
     - Optional JSON output: `python3 .cursor/skills/tester/scripts/discover_audit_targets.py . --json`
   - Read discovered package scripts, runner files, and PWA signals before deciding what to run.

2. **Runner selection priority**
   - Prefer existing `npm` / `pnpm` / `yarn` scripts that already run Playwright and Lighthouse.
   - Otherwise use checked-in runner files in common locations (`perf/`, `scripts/`, `e2e/`, `tests/`).
   - Only use ad-hoc `npx playwright` / `npx lighthouse` commands if no native runner exists.

3. **Execution matrix**
   - For Lighthouse, target all slices when technically possible:
     - `light-desktop`
     - `light-mobile`
     - `dark-desktop`
     - `dark-mobile`
   - Attempt categories:
     - `performance`
     - `accessibility`
     - `best-practices`
     - `seo`
     - `pwa` (when supported by installed Lighthouse and app signals)
   - Prefer preview or production-like mode instead of noisy local dev mode when the repo supports it.

4. **100/100 objective**
   - Always optimize toward 100/100 in Lighthouse categories and Web Vitals-related audits.
   - Do not claim false success; explicitly list blockers and remaining deltas to 100.

## Reporting contract

Always report by package/surface:

- Commands run, including whether native or adapted.
- Playwright findings: failing flows, flaky clues, console/page errors, failed requests, auth blockers.
- Lighthouse findings per matrix slice (`light-desktop`, `light-mobile`, `dark-desktop`, `dark-mobile`).
- A dedicated **100/100 gap analysis** section with highest impact opportunities.
- Explicit coverage gaps (skipped routes, no dark mode, no mobile emulation, missing credentials, unsupported PWA category).

## Guardrails

- Keep commands non-interactive whenever possible.
- Never silently skip a matrix slice; report why it was skipped.
- If the repository is not a web app, stop quickly and state that no web target was detected.
