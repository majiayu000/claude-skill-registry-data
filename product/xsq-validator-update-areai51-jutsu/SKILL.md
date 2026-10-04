---
name: xsq-validator-update
description: Upkeep pass keeping the xSquad validator suite honest — re-ground every validator against current source via a parallel read-only source wave, re-prove features live, and ship proven corrections; includes the orchestrator's lighter mid-run variant. Use for /xSq-validator-update, /xsq-validator-update, "update the validators", "audit the validator suite".
---

# /xSq-validator-update

This is the validator-upkeep command of the **xSquad** skill. This file lives inside the
xSquad package (its root holds `SKILL.md`, `commands/`, `agents/`, `references/`).

Read `commands/validator-update.md` from the package root — two levels up from this file
(`<package>/commands/validator-update.md`) — and follow that procedure exactly: index
hygiene, concurrent source wave per validator, reconcile, live pass under the run
invariants, triage (doc drift vs harness gap vs product bug), and the clean / changed /
blocked outcome. Inside a squad run, use its **mid-run variant**: only the validators
covering the changed surface, re-proved once, index updated.

Edit scope is only `.xsquad/validators/` — never product code.

If the package cannot be located from this file's own path, ask the user for the xSquad
package path; do not improvise the procedure.