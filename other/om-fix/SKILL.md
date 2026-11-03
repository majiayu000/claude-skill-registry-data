---
name: om-fix
description: Repo-local extension of om-fix - test-first at the seam, catalogue copy, generated files and the suppression ban.
---

# om-fix (money-tracker.online)

This file extends the shared `om-fix` skill installed at `.claude/skills/om-fix/SKILL.md`. Follow
its full workflow (claim, minimal change, regression tests, validation loop, output contract) with
the rules below layered on top.

## Implementation rules

- Write the failing test first, at the seam the analyzer named (skill `tdd`,
  `.claude/skills/tdd/SKILL.md`). A repository change gets its tenant-isolation case; an amount-touching
  change gets its money-invariant case.
- Copy goes through the catalogue (skill `i18n-messages`, `.claude/skills/i18n-messages/SKILL.md`):
  the key lands in `en.ts` and `pl.ts` in the same change, and a count goes through the plural
  machinery.
- After touching `src/routes/**` run `pnpm generate-routes`; after touching
  `src/server/db/schema.ts` run `pnpm db:generate` and keep the migration under `drizzle/`. Never
  hand-edit either output.
- Money stays in integer minor units; the scale is `currencies.digits`.
- Never add `@ts-ignore`, `@ts-expect-error` or `eslint-disable`, never `.skip` or `.only` a test,
  never delete one to make the gate green. A gate that only passes that way is a finding for the
  report, not a fix.
- The dependency set is frozen (`docs/SPEC.md` §3): a fix that needs a package stops and reports
  the blocker.

## Validation loop

The gate is `validation.commands` from `.ai/agentic.config.json`, in order. The two drift commands
run first; when either leaves a diff, that diff is part of the fix. Pipe the test run to a file
before quoting any count from it, and re-run failed files alone before calling a failure a flake
(`docs/SPEC.md` §7.7, skill `verifying-changes`, `.claude/skills/verifying-changes/SKILL.md`).
