---
name: "quality-performance"
description: "Speed, accessibility, and testing bars every delivered app must clear — Core Web Vitals, WCAG 2.2 AA, TDD real-browser E2E, and the build-fail gates."
triggers:
  - "performance"
  - "accessibility"
  - "a11y"
  - "test"
  - "quality"
priority: 2
pack: "testing"
stage: stable
---

# Quality & Performance — every app must clear these bars

## Core Web Vitals (per route)

- LCP ≤ 2.0s · CLS ≤ 0.05 · INP ≤ 100ms (cinematic target; ≤ 200ms hard ceiling). Per-route asset budget enforced.
- Lighthouse: Performance ≥ 75 · Accessibility ≥ 95, run in CI (Lighthouse CI).

## Accessibility (WCAG 2.2 AA)

- axe-core 0 violations at all 6 breakpoints (375 · 390 · 768 · 1024 · 1280 · 1920). ADA Title II ready.
- Everything keyboard-operable; visible focus; honors `prefers-reduced-motion`. (Contrast/target-size specifics live in `visual-experience`.)

## Testing (TDD-first, real flows)

- Failing Playwright E2E spec BEFORE implementation — watch RED → GREEN. Bug fix = failing regression test FIRST. No feature without ≥1 E2E; no fix without ≥1 regression.
- E2E runs against the PROD URL in a real browser: `goto('/')` then navigate by clicks/keyboard only (no `page.goto` after load). Deterministic (locator waits, no sleeps), parallel-safe, hermetic.
- Every clickable element · form field · nav link · API endpoint · modal · keyboard shortcut · error/empty/loading state has ≥1 E2E asserting it against prod.
- Coverage matrix: `fullyParallel` × 6 viewports × 3 browsers, sharded. Units via Vitest.
- Simulate realistic full user journeys (homepage → discover → convert) via **Cloudflare Browser Rendering or Browserbase** (whichever is configured). Drive HIGH % code coverage from these end-to-end journey runs, not just units.

## Build-fail gates (any one = fail)

- Console errors · CSP violations · 4xx/5xx · axe violations · broken hyperlinks — in ANY test — fail the build.
- AI-vision QA ≥ 8/10 on every new/changed route (random snapshot sampling per run). Visual regression via Percy / pixelmatch.

## Mocked ≠ green

- A mocked/stubbed render is NOT a pass. "Deploy succeeded" ≠ "works" — only a real-browser prod run with 0 console errors and asserted content counts as green.
