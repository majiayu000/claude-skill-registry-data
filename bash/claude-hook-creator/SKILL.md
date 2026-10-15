---
name: claude-hook-creator
description: Create or revise Anthropic Claude Code hooks. Use when Claude needs to add or modify hooks in `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, or subagent frontmatter; choose hook events, matchers, `if` filters, hook commands, stdout or stderr behavior, JSON `hookSpecificOutput`, or safe automation for notifications, formatting, policy enforcement, context reinjection, permission handling, and subagent lifecycle events.
---

# Claude Hook Creator

## Overview

Design Claude Code hooks that are deterministic, narrowly scoped, and safe to run automatically. Produce the exact settings JSON snippet, any companion script files, and compact validation guidance.

## Workflow

1. Decide whether a hook is the right primitive.
2. Prefer hooks for deterministic enforcement or automation. Prefer `CLAUDE.md`, skills, or subagents when the work depends on judgment rather than fixed rules.
3. Choose scope intentionally: `~/.claude/settings.json` for cross-project personal automation, `.claude/settings.json` for team-shared project automation, `.claude/settings.local.json` for private project-local overrides, and subagent frontmatter only when the behavior should exist only while that subagent runs.
4. Collect the minimum facts: event, matcher, whether the hook should allow, deny, ask, annotate, or inject context, any OS or tool dependencies, and whether a separate script file is safer than an inline one-liner.
5. Keep matchers narrow. Use the `if` field only on tool events and only when argument-level filtering matters.
6. Keep hook commands deterministic. Prefer small shell scripts or simple commands that read JSON from stdin and write only the intended stdout or stderr.
7. Output the exact JSON snippet, any script contents, where to place them, and a short test procedure.

## Design Rules

- Read [hook-reference.md](references/hook-reference.md) before choosing an event or structured decision format.
- Prefer project-level hooks for shared policy and subagent frontmatter hooks for behavior that should travel with a specific subagent definition.
- Remember that frontmatter hooks fire only when the agent is spawned as a subagent, not when that agent runs as the main session with `--agent`.
- Keep stdout clean unless the hook intentionally returns context or structured JSON.
- Use stderr for operator logs or block reasons.
- Use `exit 2` to block with stderr feedback, or `exit 0` with JSON for structured control. Do not mix JSON output with `exit 2`.
- Quote `"$CLAUDE_PROJECT_DIR"` when referencing project-relative scripts.
- Prefer `jq` for parsing hook JSON in shell hooks.
- Treat broad permission approvals as high risk. Keep `PermissionRequest` matchers narrow.
- Remember that multiple matching hooks run in parallel and Claude applies the most restrictive result.

## Event Selection

- `PreToolUse`: Gate or rewrite risky tool usage before execution.
- `PostToolUse`: Trigger follow-up automation after successful tool calls.
- `PermissionRequest`: Auto-answer a narrow class of permission prompts with structured JSON.
- `Notification`: Alert the user when Claude needs attention.
- `SessionStart`: Re-inject context after `compact` or at startup.
- `ConfigChange`: Audit or block configuration changes.
- `CwdChanged` or `FileChanged`: Reload environment when directory or watched files change.
- `SubagentStart` and `SubagentStop`: Run project-level automation when subagents begin or end.

## Output Format

Return:

1. The recommended settings location.
2. The complete JSON hook snippet.
3. Any companion script file contents and paths.
4. A short test procedure.
5. Brief notes on dependencies, matcher scope, or risks.

## Baseline Patterns

Use `PreToolUse` to block risky commands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(git *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-git-policy.sh"
          }
        ]
      }
    ]
  }
}
```

Use `PermissionRequest` only with narrow matchers:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

## References

- Read [hook-reference.md](references/hook-reference.md) for source-grounded event behavior, matcher rules, output rules, and official URLs.
