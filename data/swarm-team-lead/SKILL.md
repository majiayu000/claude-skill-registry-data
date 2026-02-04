---
name: swarm-team-lead
description: Auto-loads when CLAUDE_CODE_IS_TEAM_LEAD environment variable is set. Provides guidance for spawned team-leads on monitoring teammates, handling consults, assigning tasks, and coordinating the team. Use this when you are a spawned team-lead (not the original orchestrator who created the swarm).
when: CLAUDE_CODE_IS_TEAM_LEAD environment variable is set
---

# Swarm Team-Lead Guide

You are a **spawned team-lead** in a Claude Code swarm. This skill provides guidance on your responsibilities and how to coordinate your team effectively.

## Your Role

As team-lead, you are responsible for:

- **Monitoring** teammate progress and team status
- **Unblocking** teammates who are stuck or waiting
- **Responding** to consults and questions from teammates
- **Coordinating** work across the team
- **Spawning** additional teammates if needed

You are NOT a worker - you coordinate and support the team.

## Quick Start

```bash
# 1. Check your inbox (teammates may have messaged you)
/claude-swarm:swarm-inbox

# 2. View team status
/claude-swarm:swarm-status

# 3. View tasks and assignments
/claude-swarm:task-list

# 4. Respond to any teammate messages
/claude-swarm:swarm-message <teammate> "Your response"
```

## Core Operations

### Check Your Inbox

**ALWAYS check your inbox frequently** - teammates consult you for guidance:

```bash
/claude-swarm:swarm-inbox
```

Teammates reach you via `/swarm-message team-lead` which sends a message to your inbox.

**Be responsive** - teammates depend on you to stay unblocked.

### Monitor Team Status

Check overall team health:

```bash
/claude-swarm:swarm-status
```

Shows:
- Active teammates and their status
- Task assignments
- Any status mismatches

### View and Filter Tasks

See all tasks:

```bash
/claude-swarm:task-list
```

Filter to focus on what matters:

```bash
# In-progress work
/claude-swarm:task-list --status in-progress

# Blocked tasks (need attention!)
/claude-swarm:task-list --blocked

# Specific teammate's tasks
/claude-swarm:task-list --owner backend-dev
```

### Assign Tasks

When tasks need assignment:

```bash
/claude-swarm:task-update <id> --assign <teammate-name>
```

Example:
```bash
/claude-swarm:task-update 3 --assign frontend-dev
```

### Communicate with Teammates

**Message a specific teammate:**

```bash
/claude-swarm:swarm-message <teammate> "<message>"
```

**Broadcast to everyone:**

```bash
/claude-swarm:swarm-broadcast "<message>"
```

**Trigger inbox checks** (useful after sending messages):

```bash
/claude-swarm:swarm-send-text <teammate> "/swarm-inbox\r"
/claude-swarm:swarm-send-text all "/swarm-inbox\r"
```

### Spawn Additional Teammates

If the team needs more help:

```bash
/claude-swarm:swarm-spawn "<name>" "<type>" "<model>" "<prompt>"
```

Example:
```bash
/claude-swarm:swarm-spawn "qa-engineer" "tester" "sonnet" "You are the QA engineer. Write tests for the auth system. Check task list for details."
```

Verify spawn succeeded:

```bash
/claude-swarm:swarm-verify
```

## Handling Teammate Messages

When teammates message you, you'll see their message in your inbox.

**Respond promptly:**

```bash
# Check what they asked
/claude-swarm:swarm-inbox

# Respond
/claude-swarm:swarm-message backend-dev "Yes, use the existing auth middleware. See src/middleware/auth.ts"
```

**Common consult types:**

| Type | How to Handle |
|------|---------------|
| Question | Answer directly via `/swarm-message` |
| Blocker | Help unblock or reassign work |
| Decision needed | Make the call and communicate it |
| Scope issue | Clarify requirements |

## Unblocking Teammates

When a teammate is blocked:

1. **Check what's blocking them** - read their task and messages
2. **Resolve if possible** - answer questions, provide info
3. **Coordinate with others** - if another teammate needs to complete something first
4. **Update task status** - mark dependencies as resolved

```bash
# Message the blocking teammate
/claude-swarm:swarm-message api-designer "frontend-dev is waiting on the API schema. ETA?"

# Once unblocked, notify
/claude-swarm:swarm-message frontend-dev "API schema is ready at docs/api.json. You're unblocked."
```

## Best Practices

### DO

- Check inbox frequently (teammates are waiting)
- Respond to consults promptly
- Keep tasks updated
- Broadcast important team-wide changes
- Verify spawns succeeded
- Proactively check on blocked tasks

### DON'T

- Work on tasks yourself (you're the coordinator)
- Ignore teammate messages
- Let blockers sit unaddressed
- Forget to notify dependencies when tasks complete

## Quick Command Reference

| Command | Purpose |
|---------|---------|
| `/claude-swarm:swarm-inbox` | Check messages from teammates |
| `/claude-swarm:swarm-status` | View team status |
| `/claude-swarm:task-list` | View all tasks |
| `/claude-swarm:task-list --blocked` | Find blocked tasks |
| `/claude-swarm:task-update <id> --assign <name>` | Assign task |
| `/claude-swarm:swarm-message <to> <msg>` | Message teammate |
| `/claude-swarm:swarm-broadcast <msg>` | Message all |
| `/claude-swarm:swarm-send-text <target> <text>` | Send to terminal |
| `/claude-swarm:swarm-spawn <name> <type> <model> <prompt>` | Spawn teammate |
| `/claude-swarm:swarm-verify` | Verify teammates alive |

## Environment Variables

You have these environment variables set:

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_TEAM_NAME` | Your team name |
| `CLAUDE_CODE_AGENT_NAME` | `team-lead` |
| `CLAUDE_CODE_IS_TEAM_LEAD` | `true` |
| `CLAUDE_CODE_AGENT_ID` | Your unique UUID |

## See Also

- **swarm-orchestration** - Full swarm setup workflow (for creating new swarms)
- **swarm-troubleshooting** - Diagnose and fix team issues
- **swarm-teammate** - Guidance for worker teammates
