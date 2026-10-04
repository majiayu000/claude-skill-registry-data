---
name: playwright-mobile-device-lane
description: >-
  Use when adding or extending real mobile-device coverage to a Playwright suite — touch/tap specs,
  Pixel or iPhone device descriptors, `isMobile`/`hasTouch` contexts, device-pixel-ratio visual
  baselines — or when mobile specs re-run under every desktop project, snapshot directories fill
  with duplicate per-project baselines, or `locator.tap()` throws because the context has no touch.
---

# Playwright mobile device lane

## Profile keys consumed

- `make.test_e2e`
- `make.test_visual`
- `make.start_prod`
- `capabilities.visual_testing`

Every suite invocation goes through the profile's `make` target map. Skip the dependent step with a
recorded note when `make.test_e2e`, `make.test_visual`, or `make.start_prod` maps to `null`, and
record the visual half SKIPPED when `capabilities.visual_testing` is `false`.

## Overview

Shrinking a desktop window is not mobile coverage: the context still reports `isMobile: false`,
`hasTouch: false`, DPR 1 and a desktop user agent. Real coverage means extra Playwright projects
built from stock device descriptors, scoped **in both directions** so mobile specs run only on
mobile projects and desktop projects never collect them.

## When to use

- Adding touch interactions, tap flows, or a mobile viewport lane to an existing suite.
- `locator.tap()` fails with a "hasTouch" error on a desktop project.
- A visual run suddenly wants baselines named for projects that should never have run the spec.
- Mobile visual diffs look soft or miss asset regressions (CSS-downsampled captures).
- Not for: responsive layout assertions that only need a viewport size — those stay desktop specs.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `mobile-chrome` (Pixel 7, chromium) and `mobile-safari` (iPhone 14, webkit), specs
  in `tests/e2e/mobile/` and `tests/visual/mobile/`, recorded by the repository's visual-baseline
  update target.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — one `mobile-chrome`
  (Pixel 7) project scoped by `testDir` (`src/test/e2e/mobile`) plus `testIgnore` on the desktop
  projects; no mobile visual lane.
- **Component-library shape** (Storybook-first, no bootable app, published package): no —
  Storybook-driven desktop-only visual suite.

## Core pattern

Scope every project, both ways. Take the descriptor whole — never hand-set `deviceScaleFactor`,
which desynchronises from the descriptor on upgrade.

```ts
const MOBILE_LANE = '**/mobile/**/*.spec.ts';
const DESKTOP_LANE_IGNORE = '**/mobile/**';

{ name: 'chromium', testIgnore: DESKTOP_LANE_IGNORE, use: { ...devices['Desktop Chrome'] } },
{ name: 'mobile-safari', testMatch: MOBILE_LANE, use: { ...devices['iPhone 14'] } },
```

Without `testIgnore`, every desktop project re-records the whole mobile screen set under its own
project name — a 13-screen suite crossed with three desktop projects is a few hundred unwanted
baselines. Without `testMatch`, the mobile projects re-record the desktop suite at 2.6x and 3x.
Playwright interpolates the project name into the snapshot path, so each omission multiplies
baselines rather than failing loudly.

Capture mobile visuals at the emulated ratio, never by resizing a desktop helper:

```ts
await expect(page).toHaveScreenshot(`${language}_${name}.png`, {
  fullPage: true,
  animations: 'disabled',
  scale: 'device',
});
```

## What a touch lane must assert

Cover what a resized desktop window cannot: sign-in and sign-up by `tap()` only, switcher
navigation, empty-form validation that fires no request, the password-visibility toggle, a
touch-target floor on the primary controls, no horizontal overflow, and submit reachability at a
keyboard-height viewport. Playwright cannot open a native on-screen keyboard, so that last one
shrinks the layout viewport as a proxy — name the spec for what it measures.

## Pin the lane with a unit test

Config scoping decays silently. Assert, from the config and lane files as text: both descriptors are
the stock ones, the lane globs exist, every desktop project carries `testIgnore`, every mobile
project carries `testMatch`, every lane spec contains `.tap()`, no lane file (helpers included)
contains `.click(`, the visual helper uses `scale: 'device'` and never `setViewportSize`, and the
snapshot directory holds exactly one baseline per page per mobile project.

## Gotchas

- Playwright rejects `isMobile` on Firefox, so a touch project must be Chromium- or WebKit-based.
- `page.route()` holding a request open makes `waitForLoadState('networkidle')` hang until timeout.
  Wait for `'load'` or for the specific `waitForResponse` instead.
- Auto-generated MUI field ids can break `getByLabelText`; locate by placeholder text, `aria-label`,
  or a stable `name` attribute.
- `eslint-plugin-testing-library` matches every `*.ts`, and `prefer-screen-queries` misreads the
  destructured Playwright `page` fixture as a render result. The fix is a scoped config entry
  turning off that one rule for the e2e and visual spec globs — never an inline directive.
- A runtime `test.skip(...)` device guard is redundant under project scoping and trips
  `playwright/no-skipped-test` (whose `allowConditional` default is `false`).
- The target mapped by `make.start_prod` reuses an already-running stack, so baselines can be
  recorded from stale code; use the clean prod-restart target before recording (React SPA and
  Next.js shapes).

  ```bash # profile-example
  make start-prod-clean
  make test-visual-update
  ```

- A recording run scoped to one lane refreshes only that lane, leaving the other's baselines stale.
  Re-record both in the same visual-baseline update run (React SPA and Next.js shapes).

## Cost of the lane

Measured in the React SPA shape on its production stack against the pinned Playwright image:

| Suite  | Before   | After     | Delta             |
| ------ | -------- | --------- | ----------------- |
| E2E    | 87 tests | 115 tests | +28 tests, ~+31 s |
| Visual | 240      | 244       | +4 tests, ~+17 s  |

## Common mistakes

- Adding mobile projects without `testIgnore` on the desktop ones — declare both globs as shared
  constants so the directions cannot drift.
- Hand-setting DPR or user agent instead of spreading the device descriptor.
- Recording mobile baselines with the desktop `setViewportSize` helper — give the lane its own
  helper that passes `scale: 'device'`.
- Enforcing a 44 CSS px touch floor on secondary controls whose height is a design decision; keep
  the floor on primary controls and file the rest as design work.
