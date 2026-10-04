---
name: visual-qa
description: Use when a website needs rendered screenshot review, Playwright visual regression, multi-viewport checks, horizontal overflow detection, console-error checks, focus/state inspection, or a repeatable visual QA evidence set.
metadata:
  short-description: Run screenshot, viewport and visual regression QA
---

# Visual QA

## Evidence first

Do not critique only source code. Render the real interface.

## Default sequence

1. ensure the target app runs;
2. settle the intended capture state: await fonts, promote/decode lazy media, and disable nondeterministic motion;
3. assert that critical content is visible before accepting a baseline, including in reduced-motion or JavaScript-failure states;
4. capture all configured viewports;
5. inspect full-page composition and first viewport separately;
6. test critical interactive states;
7. inspect keyboard focus and sticky/fixed overlays;
8. inspect utility/micro text at native screenshot scale—technically present text can still be functionally illegible;
9. test reduced-motion mode;
10. check horizontal overflow and console/page errors;
11. use Playwright visual baselines for stable views;
12. hand screenshots to `$design-critic` without implementation justification.

## Defect format

For each issue record:
- severity: blocker / major / moderate / minor;
- viewport/state;
- observed evidence;
- design/UX impact;
- likely root cause;
- recommended correction scope: system / section / component / micro.

## Stability

Visual baselines are environment-sensitive. Keep the comparison environment consistent and only update baselines after reviewing the diff. A passing pixel comparison is not evidence when its baseline recorded hidden critical content or media that had not finished decoding.

Use `scripts/capture-screenshots.mjs` and `tests/visual.spec.ts` as starters.
