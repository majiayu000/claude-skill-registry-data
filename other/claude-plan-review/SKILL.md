---
name: claude-plan-review
description: Use when a Superpowers/Codex implementation plan should be reviewed by interactive Claude Code before implementation. Trigger on `$claude:superpowers-plan-review`, `$claude:plan-red-team`, or requests to send a plan to Claude for review.
---

# Claude Plan Review

Use this skill after Codex has drafted a plan and before implementation begins.

## Plugin Command

```text
$claude:superpowers-plan-review Review <plan-path> before Codex executes it. Check missing root-cause analysis, unsafe sequencing, verification gaps, scope drift, and unresolved user decisions.
```

Use `plan-red-team` for high-risk plans:

```text
$claude:plan-red-team Red-team <plan-path> before implementation. Identify assumptions, hidden dependencies, migration risks, rollback gaps, and missing acceptance checks.
```

Codex must invoke Claude Companion through `$claude:*` plugin commands. Do not
ask agents to run direct Claude CLI commands.

## Integration Contract

When Claude returns recommendations:

1. Save a sibling suggestions file named `<plan>.claude-suggestions.md`.
2. Split findings into accepted, partially accepted, rejected, and needs-user-decision.
3. Patch the original plan with accepted recommendations.
4. Do not proceed to implementation while Claude verdict is `NEEDS_REVISION` unless the remaining items require a user decision.

## Safety

Claude is reviewer-only. Do not let it edit files or run commands. The runner sends context through the prompt and captures the answer through the Stop hook.

Plan review prompts must include the plan path, relevant source/spec paths,
known constraints, verification expectations, and concrete questions for Claude.
Do not include secrets, `.env` files, private customer data, or production dumps.
