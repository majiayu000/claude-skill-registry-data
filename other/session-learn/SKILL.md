---
name: session-learn
description: Use when a completed work session should yield durable concepts, corrections, decisions, reusable patterns, and a traceable next action.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "The session transcript, artifacts, or execution receipts are available."
  conflicts_with: "Claiming automatic capture without a configured hook, storing raw noise as knowledge, or changing immutable sources."
---

# Session Learn

<skill_contract>
  <input>Completed session objective, actions, artifacts, verification receipts, errors, decisions, and destination paths.</input>
  <output>Deduplicated durable deltas for concepts, entities, corrections, patterns, ideas, decisions, and gaps.</output>
  <done>Each retained delta is formatted, linked, logged, provenance-preserving, and paired with a traceable next action when unresolved.</done>
  <non_goals>Automatic-capture claims without a hook, raw transcript storage, conversational filler, or immutable-source edits.</non_goals>

Close a session by extracting only reusable deltas. Invocation must be explicit or performed by a verified external hook; this skill never claims it ran automatically.

## Usage Template

Provide: session objective, actions, outputs, verification receipts, errors, decisions, and destination paths. Optional: existing notes for deduplication.

## Workflow

<intake>

Establish the session boundary and compare intended versus observed result. Ignore conversational filler and separate execution evidence from retrospective interpretation.

</intake>

<unknowns_gate>

If the session outcome or evidence is unavailable, return `INSUFFICIENT_EVIDENCE`. Ask for a missing artifact only when it determines whether a lesson is valid; otherwise preserve it as an unresolved gap.

</unknowns_gate>

<execute>

Scan for seven signal types:

1. **Concept** — a stable mechanism worth linking.
2. **Entity** — a person, system, project, or tool requiring durable context.
3. **Correction** — a prior belief or procedure disproved by evidence.
4. **Pattern** — a reusable Trigger -> Execute -> Verify -> State sequence.
5. **Idea** — an untested possibility, explicitly provisional.
6. **Decision** — choice, rationale, alternatives, owner, and review condition.
7. **Gap** — an unknown with a probe or escalation path.

Apply Closure Protocol: **Format** the smallest durable note, **Link** it to source/project/concepts, and **Log** the write plus verification. Merge semantic duplicates; preserve source immutability and provenance.

</execute>

<evaluate>

For each candidate ask: Is it new, reusable, traceable, and decision-relevant? Reject session-specific trivia and unsupported generalizations. Confirm each write exists and links resolve before reporting closure.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus session id, extracted candidates, accepted/rejected reasons, write paths, links, and closure receipt. Append corrections; do not erase superseded beliefs.

</state_contract>

## Failure Protocol

- `INSUFFICIENT_EVIDENCE`: artifacts cannot establish the lesson; preserve it as a gap.
- `BLOCKED_PERMISSION`: the destination is read-only; return the proposed note and path without claiming a write.
- `VERIFY_FAILED`: a write or link check fails; repair once or return the exact failure.
- `BUDGET_STOP`: rank remaining candidates by reuse value and persist the queue.

## Output Contract

Return `status`, `result` (accepted knowledge deltas), `evidence` (session receipts and write checks), `unknowns`, and `next_action`.

## Edge Cases

- The same concept already exists: update or link the durable note; do not create a title variant.
- The session ended unsuccessfully: capture the falsified assumption, failure evidence, and recovery path rather than a false success pattern.

## Success Metrics

- Every accepted learning is traceable to session evidence.
- Durable notes are deduplicated, linked, and verified after write.
- At least one correction, decision, pattern, or gap improves future execution when present.

## Quality Gates

- [ ] Invocation provenance is explicit; no fake auto-trigger claim.
- [ ] Facts, interpretations, and ideas are distinguishable.
- [ ] Source material remains immutable.
- [ ] Closure includes Format, Link, Log, and a receipt.

</skill_contract>
