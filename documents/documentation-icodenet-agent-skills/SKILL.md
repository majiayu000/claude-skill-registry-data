---
name: documentation
description: >-
  Writes and updates docs, READMEs, runbooks, specs, and ADRs. Use when
  documenting a feature, writing a runbook, updating README/setup docs, or
  recording decisions. Do not use for competitive research briefs or for code
  comments that only restate the next line.
---

# Documentation

Document the *why*, the run path, and the contract — not the obvious *what*.

## Workflow

1. **Audience + job** — operator, developer, or agent; one job per section.
2. **Find the owner doc** — update the canonical page; do not create a third copy of the same truth.
3. **Write** — quick start that works; real commands from the project's scripts; link out instead of duplicating.
4. **Runbooks** — steps + verification + rollback.
5. **ADRs** — context, decision, alternatives, consequences (`../architecture/references/adr-template.md`).
6. **Verify** — commands and paths match current repo reality.

## Constraints

- Prefer links to canonical docs over pasting large tables into multiple places.
- Comments in code: why/gotchas only — never restate the next line.
- Delete commented-out code; git keeps history.

## Verification

- [ ] Correct canonical file updated (or new file justified)
- [ ] Quick start / commands match current project scripts and paths
- [ ] Runbooks include verify + rollback
- [ ] ADRs have alternatives + consequences
- [ ] No duplicated “source of truth” that already lives elsewhere
