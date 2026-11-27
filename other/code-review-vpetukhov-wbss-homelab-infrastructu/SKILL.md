---
name: code-review
description: "Perform a read-only, evidence-based .NET pull request review focusing on correctness, security, architecture, performance and tests."
---

# PR / diff review (do not edit files)
- Determine baseline and diff (`git diff --stat`, `git diff --check`, relevant PR/commit); inspect surrounding callsites and tests.
- Hunt in severity order: correctness/data loss; authorization/tenancy/credentials; transaction/retry/concurrency; breaking contracts; EF N+1/query shape; resource leaks/async; architecture regressions; missing tests; maintenance. For async-heavy changes apply `/async-concurrency-review` and the `knowledge/ASYNC_AWAIT_CONCURRENCY.md` checklist (especially lost tasks, shared DbContext, cancellation, and backpressure).
- Verify each finding against actual file/line and concrete scenario; do not invent issues, recommend style-only nitpicks or demand unnecessary patterns.
- Classify **Blocker / High / Medium / Low**, include path:line, exact risk, minimal fix and a test that would catch it.
- Check PR objectives against acceptance criteria, migrations/compatibility, deployment/rollback, observability and backward compatibility.
- Run safe build/test checks only if context/environment permits; never mutate unless user separately requests fixes.
- Output `templates/PR_REVIEW.md` structure; say 'No findings identified' rather than fake praise if clean; explicitly list what was NOT assessed.
