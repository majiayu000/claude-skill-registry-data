---
name: Markdown ADRs
description: Create and maintain MADR-format Architectural Decision Records in Markdown under `docs/decisions`. Use when the user wants to document important decisions.
---

# MADR ADRs

This skill creates (and keeps tidy) **Architectural Decision Records (ADRs)** using **MADR (Markdown Architectural Decision Records) v4.0.0**.

A helpful bar for what “counts” as an *architectural decision* is Martin Fowler’s: **“a decision you wish you could get right early.”** (["Who needs an architect?"](https://web.archive.org/web/20231221064723/https://ieeexplore.ieee.org/document/1231144?arnumber=1231144), IEEE Software, 2003)


Primary reference: [Markdown Architectural Decision Records](https://adr.github.io/madr/)

## Repository layout and naming

All ADRs live in:

- `docs/decisions/NNNN-title-with-dashes.md`

Where:

- `NNNN` is a **zero-padded 4-digit** sequence number (`0001`, `0002`, …)
- `title-with-dashes` is a **lowercase slug** (letters/digits/hyphens)

If `docs/decisions/` does not exist yet, create it.

## Template

Use this copy of the [MADR 4.0.0 long-form template](ADR_TEMPLATE.md)

Create new ADRs by copying the template and replacing placeholders. Optional sections may be removed (the template marks them clearly).

## Required metadata

Each ADR must include YAML front matter at the top with:

- `status`: one of `proposed`, `accepted`, `rejected`, `deprecated`, or `superseded by ADR-NNNN`
- `date`: `YYYY-MM-DD` (update when the ADR is materially changed)

## Status emoji for the index

Maintain an index at `docs/decisions/README.md` that lists **all** ADRs with:

- status emoji
- ADR title (matching the H1 of the ADR), as a link to the full ADR
- date last updated

Use this mapping:

- 🟡 proposed
- ✅ accepted
- ❌ rejected
- ⚠️ deprecated
- 🔁 superseded

## Process

1. **Pick the next number** by scanning existing ADR filenames in `docs/decisions/` and incrementing the highest `NNNN`. Start at `0001` if none exist.
2. **Slugify the title** into `title-with-dashes` (lowercase, hyphens, no punctuation).
3. **Create the ADR** from `ADR_TEMPLATE.md`.
   - Default `status` to `proposed` unless the change set includes implementation and agreement to accept.
4. **Update `docs/decisions/README.md`**:
   - Add the ADR in numeric order.
   - Ensure the emoji matches the ADR’s `status`.
5. If an ADR is **superseded**, keep the old ADR file, set its status to `superseded by ADR-NNNN`, and update the index row emoji to 🔁.

## Output expectations

- ADR markdown should be clean and readable in GitHub rendering.
- Keep ADRs concise, but include enough context that a new reader can understand why the decision was made.
