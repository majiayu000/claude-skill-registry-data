---
name: assistant-ci-audit
description: "Audit CI and test suites for false passes, discovery gaps, stale fixtures, brittle or duplicate tests, and cost."
---

# CI and Test Maintenance Audit

Investigate whether the named checking system detects important failures and
whether its maintenance work is justified. This Analysis skill diagnoses and
recommends; findings grant no repair, deletion/quarantine, publication, install,
external-write or agent-dispatch authority. Workflow owns approved implementation,
verification owns check selection/assessment, debugging owns unknown failure
isolation, and review owns independent review.

Use this for “CI stays green when its checker fails,” “audit stale fixtures and
repeated preparation,” or “assess generated tests blocking implementation.”
One failing unit test belongs to debugging. Selecting tests for an API change
belongs to verification. Implementing a feature with fewer tests belongs to
workflow; it does not automatically need an audit.

## Procedure

1. **CAPTURE.** Pin repository/revision, dirty state and immutable bounded content identity
   (or explicit unknown), included/excluded paths,
   questions, available evidence and authority. Default to `inspect_only`.
   Establish finite task-specific action/time/resource limits before diagnostics;
   missing execution permission does not block harmless source inspection.
2. **INVESTIGATE.** Load [investigation.md](references/investigation.md). Trace
   discovery/selectors, fixtures, commands/children, reports and final gates,
   including relevant dynamic/non-import edges and duplicate or omitted work.
   Inspect commands before running them. Reuse applicable evidence; historical
   observations remain historical. Only `local_diagnostics` with explicit local
   authority and finite bounds permits execution. Probes use isolated disposable
   inputs or an authorized controlled seam, never working inputs, and require a
   baseline/control, expected/observed detection, cleanup and original hashes.
3. **ASSESS.** Load [test-maintenance.md](references/test-maintenance.md) for
   protection, brittleness, duplicate/obsolete expectations or cost. Establish
   accepted behavior first. Retain unique important protection or a source-backed
   obsolete-expectation rationale; counts and similar code alone justify nothing.
   Measurements need equivalent completed accepted protection and comparable
   conditions; failed/incomplete work cannot establish savings.
4. **REPORT.** Answer each scoped question with evidence or a missing observation.
   Distinguish reproduced defects, supported costs, hypotheses and evidence gaps.
   Preserve source-confirmed maintenance facts separately from unexecuted effects.
   Return actual runs only; empty runs/findings are valid. Stop when scoped
   questions are answered, allowance is exhausted or further attempts add no
   evidence. Material unanswered questions mean `partial` or `blocked`, never a
   concealed complete result. Complete describes this scope, not universal CI.

## Structured boundary

For structured reports and supplied evals, load `contracts/index.yaml`: entry,
current phase, selected investigation/maintenance detail and completion from
`contracts/input.yaml`, `contracts/output.yaml`, and `contracts/phase-gates.yaml`.
Missing or invalid selectors load the full named authoritative file. The initial
contracts are version `1.0`; named AuditScope/Constraints/Summary/Question/
TraceEntry/Run/Finding/Probe/Comparison records use existing YAML object transport,
validated at capture and report. This initial unmerged 1.0 is completed atomically
with its producers/evals; historical missing identity remains unknown with limits.
No new type engine or selection/controller exists.

Keep commands, host/toolchain, observations, gaps and next action bounded and
redacted. Preserve access, destructive-action, paid-call, installation and
private-data boundaries. Planned probes, valid schemas and canned fixture grades
prove neither execution nor native activation, model adherence or task benefit.
