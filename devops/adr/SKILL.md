---
name: adr
description: "Writes a MADR style architecture decision record under docs/adr, or supersedes an existing one, for a decision worth remembering. Use when an architecture, infrastructure or tooling choice needs recording."
---

# Adr

Record a decision worth remembering as a numbered ADR.

## When to use

Write an ADR when a component, protocol or data store is chosen or replaced, a cloud
provider or module boundary is picked, a deployment or release mechanism changes, a
public interface is fixed, or a dependency is added that is expensive to remove.

Skip it for behaviour preserving refactors, renames, version bumps and formatting.
Extend or supersede an existing ADR instead of writing a near duplicate.

## Steps

1. Read `AGENTS.md` for `## Deviations`. An entry that drops ADRs means: say so and stop.
2. Apply the gate above. If no ADR is warranted, say so and stop.
3. List the ADR directory. Take the highest number plus one, four digits, sequential,
   never reused. No directory yet means this is the first record: create it now.
4. Name the file `NNNN-short-title.md`, for example `0007-use-opentofu.md`.
5. Context: constraints only, no solution.
6. Decision: one sentence, present tense, then the reasons.
7. Consequences: name the negatives too. Upsides only means the record is not finished.
8. Alternatives: every real option that lost, each with the reason it lost.
9. Link related ADRs by number, and a concept doc if one exists.
10. Status is `proposed` while under review, `accepted` once agreed.
11. To replace a decision, write the new ADR, reference the old number, and set the old
    file's Status to `superseded by NNNN`. Change nothing else in the old file.
12. Ship the ADR in the pull request that makes the change, or earlier.
13. Three to six one line bullets per section. No paragraphs.

## Guardrails

- `## Deviations` checked before the directory is touched.
- Gate applied, ADR actually warranted.
- `docs/adr` created with the first record, not ahead of one.
- Next free number, four digits, never reused.
- Status is `proposed`, `accepted` or `superseded by NNNN`.
- Context holds constraints, not the solution.
- Every alternative carries its rejection reason.
- Negative consequences named. Superseded ADR changed in Status only.
- One screen, one line bullets, `CHANGELOG.md` untouched.

## Config

- `docs.adr`: directory for ADRs. Default `docs/adr`.

## References

- MADR: <https://adr.github.io/madr/>
- `concept-doc` for the design that precedes a decision.
