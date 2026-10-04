---
name: verify-change
description: Select and run checks, reproduce bugs, diagnose failing tests or CI gates, add regression tests or assess requested coverage across Python, TypeScript and integration. Use when something fails, a bug needs reproducing, or a change needs technical evidence. It supplies evidence; validate-change owns acceptance.
---

# verify-change

Read the acceptance criteria, exact diff and `docs/content/docs/equipo/verificacion.md`.
Select [Python](references/python.md), [TypeScript](references/typescript.md) or
[integration](references/integration.md) guidance according to the affected
contract.

## Loop

1. Observable criterion → hypothesis → smallest experiment.
2. The implementer corrects; add a regression that fails before the fix for the
   expected reason and passes afterward.
3. Check observable state, not only internal call counts.

## Selecting checks

- `just backend check` / `just frontend check` for static work.
- `just frontend verify` for functional frontend work.
- `just verify` for integrated backend/frontend work.
- Add API, browser, migration, docs and infrastructure (image build, compose
  config, actionlint/zizmor) checks by impact; root verify does not imply they ran.

Reuse still-applicable results; repeat only after
affected sources, config, fixtures or hypotheses change.

## Output

Report prerequisites, commands, exit codes, test selection, services and the
tested revision using [the evidence contract](../validate-change/references/evidence.md).
Distinguish a change failure, a baseline failure and a missing environment.
Hand the evidence to validate-change; verification does not accept the need.

## Gotchas

- A missing DB/browser, zero selected tests and required skips never count as
  passing.
- Preserve exit codes; do not pipe them away.
- Run checks without autofix; review-change must not repair files.
