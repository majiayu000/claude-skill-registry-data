---
name: docs-upkeep
description: "Use before finishing any change that alters what the viewer shows, adds or drops a data source or transformation, makes a decision that binds future work, or sends visitor data somewhere new; also when writing or revising an ADR, AGENTS.md or a skill."
---

# Keeping the docs current

A change is not done until the docs say so. Each kind of fact has one home;
put it there and link to it from elsewhere, never copy it.

| Fact | Its home |
|---|---|
| A decision and why, a rejected alternative | `docs/adr/` |
| What each data → look transformation does, its status | `docs/transformations.md` |
| How the scene and pipeline are built, numbers, recipes | `docs/rendering.md`, `docs/data-pipeline.md`, the `city-walker` skill |
| Rules an agent must not break, commands | `AGENTS.md` |
| A recurring procedure | a skill in `.claude/skills/` |
| What a visitor's data does | `app/(legal)/datenschutz/page.mdx` |
| History, measurements, intermediate states | git, PRs, `docs/plans/` |

## Checklist

1. Do every item of the *Definition of Done* in
   [docs/README.md](../../../docs/README.md#keeping-these-docs-current) that
   applies.
2. The guide changes in **English and German** in the same commit.
3. A Mermaid block changed: `bun run docs:diagrams`, commit the SVG.
4. Source configs changed: `bun run docs:matrix`.
5. A new third-party request, report field or storage key: the privacy
   page.

## Writing an ADR

Rules and format: [docs/adr/README.md](../../../docs/adr/README.md).

- One present-tense decision, about a page. Constants, measurements and
  file lists go to code comments or the developer docs.
- A changed decision is **rewritten in place** — no "Update" or
  "Amendment" paragraphs. A superseded ADR is deleted, and every
  reference to it (code comments, docs) is moved to its successor.
- Alternatives only where someone would otherwise retry them, each with
  its reason in a sentence.
- **Number:** the next after the highest ever used. Parallel threads have
  taken the same number three times: check main's `docs/adr/` **and** the
  open PRs' branches before taking one.
- Prefer extending the ADR that already owns the topic over a new one.

## Writing AGENTS.md or a skill

- AGENTS.md holds orientation, commands, the hard rules (one or two lines
  each, pointing at the ADR) and conventions. No file inventory, no
  rationale, no tuning numbers.
- A skill holds a procedure or a deep reference. It points at ADRs for the
  why and never restates a decision differently.
- After editing any of them, read them side by side for contradictions.
