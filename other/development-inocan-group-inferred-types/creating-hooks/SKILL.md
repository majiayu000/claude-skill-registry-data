---
name: Creating Hooks
description: Build event-driven hooks in Claude Code for validation, setup, and automation. Use when you need to validate inputs, check environment state, or automate tasks at specific lifecycle events.
---

# Creating Hooks

## Overview

Hooks are event-driven scripts that execute at specific points in Claude Code's lifecycle. They receive JSON input with session data and event-specific information, enabling validation, environment checks, and automated workflows.

## When to Use

- Validate tool inputs before execution (PreToolUse)
- Verify outputs after tool completion (PostToolUse)
- Check environment state before processing prompts (UserPromptSubmit)
- Initialize resources at session startup (SessionStart)
- Clean up resources at session end (SessionEnd)

## Hook Types

### PreToolUse
Runs before tool execution. Use for:
- Environment validation (check dependencies exist)
- Input validation (verify paths, parameters)
- Permission checks (ensure access rights)
- State verification (git status, working directory)

### PostToolUse
Runs after tool completion. Use for:
- Output validation (verify file changes)
- Quality checks (run linters, formatters)
- Side effects (update logs, metrics)
- Failure detection (check for errors)

### UserPromptSubmit
Runs before processing user input. Use for:
- Input sanitization
- Context injection
- Usage tracking
- Cost estimation

### SessionStart
Runs at session initialization. Use for:
- Environment setup
- Dependency checks
- Configuration loading
- Initialization logging

### SessionEnd
Runs at session termination. Use for:
- Cleanup tasks
- Result archiving
- Metrics reporting
- Resource deallocation

## JSON Input Structure

### Common Fields (All Events)

```json
{
  "session_id": "unique-session-identifier",
  "transcript_path": "/path/to/conversation.json",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse|PostToolUse|UserPromptSubmit|SessionStart|SessionEnd"
}
```

### Event-Specific Fields

**PreToolUse:**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "pytest tests/",
    "description": "Run test suite"
  }
}
```

**PostToolUse:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_response": {
    "success": true,
    "message": "File edited successfully"
  }
}
```

**UserPromptSubmit:**
```json
{
  "prompt": "User's input text here"
}
```

**SessionStart:**
```json
{
  "source": "startup|resume"
}
```

**SessionEnd:**
```json
{
  "reason": "user_exit|error|timeout"
}
```

## Configuration

### Path Resolution with CLAUDE_PROJECT_DIR

**Always use `$CLAUDE_PROJECT_DIR` to reference hook scripts.** Claude Code sets this environment variable to your project root, ensuring hooks work regardless of the current working directory.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

**Why this matters:**
- Claude's CWD can change during execution
- Relative paths like `./scripts/hook.sh` become fragile
- `$CLAUDE_PROJECT_DIR` always points to your project root
- Ensures hooks work from any directory

**Note:** The environment variable is only available when Claude Code spawns the hook command.

### Settings File Integration

Add hooks to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/pre-tool-hook.sh"
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
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/validate-edits.sh"
          }
        ]
      }
    ]
  }
}
```

### Matcher Patterns

- `*` - Match all tools
- `Edit` - Match specific tool
- `Edit|Write` - Match multiple tools
- `Bash(git:*)` - Match tool with pattern

## Process

1. **Identify the trigger event** - Which lifecycle point needs automation?
2. **Design hook script** - What validation or action is needed?
3. **Parse JSON input** - Extract relevant fields from stdin
4. **Implement logic** - Perform checks or automation
5. **Return exit code** - 0 for success, non-zero blocks execution
6. **Add to settings.json** - Configure hook with matcher
7. **Test hook** - Trigger event and verify behavior

## Examples

### Example 1: Pre-Tool Git Status Check

**Use case:** Warn if working directory is dirty before file operations

```bash
#!/bin/bash
# scripts/pre-tool-git-check.sh

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
  if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: Uncommitted changes in working directory"
    echo "Consider committing before editing files"
  fi
fi

exit 0  # Don't block, just warn
```

**Configuration:**
```json
{
  "PreToolUse": [{
    "matcher": "Edit|Write",
    "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/pre-tool-git-check.sh"}]
  }]
}
```

### Example 2: Post-Tool Code Formatting

**Use case:** Auto-format Python files after editing

```bash
#!/bin/bash
# scripts/post-edit-format.sh

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$TOOL_NAME" == "Edit" && "$FILE_PATH" == *.py ]]; then
  black "$FILE_PATH" --quiet
  echo "✅ Formatted $FILE_PATH with black"
fi

exit 0
```

### Example 3: Session Start Environment Check

**Use case:** Verify dependencies exist before starting

```bash
#!/bin/bash
# scripts/session-start-check.sh

MISSING=()

command -v python >/dev/null || MISSING+=("python")
command -v git >/dev/null || MISSING+=("git")
command -v jq >/dev/null || MISSING+=("jq")

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "❌ Missing dependencies: ${MISSING[*]}"
  exit 1  # Block session
fi

echo "✅ All dependencies available"
exit 0
```

## Best Practices

### Path Configuration
- ✅ **Do**: Always use `$CLAUDE_PROJECT_DIR` for hook script paths
- ✅ **Do**: Quote the path: `"$CLAUDE_PROJECT_DIR"/scripts/hook.sh`
- ❌ **Don't**: Use relative paths like `./scripts/hook.sh` (breaks if CWD changes)
- ❌ **Don't**: Use absolute paths like `/home/user/project/...` (not portable)

### Design
- ✅ **Do**: Keep hooks fast (<1 second)
- ✅ **Do**: Use specific matchers to reduce overhead
- ✅ **Do**: Return non-zero to block execution
- ❌ **Don't**: Perform expensive operations in hooks
- ❌ **Don't**: Block on warnings (use exit 0)

### Error Handling
- ✅ **Do**: Provide clear error messages
- ✅ **Do**: Log hook failures for debugging
- ✅ **Do**: Handle missing JSON fields gracefully
- ❌ **Don't**: Fail silently
- ❌ **Don't**: Assume JSON structure without validation

### JSON Parsing
- ✅ **Do**: Use `jq` for robust JSON parsing
- ✅ **Do**: Provide default values for optional fields
- ✅ **Do**: Validate required fields exist
- ❌ **Don't**: Use regex to parse JSON
- ❌ **Don't**: Assume fields are always present

### Performance
- ✅ **Do**: Exit early when hook doesn't apply
- ✅ **Do**: Cache expensive checks when possible
- ✅ **Do**: Use narrow matchers to reduce invocations
- ❌ **Don't**: Run hooks on every tool unconditionally
- ❌ **Don't**: Perform network requests without caching

## Integration Patterns

### With Git
```bash
# Check for uncommitted changes
git diff-index --quiet HEAD --

# Get current branch
git branch --show-current

# Check if file is tracked
git ls-files --error-unmatch "$FILE_PATH"
```

### With Linters
```bash
# Python
pylint "$FILE_PATH" --score=no --msg-template='{msg_id}: {msg}'

# JavaScript
eslint "$FILE_PATH" --format=compact

# Go
golint "$FILE_PATH"
```

### With Testing
```bash
# Run tests related to changed file
pytest "tests/test_${FILENAME}" --quiet

# Fast syntax check only
python -m py_compile "$FILE_PATH"
```

## Common Use Cases

### Validation Hooks
- Verify environment variables set
- Check file permissions
- Validate input parameters
- Ensure dependencies installed

### Quality Hooks
- Run linters on edited files
- Format code automatically
- Check test coverage
- Validate commit messages

### Workflow Hooks
- Update documentation
- Regenerate configuration
- Sync database schemas
- Trigger CI/CD pipelines

### Monitoring Hooks
- Log tool usage
- Track session metrics
- Report errors
- Update dashboards

## Anti-patterns

- ❌ **Don't**: Use relative or absolute paths for hook commands
  - ✅ **Do**: Use `$CLAUDE_PROJECT_DIR` for portable, reliable paths

- ❌ **Don't**: Use hooks for long-running tasks
  - ✅ **Do**: Keep hooks under 1 second

- ❌ **Don't**: Block on non-critical checks
  - ✅ **Do**: Use exit 0 for warnings

- ❌ **Don't**: Parse JSON with string manipulation
  - ✅ **Do**: Use `jq` for reliable parsing

- ❌ **Don't**: Match all tools without filtering
  - ✅ **Do**: Use specific matchers for relevant tools

- ❌ **Don't**: Ignore hook failures silently
  - ✅ **Do**: Provide clear feedback to user

## Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code/hooks
- **Settings Reference**: https://docs.claude.com/en/docs/claude-code/settings
- **JSON Parsing**: `man jq` or https://jqlang.github.io/jq/
