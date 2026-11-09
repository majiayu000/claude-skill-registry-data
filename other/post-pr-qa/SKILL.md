---
name: post-pr-qa
description: Run mode-aware QA immediately after a confirmed task, Goal, or Gauntlet PR is available, then post pass/fail evidence to the PR with inline screenshot references.
engines: [AGNOSTIC]
---

## When to use
Use after the applicable mode-aware readiness gate has authorized publication and the PR number or URL has been confirmed as available. This includes human-approved task and Gauntlet promotion PRs, automatic Goal task PRs, and approved Gauntlet progress PRs.

## Output
- QA commands run and pass/fail outcome
- generated report paths
- GitHub PR comment with QA evidence
- inline screenshot URLs in the PR comment when screenshots are part of the evidence
- mode-specific next state: task/Goal review readiness, a recorded Gauntlet progress verdict awaiting human merge or another builder round, or a recorded promotion verdict

## Notes
- Confirm the PR exists first using this GitHub tool priority: `gh pr view`, then an available `github` CLI/wrapper, then GitHub MCP/app connector metadata only when both CLI options are unavailable or unsuitable.
- Start QA immediately after PR availability is confirmed; do not wait for another user prompt.
- Choose the narrowest meaningful QA first, then broaden when risk or repository conventions require it.
- For browser/UI work, generate non-interactive evidence reports and include screenshot URLs in the PR comment.
- Local screenshot file paths do not render inline on GitHub. Upload screenshots or use CI/repository-hosted URLs before posting inline evidence.
- Mirror or link QA evidence to the task issue when a linked issue exists, but the PR comment is the primary post-PR signal.
- Post the PR QA comment through the same GitHub tool priority: `gh` first, `github` CLI/wrapper second, GitHub MCP/app connector last.
- For Gauntlet QA, use the semantic comment form, capture its exact `COMMENT_URL`, then record the corresponding immutable event. A progress pass waits for human merge; a progress failure returns to the same PR with a changed builder strategy. A promotion failure must be recorded before affected-unit remediation may begin.
- After QA is complete, report the verdict and the mode-specific next state. Do not describe a Gauntlet unit as integrated until its passing head is human-merged and the merge event is recorded.

## Commands
../commands/comment-pr-qa-results.sh "<pr_number_or_url>" "<results_summary_file>" [screenshot_or_artifact ...]
../commands/comment-pr-qa-results.sh "<pr_url>" "<results_summary_file>" --gauntlet-verdict "<pass|fail>" --head-sha "<sha>" --gauntlet-source "<project-relative-round-or-completion-event>" [--gauntlet-affected-units "<none|comma-sorted-ids>"] [screenshot_or_artifact ...]
../commands/record-gauntlet-pr-event.sh "<gauntlet>" "<item-id>" "<qa-pass|qa-fail>" "<pr-url>" "<head-branch>" "<comment-url>" --head-sha "<sha>"
../commands/record-gauntlet-promotion-qa.sh "<gauntlet>" "<pass|fail>" "<promotion-pr-url>" "<comment-url>" --head-sha "<sha>" [--affected-unit "<item-id>"]...
