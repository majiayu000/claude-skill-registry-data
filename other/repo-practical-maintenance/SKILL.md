---
name: repo-practical-maintenance
description: Use when TaF asks for practical repo maintenance across their active checkouts, especially CI failures, failing tests, PR reviews, changelogs, docs updates, release prep, deployment workflow fixes, debugging evidence, package visibility, or focused repo triage.
metadata:
  short-description: Practical repo maintenance for TaF
---

# Repo Practical Maintenance

## Default Shape

Use this skill to complete the requested repo task. Distinguish investigation, review, repair, and publication; analysis or review alone does not authorize code changes.

1. Start with the narrow repo surface the user named.
2. Check current state before assuming memory is current: `git status --short`, relevant files, logs, failing commands, or CI metadata.
3. Keep the work repo-native. Prefer existing scripts, workflows, docs, test projects, and helper APIs over new process.
4. Preserve the full requested end state. Do not close on a smaller local slice unless the user explicitly narrows scope.
5. Verify the requested behavior with the smallest meaningful check and applicable required checks. New tests should exercise actual production code and a relevant behavior or plausible failure, not serve a coverage percentage or only assert mock setup. Keep build, runtime, and deployed-artifact evidence distinct.
6. Report concrete outcomes and commands. Use numbered lists for decisions, recommendations, review findings, and next actions.

## Repeated Workflows

### CI or Test Triage

1. Identify the failing job, command, test, and recent relevant change.
2. Reproduce the smallest local command when practical.
3. If behavior changed, rebuild before trusting `--no-build` test runs.
4. When repair is authorized, trace the real production path before changing the test or implementation. Preserve meaningful assertions; fix the cause rather than weakening a test to make it pass.
5. End with the rerun command and result.

### Release or Deploy Prep

1. Inspect workflow files and artifact-producing project tasks first.
2. Confirm the artifact path or publishing command against the repo build output.
3. Keep workflow edits functional and narrow.
4. On Windows PowerShell, quote Gradle `-P...` property arguments.
5. If the user says "push it", commit and push the narrow fix without extra ceremony.
6. Complete and verify the requested publication or deployment endpoint. A passing workflow is not proof that the expected artifact is served or running. Keep optional release acceptance out of ordinary local smoke tests; retain applicable integrity and health checks.

### PR Review

1. Inspect the exact PR head, current diff, and existing review threads before reviewing or changing anything.
2. Prioritize concrete bugs, regressions, and relevant missing checks. Ground findings in a reachable trigger, consequence, and current file/line; avoid resolved, outdated, or duplicate findings. Keep a requested complexity review distinct from correctness findings.
3. For review-only requests, leave code unchanged. When the user asks for comments on the PR, publish the verified findings there; a chat summary does not complete that request.
4. When asked to handle comments, assess them against current code, repair actionable issues, validate, and push within the authorized scope. Reply and resolve only when the evidence supports resolution; explain comments that no longer apply or do not warrant a change.
5. Refresh the PR head before publishing findings or merging. If it changed, inspect the affected changes and update the review. Merge only when authorized and against the reviewed head.
6. Report findings by severity, or state that none were found. Report material verification limits without inventing test gaps or requiring unrelated checks.

### Changelog or Docs Update

1. Confirm the live docs location before editing.
2. Patch current repo docs instead of stale root notes.
3. Keep release-readiness language aligned with the user's stated bar.
4. Prefer exact, practical wording over broad product claims.

### Debugging Evidence

1. Decode the exact local symptom first.
2. Add structured evidence that helps solve the immediate issue.
3. Avoid generic logs when the user asks for actionable debugging output.
4. Keep diagnostic scope tight to the named subsystem.

## Repo Notes

- GameOverlay.NET and ModernOverlay decisions should default to hobbyist MVP/alpha language unless the user asks for a production bar.
- GameOverlay.NET timing work should compare `FrameRateLimit.Unlimited` with `PresentMode.Immediate` and inspect `PresentDuration`.
- LegionLabs overlay recommendations should stay compact and directive-style: concrete build/send/hold calls, target waves, and explicit `needs_enemy_scan` uncertainty.

## Delegation Template

Use subagents when independent work can save time or improve quality. Adapt [the bounded investigator template](references/bounded-investigator-subagent.md) when useful; give each agent explicit ownership, side-effect limits, and evidence requirements. Continue non-overlapping work locally and verify consequential changes before integration.
