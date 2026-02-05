---
name: cli-reference
description: Complete CLI command reference for Claude Code including flags, options, and usage patterns. Use when user asks about command-line options, flags, CLI usage, or command syntax.
---

# Claude Code CLI Reference

## CLI Commands

### Interactive Mode

**Start interactive REPL:**
```bash
claude
```

**Start with initial prompt:**
```bash
claude "query"
```

### Non-Interactive Mode

**Query via SDK, then exit:**
```bash
claude -p "query"
claude --print "query"
```

**Process piped content:**
```bash
cat file | claude -p "query"
echo "content" | claude -p "analyze this"
```

**Continue most recent conversation:**
```bash
claude -c
claude --continue
```

**Continue via SDK:**
```bash
claude -c -p "query"
```

**Resume session by ID:**
```bash
claude -r "<session-id>" "query"
claude --resume "<session-id>" "query"
```

### Maintenance

**Update to latest version:**
```bash
claude update
```

**Configure MCP servers:**
```bash
claude mcp
```

**Check installation health:**
```bash
claude --doctor
```

**Migrate installer:**
```bash
claude migrate-installer
```

## Key CLI Flags

### Essential Flags

| Flag | Short | Purpose | Example |
|------|-------|---------|---------|
| `--print` | `-p` | Print response without interactive mode | `claude -p "task"` |
| `--continue` | `-c` | Continue most recent conversation | `claude -c "follow up"` |
| `--resume` | `-r` | Resume session by ID | `claude -r abc123 "task"` |
| `--help` | `-h` | Show help information | `claude --help` |
| `--version` | `-v` | Show version | `claude --version` |

### Configuration Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--add-dir` | Add working directories for access | `claude --add-dir /path/to/dir` |
| `--agents` | Define custom subagents dynamically via JSON | `claude --agents '[{...}]'` |
| `--model` | Set model with alias or full name | `claude --model opus` |
| `--max-turns` | Limit agentic turns in non-interactive mode | `claude --max-turns 5` |
| `--permission-mode` | Begin in specified permission mode | `claude --permission-mode acceptAll` |
| `--allowedTools` | Specify permitted tools | `claude --allowedTools "Bash,Read"` |

### Output & Format Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--output-format` | Specify format (text, json, stream-json) | `claude -p --output-format json` |
| `--input-format` | Specify input format | `claude --input-format stream-json` |
| `--verbose` | Enable detailed logging for debugging | `claude --verbose` |
| `--debug` | Enable debug mode | `claude --debug` |

### Advanced Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--mcp-config` | Load MCP servers from JSON file | `claude --mcp-config servers.json` |
| `--append-system-prompt` | Append text to system prompt | `claude --append-system-prompt "Be concise"` |
| `--compact` | Start with compacted context | `claude --compact` |
| `--no-cache` | Disable prompt caching | `claude --no-cache` |

## Agents Flag Format

Custom subagents require JSON with:
- `description`: Purpose of the subagent
- `prompt`: System prompt for the subagent
- `tools` (optional): Array of allowed tools
- `model` (optional): Model to use

**Example:**
```bash
claude --agents '[{
  "description": "Code reviewer",
  "prompt": "Review code for quality and security",
  "tools": ["Read", "Grep", "Glob"],
  "model": "sonnet"
}]'
```

## Permission Modes

| Mode | Description |
|------|-------------|
| `ask` | Ask for permission for each operation (default) |
| `acceptAll` | Accept all operations automatically |
| `acceptEdits` | Auto-accept file edits, ask for bash |
| `acceptCommands` | Auto-accept bash, ask for edits |
| `denyAll` | Deny all operations |

**Example:**
```bash
claude --permission-mode acceptEdits -p "refactor the code"
```

## Model Aliases

| Alias | Full Model Name |
|-------|----------------|
| `sonnet` | claude-sonnet-4-5-20250929 |
| `opus` | claude-opus-4-5-20250514 |
| `haiku` | claude-haiku-4-5-20250815 |

**Example:**
```bash
claude --model opus "complex reasoning task"
claude --model haiku -p "simple query"
```

## Output Formats

### Text (Default)

Plain text output suitable for reading:
```bash
claude -p "explain this code"
```

### JSON

Structured output with metadata:
```bash
claude -p --output-format json "analyze project"
```

**JSON structure:**
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

### Stream JSON

JSONL format for real-time processing:
```bash
claude -p --output-format stream-json --input-format stream-json
```

## Environment Variables

Key environment variables affecting CLI behavior:

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API authentication |
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | Enable telemetry |
| `DISABLE_PROMPT_CACHING` | Disable caching |
| `MAX_THINKING_TOKENS` | Enable extended thinking |
| `BASH_MAX_OUTPUT_LENGTH` | Limit bash output |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens |

## Common Usage Patterns

### Quick Query
```bash
claude -p "what does this project do?"
```

### Automated Task
```bash
claude -p "run tests and fix failures" \
  --allowedTools "Bash,Read,Edit,Write" \
  --max-turns 10 \
  --permission-mode acceptAll
```

### Resume Previous Work
```bash
claude -c "continue the refactoring"
```

### Custom Configuration
```bash
claude \
  --model sonnet \
  --permission-mode acceptEdits \
  --verbose \
  --add-dir /path/to/project
```

### CI/CD Integration
```bash
claude -p "review PR changes" \
  --output-format json \
  --allowedTools "Read,Bash" \
  --max-turns 5
```

### MCP with Custom Servers
```bash
claude --mcp-config mcp-servers.json -p "fetch user data"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 130 | Interrupted (Ctrl+C) |

## Tips & Tricks

### Piping Input

```bash
# Pipe file content
cat script.py | claude -p "explain this code"

# Pipe command output
git diff | claude -p "review these changes"

# Pipe from multiple sources
cat file1.txt file2.txt | claude -p "summarize"
```

### Chaining Commands

```bash
# With AND operator
claude -p "task 1" && claude -p "task 2"

# With OR operator
claude -p "task" || echo "Failed"
```

### Background Execution

```bash
# Run in background
claude -p "long task" &

# With output redirection
claude -p "task" > output.txt 2>&1 &
```

### Parsing JSON Output

```bash
# Extract specific field with jq
claude -p "task" --output-format json | jq -r '.result'

# Get session ID
SESSION=$(claude -p "task" --output-format json | jq -r '.session_id')

# Check cost
claude -p "task" --output-format json | jq '.total_cost_usd'
```

### Using with Scripts

```bash
#!/bin/bash

# Check if task succeeded
RESULT=$(claude -p "run tests" --output-format json)
STATUS=$(echo "$RESULT" | jq -r '.subtype')

if [ "$STATUS" = "success" ]; then
  echo "Tests passed"
else
  echo "Tests failed"
  exit 1
fi
```

## Debugging

### Enable Verbose Output

```bash
claude --verbose -p "task"
```

### Enable Debug Mode

```bash
claude --debug
```

### Check Version

```bash
claude --version
```

### View Help

```bash
claude --help
claude -h
```

## Best Practices

1. **Use specific flags** for automation and scripts
2. **Enable JSON output** for programmatic parsing
3. **Set max-turns** to prevent runaway operations
4. **Configure permissions** appropriately for security
5. **Use model aliases** for readability
6. **Pipe stderr to logs** for error tracking
7. **Check exit codes** in scripts
8. **Use --allowedTools** to restrict capabilities
9. **Set timeouts** for long-running tasks
10. **Test with --verbose** before production use
