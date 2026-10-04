---
name: ci-wait
description: Discipline for waiting on PR CI, a GitHub subscription, or any background task in grc_library. Use whenever a wait is about to be armed (an Actions-runs CI wait, subscribe_pr_activity, a background command or subagent) or a wait appears stalled.
---

# CI and background-wait discipline

This skill is a trigger wrapper. The procedure of record is `references/ci-wait.md`
(gate 80 manifest-enforced). Read it and apply: the subscription + paired 60-second
fallback-timer shape, the no-MCP timeout-bounded fail-loud read of the GitHub Actions
runs for the PR head SHA (the project avoids `gh pr checks` per the sourced token
limitation in that reference), the `tools/merge-when-green.py <N> --dry-run` final
confirmed-green check, the Background-task check SOP, and the ban on long-interval
self check-ins.
