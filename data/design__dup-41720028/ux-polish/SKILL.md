---
name: ux-polish
description: Define UI tokens, accessibility rules, and consistent component behavior for the Astro frontend, plus empty/loading/error states and light hover/focus transitions. Use when adding or refining frontend UX polish and documentation under frontend/ in this repo.
---

# UX Polish

## Overview

Make the Astro frontend coherent and production-grade without architectural rewrites. Focus on tokens, a11y, state handling, and minimal-interaction polish with low JS impact.

## Workflow

1. Inspect existing global styles/components under `frontend/` to avoid style drift.
2. Define UI tokens using CSS variables or Tailwind theme strategy (typography, spacing, radii, shadows, color roles).
3. Apply accessibility guardrails (focus visibility, semantic headings, keyboard nav, contrast).
4. Add empty/loading/error states to blog list and post detail.
5. Add only hover/focus transitions (no animation libraries).
6. Document decisions in `frontend/docs/ux.md`.

## Scope

- Define tokens: typography scale, spacing scale, radii and shadows, color roles (bg/fg/muted/accent).
- Ensure accessibility: visible focus states, semantic headings, keyboard navigation, reasonable contrast.
- Add empty, loading skeleton, and error fallback states.
- Add micro-interactions via hover/focus transitions only.

## Outputs

- Add `frontend/docs/ux.md` describing tokens, component rules, and an a11y checklist.
- Apply minimal changes to global styles and components to match the rules.

## Acceptance Checklist

- Focus is visible on all interactive elements.
- Empty/loading/error states exist for blog list and post detail.
- Typography and spacing are consistent across pages.
