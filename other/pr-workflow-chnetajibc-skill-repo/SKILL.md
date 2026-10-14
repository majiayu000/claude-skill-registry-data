---
name: pr-workflow
description: "Run GitHub issues, PRs, reviews, and releases: small diffs, evidence-backed discussion, protected branches, changelogs. Use for any PR lifecycle work."
---

# pr-workflow

Small diffs, clear intent, verified discussion. The PR describes why; the diff proves what.
## Inspection

Read the full diff (not just files), linked issue, CI status, and prior review threads before commenting.

## Decision rules

Small diffs merge fast; findings need evidence + severity; every comment resolves to a change or an evidence-backed reply; re-review after history rewrites.


## Activate when

- Opening, reviewing, or iterating on PRs; managing issues, CODEOWNERS, branch protection, releases.

## Do NOT activate for

- Git mechanics (see git/*) or CI config (see devops/github-actions).

## Procedure

1. Author: one logical change per PR (~100-line review budget; split if larger), conventional commits, linked issue, test evidence in the body (intent, scope, test evidence).
2. Review: read the full diff, trace callers/sinks, demand evidence for claims; severities blocker/high/maintainability/optional (see `../../core/code-review/`).
3. Iterate: answer every comment with a change or an evidence-backed reply (change or evidence-backed reply); re-request review after history rewrites.
4. Protect: required checks, CODEOWNERS coverage, dismiss-stale-approvals on force-push, Dependabot + advisory triage.
5. Release: semver tag, changelog entry, migration notes; verify artifacts install cleanly.

## Failure modes

Rubber-stamp approvals; style-preference comments posed as defects; approving with unresolved threads; merging red CI.

## Escalation

Mechanics (rebase/conflicts) → git/*; deep findings → core/code-review.
