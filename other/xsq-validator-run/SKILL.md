---
name: xsq-validator-run
description: Run the xSquad validator suite in .xsquad/validators/ — core gates first, then feature validators driving the real app with doctor checks, evidence capture, and cleanup — and triage every failure as product bug, validator drift, or environment blocker. Use for /xSq-validator-run, /xsq-validator-run, "run the validators", "verify with validators".
---

# /xSq-validator-run

This is the validator-execution command of the **xSquad** skill. It also doubles as the
orchestrator's continuous verification gate during a squad run. This file lives inside
the xSquad package (its root holds `SKILL.md`, `commands/`, `agents/`, `references/`).

Read `commands/validator-run.md` from the package root — two levels up from this file
(`<package>/commands/validator-run.md`) — and follow that procedure exactly: core wave,
feature wave with its three invariants, failure triage (never weaken a validator to
pass), and the PASS/FAIL report with outcome clean / changed / blocked.

If the package cannot be located from this file's own path, ask the user for the xSquad
package path; do not improvise the procedure.