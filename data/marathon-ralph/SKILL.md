---
name: marathon-ralph
description: Autonomous long-running development from specifications. Use when user wants to build an application from a spec file, run continuous development, or automate feature implementation. Triggers on phrases like "marathon this", "build from spec", "autonomous development", "keep coding until done".
---

# Marathon Ralph - Autonomous Development

This skill enables autonomous, long-running development sessions that:

- Create Linear projects from specification files
- Work through issues systematically with verification
- Continue across multiple sessions via Stop hook
- Produce fully tested applications

## Triggers

Activate this skill when the user:

- Wants to build an application from a specification
- Says "marathon this [spec]" or "build from [spec]"
- Asks for autonomous/continuous development
- Wants to "keep coding until done"
- Provides a spec file and wants it implemented
- Mentions "marathon development" or "marathon session"
- Wants to implement multiple features from a spec without stopping

## Usage

### Resume Existing Marathon

```
/marathon-ralph:run
```

Or naturally: "Continue the marathon" or "Keep going"

### Start New Marathon

```
/marathon-ralph:run path/to/spec.md
```

Or naturally: "Marathon this spec.md until complete"

### Check Progress

```
/marathon-ralph:status
```

Or naturally: "How's the marathon going?"

### Cancel

```
/marathon-ralph:cancel
```

Or naturally: "Stop the marathon"

## Prerequisites

User must have Linear MCP configured:

1. `claude mcp add --transport http linear https://mcp.linear.app/mcp`
2. `/mcp` - Select Linear and authenticate via OAuth

## How It Works

1. **Setup**: Verifies Linear MCP connection is active
2. **Init**: Creates Linear project and issues from the spec file
3. **Loop**: For each issue in priority order:
   - Verify (tests, lint, types) - ensures codebase is healthy
   - Plan implementation - creates detailed implementation strategy
   - Code the feature - implements according to plan
   - Write tests - unit and integration tests
   - Write E2E tests - for web projects only
   - Commit and mark Done in Linear
4. **Continue**: Stop hook automatically restarts for next issue until all complete

## Example Workflows

### Starting a New Project

User: "Marathon this todo-app-spec.md until it's done"

1. Skill triggers on "marathon" + spec file reference
2. Runs `/marathon-ralph:run --spec-file todo-app-spec.md`
3. Creates Linear project with issues from spec
4. Begins autonomous coding loop

### Checking Progress

User: "How far along is the marathon?"

1. Skill triggers on marathon progress query
2. Runs `/marathon-ralph:status`
3. Reports current phase, issue, and completion percentage

### Stopping Early

User: "Stop the marathon, I need to change the spec"

1. Skill triggers on stop/cancel request
2. Runs `/marathon-ralph:cancel`
3. Confirms with user and cleanly stops
4. Linear project preserved for later

## State Management

Marathon state is stored in `.claude/marathon-ralph.json` in the project root. This tracks:

- Current phase (setup, init, coding, complete)
- Linear project and issue information
- Progress statistics
- Timestamps for tracking

The Stop hook reads this state to determine whether to continue autonomous operation or allow exit.
