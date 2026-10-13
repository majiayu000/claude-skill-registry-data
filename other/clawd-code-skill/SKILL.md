---
description: "Control Clawd Code via MCP protocol. Trigger with \"plan\" to write a precise execution plan then feed it to Clawd Code. Also supports direct commands, persistent sessions, agent teams, and advanced tool control."
---
# Clawd Code Skill

Control Clawd Code via MCP (Model Context Protocol). This skill unleashes the full power of Clawd Code for solanaos agents, including persistent sessions, agent teams, and advanced tool control.


---

## ⚡ Quick Start

```bash
# Start a persistent Clawd session for your project
clawd-code-skill session-start myproject -d ~/project \
  --permission-mode acceptEdits \
  --allowed-tools "Bash,Read,Edit,Write,Glob,Grep"

# Send a plan (Clawd will execute precisely)
clawd-code-skill session-send myproject --stream '<精确的执行计划>'

# Send with high effort (ultrathink) for complex reasoning
clawd-code-skill session-send myproject --stream --ultrathink 'Refactor the auth module'

# Enter plan mode — Clawd creates a plan first, then executes
clawd-code-skill session-send myproject --stream --plan 'Implement rate limiting'

# Check progress
clawd-code-skill session-status myproject

# Compact session when context gets large
clawd-code-skill session-compact myproject

# Switch model mid-session
clawd-code-skill session-model myproject opus
```

## 🎯 When to Use This Skill

### Use Persistent Sessions When:
- ✅ Multi-step tasks requiring multiple tool calls
- ✅ Iterative development (write code → test → fix → repeat)
- ✅ Long conversations needing full context
- ✅ Agent needs to work autonomously
- ✅ You want streaming real-time feedback

### Use Direct MCP Tools When:
- ✅ Single command execution
- ✅ Quick file read/write
- ✅ One-off searches
- ✅ No context needed between operations

## 📚 Command Reference

### Basic MCP Operations

```bash
# Connect to Clawd Code MCP
clawd-code-skill connect
clawd-code-skill status
clawd-code-skill tools

# Direct tool calls (no persistent session)
clawd-code-skill bash "npm test"
clawd-code-skill read /path/to/file.ts
clawd-code-skill glob "**/*.ts" -p ~/project
clawd-code-skill grep "TODO" -p ~/project -c
clawd-code-skill call Write -a '{"file_path":"/tmp/test.txt","content":"Hello"}'

# Disconnect
clawd-code-skill disconnect
```

### Persistent Sessions (Agent Loop)

#### Starting Sessions

```bash
# Basic start
clawd-code-skill session-start myproject -d ~/project

# With custom API endpoint (for Gemini/GPT proxy)
clawd-code-skill session-start gemini-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model gemini-2.0-flash

# With permission mode (plan = preview changes before applying)
clawd-code-skill session-start review -d ~/project --permission-mode plan

# With tool whitelist (auto-approve these tools)
clawd-code-skill session-start safe -d ~/project \
  --allowed-tools "Bash(git:*),Read,Glob,Grep"

# With budget limit
clawd-code-skill session-start limited -d ~/project --max-budget 1.50

# Full configuration
clawd-code-skill session-start advanced -d ~/project \
  --permission-mode acceptEdits \
  --allowed-tools "Bash,Read,Edit,Write" \
  --disallowed-tools "Task" \
  --max-budget 5.00 \
  --model clawd-opus-4-5 \
  --append-system-prompt "Always write tests" \
  --add-dir "/tmp,/var/log"
```

**Permission Modes:**
| Mode | Description |
|------|-------------|
| `acceptEdits` | Auto-accept file edits (default) |
| `plan` | Preview changes before applying |
| `default` | Ask for each operation |
| `bypassPermissions` | Skip all prompts (dangerous!) |
| `delegate` | Delegate decisions to parent |
| `dontAsk` | Never ask, reject by default |

#### Sending Messages

```bash
# Basic send (blocks until complete)
clawd-code-skill session-send myproject "Write unit tests for auth.ts"

# Streaming (see progress in real-time)
clawd-code-skill session-send myproject "Refactor this module" --stream

# With custom timeout
clawd-code-skill session-send myproject "Run all tests" -t 300000

# With effort control
clawd-code-skill session-send myproject "Quick lint fix" --effort low
clawd-code-skill session-send myproject "Design new auth system" --ultrathink

# Plan mode — Clawd creates a plan, then executes
clawd-code-skill session-send myproject --plan "Add rate limiting to all API endpoints"

# Auto-resume stopped sessions
clawd-code-skill session-send myproject "Continue the migration" --auto-resume

# NDJSON output for programmatic consumption
clawd-code-skill session-send myproject "Run tests" --stream --ndjson
```

#### Managing Sessions

```bash
# List active sessions
clawd-code-skill session-list

# Get detailed status
clawd-code-skill session-status myproject

# View conversation history
clawd-code-skill session-history myproject -n 50

# Pause and resume
clawd-code-skill session-pause myproject
clawd-code-skill session-resume-paused myproject

# Fork a session (create a branch for experiments)
clawd-code-skill session-fork myproject myproject-experiment

# Stop
clawd-code-skill session-stop myproject

# Restart a failed session
clawd-code-skill session-restart myproject
```

#### Effort & Model Control

```bash
# Set effort level for a session (persists across messages)
clawd-code-skill session-effort myproject low      # Fast, minimal thinking
clawd-code-skill session-effort myproject medium   # Balanced (default for Opus 4.6)
clawd-code-skill session-effort myproject high     # Deep thinking
clawd-code-skill session-effort myproject max      # Maximum capability, no token limit (Opus 4.6 only)
clawd-code-skill session-effort myproject auto     # Reset to default

# Switch model mid-session
clawd-code-skill session-model myproject opus
clawd-code-skill session-model myproject sonnet
clawd-code-skill session-model myproject gemini-pro

# Start session with effort preset
clawd-code-skill session-start myproject -d ~/project --effort high

# Model aliases (built-in: opus, sonnet, haiku, gemini-flash, gemini-pro)
# Custom aliases via --model-overrides
clawd-code-skill session-start myproject -d ~/project \
  --model-overrides '{"fast":"gemini-2.0-flash","smart":"clawd-opus-4-5"}'
```

#### Cost Tracking

```bash
# Show cost breakdown for a session
clawd-code-skill session-cost myproject
# → Model: clawd-opus-4-5
# → Tokens in: 12,345 | out: 3,456 | cached: 8,901
# → Breakdown: Input $0.0103 | Cached $0.0033 | Output $0.0518
# → 💰 Total: $0.0654
```

#### Branching

```bash
# Branch a session (fork + optional model/effort change)
clawd-code-skill session-branch myproject experiment
clawd-code-skill session-branch myproject fast-branch --model sonnet --effort low

# Branch preserves full conversation history from parent
# Both parent and branch continue independently
```

#### Hooks (Webhook Callbacks)

```bash
# List available hooks
clawd-code-skill session-hooks myproject

# Register webhook URLs for events
clawd-code-skill session-hooks myproject \
  --on-tool-error http://localhost:8080/webhook \
  --on-context-high http://localhost:8080/webhook \
  --on-stop http://localhost:8080/webhook

# Available hooks:
# onToolError    — a tool call failed
# onContextHigh  — context usage exceeded 70%
# onStop         — session stopped (includes cost summary)
# onTurnComplete — each turn finished (includes usage)
# onStopFailure  — API error (rate limit, auth failure)
```

#### Config Files

```bash
# Load session config from JSON file
clawd-code-skill session-start myproject --config agent.json

# agent.json example:
# {
#   "cwd": "~/project",
#   "permissionMode": "acceptEdits",
#   "allowedTools": ["Bash", "Read", "Edit", "Write"],
#   "effort": "high",
#   "maxBudget": "5.00",
#   "modelOverrides": { "fast": "gemini-2.0-flash" },
#   "appendSystemPrompt": "Always write tests"
# }
```

#### Context Management

```bash
# Compact session to reclaim context window
clawd-code-skill session-compact myproject

# Compact with custom summary
clawd-code-skill session-compact myproject --summary "Finished auth refactor, now on tests"

# Check context usage
clawd-code-skill session-context myproject
```

### Session History & Search

```bash
# Browse all Clawd Code sessions
clawd-code-skill sessions -n 20

# Search sessions by project
clawd-code-skill session-search --project ~/myapp

# Search by time
clawd-code-skill session-search --since "2h"
clawd-code-skill session-search --since "2024-02-01"

# Search by query
clawd-code-skill session-search "bug fix"

# Resume a historical session
clawd-code-skill resume <session-id> "Continue where we left off" -d ~/project
```

### Batch Operations

```bash
# Read multiple files at once
clawd-code-skill batch-read "src/**/*.ts" "tests/**/*.test.ts" -p ~/project
```

## 🤝 Agent Team Features

Deploy multiple Clawd agents working together on complex tasks.

### Basic Agent Team

```bash
# Define a team of agents
clawd-code-skill session-start team-project -d ~/project \
  --agents '{
    "architect": {
      "description": "Designs system architecture",
      "prompt": "You are a senior software architect. Design scalable, maintainable systems."
    },
    "developer": {
      "description": "Implements features",
      "prompt": "You are a full-stack developer. Write clean, tested code."
    },
    "reviewer": {
      "description": "Reviews code quality",
      "prompt": "You are a code reviewer. Check for bugs, style issues, and improvements."
    }
  }' \
  --agent architect

# Switch between agents mid-conversation
clawd-code-skill session-send team-project "Design the authentication system"
# (architect responds)

clawd-code-skill session-send team-project "@developer implement the design"
# (developer agent takes over)

clawd-code-skill session-send team-project "@reviewer review the implementation"
# (reviewer agent takes over)
```

### Pre-configured Team Templates

```bash
# Code review team
clawd-code-skill session-start review -d ~/project \
  --agents '{
    "security": {"prompt": "Focus on security vulnerabilities"},
    "performance": {"prompt": "Focus on performance issues"},
    "quality": {"prompt": "Focus on code quality and maintainability"}
  }' \
  --agent security

# Full-stack team
clawd-code-skill session-start fullstack -d ~/project \
  --agents '{
    "frontend": {"prompt": "React/TypeScript frontend specialist"},
    "backend": {"prompt": "Node.js/Express backend specialist"},
    "database": {"prompt": "PostgreSQL/Redis database specialist"}
  }' \
  --agent frontend
```

## 🔧 Advanced Features

### Tool Control

```bash
# Allow specific tools with patterns
--allowed-tools "Bash(git:*,npm:*),Read,Edit"

# Deny dangerous operations
--disallowed-tools "Bash(rm:*,sudo:*),Write(/etc/*)"

# Limit to specific tool set
--tools "Read,Glob,Grep"

# Disable all tools
--tools ""
```

### System Prompts

```bash
# Replace system prompt completely
--system-prompt "You are a Python expert. Always use type hints."

# Append to existing prompt
--append-system-prompt "Always run tests after changes."
```

### Session Management

```bash
# Resume with fork (create a branch)
--resume <session-id> --fork-session

# Use custom UUID for session
--session-id "550e8400-e29b-41d4-a716-446655440000"

# Add additional working directories
--add-dir "/var/log,/tmp/workspace"
```

### Multi-Model Support (Proxy)

Use `--base-url` to route requests through a proxy, enabling other models (Gemini, GPT) to power Clawd Code:

```bash
# Use Gemini via clawd-code-proxy
clawd-code-skill session-start gemini-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model clawd-3-5-sonnet-20241022  # Proxy will map to Gemini

# Use GPT via proxy
clawd-code-skill session-start gpt-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model clawd-3-haiku-20240307  # Proxy will map to GPT
```

**Note:** Requires `clawd-code-proxy` running on port 8082 with proper API keys configured.

```bash
# Start the proxy
cd ~/clawd/clawd-code-proxy && source .venv/bin/activate
uvicorn server:app --host 127.0.0.1 --port 8082
```

## 🎓 Best Practices

### For SolanaOS Agents

1. **Always use persistent sessions for multi-step tasks**
   ```bash
   # ❌ Bad: Multiple disconnect/reconnect cycles
   clawd-code-skill bash "step1"
   clawd-code-skill bash "step2"

   # ✅ Good: Single persistent session
   clawd-code-skill session-start task -d ~/project
   clawd-code-skill session-send task "Do step1 then step2"
   ```

2. **Use `--stream` for long-running tasks**
   ```bash
   clawd-code-skill session-send task "Run full test suite" --stream
   ```

3. **Set budget limits for safety**
   ```bash
   --max-budget 2.00  # Stop after $2 of API usage
   ```

4. **Use plan mode for critical changes**
   ```bash
   --permission-mode plan  # Preview before applying
   ```

5. **Fork before experiments**
   ```bash
   clawd-code-skill session-fork main experimental
   clawd-code-skill session-send experimental "Try risky refactor"
   ```

### Error Recovery

```bash
# If session fails:
clawd-code-skill session-status myproject  # Check what happened
clawd-code-skill session-history myproject -n 20  # See recent events
clawd-code-skill session-restart myproject  # Restart from last good state

# If you need to start over:
clawd-code-skill session-stop myproject
clawd-code-skill session-start myproject -d ~/project --resume <old-session-id>
```

## 🏗️ Architecture

```
solanaos agent
    ↓
clawd-code-skill CLI (this tool)
    ↓ HTTP
backend-api API (:18795)
    ↓ MCP
clawd mcp serve (Clawd Code)
    ↓
Your files & tools
```

## 🔌 Available Tools (via MCP)

All Clawd Code tools are accessible:

| Tool | Description |
|------|-------------|
| Bash | Execute shell commands |
| Read | Read file contents |
| Write | Create/overwrite files |
| Edit | Edit files with string replacement |
| Glob | Find files by pattern |
| Grep | Search file contents |
| Task | Launch sub-agents |
| WebFetch | Fetch web content |
| WebSearch | Search the web |
| Git* | Git operations |
| AskUserQuestion | Interactive prompts |
| ... | and 10+ more |

## 📊 Examples

### Example 1: Code Review

```bash
clawd-code-skill session-start review -d ~/myapp \
  --permission-mode plan \
  --agents '{"security":{"prompt":"Focus on security"},"quality":{"prompt":"Focus on quality"}}' \
  --agent security

clawd-code-skill session-send review \
  "Review all TypeScript files in src/, check for security issues and code quality problems" \
  --stream
```

### Example 2: Automated Testing

```bash
clawd-code-skill session-start test -d ~/myapp \
  --allowed-tools "Bash(npm:*,git:*),Read,Write" \
  --max-budget 1.00

clawd-code-skill session-send test \
  "Find all untested functions, write unit tests, run tests, fix failures"
```

### Example 3: Multi-Agent Debugging

```bash
clawd-code-skill session-start debug -d ~/myapp \
  --agents '{
    "detective": {"prompt": "Find the root cause of bugs"},
    "fixer": {"prompt": "Implement fixes"},
    "tester": {"prompt": "Verify fixes work"}
  }' \
  --agent detective

clawd-code-skill session-send debug "We have a memory leak in the API server" --stream
# Detective investigates, then hands off to fixer, then to tester
```

## 🔗 Integration with SolanaOS

When solanaos needs to perform complex coding tasks:

```bash
# From within solanaos agent context:
solanaos skills run clawd-code-skill -- session-start task -d ~/project
solanaos skills run clawd-code-skill -- session-send task "Implement feature X" --stream
solanaos skills run clawd-code-skill -- session-status task
```

Or use the skill programmatically via backend-api HTTP API (see TOOLS.md section 3).

## 📖 See Also

- **TOOLS.md section 3** - Full HTTP API documentation
- **backend-api endpoints** - Backend integration details
- **Clawd Code docs** - Official Clawd Code documentation (query via `qmd` tool)
