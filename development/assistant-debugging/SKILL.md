---
name: assistant-debugging
description: "Diagnose an unknown failure by reproducing and isolating before fixing. Use for debugging, root causes, flaky tests, or unexplained breakage."
requires:
  - assistant-review
  - assistant-verification
  - assistant-tdd
---

# Evidence-First Debugging

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Explain the failure with evidence, then make the smallest authorized durable fix.
A diagnosis-only request authorizes investigation, not source changes.

## Method

1. **Bound and reproduce.** Establish observed versus expected behavior, affected
   path, recent changes, and diagnostic safety. Run the smallest safe reproduction
   or record the concrete blocker and available logs/code/config evidence.
2. **Test plausible causes.** Rank causes by evidence, diagnostic value, cost,
   and safety. Use checks that distinguish them; retain disconfirming results.
   There is no hypothesis quota. If all are refuted, gather new evidence.
3. **Fix when authorized.** Do not patch from a guess. Before a fix or mutation
   dispatch, use assistant-verification and preserve its decision, selected IDs,
   and binding obligations. Active TDD routes through assistant-tdd's execution
   lane and meaningful authorizing RED; the generic fixer is only for inactive
   TDD. Label an uncertain emergency change as mitigation.
4. **Verify the original path.** Run the original reproduction and selected/
   binding checks against the fix. Preserve unavailable, partial, failed, and
   skipped results as gaps. Every fix, local repairs included, gets a local
   self-check plus fresh independent assistant-review. An active TDD fix needs
   the complete current canonical cycle.

## Boundaries and handoffs

Use local company-safe diagnostics; redact secrets and private data. Honor
explicit authorization before destructive, production-affecting, network,
migration, or sensitive diagnostics. Ask only for missing material information
that cannot be discovered safely. Generic workflow coordinates plan, delegation,
and review; this skill owns reproduction and cause evidence.

Load `contracts/index.yaml` for a structured diagnosis, fix/handoff, persisted
continuation, or executable consumer. Load only the current boundary: `entry`,
`current_phase`, `fix_verification` before mutation, `selected_handoff` before
selected delegation, and `completion`. Missing/invalid selectors load the full
named contract. Current v3 fix contracts preserve canonical verification/TDD
bindings and accept validated TDD v3 `reuse_green`; persisted v2 fixes stay
readable; a persisted v1.1 fix needs a refreshed decision, never inferred checks
or RED.

Load [reproduction.md](references/reproduction.md) when no adequate
exact-symptom reproduction exists yet. Load
[state-inspection.md](references/state-inspection.md) for an unresolved
runtime-state question in Python, Node or .NET that the reproduction, traceback
or logs cannot answer. Work that already has an exact-symptom reproduction loads
neither. Record `yes` or `partial` by the `reproduced` description in
`contracts/output.yaml`.

For affected acquisition/readiness, active work, cancellation, collection/finalization, shutdown, owned resources, cleanup or retry, load
`lifecycle` from the index and [lifecycle-verification.md](references/lifecycle-verification.md)
during reproduction/isolation and before fix verification. Synchronous or cosmetic
work alone adds no lifecycle loading or gate.

Load [change-impact.md](references/change-impact.md) when diagnosis/repair
consumer impact matters. Record compact applicability; shared, materially
unresolved, or explicitly carried expanded repairs retain the common artifact
and pre-Build/completion checklist results from assistant-review's expanded-work
checklist; no script or runtime is needed. Debugging 4.0 replaced the checker
receipt (`validator_result_ref`) with `checklist_result_ref`; older packets stay
readable as described in that reference.

## Result and stop rules

Explain the symptom, reproduction or blocker, supported cause, authorized fix,
verification, and remaining uncertainty. Include hypotheses that explain the
reasoning, without a full empty report template. Structured consumers retain
`contracts/output.yaml` fields and actual partial TDD logs.

Stop speculative edits when the failure is neither reproduced nor sufficiently
bounded. Say root_cause_found, mitigated, not_reproduced, blocked, or inconclusive
when the evidence does not establish a verified fix; never overstate causality.
