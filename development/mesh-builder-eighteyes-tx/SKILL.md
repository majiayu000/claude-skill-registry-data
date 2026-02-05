---
name: mesh-builder
description: Comprehensive guide for building meshes in TX V4. Covers SDK-based worker architecture, agent design, prompt templates, message protocols, and HITL workflows. Use when creating new meshes, defining agent roles, or debugging multi-agent systems.
---

# Mesh Builder: TX V4

This skill provides comprehensive guidance for creating meshes and agents in TX V4's SDK-based architecture.

## TX V4 Architecture

### Core Differences from V3

| Aspect | V3 (Legacy) | V4 (Current) |
|--------|-------------|--------------|
| **Workers** | Tmux sessions | Claude Agent SDK (`query()`) |
| **Messaging** | `tmux send-keys` | Write tool to `.ai/tx/msgs/` |
| **Queue** | File watching only | SQLite + file watching |
| **Core** | Tmux (for HITL) | Tmux (unchanged) |
| **Models** | Full model IDs | Semantic names: `opus`, `sonnet`, `haiku` |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        TX V4 System                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐        ┌──────────────────┐               │
│  │   User (tmux)    │        │   CLI Commands   │               │
│  │   - Sees core    │        │   tx start/msg   │               │
│  │   - HITL here    │        │   tx status/spy  │               │
│  └────────┬─────────┘        └────────┬─────────┘               │
│           │                           │                          │
│           ▼                           ▼                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Core Agent (tmux)                       │  │
│  │  - User interface layer                                    │  │
│  │  - HITL handler: shows ask-human, captures responses       │  │
│  │  - Routes tasks to workers via queue                       │  │
│  └───────────────────────────────┬───────────────────────────┘  │
│                                  │                               │
│                                  ▼                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   SQLite Queue (Bridge)                    │  │
│  │  - Messages flow: File → Consumer → SQLite → Dispatcher    │  │
│  │  - Tracks: messages, tasks, agent state                    │  │
│  └───────────────────────────────┬───────────────────────────┘  │
│                                  │                               │
│           ┌──────────────────────┼──────────────────────┐       │
│           │                      │                      │       │
│           ▼                      ▼                      ▼       │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐ │
│  │  Brain Agent   │    │   Dev Agent    │    │  Test Agent    │ │
│  │   (SDK/opus)   │    │  (SDK/sonnet)  │    │  (SDK/haiku)   │ │
│  │                │    │                │    │                │ │
│  │ - Know gateway │    │ - Coding       │    │ - Testing      │ │
│  │ - Spec-graph   │    │ - Refactoring  │    │ - Validation   │ │
│  └────────────────┘    └────────────────┘    └────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### SDK Worker Execution

Workers run via the Claude Agent SDK's `query()` function:

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const q = query({
  prompt: userPrompt,
  options: {
    cwd: workDir,
    model: 'opus',  // Semantic: opus, sonnet, haiku
    systemPrompt: agentPrompt,
    permissionMode: 'bypassPermissions',
    maxTurns: 50,
  }
});

for await (const msg of q) {
  // Handle assistant messages, tool calls, results
}
```

### Model Selection (Claude Opus 4.5 Era)

| Semantic Name | Use Case | Characteristics |
|---------------|----------|-----------------|
| `opus` | Complex reasoning, architecture, synthesis | Most capable, slower, higher cost |
| `sonnet` | General tasks, coding, coordination | Balanced speed/capability |
| `haiku` | Simple tasks, validation, echoing | Fastest, lowest cost |

**Recommendations**:
- **Brain agent**: `opus` (needs deep reasoning for spec-graph)
- **Dev agent**: `sonnet` or `opus` (coding requires good reasoning)
- **Test agents**: `haiku` (simple validation tasks)
- **Coordinator agents**: `sonnet` (good balance)

## Message Protocol

### Centralized Event Log

ALL messages go to `.ai/tx/msgs/` with this filename format:
```
{timestamp}-{type}-{from}--{to}-{msg-id}.md
```

Example: `1733901000-task-core--brain-brain-abc123.md`

### Message Frontmatter

```yaml
---
to: mesh/agent           # Recipient (e.g., brain/brain, core/core)
from: mesh/agent         # Sender
type: task | task-complete | ask | ask-response | ask-human
msg-id: unique-id        # For correlation
headline: Brief summary  # Human-readable
timestamp: ISO-8601      # When created
command: /slash:command  # Optional: triggers slash command
---

Message body content here.

Markdown formatting supported.
```

### Message Types

| Type | Direction | Purpose |
|------|-----------|---------|
| `task` | core → worker | Assign work |
| `task-complete` | worker → core | Report completion |
| `ask` | agent → agent | Request information |
| `ask-response` | agent → agent | Provide answer |
| `ask-human` | worker → core | Request human input (HITL) |

### Slash Command Routing

Messages can include a `command` field to trigger slash commands:

```yaml
---
to: brain/brain
from: core/core
type: task
command: /know:prepare
msg-id: task-123
headline: Execute /know:prepare
---

User requested: /know:prepare
```

The worker receives this and executes the slash command.

## Building Meshes

### Directory Structure

```
v4/
├── meshes/
│   │
│   │  # Core meshes (top-level) - main workflow meshes
│   ├── brain/                 # Knowledge gateway, spec-graph
│   │   ├── config.yaml
│   │   └── prompt.md
│   ├── dev/                   # Development, coding tasks
│   │   ├── config.yaml
│   │   └── prompt.md
│   ├── deep-research/         # Multi-agent research pipeline
│   │   ├── config.yaml
│   │   ├── interviewer/
│   │   │   └── prompt.md
│   │   ├── sourcer/
│   │   │   └── prompt.md
│   │   ├── analyst/
│   │   │   └── prompt.md
│   │   ├── researcher/
│   │   │   └── prompt.md
│   │   ├── disprover/
│   │   │   └── prompt.md
│   │   └── writer/
│   │       └── prompt.md
│   ├── test/                  # Simple test mesh
│   │   ├── config.yaml
│   │   └── prompt.md
│   │
│   │  # System meshes - internal TX functionality
│   ├── system/
│   │   └── commit-agent/      # Auto-commit functionality
│   │       ├── config.yaml
│   │       └── prompt.md
│   │
│   │  # Protagent meshes - user-defined productivity agents
│   └── protagents/
│       └── meet/              # Meeting coordination with MCP
│           ├── config.yaml
│           └── scheduler/
│               └── prompt.md
│
└── .ai/tx/
    ├── msgs/                  # Message event log
    ├── data/                  # SQLite queue
    ├── logs/                  # System logs
    └── sessions/              # Captured worker sessions
```

### Mesh Categories

| Category | Path | Purpose |
|----------|------|---------|
| **Core** | `meshes/{name}/` | Main workflow meshes (brain, dev, research) |
| **System** | `meshes/system/{name}/` | Internal TX functionality (commit-agent) |
| **Protagents** | `meshes/protagents/{name}/` | User productivity agents (meet, schedule, etc.) |

**Naming convention**: Core meshes at top level, categorized meshes in subdirectories.

### How Work Gets Done (Message Flow)

```
┌─────────────────────────────────────────────────────────────────┐
│  User Request Flow                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User types in tmux session (natural language)                │
│     └─→ "build the login feature"                                │
│                                                                  │
│  2. Core agent (Claude) interprets and writes task message       │
│     └─→ Writes to .ai/tx/msgs/{timestamp}-task-core--dev.md     │
│                                                                  │
│  3. Consumer detects file, inserts into SQLite queue             │
│     └─→ File watching → queue.insert()                          │
│                                                                  │
│  4. Dispatcher polls queue, spawns SDK worker                    │
│     └─→ query() with agent prompt + task message                │
│                                                                  │
│  5. Worker completes, writes task-complete message               │
│     └─→ .ai/tx/msgs/{timestamp}-task-complete-dev--core.md     │
│                                                                  │
│  6. Core receives completion, reports to user                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**IMPORTANT**:
- Users do **NOT** send tasks via CLI commands
- Users communicate with core agent via the tmux session (natural language)
- Core agent writes task messages to workers
- CLI tools (`tx msg`, `tx spy`, `tx logs`) are **viewers only**

### Mesh Configuration (YAML)

**Location**: `meshes/{mesh-name}/config.yaml`

```yaml
# meshes/dev/config.yaml
mesh: dev
description: "Development mesh for coding tasks"

# Intent-based routing (optional)
intents:
  patterns:
    - build
    - implement
    - "code up"
  commands:
    build: "/know:build"

agents:
  - name: worker
    model: opus
    prompt: prompt.md  # Relative to mesh directory

# MCP server integration (optional, per-agent)
# agents:
#   - name: scheduler
#     model: sonnet
#     prompt: scheduler/prompt.md
#     mcpServers:
#       gcal:
#         command: npx
#         args:
#           - gcal-mcp

entry_point: worker
completion_agent: worker

# IMPORTANT: Multi-agent meshes SHOULD have routing!
# Routing enables automatic agent-to-agent flow without core intervention
routing:
  worker:
    complete:
      core: "Task finished"
    blocked:
      core: "Need human input"
    ask:
      brain: "Need project knowledge"

# Optional: workspace for output files
workspace:
  path: ".ai/output/{task-id}/"

# Optional: rearmatter (transparency metadata)
rearmatter:
  enabled: true
  fields:
    - grade
    - confidence
    - status
    - gaps
```

### Config Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mesh` | string | Yes | Unique mesh identifier |
| `description` | string | No | Human-readable description |
| `agents` | array | Yes | List of agents in mesh |
| `entry_point` | string | No | Agent that receives initial tasks |
| `completion_agent` | string | No | Agent that signals completion |
| `type` | string | No | `ephemeral` or `persistent` |
| `routing` | object | No* | Message routing rules (*required for multi-agent meshes) |
| `intents` | object | No | Intent patterns for auto-routing |
| `workspace` | object | No | Workspace output configuration |
| `rearmatter` | object | No | Transparency metadata config |
| `system` | boolean | No | Mark as system mesh |
| `worktree` | boolean | No | Enable git worktree isolation |
| `lifecycle` | object | No | Pre/post hooks |
| `toolRestriction` | string | No | Tool access policy: `unrestricted` (default) or `mcp-only` |

### intents Field

Auto-routes tasks to meshes based on user intent:

```yaml
intents:
  patterns:
    - research
    - investigate
    - "find out"
  commands:
    research: "/know:research"
```

- `patterns`: Keywords that trigger this mesh
- `commands`: Map patterns to slash commands

### workspace Field

Configure output workspace (where workers write outputs):

```yaml
# Object format (preferred, with path template)
workspace:
  path: ".ai/research/{topic}/"
  create_on_init: true
  cleanup_on_complete: false

# Simple path format (also supported)
workspace:
  path: ".ai/output/{task-id}/"

# Legacy string format (still supported)
workspace: ".ai/research/{topic}/"
```

**Path templates** from actual meshes:
- `".ai/output/{task-id}/"` - Dev mesh (unique per task)
- `".ai/research/{topic}/"` - Deep-research mesh (topic-based)
- `".ai/know/"` - Brain mesh (fixed knowledge location)

### mcpServers Field (Agent-Level)

Configure MCP (Model Context Protocol) servers for agents that need external tool access:

```yaml
# meshes/protagents/meet/config.yaml
mesh: meet
description: "Meeting coordination agent using Google Calendar MCP"
type: ephemeral

agents:
  - name: scheduler
    model: sonnet
    prompt: scheduler/prompt.md
    mcpServers:
      gcal:
        command: npx
        args:
          - gcal-mcp

entry_point: scheduler
```

**MCP server fields**:
- `command`: Executable to run (e.g., `npx`, `node`, path to binary)
- `args`: Array of command arguments
- Server name (e.g., `gcal`) is user-defined and used for logging

**Common MCP patterns**:
```yaml
# NPX-based MCP server
mcpServers:
  gcal:
    command: npx
    args:
      - gcal-mcp

# Node script MCP server
mcpServers:
  custom:
    command: node
    args:
      - /path/to/mcp-server.js

# Multiple MCP servers
mcpServers:
  gcal:
    command: npx
    args: [gcal-mcp]
  slack:
    command: npx
    args: [slack-mcp]
```

**Note**: MCP servers run alongside the worker and provide additional tools. The agent's prompt should reference the tools the MCP server provides.

### MCP Environment Variables (`.mcp.env`)

MCP servers often require credentials (API keys, tokens, secrets). TX V4 centralizes these in `.mcp.env`:

**Setup**:
1. Copy `.mcp.env.example` to `.mcp.env`
2. Fill in your credentials
3. `.mcp.env` is gitignored - never commit actual credentials

**File location**: Project root (`.mcp.env`)

**Format**:
```bash
# .mcp.env - MCP Server Credentials
# Comments and blank lines are ignored

# Google Calendar MCP
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token

# Slack MCP
SLACK_BOT_TOKEN=xoxb-your-token
```

**How it works**:
1. Dispatcher loads `.mcp.env` when spawning workers with MCP servers
2. Environment variables are merged into each MCP server's `env` config
3. Server-specific `env` values in config.yaml override `.mcp.env` values
4. Variable names (not values) are logged for debugging

**Mesh config with env override**:
```yaml
# Server-specific env overrides .mcp.env
mcpServers:
  gcal:
    command: npx
    args: [gcal-mcp]
    env:
      GOOGLE_CALENDAR_ID: "specific@calendar.google.com"  # Overrides .mcp.env
```

**Security best practices**:
- Never commit `.mcp.env` (it's gitignored)
- Use `.mcp.env.example` as a template (safe to commit)
- Log variable names, never values
- Consider encryption at rest for highly sensitive credentials

### toolRestriction Field

Control tool access for agents in a mesh. Critical for sandboxing protagent meshes.

**Possible values**:
- `unrestricted` (default) - Full SDK tools (Read, Write, Bash, etc.) + MCP tools
- `mcp-only` - ONLY MCP server tools, no built-in SDK tools

```yaml
# meshes/protagents/meet/config.yaml
mesh: meet
description: "Meeting coordination with Google Calendar"
type: ephemeral
toolRestriction: mcp-only  # Sandboxed: only calendar MCP tools

agents:
  - name: scheduler
    model: sonnet
    prompt: scheduler/prompt.md
    mcpServers:
      google-calendar:
        command: npx
        args: ["@cocal/google-calendar-mcp"]
```

**When to use `mcp-only`**:
- **Protagent meshes** - User productivity agents that interact with external services
- **Single-purpose agents** - Agents that only need their MCP tools
- **Security-sensitive contexts** - Agents handling external data that could contain prompt injections

**Security rationale** (Principle of Least Privilege):
- **No file system access** - Can't read/write arbitrary files
- **No code execution** - Can't run bash commands
- **Sandboxed** - Can't escape to broader system capabilities
- **Prevents**: Malicious prompt injection from external data, accidental file corruption, unintended system access

**When NOT to use `mcp-only`**:
- Dev/coding meshes that need file editing
- Brain/knowledge meshes that need codebase access
- Any mesh that needs Read, Write, Bash, Grep, Glob, Edit tools

### rearmatter Field

Transparency metadata fields:

```yaml
rearmatter:
  enabled: true
  fields:
    - grade       # Letter grade (A-F)
    - confidence  # Numeric (0.0-1.0)
    - speculation # Degree of speculation
    - gaps        # Known information gaps
    - assumptions # Key assumptions made
    - status      # Current status
    - iteration   # Iteration number
  thresholds:
    confidence: 0.8
    grade: "B"
```

### Agent Prompt Template

**CRITICAL**: Focus prompts on **core workflow only**. Message protocol, file paths, and infrastructure details are **injected dynamically** by the system prompt builder.

#### What to Include (Core Workflow)

```markdown
# {Agent Name}

You are the {role} agent for TX V4.

## Your Responsibilities

1. {Responsibility 1}
2. {Responsibility 2}
3. {Responsibility 3}

## Workflow

1. Read the incoming task message
2. {Step-by-step work process}
3. {Decision logic and quality criteria}
4. Write task-complete message when finished

## Quality Standards

- {Quality criteria specific to this role}
- {When to ask for human input}
- {Success/failure conditions}
```

#### What NOT to Include (Injected Automatically)

**Do NOT hardcode these in prompts** - they are injected by the system:

- ❌ Message directory paths (`.ai/tx/msgs/`)
- ❌ Filename formats (`{timestamp}-{type}-{from}--{to}-{msg-id}.md`)
- ❌ Frontmatter schema examples (to/from/type/msg-id/etc)
- ❌ Message type enums (task, task-complete, ask-human)
- ❌ Agent addressing format (mesh/agent)
- ❌ Workspace paths (injected from config's `workspace` field)

**Why?** These are infrastructure concerns. Hardcoding them makes prompts brittle and hard to maintain. The system injects them dynamically based on mesh configuration.

### Minimal Test Agent

For testing, keep prompts SUPER lightweight - core workflow ONLY:

```markdown
# Echo Agent

You echo back messages.

## Workflow
1. Read incoming task
2. Echo the content back in a task-complete message
```

**Note**: Message destination, format, and paths are injected by the system. Prompts focus on **what** to do, not **how** to format infrastructure.

## HITL (Human-In-The-Loop)

### How HITL Works in V4

1. **Worker needs human input** → Writes `ask-human` message to core
2. **Core displays question** → User sees it in tmux
3. **User responds** → Core writes `ask-response` back to worker
4. **Worker continues** → Receives response via queue polling

### ask-human Message Format

```yaml
---
to: core/core
from: dev/worker
type: ask-human
msg-id: hitl-q1
headline: Need clarification on feature scope
timestamp: 2025-12-11T00:00:00Z
---

## Question

Should this feature include:
1. Option A - Full implementation
2. Option B - MVP only
3. Option C - Skip for now

Please advise.
```

### ask-response Format (from core)

```yaml
---
to: dev/worker
from: core/core
type: ask-response
msg-id: hitl-q1
headline: User response
timestamp: 2025-12-11T00:01:00Z
---

Go with Option B - MVP only for now.
```

## Multi-Agent Patterns

### How Routing Works

**IMPORTANT**: Routing enables automatic agent-to-agent flow without core intervention.

When an agent has routing configured in the mesh config:
1. The dispatcher extracts routing rules for that agent
2. SDK runner injects routing instructions into the task prompt
3. Agent receives clear guidance on where to route based on outcome

Example - what the agent sees in its prompt:
```markdown
## Routing Instructions

When complete, route based on outcome:

**complete** → research/sourcer
Write task message to: research/sourcer
Reason: Requirements complete, ready to source information

**blocked** → core/core
Write task message to: core/core
Reason: Cannot proceed - unclear research requirements
```

Agents without routing config receive: "When done, write a task-complete message to core/core."

### Sequential Pipeline

```
core → agent1 → agent2 → agent3 → core
```

Config:
```yaml
routing:
  agent1:
    complete: { agent2: "Pass to next stage" }
  agent2:
    complete: { agent3: "Pass to next stage" }
  agent3:
    complete: { core: "Pipeline finished" }
```

### Bidirectional (Ping-Pong)

```
core → agentA ⟷ agentB → core
```

Agents exchange multiple messages before completion.

### Fan-Out/Fan-In

```
core → coordinator → [worker1, worker2, worker3] → coordinator → core
```

Coordinator distributes work, collects results.

## Testing

### Test Harness Pattern

```typescript
import { TestHarness } from './test/helpers/harness';

const harness = new TestHarness();

// Start system
await harness.startCore();

// Insert test task
await harness.insertMessage({
  from: 'core/core',
  to: 'test/echo',
  type: 'task',
  payload: { headline: 'Echo test', body: 'Hello World' }
});

// Run worker
const result = await harness.runWorker('test/echo', { model: 'haiku' });

// Verify response
const response = await harness.waitForMessage(
  msg => msg.type === 'task-complete' && msg.from === 'test/echo'
);

expect(response.payload.body).toContain('Hello World');
```

### E2E Test Structure

```typescript
// test/e2e/XX-feature.test.ts
import { describe, it, before, after } from 'node:test';
import { TestHarness } from '../helpers/harness';

describe('Feature Test', () => {
  let harness: TestHarness;

  before(async () => {
    harness = new TestHarness();
    await harness.setup();
  });

  after(async () => {
    await harness.cleanup();
  });

  it('should do the thing', async () => {
    // Test implementation
  });
});
```

## Debugging

### CLI Commands

```bash
# Start TX V4 with core agent
tx start                # Starts core, attaches to tmux session
tx start --continue     # Starts with previous session context

# View system status
tx status               # Shows core, workers, queue stats

# View messages (interactive TUI)
tx msg                  # Interactive vim-style navigation (default)
tx msg --follow         # Follow mode for real-time updates
tx msg --json           # JSON output mode
tx msg --type task      # Filter by message type
tx msg --agent brain    # Filter by agent

# View logs (interactive TUI)
tx logs                 # Interactive with filter toggles
tx logs --last          # View previous session logs
tx logs --no-interactive  # Simple list mode

# View tasks (derived from task/task-complete pairs)
tx tasks                # Interactive watch mode (default)
tx tasks --no-watch     # One-time snapshot
tx tasks --json         # JSON output

# Real-time activity spy
tx spy                  # All activity (messages + agent output)
tx spy --messages       # Messages only
tx spy --output         # Agent output only
tx spy --agent brain    # Filter by agent
tx spy --json           # JSON output

# Stop TX
tx stop                 # Kill tmux session, cleanup
```

**IMPORTANT**: `tx msg` and `tx logs` are **viewer commands** - they show messages/logs, they don't send them. User requests go to core via the tmux session (natural language), and core writes task messages to workers.

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Worker not starting | Queue empty | Check message was inserted |
| Message not delivered | Wrong `to:` field | Verify agent ID format |
| HITL timeout | No response from core | Check core is running |
| Task stuck | Worker error | Check `tx logs` |

### Log Locations

- Debug: `.ai/tx/logs/debug.jsonl`
- Errors: `.ai/tx/logs/error.jsonl`
- E2E tests: `.ai/tx/logs/e2e-test.log`

## Best Practices

### Prompt Design

1. **Focus on workflow, not infrastructure** - Message format and paths are injected
2. **Keep test agents minimal** - Role + Workflow sections only
3. **Be specific about completion criteria** - When is the task done?
4. **Include quality standards** - What makes good work for this role?

**What to include**: Responsibilities, workflow steps, decision logic, quality criteria
**What to skip** (auto-injected): Message paths, frontmatter format, agent addresses

### Model Selection

1. **Start with haiku** for simple tasks and validation
2. **Use sonnet** for general development and coding
3. **Reserve opus** for complex reasoning (brain, architecture, synthesis)

### Message Design

1. **Use descriptive headlines** - Human-readable summaries
2. **Include msg-id** - For correlation and debugging
3. **Timestamp everything** - ISO-8601 format
4. **Structure the body** - Use markdown sections

### Routing Configuration

1. **Always add routing for multi-agent meshes** - Enables automatic agent-to-agent flow
2. **Include blocked route to core** - For when agents can't proceed
3. **Use descriptive route reasons** - Helps with debugging
4. **Single-agent meshes don't need routing** - They default to core/core

## References

- [mesh-config-reference.md](references/mesh-config-reference.md) - Config specification
- [prompt-templates.md](references/prompt-templates.md) - Prompt examples
- [workflows.md](references/workflows.md) - Message flow patterns
- [multi-agent-patterns.md](references/multi-agent-patterns.md) - Advanced patterns
- [hitl-testing.md](references/hitl-testing.md) - HITL workflows
- [debugging.md](references/debugging.md) - Troubleshooting guide
