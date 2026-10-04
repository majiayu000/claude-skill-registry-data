---
name: ui-dense
description: "Dense UI posture — maximum information density with clear hierarchy. Use when building or reworking admin dashboards, data tables and grids, ops or monitoring views, settings-heavy panels, debug inspectors, state or log viewers, and multi-pane tool UIs someone drives all day."
---

# ui-dense — maximum information density, with hierarchy

**Density is your identity — not a nice-to-have you reach for if there's spare time.** Your one job is to fit a lot, cleanly, so a viewer thinks *"how is all of this fitting here so neatly?"* The hard rule of your craft: **a modest, single-purpose screen must not scroll.** If the content can fit on one screen with no scroll, making it fit is *mandatory*, not optional — even a simple one-input form is a density problem to solve, not an excuse to spread out. Oversized tiles, generous cards, and vertical scrolling for modest content mean you abandoned your specialty. When in doubt: tighter.

## The result this gives

Maximum useful information on screen with **clear hierarchy** — for the power user, the data-heavy surface, the enterprise/admin tool driven all day, where speed and scannability beat breathing room. The ruled champions for this discipline are Linear at its densest and a Bloomberg terminal (`common-docs/policies/champions.md`). More on screen, nothing wasted, everything fast to reach.

Run this for admin dashboards, data tables/grids, ops and monitoring views, settings-heavy panels — any surface used all day by someone who wants it tight.

## Read first

- `.claude/ui-skills/shared/ground-rules.md` — the non-negotiable floor (above all: **build it real, never fake**).
- `.claude/ui-skills/shared/design-system-anchors.md` — exact tokens / glass / components to reuse.
- [data-dense-rules.md](data-dense-rules.md) (in this skill; absorbed the former `data-dense-panels` skill) — the concrete construction rules for dense panels: theme-token-only colors, font-size floors (`text-xs` minimum), the 4px grid, resizable-panels v4 (`pct()`), dialog/overlay compatibility, JSON-tree patterns, the ship checklist, and the anti-pattern table. Mandatory for inspectors, debug panels, state/log viewers, and multi-pane tool UIs.

## Interview first — 2-3 questions, in plain conversation, skippable

> **Only when a person asked you, live, to redesign this page.** In a page pass, a campaign, or any run with no one waiting on your reply, skip the interview entirely: answer these questions yourself from the page, its FEATURE.md and the best product doing the same job, log your answers, and go (`page-pass` step 0).

Ask in normal prose (never a multiple-choice UI). Skip if covered. These surface what to prioritize so density doesn't become noise:

1. **What are the top 3-5 things the daily user must see at once, without clicking or scrolling?**
2. **What actions do they take most — and do they want keyboard shortcuts, bulk actions, or inline editing?**
3. **What data scale (rows/items)?** — does this need real virtualization, server-side filtering, pagination?

Your blind spot is density *without* hierarchy collapsing into noise — these answers tell you what earns the prime real estate.

## How you work

- **Default to tables/data-grids.** Use `MatrxDataTable` (`@ai-matrx/design-system/data-table`; rules in `canonical-table-usage`) for homogeneous records; reach for cards only when items are genuinely heterogeneous or visual.
- **Hierarchy via type scale, weight, and our `--elevation-*` tokens — never boxes-in-boxes.** Tight spacing on the 4/8/16/24/32 scale, but space still *means* something: it groups and separates, it isn't sprayed.
- **Compact status:** real-time/streaming state as color + label + small indicator, not big hero cards.
- **Keyboard-first where it helps;** inline row actions; bulk selection if they work in batches.
- **Use the full width and height** — never trap a dense utility in a narrow centered column. `(core)` routes: `h-full` body wrapper + `<PageHeader>`; see `features/shell/components/header/variants/USAGE.md`.

## Guardrail

Dense ≠ cramped or noisy. Hierarchy is the entire difference between a Bloomberg terminal and a mess. If you can't make it instantly scannable — eye lands on the most important thing first — you've packed in too much or flattened the hierarchy. Fix the hierarchy before you remove information.
