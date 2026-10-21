---
name: brain-protocol
description: Load and maintain Snowshoe's spec-driven brain. Use at session start, before any behavior or product-claim change, and when CURRENT/ADRs may be stale.
---

# Brain protocol

## Read order (required)

1. `docs/brain/START_HERE.md`
2. `docs/brain/CURRENT.md` — compiled truth
3. `docs/brain/ROADMAP.md` — sequence of intent, not shipped fact
4. `docs/brain/EXPERIMENTS.md` — registry of bets, not truth

Then open only the ADRs, notes, or evidence the task needs.

## Trust

- **Truth** = `CURRENT.md` + ADRs with `status: accepted` (`active` is a lint alias only; DECISIONS table uses `accepted`).
- Experiments stay in the registry until promoted.
- `docs/evidence/**` supports a claim; it does not become true by existing.
- `docs/brain/notes/**` is working memory.
- `docs/archive/**` is historical.

## Writes (required on behavior / claim change)

If you change product behavior, positioning, non-goals, monetization, or any claim CURRENT makes:

1. Add or update an ADR under `docs/brain/DECISIONS/` (use `docs/brain/templates/DECISION_TEMPLATE.md`).
2. Update `CURRENT.md` in the **same** change so it stays the compiled truth.
3. Set frontmatter `status:` correctly (`accepted`, `proposed`, `superseded`, …).
4. Move superseded canon to `docs/archive/` rather than deleting history silently.

Do not implement application code until CURRENT says we are past scaffold-only.

## Hygiene

- Keep CURRENT short. Detail lives in ADRs.
- Do not invent metrics, users, or competitors.
- English in brain files.
