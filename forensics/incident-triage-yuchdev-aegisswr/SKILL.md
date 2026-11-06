---
name: incident-triage
description: >-
  Use when touching incident-lifecycle / investigation-flow code in Aegis SWR
  (orchestrator.py, events.py, consensus.py, incident_similarity.py, schemas
  for Hypothesis/SkepticVerdict/RCAReport/HITLRequest, or any api route that
  drives an investigation). Checks state-machine completeness, escalation
  paths, and timeout handling before the change is considered done.
allowed-tools: Read, Grep, Glob, Bash
invocation: auto
---

# Incident Triage Review

You are reviewing a change to Aegis SWR's incident-lifecycle code. Verify the
domain invariants below before declaring the change complete. Delegate a deep
domain judgement to the `incident-analyst` agent if anything looks subtle.

## 1. State-machine completeness

- Lifecycle: `detected/ingested → triaged → analysed → validated → reported →
  resolved → post-mortem`; code states `INITIALIZING → EXTRACTING → PARSING →
  ANALYZING → STORING`.
- Every state has a defined transition out (success **and** failure). No state
  can be entered without a way to leave it.
- The `EventBus` emits a `DomainEvent` for each transition so views stay in sync.

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
