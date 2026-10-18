---
name: requesting-code-review
description: Use when a change is ready for another reviewer, before merging it or asking for approval.
---

# Requesting Code Review

A reviewer works from what you hand them, not from the process that produced it. Give them a diff
and just enough context to judge it — not a narrative of how the work went.

## Guardrails

- Hand over the actual diff (or PR link), not a description of the diff. A reviewer who has to
  reconstruct what changed from prose will miss what the prose omitted.
- State what changed, why, and how it was verified — three short items, not a changelog.
- Keep the change reviewable in size. A diff too large to read in one sitting gets a shallower
  review than a smaller one, regardless of how carefully the reviewer means to read it. Split it if
  it covers more than one concern.
- Name open questions and known risks explicitly. A reviewer who has to discover a risk you already
  knew about is doing your job as well as theirs.
- Do not claim a check passed unless you ran it and read the output — see the
  `verification-before-completion` skill.

## What this is not

Not a request to pad the review with justification for every line. State the change and let the
diff speak for the mechanics; reserve prose for what a diff cannot show — intent, tradeoffs, what
was deliberately left out.

## Integration contract

When used by `plan-driven-build`, receive the plan, review base, current head, verification evidence,
and global constraints. Produce a uniquely named review package and a request containing the change,
risk, verification status, and open questions. Do not implement fixes or decide whether a finding is
accepted.
