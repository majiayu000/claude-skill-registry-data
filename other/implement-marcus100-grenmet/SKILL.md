---
name: implement
description: "Implement a piece of work based on a PRD or set of issues."
disable-model-invocation: true
---

Implement the work described by the user in the PRD or issues.

Before writing code, restate the task contract in a few lines: deliverable,
constraints, non-goals and the acceptance check that closes the task. Take it from
the issue's sections when they exist; ask only if a field cannot be inferred.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, review the final diff against the contract and Blast-Radius Gate. Then
run `node scripts/guardrails/risk-tier.mjs --base origin/dev`: for `standard` or
`high`, run `/code-review` (Codex: `/review`) so a fresh context reviews the diff, and fix or answer
every finding before committing. Follow the failure budget in `AGENTS.md`.

After required checks pass and the final diff is reviewed, agents may stage,
commit, push and open a PR for the authorized work without further confirmation.
Preserve unrelated changes, follow the repository branch/promotion workflow and
never bypass hooks or force-push. Merges and deployments still require explicit
user authorization under `AGENTS.md`.
