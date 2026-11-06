---
name: incident-triage
description: Use when touching incident-lifecycle / investigation-flow code in Aegis SWR (orchestrator.py, events.py, consensus.py, incident_similarity.py, schemas for Hypothesis/SkepticVerdict/RCAReport/HITLRequest, or any api route that drives an investigation). Checks state-machine completeness, escalation paths, and timeout handling before the change is considered done.
allowed-tools: Read, Grep, Glob, Bash
invocation: auto
---

<!-- Triggered automatically by: PostToolUse(Write|Edit) hook when the edited
path matches orchestrator.py, events.py, consensus.py, incident_similarity.py,
or schemas containing Hypothesis / SkepticVerdict / RCAReport / HITLRequest -->

# Incident Triage Review

You are reviewing a change to Aegis SWR's incident-lifecycle code. Verify the
domain invariants below before declaring the change complete. Delegate a deep
domain judgement to the `incident-analyst` agent if anything looks subtle.

**Read [references/lifecycle-invariants.md](references/lifecycle-invariants.md)
first** — it is the code-anchored ground truth for every check below (the real
LangGraph node names, the exact convergence rule and thresholds, the six
`DomainEvent`s, and the escalation/timeout/de-dup invariants). The summary here
is the checklist; that file is the authority.

## 1. State-machine completeness

- The live graph is `data_adapter → os_kernel → code_analyst → log_historian →
  skeptic → {output_synthesizer | hitl | loop to os_kernel}`.
- Every state has a defined transition out (success **and** failure). No state
  can be entered without a way to leave it; the only cycle is skeptic → os_kernel.
- The `EventBus` emits a `DomainEvent` for each transition so views stay in sync
  (six types — see the reference's EventBus table).

## 2. Escalation paths

- `ConfidenceLevel.LOW` or a rejecting `SkepticVerdict` must produce a
  `HITLRequest`, never a silently-emitted weak `RCAReport`.
- There is always a route to a human for ambiguous/failed investigations.

## 3. Timeout & failure handling

- Every external call (debugger subprocess, AI backend, DB, S3, Qdrant) has an
  explicit timeout and a defined fallback. No unbounded waits, no half-written
  reports.

## 4. De-duplication safety

- Changes to `incident_similarity.py` must not over-suppress: a genuinely new
  incident must never be dropped as a duplicate (missed escalation), and the
  same root cause must not re-alert repeatedly (alert fatigue).

## Output

Report each check as ✓/✗ with file:line evidence. If any ✗, summarise the gap
and recommend the `python-expert` fix + a `testing-expert` regression test. If the logic is subtle,
hand off to the `incident-analyst` agent for a full lifecycle assessment.

## Completion checklist

- [ ] Change verified against [references/lifecycle-invariants.md](references/lifecycle-invariants.md)
- [ ] Every graph state still has both a success and a failure exit; the only cycle remains skeptic → os_kernel
- [ ] Convergence still requires all three conditions (skeptic ≥ 0.65, consensus ≥ threshold, stable hypothesis); the max-rounds → HITL fallback is intact
- [ ] Low-confidence / rejecting-skeptic path still yields a `HITLRequest`, never a silent weak `RCAReport`
- [ ] Any new node/branch publishes its matching `DomainEvent` so views do not stall
- [ ] Every external call touched has an explicit timeout + defined fallback; store writes remain best-effort
- [ ] De-dup change cannot drop a new incident or re-alert an identical root cause
- [ ] No unredacted payload text added to logs, exceptions, stored fields, or AI prompts
- [ ] Each check reported ✓/✗ with `file:line` evidence; subtle logic handed to `incident-analyst`
