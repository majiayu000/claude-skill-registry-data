---
name: verify-ui
description: Visually verify UI changes with Playwright screenshots before proceeding. Use when a change touches frontend/UI files and needs visual confirmation, not just passing tests.
user-invocable: false
---

## Visual Verification (shared core)

This is the single source of truth for "how do we visually verify a UI change?".
`implement` (Phase 4, `phases/phase-4-implement-green.md`) and `address-review` (Phase 4)
both follow this procedure — never restate it inline in a calling skill; reference this
skill instead.

### Screenshot capture

- Prefer Playwright Test with `toHaveScreenshot()` when configured.
- Otherwise use the Playwright CLI for interactive screenshots/snapshots.
- If no browser tooling is available at all, **do not silently skip this step** — the
  caller must explicitly state that visual verification was not performed and why
  (missing tooling), so the gap is visible in the final report rather than assumed away.

### Fix-before-proceeding

Significant visual discrepancies found by the screenshot check above must be fixed, or
get explicit user acceptance, before the calling skill proceeds past its own verification
gate. Do not defer a known visual regression to "future work" without that explicit
acceptance.

### `isUiChange` heuristic (for callers with no ticket to classify)

`frontend-classification` classifies a *ticket* from its title/description/acceptance
criteria — it needs ticket text to read. Some callers (e.g. `address-review`) only have a
PR diff, with no ticket in hand. For those, classify the *diff* instead: a change is
`isUiChange = true` when any changed file path matches:

- Component/view extensions: `.tsx`, `.jsx`, `.vue`, `.svelte`, `*.component.*`
- Styling: `.css`, `.scss`
- Common UI directory names: `components/`, `views/`, `pages/` (or an equivalent
  project-specific convention documented in `CLAUDE.md`)

This is a narrower, file-path-only signal than `frontend-classification`'s keyword rule —
use it only when there is no ticket text available to classify from directly.

## Explicitly out of scope (stays with the caller)

One step is `implement`-only and deliberately **not** part of this shared skill:

- **"Persist Screenshots For The PR"** — only `implement` (Phase 9) uploads and embeds
  screenshots into a *newly created* PR body. `address-review` edits an already-open PR
  and has no screenshot-persistence/embedding step of its own.

`implement/phases/phase-4-implement-green.md` keeps that step in its own Visual
Verification section, immediately after following this skill's shared core.
