---
name: pr-release-guardrails
description: "Trigger: PR review, CI, release, deploy, rollback. Assess NutrIA changes before human approval."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use before merge or release.

# Hard Rules
- No automatic merge, deploy or approval.
- Check linked Linear issue, tests, migration safety, secrets, performance and accessibility impact.
- A missing test is an explicit risk, not a passing check.

# Execution Steps
1. Reconcile diff to acceptance criteria and architecture decision.
2. Inspect CI/test evidence and migration/rollback plan.
3. Return only actionable findings by severity.
4. Link findings to Linear and preserve release learnings in Engram.

# Output Contract
Return ready/not-ready recommendation, evidence and owner for each blocker.
