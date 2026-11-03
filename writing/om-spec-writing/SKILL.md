---
name: om-spec-writing
description: Repo-local extension of om-spec-writing - what a spec here cites, the clean-room rule and how phases are sized.
---

# om-spec-writing (money-tracker.online)

This file extends the shared `om-spec-writing` skill installed at
`.claude/skills/om-spec-writing/SKILL.md`. Follow its full workflow (skeleton, Open Questions gate,
research, design, phasing, review) with the rules below layered on top.

## What a spec cites

- Arithmetic by section number of `docs/MONEY.md`, never restated.
- Boundaries: `docs/SPEC.md` §5 (tenancy, roles, billing surface, bindings) and §6.1 (layering).
- Localisation and accessibility: `docs/SPEC.md` §9 and §10. A spec never widens the claim in
  `docs/ACCESSIBILITY.md`.
- Every product decision it relies on, by ADR number. A decision that does not exist yet gets an
  ADR in the same PR, not a paragraph in the spec.
- The plan area under `docs/plans/` it advances, when one exists, and the rows of
  `docs/agents/out-of-scope.md` it stays clear of.

## Clean room

The reference product (`docs/agents/reference.md`) is a benchmark of rendered pixels and nothing
else. A spec carries no string, name, number, layout or copy from it. The research step compares
against open-source products only.

## Phasing

- A Phase is the size of one autonomous run (`docs/SPEC.md` §8): at most one migration, one product
  area, finishable in one `om-auto-create-pr` run. Split otherwise.
- Every Step that touches a repository names its tenant-isolation case; every Step that touches an
  amount names its money-invariant case.
- Every user-facing Step lists the message keys it adds (EN + PL in the same change) and the screens
  whose rendered output changes.
- A removal or a narrowing of a schema column is two Phases in two releases (SPEC §6.1).
