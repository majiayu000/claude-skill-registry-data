---
name: claude-code-review
description: Use when a completed Codex implementation should be reviewed by interactive Claude Code. Trigger on `$claude:code-review`, `$claude:security-review`, `$claude:test-gap-review`, `$claude:release-readiness-review`, or requests for Claude code review.
---

# Claude Code Review

Use this skill after implementation, before final completion claims, merge, deploy, or handoff.

## Plugin Command

```text
$claude:code-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check correctness, regressions, missing tests, unsafe assumptions, security/data risks, and fix order.
```

For specialized modes:

```text
$claude:security-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check security risk, unsafe inputs, secrets exposure, and auth/permission regressions.
$claude:test-gap-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Find missing verification proportional to risk.
$claude:release-readiness-review Review the completed implementation. Plan: <plan-path or none>. Changed files: <enumerate files>. Verification: <commands and results>. Check whether Codex can report this complete.
```

Codex must invoke Claude Companion through `$claude:*` plugin commands. Do not
ask agents to run direct Claude CLI commands.

## Integration Contract

When Claude returns findings:

1. Read the returned `outbox_path`.
2. Prioritize P0/P1/P2 findings.
3. Fix accepted findings or explain why they are rejected.
4. Run the narrowest relevant verification after changes.
5. Mention remaining test gaps or residual risks in the final answer.

## Safety

Do not run Claude review if `claude` is missing. This plugin is not an installer and never reads Claude credentials.

Review packs must contain the plan path, changed-file list, worker/stage scope,
verification commands and results, known risks, and concrete review questions.
Do not include secrets, `.env` files, private customer data, production dumps, or
unrelated files.
