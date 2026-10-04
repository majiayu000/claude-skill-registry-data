---
name: review
description: Independently review an implemented change against its requirements, risks, scope, and verification evidence.
---

# Review

Review is an evidence-based completion gate performed independently from implementation.

## Stages

1. Read the approved proposal, requirement deltas, tasks, and stated verification results.
2. Inspect the actual diff and surrounding code, including callers and consumers.
3. Check requirement coverage, edge/failure states, compatibility, security, permissions, data handling, accessibility, performance, and scope.
4. Verify important claims with fresh tests, inspection, or direct probes. Treat agent reports as claims, not evidence.
5. Classify findings as blocking, actionable, advisory, or accepted risk.
6. Return precise findings with path/line, impact, rationale, and verification recipe.
7. Approve only when blocking findings are resolved and evidence supports the completion claim.

Review must not become a second implementation pass or expand the proposal without an explicit change decision.

## Duplicate Calls

Before repeating an identical tool call, defined as the same tool name with the same input, require
at least one of these conditions:

- the input changed;
- the prior call failed; or
- the prior output is missing.

Every repeated call must carry a one-line reason stating which condition applies and what new
evidence the call is expected to produce. An unchanged successful call with available output is not
a review step.
