---
name: XSky Core Architecture
description: This skill should be used when the user asks about "XSky architecture", "XSky class", "how XSky works", "agent execution", "workflow system", "Chain class", "Context class", or needs to understand the core framework structure and execution model.
version: 1.0.0
---

# XSky Core Architecture

This skill provides deep knowledge of XSky AI Agent framework internals.

## Overview

XSky is a multi-platform AI agent framework with these core components:

```
XSky (Orchestrator)
├── Planner (Task → Workflow XML)
├── Chain (Execution tracking)
├── Context (State management)
├── Memory (Conversation compression)
└── Agents (Task executors)
```

## Execution Flow

1. **Task Received**: User provides natural language task
2. **Planning**: Planner converts to Workflow XML using LLM
3. **Parsing**: XML parsed into agent tree with dependencies
4. **Execution**: Agents execute in dependency order
5. **Result**: Final result returned to user

## Key Classes

### XSky (`core/xsky.ts`)
Main orchestrator with these methods:
- `generate(taskPrompt)` → Creates workflow from task
- `execute(taskId)` → Runs workflow
- `run(taskPrompt)` → Generate + execute in one call
- `pauseTask(taskId)` → Pause execution
- `abortTask(taskId)` → Cancel execution

### Planner (`core/plan.ts`)
Converts natural language to Workflow XML:
- Uses LLM to analyze task and select agents
- Outputs structured XML with dependencies
- Supports replanning on failure

### Chain (`core/chain.ts`)
Tracks execution state:
- Records each agent's execution
- Stores results and errors
- Enables debugging and replay

### Context (`core/context.ts`)
Manages task state:
- `taskId` - Unique task identifier
- `variables` - Key-value storage
- `workflow` - Current workflow
- `controller` - AbortController for cancellation
- `conversation` - Chat messages during execution

### AgentContext
Per-agent execution context:
- Access to variables
- Tool execution
- Script injection
- Result storage

## Agent Architecture

All agents extend base classes:
- `Agent` - Base class with LLM dialogue loop
- `BaseBrowserAgent` - Browser abstraction
- `BaseBrowserLabelsAgent` - Element labeling approach
- `BaseFileAgent` - File system operations
- `BaseShellAgent` - Command execution

## Key Source Files

| File | Purpose |
|------|---------|
| `packages/ai-agent-core/src/core/xsky.ts` | Main orchestrator |
| `packages/ai-agent-core/src/core/plan.ts` | Workflow planner |
| `packages/ai-agent-core/src/core/chain.ts` | Execution chain |
| `packages/ai-agent-core/src/core/context.ts` | Context management |
| `packages/ai-agent-core/src/core/dialogue.ts` | LLM dialogue loop |
