---
name: status
description: Show every codex-claude-loop slug and where it stands (plan/review gates, impl marker, base)
allowed-tools: Bash, Read
---

Load the `codex-claude-loop` skill, source its lib, and run `cl_status`.

The PLAN and REVIEW columns show `approve` only when that approval is still **valid for
the current state**: the plan still hashes to what was approved, and the review still
matches this tree. A column showing the recorded word instead means the approval no
longer binds.

For each slug that is not fully approved, say in one line what the next action is: plan
needs reading, plan needs re-briefing, impl not run, impl failed, diff needs review,
blocking items need `cl_revise`, or the tree moved and needs re-review.

For a slug where both gates hold, say it is ready for `cl_release`. Do not claim it has
been released: this harness tracks gates, not deploys, so whether it shipped is something
you have to check in the project's own way (git log, tags, the deploy target).
