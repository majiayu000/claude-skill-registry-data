---
name: github-actions
description: "Build and debug GitHub Actions CI: quality gates, caching, failure triage, safe secrets. Use when creating workflows or fixing red CI."
---

# github-actions

Reproduce CI failures locally first; keep pipelines fast, hermetic, and least-privileged.

## Activate when

- Creating/modifying workflows, fixing failing checks, or addressing review comments about CI.

## Do NOT activate for

- Release tagging/versioning (see git/git-release) or PR content itself (see github/pr-workflow).

## Procedure

1. Gates: lint → typecheck → test → build; fail fast; pin actions by SHA; minimal `permissions:` per job; secrets via encrypted secrets, never logs.
2. Speed: cache deps properly keyed; matrix only what differs; split slow suites by path and duration.
3. Triage red CI: read the failing step log, reproduce with the same command locally, fix, then confirm the same command passes locally.
4. Review comments: address each with a code change or an evidence-backed reply (`references/` fixer for comment triage lives in github/pr-workflow).
5. Verify: green run on the PR, no skipped-required-checks, logs free of secrets.

## References
- Related: `../docker-compose/`, `../../tooling/ci-cd/`, `../../security/secrets-supply-chain/`.
