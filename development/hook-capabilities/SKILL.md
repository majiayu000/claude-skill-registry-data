---
name: hook-capabilities
description: Claude Code Hook system reference for capabilities, possibilities, and limitations. Use when you want to know what hooks can do.
allowed-tools: ["Read"]
---

# Claude Code Hook Capabilities

Reference for **what hooks can do** in Claude Code.

## Why Hooks Matter: The Only Guarantee

```
Hook = 100% execution guarantee (event-based)
Skill/Agent/MCP = ~20-80% (Claude's judgment)
```

**Key insight**: Hooks are the ONLY mechanism that executes without Claude's decision.
See [orchestration-patterns.md](references/orchestration-patterns.md) for forcing skill/agent activation.

## 5 Hook Roles

| Role | Description | Examples |
|------|-------------|----------|
| **Gate** | Block/allow tool execution | Prevent dangerous commands, workflow precondition checks |
| **Side Effect** | Auto-actions after tool execution | Formatters, linters, auto-commit |
| **State Manager** | Workflow state management | State file creation/deletion, phase tracking |
| **External Integrator** | External system integration | MCP calls, HTTP API, WebSocket, Slack |
| **Context Injector** | Session context injection | Load project settings, activate services |

## Event Types and Characteristics

| Event | Block | Special Features | Verification |
|-------|-------|------------------|--------------|
| SessionStart | No | source (compact/new) | Verified |
| UserPromptSubmit | Yes | **stdout auto-injects into Claude context** | Verified |
| PreToolUse | Yes | **updatedInput modifies input**, tool_use_id | Verified |
| PermissionRequest | Yes | **allow/deny/ask + input modification** | Unverified |
| PostToolUse | No | **tool_response** (access results) | Verified |
| Stop | Yes | **stop_hook_active** (loop prevention) | Verified |
| SubagentStop | Yes | parent-child correlation via tool_use_id | Unverified |
| Notification | No | includes notification_type | Verified |
| PreCompact | No | trigger (auto/manual) | Verified |
| SessionEnd | No | On session end | Unverified |

## 22 Universal Approaches

### Control Patterns

| Approach | Description | Event |
|----------|-------------|-------|
| **Iteration Control** | Track iteration count + max limit | Stop |
| **Force Continuation** | Use exit 2 to continue Claude work | Stop |
| **Promise Detection** | Detect Claude response patterns, conditional exit | Stop |
| **Infinite Loop Prevention** | Prevent recursion via parent_tool_use_id | UserPromptSubmit |
| **Threshold Branching** | Branch based on error/warning count | Stop |

### Input Manipulation

| Approach | Description | Event |
|----------|-------------|-------|
| **Input Modification** | Modify tool input via updatedInput | PreToolUse, PermissionRequest |
| **Path Normalization** | Auto-convert relative to absolute paths | PreToolUse |
| **Environment Injection** | Auto-inject environment variables | PreToolUse |
| **Dry-run Enforcement** | Auto-add --dry-run to dangerous commands | PreToolUse |

### Context Management

| Approach | Description | Event |
|----------|-------------|-------|
| **Context Injection** | stdout auto-injects into Claude context | UserPromptSubmit |
| **Progressive Loading** | Load context/skills on demand | UserPromptSubmit |
| **Skill Auto-Activation** | Keywords trigger skill suggestions | UserPromptSubmit |
| **Transcript Parsing** | Read and analyze previous responses | Stop |
| **Transcript Backup** | Backup session transcript | PreCompact |

### State Management

| Approach | Description | Event |
|----------|-------------|-------|
| **Session Cache** | Accumulate per-session state + aggregate results | PostToolUse |
| **Session Lifecycle** | Initialize/cleanup state via SessionStart/End | SessionStart/End |
| **Checkpoint Commit** | Checkpoint on every change, then squash | PostToolUse, Stop |
| **Session Branching** | Auto-isolate Git branches per session | Pre/PostToolUse |

### External Integration

| Approach | Description | Event |
|----------|-------------|-------|
| **Notification Forwarding** | Forward notifications to Slack/Discord/external | Notification |
| **Desktop/Audio Alert** | osascript, notify-send, TTS | Notification |
| **Subagent Correlation** | Track parent-child via tool_use_id | SubagentStop |

### Security & Compliance

| Approach | Description | Event |
|----------|-------------|-------|
| **Auto-Approval** | Auto-approve specific tools/commands | PermissionRequest |
| **Secret Scanning** | Detect and block API keys/secrets | PreToolUse |
| **Compliance Audit** | Compliance logging + violation detection | PostToolUse |

### Implementation Techniques

| Approach | Description | Event |
|----------|-------------|-------|
| **TypeScript Delegation** | Delegate complex logic to .ts | Any |
| **Hook Chaining** | Execute multiple hooks sequentially | Any |
| **Background Execution** | Async via run_in_background | Any |
| **Argument Pattern Matching** | Match arguments like `Bash(npm test*)` | PreToolUse |
| **MCP Tool Matching** | Match MCP like `mcp__memory__.*` | PreToolUse |
| **Prompt-Type Hook** | LLM evaluation via type: "prompt" | Any |

## Capabilities vs Limitations

| Possible | Not Possible |
|----------|--------------|
| File create/delete/modify | Block in PostToolUse |
| MCP/HTTP/WebSocket calls | Direct Claude context modification |
| UserPromptSubmit stdout to context | Delete existing context |
| PreToolUse/PermissionRequest input modification | Cancel already-executed tools |
| Continue work from Stop | Unlimited forcing (infinite loop risk) |

## Data Passing Methods (Important)

### stdin JSON (Verified)
All session/project info is passed via **stdin JSON**:
- `session_id` - Session UUID
- `cwd` - Project directory
- `transcript_path` - Session log file path
- `tool_use_id` - Tool call ID (PreToolUse/PostToolUse)

### stdin JSON Structure by Event

```bash
# UserPromptSubmit
{"prompt": "user message", "session_id": "...", "cwd": "/path"}

# PreToolUse / PostToolUse
{"tool_name": "Bash", "tool_input": {"command": "npm test"}, "session_id": "..."}

# PermissionRequest
{"tool_name": "Bash", "tool_input": {...}, "permission_type": "execute"}

# Stop
{"stop_reason": "end_turn", "session_id": "..."}

# SubagentStop
{"agent_name": "backend-dev", "result": "...", "session_id": "..."}
```

### Environment Variables (Verified)
`CLAUDE_PROJECT_DIR`, `CLAUDE_SESSION_ID` etc. are **NOT environment variables**!

Actually set environment variables:
```bash
CLAUDE_CODE_ENABLE_CFC="false"
CLAUDE_CODE_ENTRYPOINT="cli"
```

### Settings Reload
- `settings.json` changes **only apply in new sessions**

## Exit Code Reference

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success/Allow | Normal proceed |
| **1** | Error | Hook failure, show warning |
| **2** | Block/Continue | Varies by event |

**Exit 2 behavior by event**:

| Event | exit 2 Behavior |
|-------|-----------------|
| **PreToolUse** | Block tool execution |
| **PostToolUse** | Ignore result (prompt retry) |
| **PermissionRequest** | Deny permission request |
| **Stop** | Force Claude to continue |
| **UserPromptSubmit** | Abort prompt processing |

## Hook Execution Order

```
Multiple hooks on same event → Sequential execution (definition order)
One hook exits 2 → Subsequent hooks don't run
```

## Timeout Setting

```json
{"type": "command", "command": "script.sh", "timeout": 10000}
```

Default: 60000ms (1 minute)

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Not reading stdin | Missing JSON input | `INPUT=$(cat)` required |
| stdout debug output | Context pollution | Use stderr (`>&2`) |
| exit 1 vs exit 2 confusion | Unintended behavior | exit 1=error, exit 2=block |
| Parsing without jq | Unstable | Install and use jq |

## References

- [Event Details](references/event-details.md) - 10 event specifications
- [Pattern Details](references/patterns-detailed.md) - Role, usage, examples
- [Orchestration Patterns](references/orchestration-patterns.md) - **Force skill/agent activation**
- [Real-World Examples](references/real-world-examples.md) - Implementation case studies
- [Advanced Patterns](references/advanced-patterns.md) - Complex combinations
