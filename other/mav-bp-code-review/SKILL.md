---
name: mav-bp-code-review
description: Code review conventions for all projects. Covers mandatory review requirements, review scope, PR sizing, reviewer and author responsibilities, and automated review integration. Applied when creating or reviewing pull requests.
user-invocable: false
disable-model-invocation: true
---

# Code Review Standards

Ensure all code changes are reviewed before merging; in Maverick the reviewer is agent-code-reviewer running in-session, backed by branch-protection gates.

## Maverick's Rules

- **No unreviewed merges**: at least one approval on protected branches; no self-approval; stale approvals are dismissed when new commits are pushed; all CI checks must pass. Never disable or skip a check to merge faster — fix the check or the code.
- **Security is out of scope for PR review** — it runs as a separate pre-push gate via `do-cybersecurity-review` (update mode against the diff and impact set) before the PR is opened. By review time, security findings are already surfaced and folded into the PR body.
- **Review scope**: correctness, maintainability, test coverage, documentation. Style and formatting are the linter's job — do not comment on them. Do not review generated code (codegen, lockfiles) line by line, and do not request changes to correct-but-different approaches on personal preference.
- **Verdict discipline**: distinguish blocking findings from non-blocking (prefix "nit:" or "optional:"); demonstrate understanding of the change rather than rubber-stamping; approve once the code is correct, tested, and maintainable — do not hold changes hostage for perfection. AI review findings require judgement — dismiss false positives with reasoning, never silently.
- **Automated checks pass before review begins** — do not review code that fails lint, type checks, or tests.

## PR Size

| Size              | Lines changed | Review quality | Recommendation                                |
| ----------------- | ------------- | -------------- | --------------------------------------------- |
| **Small**         | < 100         | Excellent      | Ideal. Aim for this size.                     |
| **Medium**        | 100 - 400     | Good           | Acceptable for most feature work.             |
| **Large**         | 400 - 800     | Declining      | Split if possible. Flag to reviewers.         |
| **Too large**     | > 800         | Poor           | Must split. Reviewers cannot effectively review this. |

Split strategies: by layer (backend vs frontend), by feature slice (one endpoint/component per PR), by phase (refactor PR before feature PR), or by dependency (extract shared utilities/models into a preparatory PR).

## Detecting Code Review Anti-Patterns

| Pattern                                           | Issue                              | Fix                                                  |
| ------------------------------------------------- | ---------------------------------- | ---------------------------------------------------- |
| PR merged without any review                      | No review gate                     | Enable branch protection requiring approvals         |
| PR with 1000+ lines changed                       | Too large to review effectively    | Split into smaller, focused PRs                      |
| All review comments are style nits                 | Wasted review effort               | Configure linters to catch style; focus on logic     |
| Reviewer approves without comments on large PR     | Rubber-stamp review                | Reviewers must demonstrate understanding of the change |
| Author pushes "fix review" commits without context | Lost review trail                  | Explain what was changed in response to which comment |
| Self-approval on protected branch                  | Missing review gate                | Configure branch protection to disallow self-approval |
| Skipping CI to merge faster                        | Bypassing quality gates            | CI must pass; fix failures, do not skip them         |

<!-- maverick-plugin-version: 4.0.2-dev -->
