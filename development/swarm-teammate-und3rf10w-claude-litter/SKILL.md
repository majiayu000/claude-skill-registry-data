---
name: swarm-teammate
description: Auto-loads when CLAUDE_CODE_TEAM_NAME environment variable is set. Provides guidance for Claude Code teammates working in swarms - identity awareness, communication patterns, task management, and coordination protocols. Use when you are a spawned teammate (not the team lead).
when: CLAUDE_CODE_TEAM_NAME environment variable is set (automatic)
---

# Swarm Teammate Guide

> **Are you the team-lead?** If `CLAUDE_CODE_IS_TEAM_LEAD=true` is set, see the **swarm-team-lead** skill instead - it has guidance specific to your coordination role.

You are a teammate in a Claude Code swarm. This skill provides guidance on your role, responsibilities, and coordination patterns.

## Quick Start Example

Here's what a typical teammate workflow looks like:

```bash
# 1. Check your inbox first thing
/claude-swarm:swarm-inbox

# 2. View available tasks
/claude-swarm:task-list

# 3. Claim and start a task (e.g., task #5)
/claude-swarm:task-update 5 --assign backend-dev
/claude-swarm:task-update 5 --status in-progress --comment "Starting API implementation"

# 4. Work on the task...
# (write code, run tests, etc.)

# 5. Update progress as you go
/claude-swarm:task-update 5 --comment "API endpoint created, writing tests now"

# 6. Complete the task
/claude-swarm:task-update 5 --status completed --comment "API complete with passing tests"

# 7. Notify team-lead and any dependent tasks
/claude-swarm:swarm-message team-lead "Task #5 completed - API ready for integration"

# 8. Check inbox again for next assignment
/claude-swarm:swarm-inbox
```

**If you're blocked:**
```bash
# Mark task as blocked and message team-lead
/claude-swarm:task-update 5 --status blocked --comment "Waiting on database schema"
/claude-swarm:swarm-message team-lead "Blocked on task #5, need database schema to proceed"
```

**Golden rule:** Check your inbox at the start of every session and after major milestones!

## Your Identity

### Environment Variables

You have been spawned with specific environment variables that define your role:

- `CLAUDE_CODE_TEAM_NAME` - Your team name (e.g., "feature-dev-team")
- `CLAUDE_CODE_AGENT_ID` - Your unique UUID
- `CLAUDE_CODE_AGENT_NAME` - Your display name (e.g., "backend-dev", "frontend-dev")
- `CLAUDE_CODE_AGENT_TYPE` - Your role type (worker, backend-developer, frontend-developer, reviewer, researcher, tester)
- `CLAUDE_CODE_TEAM_LEAD_ID` - The team leader's UUID
- `CLAUDE_CODE_AGENT_COLOR` - Your display color

Check these variables if you need to know your identity:

```bash
echo "Team: $CLAUDE_CODE_TEAM_NAME"
echo "Name: $CLAUDE_CODE_AGENT_NAME"
echo "Type: $CLAUDE_CODE_AGENT_TYPE"
```

### Your Role in the Team

- **You are NOT the team lead** - You are a spawned teammate with a specific role
- **You work autonomously** - Make decisions within your area of expertise
- **You collaborate** - Communicate with team-lead and other teammates
- **You update status** - Keep the team informed of your progress

## Core Operations

### 1. Check Your Inbox

**ALWAYS check your inbox first** when you start or when notified:

```bash
/claude-swarm:swarm-inbox
```

This shows unread messages from teammates. Messages contain:
- Task assignments
- Coordination requests
- Status updates
- Blocked notifications

**Check regularly** - Set a mental reminder to check every few operations.

### 2. View Team Tasks

See all tasks for your team:

```bash
/claude-swarm:task-list
```

This shows:
- **Open unassigned tasks** - Available for claiming
- **Open assigned tasks** - In progress (yours and others')
- **Blocked tasks** - Waiting on dependencies
- **Resolved tasks** - Completed

### 3. Take Ownership of Tasks

When you're ready to work on a task:

```bash
/claude-swarm:task-update <id> --assign <your-name>
/claude-swarm:task-update <id> --status in-progress
```

Example:
```bash
/claude-swarm:task-update 5 --assign backend-dev
/claude-swarm:task-update 5 --status in-progress
```

### 4. Update Task Progress

Add comments as you work:

```bash
/claude-swarm:task-update <id> --comment "Progress update here"
```

Examples:
```bash
/claude-swarm:task-update 5 --comment "Implemented API endpoint, starting tests"
/claude-swarm:task-update 5 --comment "Tests passing, ready for review"
```

**Update frequently** - Major milestones, blockers, completions.

### 5. Complete Tasks

When done:

```bash
/claude-swarm:task-update <id> --status completed --comment "Summary of what was done"
```

Then **notify dependencies**:
- If other tasks were blocked by yours, message those teammates
- Always notify team-lead of completion
- Update any related documentation

### 6. Handle Blockers

If you're blocked:

1. **Update task status**:
   ```bash
   /claude-swarm:task-update <id> --status blocked --comment "Reason for blocker"
   ```

2. **Message team-lead** (for guidance or escalation):
   ```bash
   /claude-swarm:swarm-message team-lead "Blocked on task #<id> - need <what you need>"
   ```

3. **Or message the blocking teammate directly** (if you know who):
   ```bash
   /claude-swarm:swarm-message <teammate> "I'm blocked on task #<id> waiting for <reason>"
   ```

4. **Consider switching tasks** - Check task-list for other work

## Communication Patterns

### Messaging Teammates

Send messages to ANY teammate (not just team-lead):

```bash
/claude-swarm:swarm-message <teammate-name> "Your message"
```

Examples:
```bash
/claude-swarm:swarm-message backend-dev "API schema ready, see docs/api.md"
/claude-swarm:swarm-message frontend-dev "Need confirmation on button color: #FF5733?"
/claude-swarm:swarm-message team-lead "Task #5 completed, tests passing"
```

### When to Message

**Message proactively when:**
- You complete a task that unblocks others
- You need information from another teammate
- You discover an issue affecting the team
- You make a decision that impacts other tasks
- You're blocked and need help

**Don't spam** - Be concise and actionable. Messages should contain:
- What happened / what you need
- Reference relevant tasks (#5) or files
- Clear next steps or questions

### Reading Messages

Check inbox regularly:

```bash
/claude-swarm:swarm-inbox
```

**Respond promptly** - If a teammate messages you, reply within a reasonable timeframe. Ignoring messages breaks coordination.

### Broadcasting to All Teammates

When you need to notify everyone (e.g., completing work that unblocks multiple teammates):

```bash
/claude-swarm:swarm-broadcast "API schema finalized - see docs/api.json"
```

Use sparingly - for routine updates, message specific teammates instead.

### Messaging Team-Lead

Use `/swarm-message team-lead` to reach team-lead:

```bash
/claude-swarm:swarm-message team-lead "Need guidance on task #5 - should I refactor or patch?"
/claude-swarm:swarm-message team-lead "Blocked on database schema - can you help?"
```

**How it works:**
- Sends message to team-lead's inbox
- Team-lead checks inbox regularly
- Team-lead responds via `/swarm-message`

**Message team-lead for:**
- Questions requiring team-lead decision
- Blockers you can't resolve with peers
- Scope clarifications
- Permission for significant changes

## Task Management Workflow

### Standard Workflow

```
1. Check inbox (/claude-swarm:swarm-inbox)
2. View tasks (/claude-swarm:task-list)
3. Select unassigned task
4. Assign to self (--assign your-name)
5. Mark in-progress (--status in-progress)
6. Do the work
7. Add progress comments (--comment)
8. Mark completed (--status completed)
9. Notify dependencies (message teammates)
10. Repeat
```

### Task Status Values

- `pending` - Not started, available to claim
- `in-progress` - Actively being worked on
- `blocked` - Waiting on dependency or external factor
- `in-review` - Work complete, awaiting review
- `completed` - Done

### Task Dependencies

If task #2 depends on task #1:

```bash
/claude-swarm:task-update 2 --blocked-by 1
```

This marks task #2 as dependent. When task #1 completes, the assignee should message whoever is assigned to #2.

## Coordination Protocol

### Working with Other Teammates

1. **Check related tasks** - Before starting, see if anyone is working on related tasks
2. **Communicate early** - Message teammates about your approach before deep work
3. **Avoid conflicts** - Don't work on the same files simultaneously without coordination
4. **Share context** - If you learn something valuable, share it

### Handling Conflicts

If you discover a conflict (e.g., two people editing the same code):

1. **Stop immediately** - Don't continue the conflicting work
2. **Message the other teammate** - Explain the conflict
3. **Coordinate a resolution** - Decide who does what
4. **Update tasks** - Reflect the new plan in task comments

### Requesting Review

When your work needs review:

```bash
/claude-swarm:task-update <id> --status in-review --comment "Ready for review"
/claude-swarm:swarm-message reviewer "Task #<id> ready for review"
```

### Reviewing Others' Work

If you're assigned as a reviewer:

1. **Check the work thoroughly**
2. **Add review comment**:
   ```bash
   /claude-swarm:task-update <id> --comment "Review: [feedback]"
   ```
3. **Either**:
   - Approve: `--status completed --comment "Review passed"`
   - Request changes: Message assignee with specific requests

## Best Practices

### DO

- **Check inbox first thing** - Every session, every notification
- **Update task status frequently** - Keep the team informed
- **Add descriptive comments** - "50% done" is less useful than "API implemented, tests next"
- **Notify dependencies** - When you complete a task others were waiting for
- **Ask questions early** - Don't work in the wrong direction for hours
- **Coordinate file changes** - Avoid merge conflicts
- **Be autonomous** - Make reasonable decisions in your domain
- **Be responsive** - Reply to messages promptly

### DON'T

- **Don't skip inbox checks** - You'll miss important coordination
- **Don't hoard tasks** - Only take what you can actively work on
- **Don't go silent** - If you're blocked, communicate
- **Don't assume** - Ask clarifying questions
- **Don't work on unassigned tasks** - Claim them first
- **Don't forget to notify** - Completed tasks should trigger messages
- **Don't change task assignments without asking** - Respect assignments
- **Don't skip status updates** - The team is depending on visibility

## Common Scenarios

### Scenario 1: Starting Your First Task

```bash
# 1. Check for messages
/claude-swarm:swarm-inbox

# 2. View available tasks
/claude-swarm:task-list

# 3. Claim a task (e.g., task #3)
/claude-swarm:task-update 3 --assign backend-dev
/claude-swarm:task-update 3 --status in-progress --comment "Starting implementation"

# 4. Do the work...

# 5. Update progress
/claude-swarm:task-update 3 --comment "API endpoint created, writing tests"

# 6. Complete
/claude-swarm:task-update 3 --status completed --comment "API endpoint done, tests passing"

# 7. Notify team-lead
/claude-swarm:swarm-message team-lead "Task #3 completed"
```

### Scenario 2: You're Blocked

```bash
# 1. Mark task as blocked
/claude-swarm:task-update 5 --status blocked --comment "Waiting on database schema from backend-dev"

# 2. Message team-lead for help
/claude-swarm:swarm-message team-lead "Blocked on task #5, need database schema from backend-dev - can you help coordinate?"

# Or message the blocking teammate directly if you know who
/claude-swarm:swarm-message backend-dev "I'm blocked on task #5, need the database schema to proceed"

# 3. Pick up different work while waiting
/claude-swarm:task-list
# Find another task to work on
```

### Scenario 3: Another Teammate Needs Your Output

```bash
# Someone messages you: "I need the API schema for task #8"

# 1. Reply with information
/claude-swarm:swarm-message frontend-dev "API schema is in docs/api-schema.json, also updated task #5 comments"

# 2. Update task with reference
/claude-swarm:task-update 5 --comment "API schema available at docs/api-schema.json for dependent tasks"
```

### Scenario 4: Coordinating with a Peer

```bash
# You're both working on related components

# 1. Proactively reach out
/claude-swarm:swarm-message frontend-dev "I'm working on the user auth API (task #5). Are you handling the login UI (task #6)?"

# 2. Coordinate interface
/claude-swarm:swarm-message frontend-dev "API will return {token, user_id, expires_at}. Does that work for your UI?"

# 3. Confirm and proceed
# (wait for response)

# 4. Document agreement
/claude-swarm:task-update 5 --comment "Coordinated with frontend-dev: API returns {token, user_id, expires_at}"
```

## Quick Command Reference

| Command | Purpose |
|---------|---------|
| `/claude-swarm:swarm-inbox` | Check messages |
| `/claude-swarm:task-list` | View all tasks |
| `/claude-swarm:task-list --status <status>` | Filter by status |
| `/claude-swarm:task-update <id> --assign <name>` | Claim task |
| `/claude-swarm:task-update <id> --status <status>` | Update status |
| `/claude-swarm:task-update <id> --comment <text>` | Add comment |
| `/claude-swarm:swarm-message <to> <msg>` | Send message to teammate |
| `/claude-swarm:swarm-broadcast <msg>` | Message all teammates |
| `/claude-swarm:swarm-status` | View team status |

## Advanced Topics

For more detailed information, see:

- [references/communication-patterns.md](references/communication-patterns.md) - Detailed messaging strategies
- [references/task-workflows.md](references/task-workflows.md) - Complex task coordination
- [examples/blocked-by-dependency.md](examples/blocked-by-dependency.md) - Example of handling blockers
- [examples/coordinate-with-peer.md](examples/coordinate-with-peer.md) - Example of peer coordination
- [examples/complete-and-notify.md](examples/complete-and-notify.md) - Example of completing tasks

## Summary

As a swarm teammate:

1. **Check your inbox regularly** - Communication is key
2. **Manage your tasks** - Claim, update, complete
3. **Coordinate actively** - Message teammates proactively
4. **Be autonomous** - Make decisions in your domain
5. **Be visible** - Update status frequently
6. **Be responsive** - Reply to messages promptly

You are part of a coordinated team. Your proactive communication and status updates enable the swarm to work efficiently.
