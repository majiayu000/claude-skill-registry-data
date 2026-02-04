---
name: ccg-guardian
description: "Use this skill when working on code projects that need memory persistence, code validation, multi-agent coordination, or workflow tracking. Activates Claude Code Guardian MCP tools."
allowed-tools:
  - mcp__code-guardian__*
---

# CCG Guardian Skill

Enterprise-grade development assistance with persistent memory, code validation, and multi-agent coordination.

## When to Use

Activate this skill when:
- Starting a new development session (call `session_init`)
- Need to remember decisions, patterns, or context across sessions
- Want code validation before commits (security, quality checks)
- Working on multi-file tasks that need progress tracking
- Need specialized agent guidance (Trading, Laravel, React, Node.js)

## Core Capabilities

### 1. Memory System
```
memory_store     - Save decisions, facts, patterns (importance 1-10)
memory_recall    - Search memories by query, tags, type
memory_list      - List all memories with filters
```

### 2. Guard System (10 Security Rules)
```
guard_validate   - Check code for vulnerabilities
guard_check_test - Detect fake tests without assertions
guard_rules      - List all validation rules
```

**Rules include:** SQL Injection, XSS, Command Injection, Path Traversal, Prompt Injection, Hardcoded Secrets, Empty Catch, Disabled Features, Fake Tests, Emoji in Code

### 3. Workflow & Tasks
```
workflow_task_create   - Create task with priority/tags
workflow_task_start    - Begin working on task
workflow_task_complete - Mark task done
workflow_current       - Get current active task
```

### 4. Multi-Agent System
```
agents_list      - List specialized agents
agents_select    - Auto-select best agent for task
agents_coordinate - Coordinate multiple agents
```

**Available Agents:**
- **Trading Agent** - Quant systems, risk management, backtesting
- **Laravel Agent** - PHP backend, Eloquent, REST APIs
- **React Agent** - Components, hooks, state management
- **Node Agent** - Event-driven, workers, orchestration

### 5. Resource Management
```
resource_status           - Token usage and checkpoints
resource_checkpoint_create - Save current progress
resource_checkpoint_restore - Restore from checkpoint
```

## Workflow Pattern

```
1. session_init          → Load memory, check status
2. workflow_task_create  → Define what you're doing
3. memory_recall         → Get relevant context
4. [do work]
5. guard_validate        → Check code quality
6. memory_store          → Save important decisions
7. workflow_task_complete → Mark done
8. session_end           → Save all data
```

## Best Practices

1. **Always start with `session_init`** - Loads previous context
2. **Store important decisions** - Use importance 8-10 for critical items
3. **Validate before commit** - Run `guard_validate` on changed files
4. **Track progress** - Use workflow tasks for multi-step work
5. **End sessions properly** - Call `session_end` to persist data

## Example Usage

"Use CCG to help me refactor the authentication module with proper memory and validation"

Claude will:
1. Initialize session and recall relevant memories
2. Create a task for tracking
3. Select appropriate agent (Node or Laravel)
4. Apply changes with guard validation
5. Store decisions for future reference
