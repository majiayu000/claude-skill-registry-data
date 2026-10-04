---
name: schedule-management
description: Executive Assistant skill for calendar and schedule management. Use when managing meetings, detecting time conflicts, scheduling learning time, or coordinating across contexts. Triggers on phrases like "schedule meeting", "check calendar", "find time", "what's on my calendar", "schedule conflict", or "block time".
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Schedule Management

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Manage calendar, detect conflicts, and coordinate time across professional contexts.

## Core Capabilities

### 1. Calendar Query
```
"What's on my calendar today/this week?"
"Do I have any conflicts this week?"
"When is my next meeting with X?"
```

### 2. Time Block Management
```
"Block 2 hours for deep work on Thursday"
"Schedule learning time for Saturday 9-11 AM"
"Find 1 hour for a call with [person]"
```

### 3. Conflict Detection
```
"Check for deadline collisions this month"
"Do I have any overlapping commitments?"
"Flag conflicts between contexts"
```

### 4. Context-Aware Scheduling
```
"Schedule work context during 9-5"
"Find evening time for side-project work"
"Protect my learning time blocks"
```

## Data Sources

### Context Time Blocks
Read from `pos.yaml`:
```yaml
time_blocks:
  - days: [mon, tue, wed, thu, fri]
    hours: "09:00-17:00"
    timezone: "Europe/Berlin"
```

### Learning Schedule
Read from `contexts/personal/learning/goals.yaml`:
```yaml
schedule:
  weekly_hours_target: 5
  preferred_times:
    - day: sat
      hours: "09:00-11:00"
    - day: sun
      hours: "14:00-16:00"
```

### Project Deadlines
Read from `programs/registry.yaml` and context status files.

## Autonomy Levels

Based on EA autonomy SOP (`docs/system/sops/ea-autonomy-levels.md`):

| Action | Level | Behavior |
|--------|-------|----------|
| Query calendar | 1 | Execute immediately |
| Block personal time | 1 | Execute immediately |
| Reschedule internal | 2 | Execute, notify user |
| External meeting | 3 | Propose, await approval |
| Cancel commitment | 3 | Propose, await approval |

## Conflict Detection Logic

### Time Overlap
```
conflict if:
  event_a.end > event_b.start AND
  event_a.start < event_b.end
```

### Context Conflict
```
conflict if:
  event_a.context != event_b.context AND
  same_time_block(event_a, event_b) AND
  both_require_attention
```

### Deadline Collision
```
collision if:
  deadline_a within 3 days of deadline_b AND
  combined_effort > available_hours
```

## Output Formats

### Calendar View
```
## Today (2026-01-08, Wednesday)

| Time | Event | Context | Notes |
|------|-------|---------|-------|
| 09:00-10:00 | Standup | work | Recurring |
| 14:00-15:00 | 1:1 with Manager | work | |
| 19:00-20:00 | Client sync | client-a | Consulting |
```

### Conflict Report
```
## Conflicts Detected

### High Priority
1. **Jan 10**: Work deadline vs client presentation
   - Work: Blog post due
   - Client: Steering committee presentation
   - Recommendation: Complete blog Thursday, present Friday

### Medium Priority
2. **Jan 15**: Overlapping meetings
   - 14:00: Work team sync
   - 14:30: Client call
   - Recommendation: Reschedule client call to 15:00
```

### Time Suggestion
```
## Available Slots for 1-hour Meeting

| Date | Time | Context | Notes |
|------|------|---------|-------|
| Thu Jan 9 | 11:00-12:00 | work | Before lunch |
| Thu Jan 9 | 16:00-17:00 | work | End of day |
| Fri Jan 10 | 10:00-11:00 | work | Morning slot |
```

## Integration

### With Learning Coach
- Protect scheduled learning time
- Flag when work encroaches on learning blocks
- Track learning hours vs target

### With Program Manager
- Pull deadline data for conflict detection
- Surface delivery date conflicts
- Coordinate cross-context milestones

### With Context System
- Respect context time blocks
- Apply context-appropriate scheduling rules
- Track context switches and transitions

## Commands

```
@ea schedule     - Open schedule management
@ea calendar     - Show today/week view
@ea conflicts    - Run conflict detection
@ea findtime     - Find available slots
@ea block        - Block time for task
```

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
