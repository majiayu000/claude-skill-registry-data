---
name: plugin-test-framework
description: Virtual test environment for Claude Code hooks, plugins, and agents. Use when testing or validating plugin components without affecting production.
version: 1.0.0
---

# Plugin Test Framework

Create isolated virtual test environments to verify hooks, plugins, and agents work correctly.

## Quick Start

```bash
# Create test environment
/skillmaker:test-env hook     # Hook test environment
/skillmaker:test-env plugin   # Full plugin test
/skillmaker:test-env agent    # Agent test

# Run tests
/skillmaker:run-tests /tmp/test-env
```

## Test Environment Structure

```
/tmp/plugin-test-{uuid}/
├── .claude/
│   ├── settings.json          # Hook configurations
│   └── hooks/
│       ├── *.sh               # Hook scripts
│       └── logs/              # Execution logs
├── .claude-plugin/
│   └── plugin.json            # Plugin metadata
├── commands/
│   └── *.md                   # Slash commands
├── skills/
│   └── */SKILL.md             # Skills
├── agents/
│   └── *.md                   # Agent definitions
├── run-tests.sh               # Test runner
└── TEST-RESULTS.md            # Results
```

## Test Types

### 1. Hook Tests

Verify hook scripts respond correctly to events.

**Test Cases:**
| Test | Input | Expected |
|------|-------|----------|
| Block dangerous command | `rm -rf /` | `permissionDecision: "deny"` |
| Modify input | `npm publish` | `updatedInput` with `--dry-run` |
| Auto-allow safe | `echo hello` | `permissionDecision: "allow"` |
| Log success | PostToolUse + success | `success: true` in log |
| Log failure | PostToolUse + error | `success: false` in log |
| Context inject | UserPromptSubmit | stdout becomes context |
| Stop control | Stop + incomplete | `decision: "block"` |

**Hook Test JSON Format:**
```json
{
  "session_id": "test-001",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {"command": "rm -rf /important"},
  "cwd": "/tmp/test"
}
```

### 2. Plugin Tests

Verify plugin structure and component registration.

**Validation Checks:**
- [ ] `.claude-plugin/plugin.json` exists and valid
- [ ] `commands/*.md` have correct frontmatter
- [ ] `skills/*/SKILL.md` have correct structure
- [ ] `agents/*.md` have correct format
- [ ] `hooks/hooks.json` is valid (if exists)

**Plugin Structure Validation:**
```bash
# Check required fields in plugin.json
jq -e '.name and .description' .claude-plugin/plugin.json

# Validate command frontmatter
for cmd in commands/*.md; do
  grep -q "^description:" "$cmd"
done
```

### 3. Agent Tests

Verify agent definitions and tool access.

**Agent Test Cases:**
| Test | Check |
|------|-------|
| Tool list valid | All tools exist in Claude Code |
| Description present | Non-empty description |
| Prompt template | Valid prompt structure |
| Model specification | Valid model (sonnet/opus/haiku) |

## Test Runner API

### Create Test Environment

```bash
create_test_env() {
    local TYPE="$1"  # hook, plugin, agent, full
    local TEST_DIR="/tmp/plugin-test-$(date +%s)"

    mkdir -p "$TEST_DIR/.claude/hooks/logs"
    mkdir -p "$TEST_DIR/.claude-plugin"
    mkdir -p "$TEST_DIR/commands"
    mkdir -p "$TEST_DIR/skills/test-skill"
    mkdir -p "$TEST_DIR/agents"

    # Generate based on type
    case "$TYPE" in
        hook) generate_hook_tests "$TEST_DIR" ;;
        plugin) generate_plugin_tests "$TEST_DIR" ;;
        agent) generate_agent_tests "$TEST_DIR" ;;
        full) generate_all_tests "$TEST_DIR" ;;
    esac

    echo "$TEST_DIR"
}
```

### Run Tests

```bash
run_tests() {
    local TEST_DIR="$1"
    local RESULTS="$TEST_DIR/TEST-RESULTS.md"

    echo "# Test Results" > "$RESULTS"
    echo "Date: $(date)" >> "$RESULTS"

    # Hook tests
    if [ -d "$TEST_DIR/.claude/hooks" ]; then
        run_hook_tests "$TEST_DIR" >> "$RESULTS"
    fi

    # Plugin validation
    if [ -f "$TEST_DIR/.claude-plugin/plugin.json" ]; then
        validate_plugin "$TEST_DIR" >> "$RESULTS"
    fi

    # Agent validation
    if [ -d "$TEST_DIR/agents" ]; then
        validate_agents "$TEST_DIR" >> "$RESULTS"
    fi

    cat "$RESULTS"
}
```

## Hook Test Templates

### PreToolUse Guard Hook

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Block dangerous patterns
if echo "$COMMAND" | grep -qE "rm\s+-rf\s+/"; then
    jq -n '{
      "hookSpecificOutput": {
        "permissionDecision": "deny"
      },
      "systemMessage": "Dangerous command blocked"
    }'
    exit 0
fi

exit 0
```

### PostToolUse Logger

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
RESPONSE=$(echo "$INPUT" | jq -c '.tool_response // {}')

SUCCESS=true
echo "$RESPONSE" | grep -qiE "(error|failed)" && SUCCESS=false

jq -n --arg tool "$TOOL_NAME" --argjson success "$SUCCESS" \
    '{tool: $tool, success: $success, timestamp: now|todate}'
```

### UserPromptSubmit Context Injector

```bash
#!/bin/bash
INPUT=$(cat)

# stdout becomes Claude context
echo "=== Test Context ==="
echo "Environment: TEST"
echo "Time: $(date)"
echo "==================="

exit 0
```

## Plugin Validation

### plugin.json Schema

```json
{
  "name": "string (required)",
  "description": "string (required)",
  "version": "string (optional)",
  "author": {
    "name": "string",
    "email": "string"
  }
}
```

### Command Frontmatter

```yaml
---
description: Required description
argument-hint: Optional hint
allowed-tools: ["Tool1", "Tool2"]
---
```

### Skill Structure

```
skills/skill-name/
├── SKILL.md          # Required
└── references/       # Optional
    └── *.md
```

## Agent Validation

### Agent Format

```markdown
---
description: Agent description
allowed-tools: ["Read", "Write", "Bash"]
model: haiku  # or sonnet, opus
---

# Agent Name

Agent prompt content...
```

### Valid Tools List

```
Read, Write, Edit, Bash, Glob, Grep, Task,
TodoWrite, WebFetch, WebSearch, AskUserQuestion,
NotebookEdit, NotebookRead, KillShell, Skill
```

## Usage Examples

### Test a Hook Script

```bash
# Simulate PreToolUse event
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | \
    ./hook-script.sh
```

### Validate Plugin Structure

```bash
# Quick validation
test -f .claude-plugin/plugin.json && \
    jq -e '.name' .claude-plugin/plugin.json && \
    echo "Plugin valid"
```

### Test Agent Definition

```bash
# Check agent frontmatter
head -10 agents/my-agent.md | grep -E "^(description|allowed-tools|model):"
```

## Test Results Format

```markdown
# Test Results
Date: 2026-01-02

## Hook Tests
- ✅ Block dangerous rm
- ✅ Modify npm publish
- ✅ Auto-allow safe commands
- ✅ Log tool usage

## Plugin Validation
- ✅ plugin.json valid
- ✅ Commands have frontmatter
- ✅ Skills structured correctly

## Agent Validation
- ✅ All agents have descriptions
- ✅ Tool lists valid

## Summary
- Passed: 10/10
- Failed: 0/10
```

## Integration with CI

```yaml
# .github/workflows/test-plugin.yml
name: Plugin Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create test environment
        run: ./scripts/create-test-env.sh
      - name: Run tests
        run: ./scripts/run-tests.sh
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: TEST-RESULTS.md
```
