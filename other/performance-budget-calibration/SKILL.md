---
name: performance-budget-calibration
description: >-
  Use when a byte budget is calibrated against the wrong unit and therefore cannot fire — setting or
  reviewing a Lighthouse `resource-summary` script or total size assertion, a gzip entrypoint or
  per-chunk ceiling, or a bundler size hint; a budget that has never failed while a real regression
  shipped; a bundler raw-byte hint and a Lighthouse assertion that disagree by a large factor; or a
  diff that edits budget numbers without a measured baseline.
---

# Performance budget calibration

## Profile keys consumed

- `make.build`
- `make.start_prod`
- `make.lighthouse_desktop`
- `make.lighthouse_mobile`
- `make.storybook_build`
- `quality.lighthouse_desktop`
- `quality.lighthouse_mobile`
- `capabilities.lighthouse`
- `capabilities.storybook`
- `framework.bundler`

Skip this skill with a recorded note when `capabilities.lighthouse` is `false`; skip any individual
step whose `make.*` key maps to `null`. The clean prod restart and the budget-enforcing target have
no logical key — invoke the repository's own targets for them.

## Overview

Lighthouse `resource-summary` and any budget read from a live server measure **transfer** bytes, and
the production server compresses. A budget calibrated against uncompressed build output is several
times the real number, so it can never fire — a gate that cannot fail is worse than no gate, because
it looks like coverage.

## When to use

- Setting a new script/total byte budget, or raising one that "keeps failing".
- A budget has never failed and a real regression shipped past it.
- Reconciling a bundler size hint with a Lighthouse assertion that disagrees by a large factor.
- Reviewing a change that edits budget numbers.
- Not for: category-score assertions (performance, accessibility) — those are not byte budgets, and
  they are governed by `quality.lighthouse_desktop` / `quality.lighthouse_mobile`.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — `config/performance-budget.json` is the single source for raw, gzip, and
  Lighthouse budgets; enforced by the `framework.bundler` size hints, `scripts/bundle-size-report.mjs`,
  and the repository's budget-enforcing target. See the repository's own quality documentation
  section on performance budgets, bundle reports, and route splitting.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — no central budget
  file; per-URL `scriptBytes` / `totalBytes` live in `lighthouserc.mobile.js` and
  `lighthouserc.desktop.js`. The production image also serves with `serve@14`, so the same
  compression rule applies.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  `lighthouserc.js` audits Storybook story iframes from the static Storybook build produced by
  `make.storybook_build`; there is no byte-budget file to calibrate.

## Raw versus transfer

Keep the two families separate and label them in the config:

- **Raw** budgets are uncompressed emitted bytes, enforced by the bundler's size hints at build
  time. They catch a chunk doubling regardless of how it is served.
- **Transfer** budgets are what the browser downloads. `serve@14` applies its compression middleware
  unless compression is explicitly disabled, so responses carry `Content-Encoding: gzip` and every
  Lighthouse `resource-summary` number is compressed.

A single set of numbers cannot serve both. Assuming the server does not compress makes a transfer
budget roughly two to three times too generous.

## Procedure

1. Build via the target mapped by `make.build` and start the production stack via the repository's
   clean prod-restart target, then confirm compression is on:

   ```bash # profile-example
   make build-out
   make start-prod-clean
   # the prod stack listens on PROD_PORT (3001 by default)
   curl -sI -H 'Accept-Encoding: gzip' http://localhost:3001/ | grep -i content-encoding
   ```

2. Measure each audited URL — script transfer and total transfer — from the browser network panel or
   the Lighthouse report itself (the targets mapped by `make.lighthouse_desktop` /
   `make.lighthouse_mobile`), not from the build output listing. A **clean** prod restart rather
   than the plain start target mapped by `make.start_prod` matters — the latter reuses an
   already-running container, so the numbers can silently come from an older build.

3. Set each budget to the **heaviest** audited URL plus roughly 30–35% headroom, and record the
   measured baseline and the rationale next to the number so the next reviewer can tell a
   recalibration from a relaxation.

4. Prove the gate can fail. Add throwaway weight, run the enforcing target, confirm it exits
   non-zero, then remove it. In the React SPA shape the same script backs the pull-request
   bundle-size report, so a breach also fails that workflow:

   ```bash # profile-example
   make perf-budget
   ```

5. Keep any documentation table that mirrors the numbers in the same change — the config file is
   authoritative and the prose is a copy.

## Common mistakes

- Calibrating from raw build output while the gate measures compressed transfer.
- Setting a budget without ever seeing it fail, so a typo in the assertion key goes unnoticed.
- Treating static fonts as growth headroom — they inflate the total but never change; note their
  share in the rationale.
- Raising a budget to make a build pass instead of splitting or shrinking the bundle.
- Editing the mirrored table in documentation and leaving the config untouched, or the reverse.
