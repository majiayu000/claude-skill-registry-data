---
name: incident-triage
description: Use when touching incident-lifecycle / investigation-flow code in Aegis SWR (orchestrator.py, events.py, consensus.py, incident_similarity.py, schemas for Hypothesis/SkepticVerdict/RCAReport/HITLRequest, or any api route that drives an investigation). Checks state-machine completeness, escalation paths, and timeout handling before the change is considered done.
allowed-tools: Read, Grep, Glob, Bash
invocation: /incident-triage
# Ported from Claude (.claude/skills/incident-triage/SKILL.md) on 2026-07-03
# Note: In Claude this skill ran automatically via PostToolUse hook when lifecycle files were edited.
#       In Copilot, invoke /incident-triage manually when touching those files.
---

# Incident Triage Review

You are reviewing a change to Aegis SWR's incident-lifecycle code. Verify the
domain invariants below before declaring the change complete. Delegate a deep
domain judgement to the `incident-analyst` agent if anything looks subtle.

**Read `.github/copilot/skills/incident-triage/references/lifecycle-invariants.md`
first** — it is the code-anchored ground truth for every check below.

> **Copilot note**: In Claude Code this ran automatically via a PostToolUse hook
> when files matching `orchestrator.py`, `events.py`, `consensus.py`,
> `incident_similarity.py`, or lifecycle schemas were edited. In Copilot CLI,
> invoke `/incident-triage` manually whenever you touch those files.

## 1. State-machine completeness

- The live graph is `data_adapter → os_kernel → code_analyst → log_historian →
  skeptic → {output_synthesizer | hitl | loop to os_kernel}`.
- Every state has a defined transition out (success **and** failure). No state
  can be entered without a way to leave it; the only cycle is skeptic → os_kernel.
- The `EventBus` emits a `DomainEvent` for each transition.

## 2. Escalation paths

- `ConfidenceLevel.LOW` or a rejecting `SkepticVerdict` must produce a
  `HITLRequest`, never a silently-emitted weak `RCAReport`.
- There is always a route to a human for ambiguous/failed investigations.

## 3. Timeout & failure handling

- Every external call (debugger subprocess, AI backend, DB, S3, Qdrant) has an
  explicit timeout and a defined fallback.

## 4. De-duplication safety

- Changes to `incident_similarity.py` must not over-suppress genuine new incidents,
  and must not re-alert for already-known root causes.

## Output

Report each check as ✓/✗ with file:line evidence. If any ✗, summarise the gap
and recommend the `python-expert` fix + a `testing-expert` regression test.

## Completion checklist

- [ ] Change verified against `references/lifecycle-invariants.md`
- [ ] Every graph state still has both a success and a failure exit
- [ ] Low-confidence / rejecting-skeptic path still yields a `HITLRequest`
- [ ] Any new node/branch publishes its matching `DomainEvent`
- [ ] Every external call touched has an explicit timeout + defined fallback
- [ ] De-dup change cannot drop a new incident or re-alert an identical root cause
- [ ] No unredacted payload text added to logs, exceptions, stored fields, or AI prompts
