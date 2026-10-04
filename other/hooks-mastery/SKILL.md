---
name: hooks-mastery
description: 'USE THIS SKILL for building Claude Code hooks — all 24 hook events, 4 hook types (command, http, prompt, agent), conditional `if` filtering, decision control patterns, validators, and self-correcting workflows.'
---

# Hooks Mastery

Build hooks that make Claude self-correcting. This skill teaches the craft of hook development — when to use which event, how to filter efficiently, decision patterns that differ by event, and production-ready recipes.

For full event schemas and JSON formats, grep the CLI docs: `grep -A 200 "^PAGE: /hooks.md" cli-full-docs.txt`

## When to Use This Skill

- Building any kind of hook (validation, notification, formatting, policy)
- Setting up self-correcting workflows (PostToolUse → Claude fixes → passes)
- Adding quality gates (Stop hooks that block until standards met)
- Preventing dangerous operations (PreToolUse guards)
- Integrating Claude Code with external services (HTTP hooks, webhooks)
- Building LLM-based verification (prompt/agent hooks)
- Reactive environment management (CwdChanged, FileChanged)

## Hook System at a Glance

24 events. 4 hook types. Hooks fire at specific lifecycle points — your code runs, returns a decision, and Claude acts on it.

### Events by Category

**Session lifecycle:**

| Event                | Fires when                             | Can block? |
| -------------------- | -------------------------------------- | ---------- |
| `SessionStart`       | Session begins/resumes/compacted       | No         |
| `SessionEnd`         | Session terminates                     | No         |
| `UserPromptSubmit`   | User submits prompt, before processing | Yes        |
| `InstructionsLoaded` | CLAUDE.md or rules file loaded         | No         |
| `ConfigChange`       | Settings/skills file modified          | Yes        |

**Tool execution (the agentic loop):**

| Event                | Fires when                      | Can block?                 |
| -------------------- | ------------------------------- | -------------------------- |
| `PreToolUse`         | Before tool executes            | Yes (allow/deny/ask/defer) |
| `PermissionRequest`  | Permission dialog about to show | Yes (allow/deny)           |
| `PermissionDenied`   | Auto-mode denied a tool call    | No (but can signal retry)  |
| `PostToolUse`        | After tool succeeds             | No (tool already ran)      |
| `PostToolUseFailure` | After tool fails                | No                         |

**Completion & tasks:**

| Event           | Fires when                 | Can block? |
| --------------- | -------------------------- | ---------- |
| `Stop`          | Claude finishes responding | Yes        |
| `StopFailure`   | Turn ends due to API error | No         |
| `TaskCreated`   | TaskCreate tool used       | Yes        |
| `TaskCompleted` | Task marked completed      | Yes        |

**Agents & teams:**

| Event           | Fires when                   | Can block? |
| --------------- | ---------------------------- | ---------- |
| `SubagentStart` | Subagent spawned             | No         |
| `SubagentStop`  | Subagent finishes            | Yes        |
| `TeammateIdle`  | Agent team member going idle | Yes        |

**Environment & files:**

| Event          | Fires when                   | Can block? |
| -------------- | ---------------------------- | ---------- |
| `CwdChanged`   | Working directory changes    | No         |
| `FileChanged`  | Watched file changes on disk | No         |
| `Notification` | Claude sends a notification  | No         |

**Compaction:**

| Event         | Fires when                 | Can block? |
| ------------- | -------------------------- | ---------- |
| `PreCompact`  | Before context compaction  | No         |
| `PostCompact` | After compaction completes | No         |

**Worktrees & MCP:**

| Event               | Fires when                       | Can block? |
| ------------------- | -------------------------------- | ---------- |
| `WorktreeCreate`    | Worktree being created           | Yes        |
| `WorktreeRemove`    | Worktree being removed           | No         |
| `Elicitation`       | MCP server requests user input   | Yes        |
| `ElicitationResult` | User responds to MCP elicitation | Yes        |

### The Four Hook Types

```json
{"type": "command", "command": "path/to/script.py"}
{"type": "http",    "url": "http://localhost:8080/hook"}
{"type": "prompt",  "prompt": "Check if all tasks are complete..."}
{"type": "agent",   "prompt": "Verify tests pass. Run the suite."}
```

**When to use each:**

| Type      | Use when                                                | Speed  | Can use tools? |
| --------- | ------------------------------------------------------- | ------ | -------------- |
| `command` | Deterministic rules, file validation, formatting        | Fast   | No             |
| `http`    | External services, team audit logs, CI/CD webhooks      | Fast   | No             |
| `prompt`  | Judgment calls a script can't make (single LLM call)    | Medium | No             |
| `agent`   | Verification that requires reading files, running tests | Slow   | Yes            |

Default to `command`. Use `prompt` when the decision needs judgment. Use `agent` when verification needs codebase access. Use `http` for external integration.

### Where Hooks Live

| Location                      | Scope                  | Shareable             |
| ----------------------------- | ---------------------- | --------------------- |
| `~/.claude/settings.json`     | All projects           | No                    |
| `.claude/settings.json`       | This project           | Yes (commit it)       |
| `.claude/settings.local.json` | This project           | No (gitignored)       |
| Managed policy settings       | Organization-wide      | Admin-controlled      |
| Plugin `hooks/hooks.json`     | When plugin enabled    | Bundled with plugin   |
| Skill/agent frontmatter       | While component active | In the component file |

## Matchers & Conditional Filtering

Two levels of filtering: `matcher` (group-level) and `if` (handler-level).

### Matcher — filter which events fire the group

The `matcher` is a regex against an event-specific field. Different events match on different things:

| Events                                      | Matcher filters     | Examples                                      |
| ------------------------------------------- | ------------------- | --------------------------------------------- |
| Tool events (PreToolUse, PostToolUse, etc.) | Tool name           | `Bash`, `Edit\|Write`, `mcp__.*`              |
| `SessionStart`                              | How session started | `startup`, `resume`, `compact`                |
| `SessionEnd`                                | Why session ended   | `clear`, `resume`, `logout`                   |
| `Notification`                              | Notification type   | `permission_prompt`, `idle_prompt`            |
| `SubagentStart/Stop`                        | Agent type          | `Explore`, `Plan`, custom names               |
| `ConfigChange`                              | Config source       | `user_settings`, `project_settings`, `skills` |
| `FileChanged`                               | Filename (basename) | `.envrc`, `.env`                              |
| `StopFailure`                               | Error type          | `rate_limit`, `server_error`                  |
| `InstructionsLoaded`                        | Load reason         | `session_start`, `path_glob_match`            |

Some events have **no matcher support** and always fire: `UserPromptSubmit`, `Stop`, `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `CwdChanged`, `WorktreeCreate`, `WorktreeRemove`.

### The `if` Field — filter which handlers spawn (v2.1.85+)

The `if` field uses permission rule syntax to match tool name AND arguments. This avoids spawning the hook process when it's not needed.

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
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-git-policy.sh"
          }
        ]
      }
    ]
  }
}
```

The hook only spawns when the Bash command starts with `git`. Other Bash commands skip it entirely.

**`if` only works on tool events:** `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`. Adding `if` to any other event prevents the hook from running.

**Pattern examples:**

- `"Bash(git *)"` — only git commands
- `"Bash(rm *)"` — only rm commands
- `"Edit(*.ts)"` — only TypeScript files
- `"Write(*.py)"` — only Python files

**Why this matters:** Without `if`, a `PreToolUse` hook on `Bash` spawns a process for every single shell command. With `if: "Bash(git *)"`, it only spawns for git commands. In a long session with hundreds of Bash calls, this is the difference between 3 hook invocations and 300.

### Other Handler Fields

| Field           | Default                                   | Purpose                                               |
| --------------- | ----------------------------------------- | ----------------------------------------------------- |
| `timeout`       | 600s (command), 30s (prompt), 60s (agent) | Seconds before canceling                              |
| `statusMessage` | none                                      | Custom spinner text while hook runs                   |
| `async`         | false                                     | Run in background without blocking (command only)     |
| `once`          | false                                     | Run only once per session, then removed (skills only) |

## Decision Control

**This is the part most people get wrong.** Different events use different output patterns. There is no universal format.

### Pattern 1: Top-level `decision` (PostToolUse, Stop, UserPromptSubmit, SubagentStop, ConfigChange)

```json
{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}
```

Or exit code 2 with reason on stderr. These events also support `additionalContext`.

### Pattern 2: `hookSpecificOutput` with `permissionDecision` (PreToolUse)

**This is the current format. The old top-level `decision: "block"` is deprecated for PreToolUse.**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Four decisions: `allow` (skip permission prompt), `deny` (cancel tool call), `ask` (show prompt to user), `defer` (pause for later resume in headless mode).

PreToolUse can also **rewrite tool input** and **inject context**:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": { "command": "npm run lint -- --fix" },
    "additionalContext": "Running in production environment."
  }
}
```

When multiple PreToolUse hooks disagree: `deny` > `defer` > `ask` > `allow`.

### Pattern 3: `hookSpecificOutput` with `decision.behavior` (PermissionRequest)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [{ "type": "setMode", "mode": "acceptEdits", "destination": "session" }]
    }
  }
}
```

### Pattern 4: `hookSpecificOutput` with `retry` (PermissionDenied)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

### Pattern 5: Exit code only (TaskCreated, TaskCompleted, TeammateIdle)

Exit 2 + stderr message to block. No JSON decision control needed. These events also accept `{"continue": false, "stopReason": "..."}` to stop the teammate entirely.

### Pattern 6: Context injection (SessionStart, UserPromptSubmit)

Plain text on stdout is added to Claude's context. Or use JSON:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current sprint: auth refactor. Use Bun, not npm."
  }
}
```

### Pattern 7: Prompt/agent hooks (any blocking event)

Prompt and agent hooks return `{"ok": true}` or `{"ok": false, "reason": "what's wrong"}`. The model decides — you write the evaluation criteria.

### The Simple Path: Exit Codes

For most hooks, you don't need JSON at all:

- **Exit 0** — allow (stdout parsed as JSON if present)
- **Exit 2** — block (stderr fed to Claude as error message)
- **Other** — non-blocking error (logged, execution continues)

## Building Command Hooks

### The Validator Pattern

All command-type validators follow this structure (PEP 723 uv script):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]  # add what you need
# ///

import json, sys
from pathlib import Path

def main():
    # 1. Read hook input from stdin
    hook_input = json.loads(sys.stdin.read())

    # 2. Extract what you need
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path")

    # 3. Validate
    errors = your_validation_logic(file_path)

    # 4. Return decision
    if errors:
        # For PostToolUse/Stop: use top-level decision
        print(json.dumps({
            "decision": "block",
            "reason": "Fix these:\n" + "\n".join(errors)
        }))
        # For PreToolUse: use hookSpecificOutput instead
        # print(json.dumps({
        #     "hookSpecificOutput": {
        #         "hookEventName": "PreToolUse",
        #         "permissionDecision": "deny",
        #         "permissionDecisionReason": "Fix these:\n" + "\n".join(errors)
        #     }
        # }))
    else:
        print(json.dumps({}))  # Pass

if __name__ == "__main__":
    main()
```

### Environment Variables

| Variable              | Available in                          | Purpose                                      |
| --------------------- | ------------------------------------- | -------------------------------------------- |
| `$CLAUDE_PROJECT_DIR` | All hooks                             | Project root — use for script paths          |
| `$CLAUDE_ENV_FILE`    | SessionStart, CwdChanged, FileChanged | Write `export K=V` lines to persist env vars |
| `$CLAUDE_PLUGIN_ROOT` | Plugin hooks                          | Plugin installation directory                |
| `$CLAUDE_PLUGIN_DATA` | Plugin hooks                          | Plugin persistent data directory             |
| `$CLAUDE_CODE_REMOTE` | All hooks                             | `"true"` in remote web environments          |

### The `stop_hook_active` Guard

Stop hooks fire when Claude finishes responding. If your Stop hook blocks, Claude works on the issue and finishes again — firing the Stop hook again. Without a guard, this loops forever:

```python
def main():
    hook_input = json.loads(sys.stdin.read())

    # CRITICAL: Check if we're already in a stop-hook correction cycle
    if hook_input.get("stop_hook_active"):
        print(json.dumps({}))  # Allow Claude to stop
        return

    # ... your validation logic ...
```

## Path Resolution Best Practices

### The Problem: Fragile Parent Counting

```python
# WRONG — breaks if validator moves to different depth
project_root = Path(__file__).parent.parent.parent
```

### The Solution: Anchor-Based Root Finding

```python
def find_project_root(start_path: Path, anchor_files: list[str]) -> Path:
    """Walk up until finding a directory with an anchor file."""
    current = start_path.resolve()
    for _ in range(10):
        for anchor in anchor_files:
            if (current / anchor).exists():
                return current
        if current.parent == current:
            break
        current = current.parent
    raise FileNotFoundError(
        f"Could not find project root from {start_path}. "
        f"Searched for: {anchor_files}"
    )

project_root = find_project_root(
    Path(__file__).parent,
    anchor_files=[".git", "package.json", "pyproject.toml"]
)
```

### Pre-flight Sanity Checks

After finding project root, verify it has expected structure:

```python
def verify_project_root(project_root: Path, expected_paths: list[str]) -> list[str]:
    """Returns list of missing paths (empty = all verified)."""
    return [p for p in expected_paths if not (project_root / p).exists()]

missing = verify_project_root(project_root, ["src", ".claude"])
if missing:
    # This is a VALIDATOR BUG, not a validation failure
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"Validator configuration error!\n"
            f"Project root: {project_root}\n"
            f"Missing expected paths: {missing}\n"
            f"The validator needs fixing, not the code."
        )
    }))
    return
```

**Why this matters:** Distinguishes validator bugs from validation failures. Prevents false positives that waste time in self-correction loops.

### Common Anchor Files

| Project type          | Anchor files                            |
| --------------------- | --------------------------------------- |
| Python                | `pyproject.toml`, `setup.py`, `.git`    |
| JavaScript/TypeScript | `package.json`, `tsconfig.json`, `.git` |
| Rust                  | `Cargo.toml`, `.git`                    |
| Go                    | `go.mod`, `.git`                        |
| Any git repo          | `.git`                                  |

## Recipes

### Auto-format after edits

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### Block edits to protected files (with `if`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "if": "Edit(.env*)|Write(.env*)",
            "command": "echo 'Blocked: .env files are protected' >&2 && exit 2"
          }
        ]
      }
    ]
  }
}
```

### Desktop notification when Claude is idle

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs attention\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Direnv-style environment reload

```json
{
  "hooks": {
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ],
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

### Re-inject context after compaction

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun not npm. Run bun test before committing.'"
          }
        ]
      }
    ]
  }
}
```

### Auto-approve ExitPlanMode

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

### Prompt-type quality gate (LLM-based verification)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all requested tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains\"}."
          }
        ]
      }
    ]
  }
}
```

### Agent-type test verification

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Run the test suite and verify all tests pass. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### HTTP audit logging

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": { "Authorization": "Bearer $MY_TOKEN" },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

### Audit config changes

```json
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

## Working Examples

### PostToolUse: CSV Validator

See `${CLAUDE_SKILL_DIR}/examples/posttooluse-csv-validator.py`

Validates CSV files are parseable and non-empty after Edit|Write. Claude self-corrects if invalid.

### Stop: Linter Validator

See `${CLAUDE_SKILL_DIR}/examples/stop-ruff-validator.py`

Runs ruff linter when Claude finishes. Blocks completion until all linting passes. Includes `stop_hook_active` guard to prevent infinite loops.

### PreToolUse: Deletion Guard

See `${CLAUDE_SKILL_DIR}/examples/pretooluse-deletion-guard.py`

Prevents deletion of critical files (.git, .claude, package.json, etc.). Uses `hookSpecificOutput` with `permissionDecision: "deny"`.

### PreToolUse: Git Policy (with `if` filtering)

See `${CLAUDE_SKILL_DIR}/examples/pretooluse-git-policy.py`

Blocks force-pushes and main branch pushes. Demonstrates `if: "Bash(git *)"` to only spawn on git commands. Uses `hookSpecificOutput` pattern.

### PostToolUse: Project Structure Validator

See `${CLAUDE_SKILL_DIR}/examples/posttooluse-project-structure-validator.py`

Demonstrates anchor-based root finding and pre-flight sanity checks. Validates JSON manifests and checks referenced files exist.

## Templates

### Basic Validator Template

See `${CLAUDE_SKILL_DIR}/templates/validator-template.py`

Copy and modify. Includes `find_project_root()`, `verify_project_root()`, and both decision output patterns (top-level for PostToolUse/Stop, hookSpecificOutput for PreToolUse).

### File-Specific Validator Template

See `${CLAUDE_SKILL_DIR}/templates/file-validator-template.py`

For validators that check specific file types (JSON, YAML, etc.)

## Best Practices

1. **Use `if` to reduce hook overhead** — Don't spawn a process for every Bash command when you only care about `git`
2. **Keep validators focused** — One validator per concern
3. **Clear error messages** — Tell Claude exactly what's wrong and how to fix it
4. **Fast execution** — Validators run frequently, keep them under 5 seconds
5. **Use logging** — Write to a file for debugging, don't spam stderr
6. **Guard Stop hooks** — Check `stop_hook_active` to prevent infinite loops
7. **Use uv for dependencies** — PEP 723 inline dependencies for portability
8. **Choose the right decision pattern** — PreToolUse uses `hookSpecificOutput`, most others use top-level `decision`
9. **Test standalone** — Pipe sample JSON to test without Claude
10. **Prefer `if` over script-level filtering** — `if: "Bash(git *)"` is cheaper than spawning a script that checks `tool_name == "Bash"` and `command.startswith("git")`

## Debugging

**Test a validator standalone:**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force"},"hook_event_name":"PreToolUse"}' | \
    python .claude/hooks/validators/git-policy.py
```

**Browse configured hooks:**

```
/hooks
```

**Toggle verbose mode** (`Ctrl+O`) to see hook output in the transcript.

**Run with full debug logging:**

```bash
claude --debug
```

**Common issues:**

- Hook not firing → check matcher is correct (`/hooks` to verify)
- JSON parse error → shell profile echoing text (wrap in `if [[ $- == *i* ]]`)
- Stop hook looping → missing `stop_hook_active` guard
- PreToolUse returning wrong format → use `hookSpecificOutput`, not top-level `decision`
- `if` field ignored → only works on tool events, requires v2.1.85+
- Hook spawning too often → add `if` field to narrow scope
