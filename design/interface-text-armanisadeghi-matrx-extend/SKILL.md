---
name: interface-text
type: Skill
title: "interface-text — in-app text is layout: labels, not prose"
description: "Rules for every string rendered inside the app, plus the sweep that removes in-app prose. Use when writing or changing a label, hint, description, tooltip, empty state or KPI tile in a .tsx file, or when running Pattern Patrol P14 or asked to find or fix long UI text."
tags: [ui, copy, microcopy, patrol, design-system]
timestamp: 2026-09-30T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/interface-text/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# interface-text — in-app text is layout

Doctrine (read once): `common-docs/policies/interface-text-is-layout.md`.

You are writing **interface text**, not prose. Every string the app renders sits in a **slot**
owned by a component, has a **character budget**, and has **siblings** that must match. The
screen is not where you explain, justify, or prove anything — that is what the commit message,
the code comment and `FEATURE.md` are for.

## The card — apply to every string you write or touch

1. **Who is this sentence for?** If it helps someone reading the diff — a formula, a function or
   table name, where the number comes from, what changed, what is not built yet, which other
   page agrees with it — it is **author-facing**. Put it in a code comment or the commit. It
   never renders.
2. **Label first.** Make the label carry the meaning (`Batch savings (7d)`). A number that needs
   a paragraph gets a better label; a definition that is still needed gets **one sentence in the
   tooltip slot**: `title=` on `KpiTile`, `components/official/InfoHint` everywhere else (hover,
   keyboard and touch — a native `title=` attribute on text is unreachable on phones).
3. **Fit the slot.** Secondary text ≤ **60** chars, one line, never two sentences. Tooltip ≤
   **140**, one sentence. Placeholder ≤ **60**, an example value. Dialog description / empty /
   error state ≤ **140**, at most two sentences: what happened, what to do. No sentence under
   a page or section title — ever.
4. **Look at the row and the column.** Your text sets the height of every tile in its row and
   the width of every cell in its column. Fill a **visible** slot on **all siblings, at similar
   length and in the same shape, or on none**. Tooltips are hidden and per need — never add one
   to a sibling just to match.
5. **Use the primitive that enforces the budget.** `components/official/kpi/KpiTile` +
   `KpiGrid` for KPI rows (one-line `hint`, `title` tooltip). If the official primitive "cuts
   off" your text, your text is too long — shorten it; never hand-roll a component to escape
   the limit. A local component that renders unbounded secondary text is itself a finding.
6. **A tooltip states only what you verified in the code or the data contract.** Cannot prove
   the definition ("since midnight", "today's budget")? Write no tooltip — a wrong definition
   is worse than none.
7. **Honesty is state, not prose.** Unmeasured → `—` with the reason in the tooltip. Partial
   feature → the Coming Soon registry. Never "not yet reported by the backend", never "Backfill
   brings this up to 100%".
8. **See it rendered, then check it.** In matrx-frontend run
   `pnpm check:interface-text --changed` before committing; any other repo:
   `node ../matrx-frontend/scripts/interface-text/check-interface-text.mjs --root=. --changed`.
   Every `NOVEL` line on your diff is fixed before commit.

## Rationalizations

From the 2026-09-30 baseline runs (`evals.md`) — each one produced a defect.

| Excuse (verbatim) | Reality |
|---|---|
| "the shared tile cuts off long hints" | That is the budget working. Shorten the text; keep the primitive. |
| "swapping only this row would make one page look two ways… should be its own change" | Adopt the primitive for the whole page in this change; it is a few lines. |
| "the rule that every number names its window and item count" | The label `(7d)` names the window; a count fits a 60-char hint. A sentence is not required. |
| "Both are a screen lying." → adds a sentence | Honesty is `—` + tooltip, a badge, or a registry entry. |
| "in the same words the Platform Spend 'Saved by batching' headline uses" | Consistency means the same **label**, not the same paragraph copied to two pages. |
| (with the skill) tooltips added to all six tiles "so the row matches" — two invented "since midnight" / "today's budget" | Parity is for visible slots. An unverified definition is fabrication; leave the tooltip out. |

## Red flags — stop and re-read the card

- You are about to paste words from your commit message, `FEATURE.md` or a code comment into JSX.
- Your string contains a dot-separated or snake_case name, a backtick, "backend", "server", or "not yet".
- One sibling gets a hint and the others do not.
- You are writing a second sentence in a hint or description.
- You are choosing a local component over `components/official/*` because of text length.
- You are writing a tooltip definition you did not read in the code or the data contract.

## The sweep — Discover → Review → Fix → Confirm (Pattern Patrol P14)

Each phase is its own agent. Read **only the file for the phase you were given**:

| Phase | Lane | Read |
|---|---|---|
| Discover — build units for a slice, classify each, propose the exact fix; the validator must pass | `quick` with **sonnet** (haiku mapped rules to verdicts without reading and cut rewrites mid-sentence — 2026-09-30) | `discover.md` |
| Review — accept or correct the classifications, find primitive-level fixes, batch the work, pick what goes to Arman | `standard` (opus — judgment over the classifications) | `review.md` |
| Fix — apply a reviewed batch in its files | `quick` (sonnet) for mechanical batches, `standard` otherwise | `fix.md` |
| Confirm — independent check of a fixed batch | `standard` (sonnet), never the fixer | `confirm.md` |

The proof record and regression scenario for this skill is `evals.md`; the next editor reruns it.
