---
name: resolve-repository-state
user-invocable: true
version: 1.2.2
argument-hint: <contradiction-id>
description: >
  Resolve an explicit Normalized Repository State contradiction. This is the
  sole writer allowed to update frozen repository facts or accepted decisions.
  Triggers: "resolve repository state", "resolve contradiction", "update a
  frozen repository fact".
---

# Resolve Repository State

Resolve evidence conflicts explicitly and publish the next frozen snapshot.

## Turn contract

```
✓ A named contradiction and both evidence sources were read
✓ The disposition is accepted, rejected, or needs-input
✓ Accepted/rejected results publish a frozen snapshot; needs-input stops without freezing
✓ No unrelated fact or decision changed
✓ The closing → Next: block is printed last
```

## Step 0 — Discover the project (always first)

Read the agent guide, documentation map, frozen ledger, and the requested
contradiction before deciding anything.

## Process

1. Read the frozen ledger and the contradiction row named by the user.
2. Verify both the frozen fact's evidence and the proposed new evidence.
3. Choose one result: accept new evidence, reject it, or request human input.
4. If human input is required, update the contradiction row with the exact
   missing evidence or decision, keep snapshot status `contradicted`, and stop
   without incrementing the snapshot identifier or publishing a frozen snapshot.
5. For an accepted result, supersede the fact or decision with a new row that
   cites both evidence sources. For a rejected result, retain the fact and
   record why.
6. For accepted or rejected results only, update the contradiction row,
   increment the snapshot identifier, set status to `frozen`, and record the
   next frozen snapshot's source revision.

## Guardrails

- This skill is the sole writer for updates to frozen facts and accepted decisions.
- A consumer may propose a contradiction but never resolve it inline.
- Inference and documentation alone are insufficient to update a fact.

## Portability

Without a slash menu, open this file and follow its process in a fresh turn.

## Relationship to other skills

Consumes contradictions from every workflow role and produces the snapshot that
discovery, planning, execution, review, and audit reuse. The contradiction's
`Reported by` field identifies the interrupted role to resume; resolution never
defaults a review, audit, or status interruption to planning.

## Done when

The contradiction has a recorded disposition, and either the next frozen
snapshot is internally consistent or the missing human input is explicit.

If human input is required:

→ Next: provide the requested evidence or decision — resolution cannot continue yet
  · evidence supplied → rerun /resolve-repository-state <contradiction-id>

Otherwise:

→ Next: resume the interrupted workflow named by `Reported by` — continue from the resolved snapshot
  · planning was interrupted → /unit-lane <slug>
  · implementation was interrupted → /execute-phase <NN>
  · review, audit, or status was interrupted → rerun that same skill
