---
name: name-product
description: End-to-end product naming pipeline — brief → competitor scan → theme-by-theme generation → clearance → selection → TLD/budget → lock. Embeds the operator's default iterative shortlist-by-theme selection method. Use to name a new product or rename an existing one. Composes competitor-research and name-clearance.
---

# name-product

> **The Patently lesson + the ~50-name lesson.** Naming "Patently" (an AI **patent** tool)
> collided with an 8-yr-old AI patent platform — a free domain proved nothing. And a
> diligent sweep of ~50 candidates showed real single words and common suffixes (-ly) are
> essentially gone in software/AI; the survivors were coined compounds and -proof forms.
> **So: clear the name not the domain, and don't burn the whole budget hunting for a
> perfect real word that doesn't exist — but never *assume* a word is taken; check it.**

## When you activate

- Naming a new product, or renaming one (before any domain purchase — hard gate in the go-live flow).

## Core principles (carry these through every phase)

- **Positioning first.** A name only feels *right* when pointed at a sharp positioning. Never generate in a vacuum.
- **Don't assume — check.** Never write off a dictionary word as "taken" without checking. A taken `.com` is *not* a dead name; same-industry collision is what kills.
- **Keep the aperture wide.** Explore real-related, real-unrelated (arbitrary), and made-up words. Bias toward arbitrary/coined for clearability *and* trademark strength, but don't pre-filter creativity.
- **Don't converge early.** Diverge wide, then shortlist *by direction*; give the operator the wheel at each gate. (See [[feedback_dont_converge_early]].)
- **Keep two ledgers:** a **parking lot** (liked-but-flagged — revisit, don't discard) and a **rejected-names + why** log (never re-pitch a killed name).

## Pipeline

**Phase 0 — Brief.** Lock: core idea · ICP / target group · positioning (hero user, the one promise, the feeling, the enemy). Decide *literal vs abstract*. Save to `products/<slug>/naming-brief.md`.

**Phase 1 — Competitor scan.** Run the `competitor-research` skill. Outputs the naming conventions of the space, the white-space, and the **collision baseline** (names/roots to avoid).

**Phase 2 — Theme select.** Propose themes (territories) flowing from the positioning, each with **sub-lanes**: *real-related · real-unrelated/arbitrary · made-up/coined · structural* (suffixes like -ly/-ify/-o, "agent"/persona patterns, compounds, -proof, etc.). **Exhaust one theme before the next**, or have the operator pick the order. Confirm before generating.

**Phase 3 — Generate wide.** Within the chosen theme/lane, generate a generous batch (10–20). Creativity not pre-filtered. Include dictionary words — they get *checked*, not assumed.

**Phase 4 — Clear.** Run `name-clearance`: domain prefilter (signal, not gate) → same-industry collision → trademark signal (USPTO/EUIPO classes 9/42/45) → famous-crowding/SEO. Liked-but-flagged → parking lot. Killed → rejected log.

**Phase 5 — Select (the operator's default method).** Present **cleared survivors grouped by theme** in a compact table, then ask the operator to react/shortlist via multi-select — *options, never a verdict*. If a theme is exhausted with nothing loved, return to Phase 2 for the next theme. Iterate until there's a shortlist the operator actually likes.

**Phase 6 — TLD + budget.** For finalists, full TLD sweep (`check-domains.ts`) and align on **budget** (premium `.com` purchase vs accept `.ai`/`.legal`/`.io`). Confirm the operator's domain-tier preference.

**Phase 7 — Lock.** Recommend the strongest finalist, but the pick is the operator's. State plainly: a **paid attorney trademark knockout** (USPTO + jurisdiction, relevant classes) is required before committing. Then hand off to rebrand + domain attach.

## Artifacts (persist per product)

- `products/<slug>/naming-brief.md` — the Phase 0 brief.
- `products/<slug>/competitors.md` — from competitor-research (compounds over time).
- `products/<slug>/naming-shortlist.md` — parking lot + rejected-names-and-why + current shortlist.

## Output

Always end a round with: the cleared shortlist (grouped by theme, with evidence + domain), the parking lot, and a single clear question giving the operator the wheel on what to explore next.
