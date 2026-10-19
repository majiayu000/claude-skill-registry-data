---
name: system-decomposer
description: "Composite: runs the full Löwy's Method decomposition of a system or feature (volatilities → layers → call chains → wiring → diagrams) with a checkpoint after each phase. Invoked by `lowys-method` or by the user with /lowy:system-decomposer."
argument-hint: <system description or requirements>
---

Part of the `lowy` plugin, which depends on the `dmf` plugin: invoke skills by their namespaced name (`lowy:list-volatilities` for this plugin, `dmf:domain-modeling` for DMF).

Execute a full Löwy's Method decomposition for the following system: $ARGUMENTS

**Read** `${CLAUDE_PLUGIN_ROOT}/references/artifact-pipeline.md` first.
All files go to the design directory `cc-docs/design/<topic>/`; settle `<topic>` before Phase 1, so that `dmf:domain-discovery` writes `01` into the same folder when it runs.
If `cc-docs/architecture.md` exists, read it and apply it as described in `${CLAUDE_PLUGIN_ROOT}/references/project-profile.md`.

Follow these phases in order, confirming with the user before advancing to each next phase.
Phase numbers match the numbered files they produce.

## Phase 1: Domain Context (optional)
If `01-domain-discovery.md` exists, use it.
Otherwise ask whether to run `dmf:domain-discovery` first (recommended when the domain is unfamiliar) or to proceed from the requirements alone.

## Phase 2: Decompose → `02-volatilities.md`
Use the `list-volatilities` skill to:
- Identify core use cases (2–6)
- Apply axes of volatility
- Scrub for solutions masquerading as requirements
- Produce a volatilities list
- Map volatilities to candidate services

**Checkpoint:** Present the volatilities list and candidate services. Ask for confirmation.

## Phase 3: Structure → `03-layered-architecture.md`
Use the `classify-structure` skill to:
- Assign each candidate service to a layer using the Four Questions
- Apply naming conventions (PascalCase, correct suffix, correct prefix type)
- Run the Design Don'ts checklist
- Validate ratios (Managers-to-Engines golden ratio)
- Check expendability of each Manager

**Checkpoint:** Present the classified architecture table. Ask for confirmation.

## Phase 5: Validate → `05-call-chains.md`
Use the `validate-use-cases` skill to:
- Produce call chains for each core use case
- Check closed-architecture compliance
- Verify symmetry across call chains
- Validate non-core use cases with the same services

**Checkpoint:** Present call chains and verdict (✅/⚠️/❌). Ask for confirmation.
On ❌, return to Phase 2 for the missing volatility instead of continuing.

## Phase 7: Wire → `07-service-wiring.md` (optional)
Use the `wire-services` skill when the system has more than one subsystem, asynchronous or long-running use cases, or the user asks how services communicate.
Otherwise skip it and say so.

**Checkpoint:** Present the wiring table and event catalog. Ask for confirmation.

## Diagrams
Use the `generate-diagram` skill to:
- Generate a layered architecture overview diagram
- Generate a call chain or sequence diagram for each core use case

Present all diagrams as final deliverables.

## Final Check
Offer `/lowy:design-check <topic>`: it re-traces every use case, simulates a change on each volatility axis, checks `04` when it exists, and lists stale files.
Run it again whenever a numbered file changes.
