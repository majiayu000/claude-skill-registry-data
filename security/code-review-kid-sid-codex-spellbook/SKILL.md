---
name: code-review
description: Pull request review guidance for correctness, security, tests, performance, API contract drift, migrations, and error handling. Use when reviewing diffs, pull requests, or risky refactors.
---

# Code Review

Review code for correctness first, then for safety, operability, and maintainability.

## When to Activate

- Review a pull request before approval
- Audit a migration or rollout plan
- Check for missing tests on changed logic
- Evaluate API or schema contract changes
- Inspect security-sensitive authentication code
- Separate blockers from optional cleanup
- Summarize review findings for a teammate

## Review Order

| Priority | Check |
| --- | --- |
| 1 | Logic correctness and regression risk |
| 2 | Security, privacy, and data integrity |
| 3 | Test coverage and validation gaps |
| 4 | Performance, scaling, and resource usage |
| 5 | Style, naming, and cleanup |

## Blocking vs Suggestion

| Comment Type | Use When | Prefix |
| --- | --- | --- |
| Blocking | Incorrect behavior, security hole, migration risk, broken contract | `Blocking:` |
| Suggestion | Readability improvement, minor cleanup, non-critical refactor | `Suggestion:` |
| Question | Intent or assumption is unclear | `Question:` |

## What to Check

| Area | Questions |
| --- | --- |
| Logic | Are edge cases, retries, and failure paths handled? |
| Security | Are auth checks, secrets, and untrusted inputs handled safely? |
| Tests | Do tests cover new behavior and likely regressions? |
| Performance | Does this add N+1 queries, repeated allocations, or hot-loop work? |
| API contracts | Will clients or jobs break on shape changes? |
| Migrations | Is rollout safe across old and new code versions? |
| Error handling | Are failures explicit, typed, and observable? |

## Tone

| Preferred | Avoid |
| --- | --- |
| Direct, specific, file-scoped feedback | Vague comments like "this feels wrong" |
| Explain impact | Nitpicks framed as blockers |
| Offer a fix path when practical | Personal or emotional language |

BAD

```text
This code is bad. Please redo.
```

GOOD

```text
Blocking: [payments/service.ts] charge retries on 500 but not on timeout, so transient network failures can still drop payments. Add retry handling for socket timeout errors and cover it with a test.
```

## Checklist

- [ ] Logic changes were checked against edge cases and failure paths
- [ ] Security-sensitive code paths were reviewed explicitly
- [ ] New behavior has sufficient test coverage
- [ ] Performance-sensitive paths were inspected for regressions
- [ ] API contract changes are documented and compatible
- [ ] Migrations are safe for mixed-version deploys
- [ ] Feedback is labeled as blocking, suggestion, or question
