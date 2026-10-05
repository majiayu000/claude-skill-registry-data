---
name: land-feature
description: Devkit overlay on /finalize — append the COMPLETE_ACTIONS.md entry and reconcile CLAUDE.md invariants for repos that use that ledger contract. Trigger on:- land this, ship it, log this, wrap up, COMPLETE_ACTIONS entry.
allowed-tools: Read, Edit, Write, Bash, Grep
model: claude-sonnet-4-6
---

# Landing a feature (overlay)

This is the **overlay** step for repos whose `CLAUDE.md` states the contract:
*"Feature lands → a `COMPLETE_ACTIONS` entry. Invariant changes → a `CLAUDE.md` edit.
Nothing else goes in `CLAUDE.md`; it is not a changelog."* It executes that contract,
then defers all commit mechanics to `/finalize`.

> **Orient first:** read `.specify/memory/constitution.md`, then the target repo's
> `CLAUDE.md` and its plan index header — they govern that repo's doc set, invariants and
> plan-status vocabulary.

## When to use this

- The repo has a `docs/COMPLETE_ACTIONS.md` ledger and a numbered-invariant `CLAUDE.md`.
- Otherwise use `/finalize` directly — it is the generic land step.

## Steps

**1. Read the ledger's tail** and match the existing heading style — don't invent one.

```bash
tail -30 docs/COMPLETE_ACTIONS.md
```

**2. Append one entry**, newest last:

```markdown
## <short searchable title> (YYYY-MM-DD)
- `<module>/<class>/<function>`: what it now does, present tense.
- Load-bearing behaviour stated explicitly (a default, a refusal, a version pin).
- Consumers migrated / deploy files added, if any.
```

Append only — never rewrite or reorder. One entry per landed feature, not per commit.
Today's real date. Describe the end state, not the diff.

**3. Edit `CLAUDE.md` only if a numbered invariant's text is now false**, or a new module
belongs in the map. A bug fix, a refactor, or a new tool on an existing tenant is
**no edit**. Consult the repo's own change→action table if it has one.

**4. Update `README.md`** only if the public surface changed — a new/changed public
signature, a new entry point, a change to the documented way of extending the project.

**5. Hand off to `/finalize`** for done-checks, version bump, plan-index flip to
`implemented`, and the staged conventional commit on user confirmation. Do not run the
tests or commit here — that is `finalize`'s job.

## What not to do

- Don't rewrite or reorder existing ledger entries — the file is append-only.
- Don't edit `CLAUDE.md` for a bug fix, a refactor, or a new tool on an existing tenant.
- Don't write the ledger entry while a regression is outstanding.
- Don't duplicate `finalize`'s commit/version steps here.
