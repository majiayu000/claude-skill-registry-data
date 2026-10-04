---
name: superpowers-guard
description: >
  Use when the user wants maximum safety — "guard mode", "full safety", "lock it down",
  "protect this", "maximum safety", "prod safety", "production guard". Combines destructive
  command warnings and directory-scoped edit restrictions. Use for prod work, live systems,
  or when you want to prevent accidental modifications outside a scope.
---

> **DEPRECATED** — use `/guard` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Guard Mode

**Purpose:** Full safety mode — destructive command warnings + directory-scoped edit restrictions in one command.

---

## What Gets Protected

### 1. Destructive Command Warnings

Every Bash command is checked against dangerous patterns before execution:

| Pattern | Examples |
|---------|---------|
| Recursive delete | `rm -rf`, `rm -r --no-preserve-root` |
| Database drops | `DROP TABLE`, `DROP DATABASE`, `dropdb`, `DELETE FROM .* WHERE` |
| Force push | `git push --force`, `git push -f`, `git push +f` |
| Git reset destructive | `git reset --hard`, `git reset --mixed` |
| Kubernetes destruction | `kubectl delete`, `kubectl drain`, `kubectl scale 0` |
| Docker destruction | `docker system prune -a`, `docker rmi -f` |
| Pip destructive | `pip uninstall -y` (with `-e`, `-r`) |
| Env file writes | Writing to `.env` files directly |

**Safe exemptions:** `node_modules`, `.next`, `dist`, `build`, `.cache`, `__pycache__`, `.git/objects`

When a dangerous command is detected:
- Warn the user with a clear explanation of the risk
- Ask for explicit confirmation before proceeding
- The user can override any warning

### 2. Edit Boundary

File edits are restricted to a user-specified directory. Any Edit or Write targeting a file outside the boundary is **blocked**.

---

## Setup

Ask the user which directory to restrict edits to:

```
Guard mode: which directory should I restrict edits to?
Destructive command warnings are always on.
Files outside this directory will be blocked from editing.
```

Use AskUserQuestion with a text input.

Once the user provides a directory:

```bash
# Resolve to absolute path
FREEZE_DIR=$(cd "<user-provided-path>" 2>/dev/null && pwd)
echo "$FREEZE_DIR"

# Ensure trailing slash
FREEZE_DIR="${FREEZE_DIR%/}/"
echo "Freeze boundary: $FREEZE_DIR"

# Save state
STATE_DIR="$HOME/.claude"
mkdir -p "$STATE_DIR"
echo "GUARD_ACTIVE=1" >> "$STATE_DIR/guard-state.txt"
echo "FREEZE_DIR=${FREEZE_DIR}" >> "$STATE_DIR/guard-state.txt"
echo "GUARD_ACTIVATED=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$STATE_DIR/guard-state.txt"

# Create check script
cat > "$STATE_DIR/check-guard.sh" << 'SCRIPT'
#!/bin/bash
FILE="$1"
STATE="$HOME/.claude/guard-state.txt"
if [ -f "$STATE" ]; then
  FREEZE_DIR=$(grep "^FREEZE_DIR=" "$STATE" | cut -d= -f2)
  if [ -n "$FREEZE_DIR" ] && [ -n "$FILE" ]; then
    case "$FILE" in
      "$FREEZE_DIR"*)
        echo "ALLOWED"
        ;;
      *)
        echo "BLOCKED: $FILE is outside freeze boundary $FREEZE_DIR"
        echo "Block this operation? (yes/no)"
        read -r answer
        if [ "$answer" != "yes" ]; then
          exit 1
        fi
        ;;
    esac
  fi
fi
echo "ALLOWED"
SCRIPT
chmod +x "$STATE_DIR/check-guard.sh"
```

Tell the user:
```
Guard mode active.

Two protections are running:
1. Destructive command warnings — rm -rf, DROP TABLE, force-push etc. will warn before executing (you can override)
2. Edit boundary — file edits restricted to <path>/
```

---

## How It Works

### Destructive Command Check

Before any Bash tool call, check the command against the dangerous patterns above. If matched:
1. Print a warning with the specific risk
2. Print the exact command that was flagged
3. Ask the user: "Proceed anyway?" (yes/no)
4. If yes, execute. If no, don't execute.

### Edit Boundary Check

Before any Edit or Write tool call:
1. Read `FREEZE_DIR` from `$HOME/.claude/guard-state.txt`
2. Check if the target file path starts with `$FREEZE_DIR`
3. If outside: BLOCK the operation, print a warning, explain the boundary
4. If inside: proceed normally

**Read, Bash, Glob, Grep, and other tools are unaffected** — only Edit and Write are blocked.

---

## Deactivation

To remove the edit boundary:
```
Say "/unfreeze" or type "unfreeze" to remove the edit boundary.
To fully deactivate guard mode, end the session.
```

The destructive command warnings are session-scoped and cannot be individually deactivated — they expire when the session ends.

---

## Limitations

- **Bash commands can still bypass** — tools like `sed`, `perl`, `dd` via Bash can write outside the boundary. The Edit/Write block is the guard, not Bash.
- **State file is not encrypted** — `guard-state.txt` contains directory paths in plaintext.
- **No network-level protection** — guard mode doesn't prevent exfiltration via curl/wget.

---

## PreToolUse

### Skill-Finder FTS Hook

Before any Read, Glob, Grep, or Agent tool call, check if the arguments look skill-related and run the FTS hook:

```bash
TOOL_NAME="{{tool_name}}"
TOOL_ARGS="{{tool_args}}"

# Only run for Read/Glob/Grep/Agent
case "$TOOL_NAME" in
  Read|Glob|Grep|Agent)
    ~/.claude/skills/_fts/bin/fts-hook.sh "$TOOL_NAME" $TOOL_ARGS 2>&1
    ;;
esac
```

**Note:** The FTS hook is advisory — it never blocks tools. Its stderr output appears in the session context as "FTS suggestion (Phase 4)".

### Blocked Tools Fan-Out

Before any Edit or Write tool call, after the Edit Boundary check, emit the blocked attempt to the RoomManager fan-out sink:

```bash
TOOL_NAME="{{tool_name}}"
TARGET="{{tool_args[0]}}"
STATE="$HOME/.claude/guard-state.txt"

# Only emit for blocked Edit/Write attempts (not general Bash)
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
  if [[ -f "$STATE" ]]; then
    FREEZE_DIR=$(grep "^FREEZE_DIR=" "$STATE" | cut -d= -f2 2>/dev/null || true)
    if [[ -n "$FREEZE_DIR" && "$TARGET" != "$FREEZE_DIR"* ]]; then
      # Emit to RoomManager fan-out (async-safe, never blocks the tool)
      bun --bun "$HOME/.claude/skills/_guard/blocked_tools_log.ts" \
        "$TOOL_NAME" "$TARGET" "outside_freeze_boundary" \
        2>/dev/null &
    fi
  fi
fi
```

**Note:** The fan-out write is fire-and-forget (`&`) — it never blocks the tool call or the session. The sink at `agency-rooms/operations/events/blocked_tools.jsonl` is written best-effort.

### Delegation Fan-Out

Before any Agent tool call, emit a DELEGATION_START event to the audit log.
The parent_id is the current session; child_id is the agent name/type being spawned.

```bash
PARENT_ID="{{session_id}}"
CHILD_ID="{{tool_args[0]:-unknown}}"
AGENT_TYPE="{{tool_args[1]:-general-purpose}"

~/.claude/skills/_guard/bin/delegation-spawn.sh \
  start "$PARENT_ID" "$CHILD_ID" "$AGENT_TYPE" \
  >> ~/.claude/delegation_events.jsonl 2>/dev/null &
```

**Note:** Fire-and-forget (`&`) — delegation audit writes never block the Agent tool. The END event is emitted by the delegatee agent on completion.

## Completion Status

- **DONE** — Guard mode activated, boundary set, user notified
- **BLOCKED** — User didn't provide a directory
- **NEEDS_CONTEXT** — Need to know what directory to protect
