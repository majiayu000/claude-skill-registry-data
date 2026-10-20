---
name: product-documenting-specs
description: Add or move a document under the project's documentation directory (e.g.
  docs/). Use whenever someone wants to create a new spec, decision record, overview,
  business/pricing note, design doc, blog draft, or archive an old one — or move/rename
  an existing doc. The documentation tree is organized by purpose with a strict authority
  hierarchy and a single source of truth for pricing and business rules; this skill
  enforces the four rules so a new file does not reintroduce the confusion the structure
  was built to remove.
tags:
- documentation
- specifications
- docs index
- specs publishing
- authority badge
user-invocable: true
---
# Skill: Documenting Product Specs

The project's documentation directory (e.g., `docs/`) is organized **by purpose, not by version**, with a strict authority order and a single source of truth for financial, pricing, and business metrics. A careless new file silently breaks that. Before creating ANY file under the documentation directory, answer the four gates below — **stop and fix** if any gate fails. Full map & rules live in the documentation index (e.g., `docs/README.md`).

## The folders (pick exactly one)

| Folder | For | Authority |
|---|---|---|
| `overview/` | Plain-language entry: what the product is + roadmap. No technical detail. | AUTHORITY |
| `decisions/` | Locked, hard-to-reverse choices. Overrides every other doc. | AUTHORITY (highest) |
| `specs/` | Engineering specs — *how* to build it (schema, API, pipeline). | AUTHORITY |
| `business/` | Pricing / credits / cost of goods sold (COGS). **The ONLY place numbers are defined.** | AUTHORITY (single source) |
| `design/` | apps/web design system + UX. | AUTHORITY |
| `content/` | Marketing & blog drafts. Verify before publish. | DRAFT |
| `archive/` | Superseded / historical. Never build to it. | INVALID |

## The four gates (all must pass)

**Gate 1 — STATUS badge.** Line 1 of every doc MUST be a status badge:
`> **STATUS:** AUTHORITY | DRAFT | REFERENCE | INVALID — <one-line reason>`
No badge → the doc is rejected. (Authority dictionary: `AUTHORITY` = build to it · `DRAFT` = draft · `REFERENCE` = pointer/info · `INVALID` = do not build to it.)

**Gate 2 — No loose price/COGS numbers.** A doc may NOT define a credit, price, margin, or cost number. It may only **reference** the central business/pricing document (e.g., `docs/business/Pricing_and_Product_Simulation.md` or similar pricing section). Product facts that are *not* money (batch limits, thresholds, model names) are fine inline. If you typed currency or credit figures outside the pricing document, replace it with a reference to the central document.

**Gate 3 — Register in the map.** List the new doc in the documentation index (e.g., `docs/README.md`): add a bullet under the correct folder heading in the list of active documents, giving its filename + one-line purpose in the existing bullet style. The folder table at the top lists *folders*, not individual docs — don't add a row there. A doc that isn't in the README map doesn't exist.

**Gate 4 — Declare the audience; don't mix silently.** State the audience in the first paragraph: **product/business**, **technical**, or **mixed**. If `mixed` is unavoidable, split explicitly: first sections = product/business decisions, subsequent sections = engineering. (The legacy, large PRDs that interleave both are the exact pain this rule prevents.)

## Then

- **Duplication check:** does this content already live in another doc? If yes, **update that doc or reference it** — do not open a new file. (Pricing numbers especially: reference the central document, never restate.)
- **Naming:** folder = lowercase single word, ASCII. File = `Title_Case_With_Underscores.md`, ASCII only. Exception: module artifacts or specs use the standard filenames defined by the project's development workflow.
- **Moving/renaming:** always `git mv` (preserves history). If you move a live doc, also fix its row in the documentation index map.
- **Archiving:** set the badge to `INVALID`, `git mv` into `archive/`, and update any doc that pointed to it so the pointer targets the live source — never leave a live doc pointing at an archived one.
