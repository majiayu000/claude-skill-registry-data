---
name: fix-issues
description: "Use when the user says 'fix issues' or asks why the current PR is not merge ready: merge conflicts, failing CI (Buildkite or GitHub Actions), failing build, or PR metadata problems. Does not handle review comments (use tony:pr-comments)."
---

# Fix Issues

## Purpose

Find and fix everything other than review comments that blocks the
current PR from being merge ready.

Invoking this skill is the explicit request to commit and push for this
run. It does not carry over to any other work in the session.

## Scope

- **In:** merge conflicts, failing Buildkite builds (if the repo uses
  Buildkite), failing GitHub checks and build errors, PR metadata (title,
  labels, description, draft state), and any other non-comment blocker
  `gh` reports.
- **Out:** review comments and review threads. Hand those to
  `tony:pr-comments`.

## Process

1. **Find the PR.** Run
   `gh pr view --json number,url,title,body,labels,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,baseRefName`.
   If it fails, stop and say what is missing.

2. **List every blocker** before fixing any. Check:
   1. `mergeable` and `mergeStateStatus`: conflicts or a stale base.
   2. `statusCheckRollup`: each failed or errored check, with its URL.
   3. Buildkite, if `.buildkite/` exists or a check links to
      buildkite.com: use the Buildkite MCP tools
      (`get_build_failure_summary` first) to find failing jobs.
   4. PR metadata: title format, labels, description, ticket link,
      draft state. Follow the repo's CONTRIBUTING and the user's
      global rules.
   5. Anything else `gh pr checks` or `gh pr view` flags.
   Ignore pending checks and soft failures. Skip review comments.

3. **Classify each blocker** as fixable here (code, merge, config,
   metadata) or not (needs approval, outside access, flaky infra).
   Report the second kind without acting on it.

4. **Fix in this order:**
   1. Merge conflicts: follow `tony:fix-merge-conflicts`.
   2. Build, lint, type, and test failures: reproduce locally, find the
      root cause from the logs, fix it. Do not retry a red build hoping
      it passes. Re-run only when the logs show a flake, and say so.
   3. PR metadata: fix with `gh pr edit`.

5. **Verify locally**, then **commit and push** code fixes to the PR
   branch. Never force-push unless the user says so.

6. **Re-check.** Wait for checks to re-run and read the new status. If
   a blocker persists after two fix attempts, stop and ask.

## Output

1. **Blockers found:** each one and its source.
2. **Fixed:** what changed, with the commit hash.
3. **Not fixed:** each remaining blocker and why.
4. **Status:** current merge readiness. Say if review comments remain
   and suggest `tony:pr-comments`.
