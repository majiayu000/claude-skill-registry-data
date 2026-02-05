---
name: headless
description: How to run Claude Code in headless mode for automation, scripting, and CI/CD integration. Use when user asks about non-interactive mode, automation, scripting, or programmatic usage.
---

# Claude Code Headless Mode

## Overview
Headless mode enables running Claude Code programmatically via command line without an interactive UI, making it suitable for automation, scripts, and integration with other tools.

## Basic Usage
The primary interface is the `claude` command with the `--print` (or `-p`) flag for non-interactive execution:

```bash
claude -p "Stage my changes and write commits" \
  --allowedTools "Bash,Read" \
  --permission-mode acceptEdits
```

## Key Configuration Options

| Flag | Purpose | Example |
|------|---------|---------|
| `--print`, `-p` | Run non-interactively | `claude -p "query"` |
| `--output-format` | Set output type (text, json, stream-json) | `claude -p --output-format json` |
| `--resume`, `-r` | Resume by session ID | `claude --resume abc123` |
| `--continue`, `-c` | Continue recent conversation | `claude --continue` |
| `--allowedTools` | Specify permitted tools | `claude --allowedTools "Bash,Read"` |
| `--mcp-config` | Load MCP servers from JSON | `claude --mcp-config servers.json` |

## Output Formats

### Text Output (Default)
Returns plain text response.

### JSON Output
Provides structured data with metadata:
```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "duration_ms": 1234,
  "num_turns": 6,
  "result": "Response text...",
  "session_id": "abc123"
}
```

### Streaming JSON Output
Emits messages as received in JSONL format, useful for real-time processing.

## Input Methods

### Text Input
Direct arguments or stdin:
```bash
echo "Explain this code" | claude -p
```

### Streaming JSON Input
Multiple conversation turns via stdin using JSONL format with `-p`, `--output-format stream-json`, and `--input-format stream-json`.

## Multi-turn Conversations

Resume existing sessions:
```bash
claude --continue "Refactor for performance"
claude --resume 550e8400-e29b-41d4-a716-446655440000 "Fix linting issues"
```

## Integration Examples

### SRE Incident Response
Diagnose issues with severity assessment using allowed tools and MCP configuration for monitoring integrations.

### Security Review
Audit pull request diffs for vulnerabilities and compliance issues using Read and WebSearch tools.

### Legal Assistant
Multi-step document review maintaining session context across separate requests.

## Best Practices

- Use JSON output for programmatic parsing and integration
- Parse results with tools like `jq` for data extraction
- Handle errors by checking exit codes and stderr
- Maintain session context for multi-turn workflows
- Implement timeouts for long-running operations
- Respect rate limits with delays between requests
- Leverage session management for maintaining conversation state

## Example: Automated Code Review

```bash
#!/bin/bash
# Review PR changes in headless mode

RESULT=$(claude -p "Review changes in git diff for security issues" \
  --allowedTools "Bash,Read,Grep" \
  --output-format json \
  --permission-mode acceptAll)

# Parse result
echo "$RESULT" | jq -r '.result'

# Check exit code
if [ $? -ne 0 ]; then
  echo "Review failed"
  exit 1
fi
```

## Example: CI/CD Integration

```bash
# In .gitlab-ci.yml or GitHub Actions
claude -p "Run tests and fix any failures" \
  --allowedTools "Bash,Read,Edit,Write" \
  --max-turns 10 \
  --output-format json
```

## Error Handling

Check exit codes and parse error messages:
- Exit code 0: Success
- Non-zero: Error occurred (check stderr)

```bash
if ! claude -p "task" 2>error.log; then
  echo "Error: $(cat error.log)"
  exit 1
fi
```

## Session Management

Save session IDs for continuation:
```bash
# First run
RESULT=$(claude -p "Start analysis" --output-format json)
SESSION_ID=$(echo "$RESULT" | jq -r '.session_id')

# Continue later
claude --resume "$SESSION_ID" "Continue analysis"
```
