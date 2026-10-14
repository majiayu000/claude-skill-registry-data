---
name: code-review
description: "Review the actual diff defect-first with evidence: correctness, security, performance, compat, tests. Severities blocker/high/maintainability/optional. No stylistic nitpicks as defects."
---

# code-review

Read the diff, not just the files. Every finding needs evidence, a severity, and a fix.

## Activate when

- Before merging any change; after finishing a feature; when asked to review.
- Self-review before claiming completion (with `git diff` + test output as evidence).

## Do NOT activate for

- Responding to review feedback received (address comments per github/pr-workflow).
- Security-deep audits (see security/secure-baseline) or pure formatting (see tooling/formatting).

## Procedure

1. Intent: state what the change claims to do in one paragraph; list every file touched and flag unrelated scope.
2. Trace: callers → changed code → dependencies; follow data flow into sinks (DB, shell, FS, network, auth).
3. Check, in order: correctness, security (authz on new paths, injection, secret leaks), error handling, concurrency, performance (N+1, unbounded work), API/backward compatibility, migrations, tests, docs.
4. Confidence: HIGH (proven by test/trace) first; MEDIUM with reproduction steps; LOW marked needs-confirmation, never a blocker.
5. Severity: blocker (must fix before merge), high-risk (fix now), maintainability concern (fix or track as debt), optional improvement (author's call).
6. Verify: confirm tests cover each blocker fix; re-read the final diff; never claim "reviewed, all good" without listing what was checked.

## References
- Feedback replies: `../../github/pr-workflow/`.
- Security integration: findings in auth/input/crypto/secrets escalate to `../../security/secure-baseline/`; the security review runs on the implementation, then this review re-verifies the final diff — never the reverse order.
