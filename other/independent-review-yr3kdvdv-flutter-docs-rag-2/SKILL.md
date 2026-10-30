---
name: independent-review
description: Review a ready PR or commit against requirements with evidence. Use for review of a specific SHA; reports findings with priority, file/line, scenario, evidence and minimal fix.
---

# independent-review

## Inputs
Commit SHA or PR number, `docs/requirements.md`, `docs/architecture.md`, latest handoff.

## Steps
1. Record the reviewed SHA (`git rev-parse HEAD`) and that the tree is clean.
2. Re-run documented setup and tests yourself; quote real exit codes.
3. For each finding: priority (P0 blocker / P1 / P2), file:line, failure scenario, evidence,
   minimal fix. Separate defects from hypotheses and optional improvements.
4. List checks you could not run and why.
5. State the reviewing tool and model honestly. A Claude subagent reviewing Claude's code is
   not an independent model review; say so.

## Outputs
`docs/reviews/<topic>.md` (or text if no write access) with SHA and findings.

## Boundaries
Do not modify the code under review. Do not merge.
