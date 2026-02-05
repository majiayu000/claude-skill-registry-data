---
name: gemini-json-parsing
description: Parse Gemini CLI headless output (JSON and stream-JSON formats). Covers response extraction, stats interpretation, error handling, and tool call analysis. Use when processing Gemini CLI programmatic output.
allowed-tools: Read, Bash
---

# Gemini JSON Parsing

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini JSON output:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific output format topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

Skill for parsing Gemini CLI's structured output formats. Essential for integration workflows where Claude needs to process Gemini's responses programmatically.

## When to Use This Skill

**Keywords:** parse gemini output, json output, stream json, gemini stats, token usage, jq parsing, gemini response

**Use this skill when:**

- Extracting responses from Gemini JSON output
- Analyzing token usage and costs
- Parsing tool call statistics
- Handling errors from Gemini CLI
- Building automation pipelines

## Output Formats

### Standard JSON (`--output-format json`)

Single JSON object returned after completion:

```json
{
  "response": "The main AI-generated content",
  "stats": {
    "models": {
      "gemini-2.5-pro": {
        "api": {
          "totalRequests": 2,
          "totalErrors": 0,
          "totalLatencyMs": 5053
        },
        "tokens": {
          "prompt": 24939,
          "candidates": 20,
          "total": 25113,
          "cached": 21263,
          "thoughts": 154,
          "tool": 0
        }
      }
    },
    "tools": {
      "totalCalls": 1,
      "totalSuccess": 1,
      "totalFail": 0,
      "totalDurationMs": 1881,
      "totalDecisions": {
        "accept": 0,
        "reject": 0,
        "modify": 0,
        "auto_accept": 1
      },
      "byName": {
        "google_web_search": {
          "count": 1,
          "success": 1,
          "fail": 0,
          "durationMs": 1881
        }
      }
    },
    "files": {
      "totalLinesAdded": 0,
      "totalLinesRemoved": 0
    }
  },
  "error": {
    "type": "ApiError",
    "message": "Error description",
    "code": 500
  }
}
```

### Stream JSON (`--output-format stream-json`)

Newline-delimited JSON (JSONL) with real-time events:

| Event Type | Description | Fields |
| --- | --- | --- |
| `init` | Session start | session_id, model, timestamp |
| `message` | User/assistant messages | role, content, timestamp |
| `tool_use` | Tool call requests | tool_name, tool_id, parameters |
| `tool_result` | Tool execution results | tool_id, status, output |
| `error` | Non-fatal errors | type, message |
| `result` | Final outcome | status, stats |

Example stream:

```jsonl
{"type":"init","timestamp":"2025-10-10T12:00:00.000Z","session_id":"abc123","model":"gemini-2.5-flash"}
{"type":"message","role":"user","content":"List files","timestamp":"2025-10-10T12:00:01.000Z"}
{"type":"tool_use","tool_name":"Bash","tool_id":"bash-123","parameters":{"command":"ls -la"}}
{"type":"tool_result","tool_id":"bash-123","status":"success","output":"file1.txt\nfile2.txt"}
{"type":"message","role":"assistant","content":"Here are the files...","delta":true}
{"type":"result","status":"success","stats":{"total_tokens":250}}
```

## Common Extraction Patterns

### Extract Response Text

```bash
# Get main response
gemini "query" --output-format json | jq -r '.response'

# With error handling
result=$(gemini "query" --output-format json)
if echo "$result" | jq -e '.error' > /dev/null 2>&1; then
  echo "Error: $(echo "$result" | jq -r '.error.message')"
else
  echo "$result" | jq -r '.response'
fi
```

### Token Statistics

```bash
# Total tokens used
echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add'

# Cached tokens (cost savings)
echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add'

# Billable tokens
total=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add')
cached=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add')
echo "Billable: $((total - cached))"

# Tokens by model
echo "$result" | jq '.stats.models | to_entries[] | "\(.key): \(.value.tokens.total) tokens"'
```

### Tool Call Analysis

```bash
# Total tool calls
echo "$result" | jq '.stats.tools.totalCalls'

# List tools used
echo "$result" | jq -r '.stats.tools.byName | keys | join(", ")'

# Tool success rate
total=$(echo "$result" | jq '.stats.tools.totalCalls')
success=$(echo "$result" | jq '.stats.tools.totalSuccess')
echo "Success rate: $((success * 100 / total))%"

# Detailed tool stats
echo "$result" | jq '.stats.tools.byName | to_entries[] | "\(.key): \(.value.count) calls, \(.value.durationMs)ms"'
```

### Model Usage

```bash
# List models used
echo "$result" | jq -r '.stats.models | keys | join(", ")'

# Model latency
echo "$result" | jq '.stats.models | to_entries[] | "\(.key): \(.value.api.totalLatencyMs)ms"'

# Request counts
echo "$result" | jq '.stats.models | to_entries[] | "\(.key): \(.value.api.totalRequests) requests"'
```

### Error Handling

```bash
# Check for errors
if echo "$result" | jq -e '.error' > /dev/null 2>&1; then
  error_type=$(echo "$result" | jq -r '.error.type // "Unknown"')
  error_msg=$(echo "$result" | jq -r '.error.message // "No message"')
  error_code=$(echo "$result" | jq -r '.error.code // "N/A"')
  echo "Error [$error_type]: $error_msg (code: $error_code)"
  exit 1
fi
```

### File Modifications

```bash
# Lines changed
echo "$result" | jq '"Added: \(.stats.files.totalLinesAdded), Removed: \(.stats.files.totalLinesRemoved)"'
```

## Stream Processing

### Filter by Event Type

```bash
# Get only tool results
gemini --output-format stream-json -p "query" | jq -r 'select(.type == "tool_result")'

# Get only errors
gemini --output-format stream-json -p "query" | jq -r 'select(.type == "error")'

# Get assistant messages
gemini --output-format stream-json -p "query" | jq -r 'select(.type == "message" and .role == "assistant") | .content'
```

### Real-time Monitoring

```bash
# Watch tool calls as they happen
gemini --output-format stream-json -p "analyze code" | while read line; do
  type=$(echo "$line" | jq -r '.type')
  case "$type" in
    tool_use)
      tool=$(echo "$line" | jq -r '.tool_name')
      echo "[TOOL] Calling: $tool"
      ;;
    tool_result)
      status=$(echo "$line" | jq -r '.status')
      echo "[RESULT] Status: $status"
      ;;
    error)
      msg=$(echo "$line" | jq -r '.message')
      echo "[ERROR] $msg"
      ;;
  esac
done
```

## Quick Reference

| What | jq Command |
| --- | --- |
| Response text | `.response` |
| Total tokens | `.stats.models \| to_entries \| map(.value.tokens.total) \| add` |
| Cached tokens | `.stats.models \| to_entries \| map(.value.tokens.cached) \| add` |
| Tool calls | `.stats.tools.totalCalls` |
| Tools used | `.stats.tools.byName \| keys \| join(", ")` |
| Models used | `.stats.models \| keys \| join(", ")` |
| Error message | `.error.message // "none"` |
| Error type | `.error.type // "none"` |
| Lines added | `.stats.files.totalLinesAdded` |
| Lines removed | `.stats.files.totalLinesRemoved` |
| Total latency | `.stats.models \| to_entries \| map(.value.api.totalLatencyMs) \| add` |

## Complete Example

```bash
#!/bin/bash
# Analyze code and report stats

result=$(cat src/main.ts | gemini "Review this code for security issues" --output-format json)

# Check for errors
if echo "$result" | jq -e '.error' > /dev/null 2>&1; then
  echo "Error: $(echo "$result" | jq -r '.error.message')"
  exit 1
fi

# Extract response
echo "=== Security Review ==="
echo "$result" | jq -r '.response'

# Report stats
echo ""
echo "=== Stats ==="
total=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.total) | add // 0')
cached=$(echo "$result" | jq '.stats.models | to_entries | map(.value.tokens.cached) | add // 0')
models=$(echo "$result" | jq -r '.stats.models | keys | join(", ") | if . == "" then "none" else . end')
tools=$(echo "$result" | jq '.stats.tools.totalCalls // 0')

echo "Tokens: $total (cached: $cached)"
echo "Models: $models"
echo "Tool calls: $tools"
```

## Test Scenarios

### Scenario 1: Extract Response

**Query**: "How do I extract the response from Gemini JSON output?"
**Expected Behavior**:

- Skill activates on "parse gemini output" or "json output"
- Provides jq extraction pattern
**Success Criteria**: User receives `.response` extraction command

### Scenario 2: Token Usage Analysis

**Query**: "How do I track token usage from Gemini CLI?"
**Expected Behavior**:

- Skill activates on "token usage" or "gemini stats"
- Provides stats extraction patterns
**Success Criteria**: User receives token calculation jq commands

### Scenario 3: Stream Processing

**Query**: "How do I process Gemini CLI stream-json output?"
**Expected Behavior**:

- Skill activates on "stream json"
- Provides JSONL processing patterns
**Success Criteria**: User receives real-time stream processing example

## References

Query `gemini-cli-docs` for official documentation on:

- "json output format"
- "stream-json output"
- "headless mode"

## Version History

- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
