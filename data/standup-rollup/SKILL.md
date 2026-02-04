---
name: standup-rollup
description: Aggregate daily standups into team summary with blockers analysis
auto_trigger: true
trigger_keywords:
  - standup rollup
  - standup summary
  - team standup
  - aggregate standups
  - standup report
  - sprint standup
  - weekly standup summary
  - standup blockers
allowed-tools: Task, Read, mcp__flywheel__search_notes, mcp__flywheel__get_recent_notes, mcp__flywheel__get_section_content
---

# Standup Rollup

Aggregate daily standup notes into a team summary, tracking what each person worked on and identifying blockers.

## Trigger Detection

Activate when user:
- Wants a summary of team standups
- Needs to see who worked on what
- Wants to identify blockers across the team

## Examples

- "Summarize this week's standups"
- "What did the team work on this week?"
- "Show me standup blockers"
- "Team standup report for sprint 5"
- "Aggregate standups from meetings/standups/"

## Process

1. **Identify Scope**
   - If folder specified, use it
   - If date range specified, filter by dates
   - Default: last 5 standup notes

2. **Delegate to Agent**
   ```
   Task(
       subagent_type="standup-agent",
       description="Aggregate standups",
       prompt="Aggregate standup notes from [scope]. Generate team summary with blockers."
   )
   ```

3. **Present Results**
   - Per-person work summary
   - Common blockers
   - Sprint velocity insights

## Difference from Weekly Rollup

| Aspect | Weekly Rollup | Standup Rollup |
|--------|---------------|----------------|
| Scope | Individual daily notes | Team standup meetings |
| Format | Personal habits/achievements | Yesterday/Today/Blockers |
| Output | Personal weekly summary | Team velocity report |
| Focus | Self-reflection | Team coordination |

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | N/A | Read-only skill |
| 2. File Exists Check | N/A | Agent validates |
| 3. Chain Validation | N/A | Single delegation |
| 4. Mutation Confirm | N/A | No mutations |
| 5. MCP Health | N/A | Agent checks |
| 6. Post Validation | N/A | Agent verifies |
