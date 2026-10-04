---
name: orchestration-envelope
user-invocable: false
version: 2.2.1
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal machine-result contract for headless agentic-workflow drivers. The
  executable source is @gtrabanco/agentic-workflow-schema: strict Envelope v2
  for workflow-status, compact SkillOutcome v1 for driven work, compatibility
  parsing, and deterministic document snapshots. Not a menu entry.
---

# Machine result contract (internal)

Interactive skills remain text-first. A headless driver obtains a compact,
validated result at the boundary; it does not add a repeated JSON section to
every user-facing skill.

The canonical [Turn contract](references/TURN_CONTRACT.md) remains here for
the executor and review skills that load it.

The executable source of truth is
[`@gtrabanco/agentic-workflow-schema`](../../packages/agentic-workflow-schema/):
types, JSON Schemas, `renderOutputInstruction(skill)`, `parseTurn(input)`, and
`compileWorkflowSnapshot(input)`. This document states the policy only; do not
copy a second schema here.

## Output profiles

`WORKFLOW_SKILL_PROFILES` is the authoritative inventory.

- `workflow-status` always returns the strict **Envelope v2** sensor result.
  Its envelope includes the detailed project view under `detail`.
- The other driver-invoked skills return **SkillOutcome v1** only when the
  driver appends `renderOutputInstruction(skill)` to that invocation. It has
  the small model-owned fields: outcome, next intent/targets, blockers,
  questions, discoveries, and evidence references.
- `advance` (the companion pi package command) is the conductor, not a worker
  profile: it runs as deterministic code over the sensor envelope and never
  emits a worker SkillOutcome.
- Interactive invocations emit their normal human-readable reports; no driver
  result is required.

Both results are one final fenced `json` block. The package rejects unknown
keys at the routing boundary. Repository facts are never reconstructed from
model prose: the driver compiles `WorkflowSnapshot v1` from its selected,
versioned documents and caller-supplied repository facts.

## Driver protocol

1. Read the profile and append `renderOutputInstruction(skill)` only for a
   driven invocation.
2. Pass the final response to `parseTurn({skill, text, context})`. Keep the
   returned source and diagnostics with the run journal.
3. On an absent, malformed, or invalid machine result, re-invoke the same
   session once with: `Emit only the machine result for the turn above.`
4. Parse the repair reply. A second failure is driver-level `FAILED`; never
   retry indefinitely and never turn arbitrary prose into workflow facts.

Compatibility is deliberately narrow: it can repair documented legacy v2
shapes only when the missing value is mechanically knowable. A nonzero issue
count without issue identities, an unmatched numeric unit id, or unrelated
prose remains invalid and is surfaced to the driver.

## Contract evolution

- Envelope v2 is strict for new drivers. `detail` is required (usually `null`)
  and skill-specific extensions live inside it; `design_candidates`, for
  example, is `detail.design_candidates`, never a root key.
- `workflow-status` retains Envelope v2 for existing sensor consumers.
  `parseEnvelope()` remains the legacy-compatible package API; new consumers
  use `parseEnvelopeV2Strict()` or `parseTurn()`.
- `SkillOutcome v1` and `WorkflowSnapshot v1` are separate, versioned JSON
  Schemas. A breaking change to any published contract is a package major.

## Normalized Repository State

Drivers call `discover-repository-state` before planning and retain the frozen
`docs/workflow/REPOSITORY_STATE.md` reference. `WorkflowSnapshot v1` preserves
unknowns, provenance, and declared contradictions; a driver routes a
contradiction to `resolve-repository-state` rather than silently replacing it.
