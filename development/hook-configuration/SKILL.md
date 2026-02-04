---
name: hook-configuration
description: >
  Use this skill when creating or refining Claude Code hooks. Hooks are shell commands that execute
  at specific lifecycle events (tool use, prompt submit, notifications, session events). Helps design
  event handlers for notifications, formatting, logging, feedback, and permission control. Automatically
  invoked when user requests "create a hook", "add automation", "event handler", "workflow automation",
  or mentions hook development.
allowed-tools: Read, Write, Edit, Grep, Bash(which:*), Bash(jq:*), Bash(osascript:*)
---

# Hook Configuration Skill

This skill helps create production-ready Claude Code hooks following Anthropic's official specifications.

## What are Hooks?

**Hooks** are user-defined shell commands that execute at various points in Claude Code's lifecycle. They provide:

- **Deterministic control**: Ensure actions happen automatically, not relying on LLM decisions
- **Workflow automation**: Format code, run linters, log commands
- **Custom notifications**: Alert when Claude needs input
- **Permission systems**: Block sensitive file modifications
- **Feedback loops**: Validate code changes against conventions

## Hook vs Skill vs Command

| Feature | Hook | Skill | Command |
|---------|------|-------|---------|
| **Trigger** | Lifecycle event | Context match | User invocation |
| **Type** | Shell command | AI capability | Prompt template |
| **Use case** | Automation, validation | Autonomous features | Reusable prompts |
| **Control** | Deterministic | LLM-driven | User-initiated |

**When to use Hooks**: Automatic formatting, logging, notifications, permission control, code validation

## Hook Events

Ten lifecycle events trigger hooks:

### 1. PreToolUse
Executes **after Claude creates tool parameters but before processing**.

**Use cases**:
- Block edits to sensitive files (.env, production configs)
- Validate bash commands before execution
- Request confirmation for destructive operations
- Log all tool usage for auditing
- Modify tool inputs programmatically

**Blocking capability**: Yes - exit code 2 blocks with error fed to Claude; JSON output with `"permissionDecision": "deny"` also blocks

### 2. PostToolUse
Runs **immediately after successful tool completion**.

**Use cases**:
- Format code after edits (Prettier, Black, gofmt)
- Run linters after file modifications
- Sync changes to external systems
- Update indexes or caches

**Blocking capability**: No - tool already executed

### 3. UserPromptSubmit
Fires when users **submit prompts, before Claude processes them**.

**Use cases**:
- Inject context automatically (git status, env variables)
- Log user interactions
- Validate prompt safety
- Add project-specific context

**Blocking capability**: Yes - JSON output with `"decision": "block"` prevents submission

### 4. PermissionRequest
Activates when **permission dialogs appear to users**.

**Use cases**:
- Auto-approve safe operations
- Auto-deny dangerous operations
- Log permission requests
- Provide context for decisions

**Blocking capability**: Yes - can allow, deny, or pass through to user

### 5. Notification
Triggers when **Claude Code sends notifications**.

**Use cases**:
- Custom notification sounds
- Desktop notifications (macOS, Linux, Windows)
- Send to Slack/Discord
- Visual alerts

**Blocking capability**: No - notification already generated

### 6. Stop
Activates when **the main agent finishes responding**.

**Use cases**:
- Run tests after code generation
- Update documentation
- Commit changes automatically
- Trigger deployments

**Blocking capability**: Yes - JSON output with `"decision": "block"` prevents stop

### 7. SubagentStop
Runs when **subagent tasks complete**.

**Use cases**:
- Log subagent results
- Validate subagent outputs
- Trigger next workflow steps
- Aggregate subagent data

**Blocking capability**: Yes - JSON output with `"decision": "block"` prevents stop

### 8. PreCompact
Executes **before context window compaction operations**.

**Use cases**:
- Save conversation state
- Export conversation history
- Archive important context

**Blocking capability**: Yes - can prevent compaction

### 9. SessionStart
Triggers at **session initialization or resumption**.

**Use cases**:
- Load project context
- Initialize environment variables
- Display project status
- Check for updates

**Blocking capability**: No - session already started

### 10. SessionEnd
Runs when **sessions terminate**.

**Use cases**:
- Save session state
- Cleanup temporary files
- Export logs
- Trigger cleanup scripts

**Blocking capability**: No - session already ending

## Hook Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Editing file' >> /tmp/claude-audit.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.py$'; then black \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Configuration Structure

```json
{
  "hooks": {
    "EventName": [                     // Event type (PreToolUse, PostToolUse, etc.)
      {
        "matcher": "ToolPattern",      // Tool name, regex (pipe-separated), or "*" for all
        "hooks": [                     // Array of hooks for this matcher
          {
            "type": "command",         // "command" or "prompt"
            "command": "shell command", // Shell command to execute
            "timeout": 60              // Optional timeout in seconds (default: 60)
          }
        ]
      }
    ]
  }
}
```

### Configuration Locations

- **User-level**: `~/.claude/settings.json` (all projects)
- **Project-level**: `.claude/settings.json` (this project, team-shared)
- **Local**: `.claude/settings.local.json` (uncommitted, project-specific overrides)
- **Plugin-level**: `plugin-name/hooks/hooks.json` (bundled with plugin)

## Matchers

### Tool Matching

**Exact match**:
```json
{
  "matcher": "Edit"
}
```

**Regex pattern** (use pipe for OR):
```json
{
  "matcher": "Edit|Write|MultiEdit"
}
```

**Wildcard** (match all tools):
```json
{
  "matcher": "*"
}
```

**Common tool names**: Bash, Read, Write, Edit, MultiEdit, Glob, Grep, Task, WebFetch, WebSearch, TodoRead, TodoWrite, NotebookRead, NotebookEdit

**MCP tools**: Use `mcp__<server>__<tool>` pattern (e.g., `mcp__github__create_issue`)

### Accessing Tool Data

Hook input arrives via **stdin as JSON**. Use `jq` to extract values:

```bash
# Access file_path from Edit tool
jq -r '.tool_input.file_path'

# Access bash command
jq -r '.tool_input.command'

# Check if file matches pattern
jq -r '.tool_input.file_path' | { read file_path; if echo "$file_path" | grep -q '\.py$'; then echo "Python file"; fi; }

# Access tool response (PostToolUse only)
jq -r '.tool_response'
```

**Common JSON fields**:
- `.session_id` - Current session identifier
- `.transcript_path` - Path to conversation transcript
- `.cwd` - Current working directory
- `.tool_name` - Name of the tool being used
- `.tool_input` - Tool parameters (varies by tool)
- `.tool_response` - Tool output (PostToolUse only)
- `.hook_event_name` - Name of the event

**Environment variables**:
- `$CLAUDE_PROJECT_DIR` - Project root absolute path
- `$CLAUDE_ENV_FILE` - For SessionStart hooks to persist environment variables
- `$CLAUDE_CODE_REMOTE` - "true" if remote execution, empty if local
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory path (plugin hooks only)

## Hook Types

### Command Hooks

Execute bash scripts with stdin JSON input:

```json
{
  "type": "command",
  "command": "jq -r '.tool_input.file_path' | xargs -I {} prettier --write {}"
}
```

**Exit codes**:
- `0` - Success; stdout shown to user (except UserPromptSubmit shows to Claude)
- `2` - Blocking error; stderr fed to Claude as context
- Other - Non-blocking error; stderr shown to user

### Prompt Hooks

Send input to LLM (Haiku) for decisions (PreToolUse, Stop, SubagentStop, UserPromptSubmit):

```json
{
  "type": "prompt",
  "prompt": "Analyze this tool use and decide if it should be allowed: {{input}}"
}
```

Returns JSON with decision fields.

## Controlling Execution

### Blocking with Exit Codes

For PreToolUse only - exit code `2` blocks execution:

```bash
#!/bin/bash
# Block edits to .env files
file_path=$(jq -r '.tool_input.file_path')
if [[ "$file_path" == ".env" ]]; then
  echo "ERROR: Cannot edit .env file" >&2
  exit 2  # Blocks the edit
fi
exit 0  # Allows the edit
```

### Blocking with JSON Output

For PreToolUse, UserPromptSubmit, Stop, SubagentStop:

```json
{
  "permissionDecision": "deny",  // PreToolUse: "allow", "deny", "ask"
  "decision": "block",            // UserPromptSubmit/Stop/SubagentStop
  "reason": "Explanation shown to user",
  "systemMessage": "Warning message",
  "updatedInput": {...},          // PreToolUse: modify tool parameters
  "continue": false,              // Stop Claude execution
  "stopReason": "User message",
  "suppressOutput": true          // Hide from transcript
}
```

## Security Considerations

**⚠️ CRITICAL**: Hooks execute arbitrary shell commands automatically with your credentials.

**Security checklist**:
1. ✅ Review all hook commands before adding
2. ✅ Validate commands don't expose credentials
3. ✅ Avoid logging sensitive information
4. ✅ Test hooks in safe environment first
5. ✅ Limit hook scope with specific matchers
6. ✅ Always quote shell variables (`"$VAR"`)
7. ✅ Use absolute paths and check for path traversal
8. ✅ Avoid processing `.env`, `.git`, credentials files

**Hook configuration changes** require explicit review via `/hooks` menu before affecting current sessions.

## Practical Examples

### 1. Command Logging

Log all bash commands to audit file:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \\\"No description\\\")\"' | xargs -I {} sh -c 'echo \"$(date \"+%Y-%m-%d %H:%M:%S\") - {}\" >> ~/.claude-audit.log'"
          }
        ]
      }
    ]
  }
}
```

### 2. TypeScript/JavaScript Formatting

Auto-format after edits:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -qE '\\.(ts|tsx|js|jsx)$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 3. Python Formatting

Format Python files with Black and isort:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.py$'; then black \"$file_path\" && isort \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 4. File Protection

Block edits to sensitive files:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -qE '\\.(env|env\\..*|git/config|secrets\\.yaml)$'; then echo 'ERROR: Cannot edit protected file' >&2; exit 2; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 5. macOS Notification

Alert when Claude awaits input:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs your input\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

### 6. Linux Notification

Desktop notification with notify-send:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input' -u normal -t 5000"
          }
        ]
      }
    ]
  }
}
```

### 7. Git Safety Check

Warn before force push:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' | { read cmd; if echo \"$cmd\" | grep -q 'git push --force'; then echo '⚠️ WARNING: Force push detected. Press Enter to continue or Ctrl+C to cancel' >&2; read; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 8. Run Tests After Code Changes

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f package.json ]; then npm run test:quick 2>&1 | head -20; fi"
          }
        ]
      }
    ]
  }
}
```

### 9. Session Context on Start

Load project info when session starts:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"📋 Project: $(basename $(pwd)) | Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A') | Files changed: $(git status --short 2>/dev/null | wc -l)\""
          }
        ]
      }
    ]
  }
}
```

### 10. Multi-Language Formatting

Format multiple languages automatically:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; case \"$file_path\" in *.py) black \"$file_path\" && isort \"$file_path\";; *.ts|*.tsx|*.js|*.jsx) npx prettier --write \"$file_path\";; *.go) gofmt -w \"$file_path\";; *.rs) rustfmt \"$file_path\";; esac; }"
          }
        ]
      }
    ]
  }
}
```

## Advanced Patterns

### Conditional Execution

Execute only in specific conditions:

```bash
#!/bin/bash
# ~/.claude/hooks/conditional-formatter.sh

file_path=$(jq -r '.tool_input.file_path')

# Only format files in frontend/ directory
if [[ "$file_path" == frontend/* ]]; then
  case "$file_path" in
    *.ts|*.tsx)
      prettier --write "$file_path"
      ;;
    *.css)
      prettier --write "$file_path"
      ;;
  esac
fi
```

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/conditional-formatter.sh"
          }
        ]
      }
    ]
  }
}
```

### Environment-Specific Hooks

Different behavior per environment:

```bash
#!/bin/bash
# Check NODE_ENV before running tests

if [[ "$NODE_ENV" == "production" ]]; then
  echo "⚠️ Production environment - running full test suite..."
  npm run test:full
else
  echo "Development environment - running quick tests"
  npm run test:quick
fi
```

### Structured Logging with Context

Include git context in logs:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r --arg branch \"$(git rev-parse --abbrev-ref HEAD 2>/dev/null)\" --arg ts \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\" '{timestamp: $ts, branch: $branch, tool: .tool_name, command: .tool_input.command}' >> ~/.claude-context.jsonl"
          }
        ]
      }
    ]
  }
}
```

## Testing Your Hooks

### 1. Create Test Hook

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -I {} echo 'Reading: {}' >> /tmp/hook-test.log"
          }
        ]
      }
    ]
  }
}
```

### 2. Trigger the Hook

Ask Claude to read a file.

### 3. Verify Execution

```bash
cat /tmp/hook-test.log
# Should show: Reading: <file-path>
```

### 4. Test Blocking

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read fp; if [[ \"$fp\" == \"test.txt\" ]]; then echo 'Blocked test.txt' >&2; exit 2; fi; }"
          }
        ]
      }
    ]
  }
}
```

Attempt to edit test.txt - should be blocked.

## Common Mistakes to Avoid

❌ **Incorrect JSON structure**:
```json
{
  "hooks": [  // Wrong - should be object with event names as keys
    {"event": "PreToolUse", ...}
  ]
}
```

✅ **Correct structure**:
```json
{
  "hooks": {
    "PreToolUse": [  // Event name as key
      {"matcher": "Edit", ...}
    ]
  }
}
```

❌ **Using old environment variable syntax**:
```json
{
  "command": "black \"$file_path\""  // Variables don't work this way
}
```

✅ **Using jq to extract from stdin**:
```json
{
  "command": "jq -r '.tool_input.file_path' | xargs -I {} black {}"
}
```

❌ **Blocking in non-blocking events**:
```json
{
  "hooks": {
    "PostToolUse": [  // Can't block after execution
      {"matcher": "Edit", "hooks": [{"type": "command", "command": "exit 2"}]}
    ]
  }
}
```

❌ **Logging sensitive data**:
```json
{
  "command": "jq '.' | curl -d @- https://external-log-service.com"
}
```

✅ **Safe local logging**:
```json
{
  "command": "jq -r '{timestamp: now, tool: .tool_name}' >> ~/.local-audit.jsonl"
}
```

## Resources

Reference the examples directory for:
- Complete hook configurations for common scenarios
- Security-focused hook patterns
- Platform-specific notification scripts
- Multi-step automation workflows

---

**Next Steps**: After creating hooks, test in a safe environment, verify they don't leak credentials, check performance impact, and document for team members. Use `/hooks` menu to review and approve hook configuration changes.
