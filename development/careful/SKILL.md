---
name: mk:careful
version: 0.1.0
description: |
  Session-scoped safety guardrails for destructive commands. Warns before rm -rf,
  DROP TABLE, force-push, git reset --hard, kubectl delete, and similar destructive
  operations. User can override each warning. Active for the current session only.
  Use when touching prod, debugging live systems, or working in a shared environment.
  Use when asked to "be careful", "safety mode", "prod mode", or "careful mode".
  NOT for scoping edits to a specific directory (see mk:freeze).
allowed-tools:
  - Bash
  - Read
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: bash ${CLAUDE_SKILL_DIR}/bin/check-careful.sh
          statusMessage: Checking for destructive commands...
source: gstack
keywords:
  - careful
  - safety-mode
  - destructive-commands
  - prod-mode
  - guardrails
when_to_use: Use when working in prod or with destructive commands — warns before rm -rf, DROP TABLE, force-push. NOT for scoping edits to a directory (see mk:freeze).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# /careful — Destructive Command Guardrails

Safety mode is now **active**. Every bash command will be checked for destructive
patterns before running. If a destructive command is detected, you'll be warned
and can choose to proceed or cancel.

```bash
mkdir -p .meowkit/telemetry
echo '{"skill":"careful","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","repo":"'$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")'"}'  >> .meowkit/telemetry/skill-usage.jsonl 2>/dev/null || true
```

## What's protected

See [references/destructive-patterns.md](references/destructive-patterns.md) for full pattern list.

## How it works

The hook reads the command from the tool input JSON, checks it against the
patterns above, and returns `permissionDecision: "ask"` with a warning message
if a match is found. You can always override the warning and proceed.

To deactivate, end the conversation or start a new one. Hooks are session-scoped.

## Hooks

- **PreToolUse on Bash**: Warns before destructive commands (rm -rf, DROP TABLE, force-push, reset --hard, kubectl delete)
- Session-scoped — only active when `mk:careful` is invoked
- User can override each warning individually
- **Interaction with mk:investigate**: When careful is active during an investigation, destructive-Bash warnings still fire. Debugging commands that touch state require explicit user confirmation per warning — do not bypass.

## Gotchas

- **False positives on legitimate operations**: Pattern matching `rm` or `drop` in file content, not commands → Check command context, not just string presence
- **Overly broad regex blocking development**: Guard triggers on test fixtures or documentation mentioning destructive commands → Scope guards to actual Bash tool invocations only
