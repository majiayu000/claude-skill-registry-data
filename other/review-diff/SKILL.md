---
name: review-diff
description: Use when reviewing a working-tree diff or specified local Git range and reporting only actionable, evidence-backed findings.
---

# Review Diff

Use this as the minimal read-only path for an explicitly scoped working-tree
diff or local Git range when contract reconciliation is not requested. It does
not require a SPEC and is not part of an approval workflow.

## Review contract

- If no scope is supplied, review the current working-tree diff. If a scope is
  supplied, verify it is a valid local Git diff range before reviewing it.
- Inspect only the requested diff and the minimum adjacent code needed to assess
  it. Do not edit files, run tests, fetch, access external resources, or change
  Git state.
- Report actionable correctness, security, performance, regression, compatibility,
  concurrency, error-handling, and maintainability findings only. Do not restate
  the diff or invent findings.
- Redact secrets, credentials, tokens, private data, and sensitive configuration
  from finding text and quoted evidence. Report the existence and location of a
  sensitive value without reproducing it.
- Order findings by severity. Every finding must include a concise title, exact
  file and line evidence, impact, and a concrete remediation direction.
- If there are no actionable findings, say so in one sentence. Then list only
  concise residual risks and testing gaps. A finding-free result is a review
  verdict, not user approval of the change.
- Do not approve, merge, commit, push, publish, deploy, or modify the reviewed
  work. The user retains every follow-up decision.
