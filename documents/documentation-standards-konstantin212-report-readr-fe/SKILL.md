---
name: documentation-standards
description: Use when creating or updating a doc under docs/ — enforces the single-source-of-truth hierarchy, docs/INDEX.md registry, changelog rules, and one-concept-per-file.
---

# Documentation Standards

## Single source of truth

- All project documentation lives under `docs/`. Before writing a new doc,
  check whether the concept is already documented — edit the existing doc
  instead of creating a near-duplicate.

## `docs/INDEX.md` registry

- `docs/INDEX.md` is the registry the business-analyst and architect read
  first. Every business-logic item and architecture entry must appear there as:
  **title + 1–2 line description + link**.
- Any doc addition, change, or removal **must** update `docs/INDEX.md` in the
  same change — a doc that isn't indexed is effectively lost.

## Structure

- Keep a strict, scalable hierarchy under `docs/` (e.g. business logic,
  architecture, specs & plans as separate sections/folders) rather than a flat
  dump of files.
- **One concept per file.** Don't merge unrelated topics into one doc, and
  don't split one concept across multiple files.

## Changelog rules

- When a doc changes in a way that reflects a real decision, record: **what**
  changed, **why**, **when**, and a link to the relevant spec/plan.

## Avoid duplication

- Watch for near-duplicate docs covering the same ground from a slightly
  different angle — consolidate them rather than letting both survive.
