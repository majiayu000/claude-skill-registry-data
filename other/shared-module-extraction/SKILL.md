---
name: shared-module-extraction
description: >-
  Use when a duplication gate flags cloned component code — a jscpd failure, a qlty `similar-code`
  comment, or two components differing only in a path, a viewBox, or a stroke width — and the fix is
  to extract the block into a shared internals module that several components already render.
---

# Shared module extraction

## Profile keys consumed

- `make.lint_dup`
- `make.test_visual`
- `capabilities.visual_testing`
- `quality.jscpd_clones`
- `quality.visual_diffs`
- `architecture.source_root`

## Overview

Extracting duplicated component internals is only half the job. Because the extraction changes what
every consumer renders, the full visual suite is the proof: a run that rewrites no baseline means
the rendered output is byte-identical and the extraction is safe.

## When to use

- A duplication gate reports a clone of roughly twenty lines or more between components.
- Two icon or field wrappers share structure and differ only in data (path, viewBox, stroke width,
  label).
- A shared internals barrel already exists and a third consumer is about to hand-roll a fourth copy.
- Not for: incidental similarity below the gate's token threshold — abstracting that pushes toward a
  worse shape than the duplication.

## Applicability gate

The proof step needs a visual suite. Skip step 4 and step 5 with a recorded note when
`capabilities.visual_testing` is `false` or the target mapped by `make.test_visual` is `null`, and
substitute the closest available render evidence (component snapshot tests, then a manual pass over
every consumer). When `make.lint_dup` maps to `null` there is no duplication gate to re-run, so skip
step 7 with a recorded note and confirm the clone is gone by reading both former sites.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the target mapped by `make.lint_dup` runs jscpd at zero tolerance (`.jscpd.json`,
  75 tokens / 5 lines over the source root), and the target mapped by `make.test_visual` drives the
  per-spec baselines under the visual specs' snapshot directories.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — no jscpd gate;
  duplication surfaces only as a qlty `similar-code` comment, and the visual specs and baselines
  live under the test tree's visual directory.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — shared
  internals live in a field-controls directory behind its `index.ts` barrel, and the target mapped
  by `make.test_visual` runs the chromium baselines under the visual test directory.

## Procedure

1. **Confirm it is a real clone.** Read both sites and identify what varies. If the difference is
   data (a path string, a size, a label) the block is extractable; if the difference is behaviour,
   extract the shared part only.
2. **Extract into the repo's shared internals location** under `architecture.source_root`, not into
   one of the consumers, and export it from that directory's barrel so consumers import through the
   public path.
3. **Replace every consumer**, not just the two the gate named — leaving one copy behind keeps the
   gate red and re-splits the code path.
4. **Run the full visual suite** through the target mapped by `make.test_visual`, not the specs for
   the components touched. A shared module reaches consumers the diff does not mention. Then read
   the working tree for rewritten baselines, under whichever visual test directory the repository
   keeps them in.

   ```bash # profile-example
   # With a profile whose make.test_visual maps to `test-visual` and baselines under tests/visual:
   make test-visual
   git status --porcelain tests/visual
   ```

5. **Require zero rewritten baselines.** No `.png` shows as modified and no diff image is produced,
   so the rendered DOM is unchanged for every consumer. That is the pass condition, and it is the
   same `quality.visual_diffs` ceiling of `0` that CI enforces.
6. **If a baseline does change, stop and diagnose.** A rewritten snapshot means the extraction
   altered rendering — a lost prop, a changed default, a wrapper element added. Fix the extracted
   module until the suite is clean; only refresh baselines when the visual change is the intended
   outcome of a separate, reviewed change.
7. **Re-run the duplication gate** through the target mapped by `make.lint_dup` to confirm the clone
   is gone rather than merely relocated — `quality.jscpd_clones` is a ceiling of `0`.

## Preventing the next clone

New inline markup of a kind the shared module already covers — another icon wrapper, another field
adornment — reuses the shared module from the start. Hand-rolling a near-copy just re-enters the
duplication gate on the next run and costs a second extraction plus a second full visual run.

## Common mistakes

- Running only the specs for the components in the diff, so a third consumer regresses unnoticed.
- Accepting rewritten baselines as "close enough" — that converts an unreviewed rendering change
  into the new reference.
- Extracting behaviour along with markup, which turns one clone into a shared module with a flag
  argument for each caller.
- Leaving the last consumer un-migrated, so the gate stays red and both code paths must be
  maintained.
- Deduplicating by loosening the gate's token or line thresholds instead of removing the clone.
