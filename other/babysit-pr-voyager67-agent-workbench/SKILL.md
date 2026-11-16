---
name: babysit-pr
description: Monitor a GitHub pull request's check state and follow up on actual failures. Use when asked to watch CI or keep an existing PR moving.
---

# Babysit a Pull Request

The bundled watcher reports GitHub check-state changes only. It does not inspect review threads, prove application correctness, or certify merge readiness.

1. Confirm the PR number/URL, repository, intended monitoring window, and available authenticated `gh` CLI.
2. Run `scripts/pr_wait.py <PR number or URL>` from this skill directory. Use a reasonable interval; stop with Ctrl+C when monitoring is no longer needed.
3. Inspect failing checks by opening their linked logs. Identify the actual failing command and affected code.
4. Reproduce locally where practical, fix only validated issues, and rerun relevant tests.
5. Check review threads and required approvals separately in GitHub; the watcher does not do this.
6. Report status, failure details, fixes, checks rerun, and unresolved blockers.

Do not push fixes, dismiss reviews, re-run expensive jobs, or merge without authorization. Never report readiness based on a green check list alone.
