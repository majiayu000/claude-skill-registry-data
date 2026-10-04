---
name: score-the-claim
description: Scores the claim into pays in full, pays in part or does not pay, with the amount payable, the amount cut, and the rule it fails or the evidence it lacks named on every cut. Use it when running `ref/prt/check-and-pay-a-claim`.
license: CC-BY-4.0
metadata:
  agent: claim-check
  agent-version: "1"
---

# Score the claim

## What it does

Scores the claim into pays in full, pays in part or does not pay, with
the amount payable, the amount cut, and the rule it fails or the
evidence it lacks named on every cut.

## Where it happens

The agent does this in one activity across one reference process. Each
one names the activity as that process words it.

- **Score the Claim**
  - `ref/prt/check-and-pay-a-claim`, activity 10 -
    [Check and Pay a Claim](../../../../processes/partners/check-and-pay-a-claim.md)

## What to record

Per claim: the approval it was checked against, at its version, and the
evidence list agreed at that approval. The completeness check, naming
every document the approval asked for and whether it arrived. The match
between the activity claimed and the activity approved, on date, place
and scope. Each evidence item marked present, missing or insufficient.
Each cost line scored against the eligible activity list at its version,
with the rule it passes or fails. The invoice check, naming amounts,
dates, tax treatment and who was actually paid. The duplicate check,
naming where else a cost appeared if it did. The score, with the amount
payable, the amount cut, and a reason on every cut. For any line the
rules could not reach, the person who decided it and what they decided.
A run can be replayed line by line from what it left behind.

That contract covers every activity this abstract agent takes on, and it
is repeated in `com.agentcatalog.agent/RECORDS.md`. What the abstract
agent does not do is in `com.agentcatalog.agent/NOT.md`.
