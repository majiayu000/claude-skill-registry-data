---
name: careful
description: Activate safety guards for the session. Use /careful before critical operations — blocks rm -rf, DROP TABLE, git push --force, kubectl delete namespace, docker system prune via PreToolUse hook.
disable-model-invocation: true
user-invocable: true
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            INPUT=$(cat)
            CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
            if echo "$CMD" | grep -qiE 'rm\s+-rf\s+/|DROP\s+(TABLE|DATABASE)|git\s+push\s+--force|git\s+push\s+-f|kubectl\s+delete\s+namespace|docker\s+system\s+prune|npm\s+publish|pypi\s+upload'; then
              echo "🛑 BLOCKED by /careful: '$CMD' matches a dangerous command pattern"
              exit 2
            fi
---

# /careful — Session Safety Guards

When this skill is active, the following commands are **blocked** via a PreToolUse hook:

| Pattern | Reason |
|---------|--------|
| `rm -rf /` | Prevents filesystem destruction |
| `DROP TABLE` / `DROP DATABASE` | Prevents data loss |
| `git push --force` / `git push -f` | Prevents history rewriting |
| `kubectl delete namespace` | Prevents cluster destruction |
| `docker system prune` | Prevents image/volume loss |
| `npm publish` / `pypi upload` | Prevents accidental publication |

## How It Works

The PreToolUse hook intercepts every Bash command and checks it against blocked patterns. If a match is found, the command is **blocked** (exit code 2) and a warning is injected.

## When to Use

Activate before:
- Working on production infrastructure
- Running migration scripts
- Handling sensitive data operations
- Any task where a typo could be catastrophic

Deactivate by starting a new session (hooks are session-scoped).

