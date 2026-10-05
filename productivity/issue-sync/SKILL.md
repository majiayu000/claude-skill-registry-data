---
name: issue-sync
displayName: Issue Sync
tagline: Synchronize issues and tasks across GitHub, Jira, and Linear in real-time.
description: |
  Keeps issues synchronized across multiple project management tools. Maps
  statuses, priorities, and assignees between GitHub Issues, Jira tickets, and
  Linear issues. Prevents duplicate work, ensures consistent tracking, and
  provides a unified view of all work items.
department:
  - Engineering
  - Project Management
use_cases:
  - Project Management
  - Cross-tool Sync
  - Workflow Automation
tools_required:
  - GitHub MCP
  - Jira MCP
  - Linear MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Sync all high-priority issues from Jira project "PLATFORM" to Linear team "Platform".
  Map Jira statuses to Linear statuses.
exampleOutput: |
  Issue Sync Report — PLATFORM -> Platform

  SYNCED
  Total Issues:    34
  Created in Linear: 12 (new since last sync)
  Updated:         18 (status/priority changes)
  Skipped:         4 (already in sync)

  STATUS MAPPING
  Jira "To Do"       -> Linear "Todo"
  Jira "In Progress" -> Linear "In Progress"
  Jira "In Review"   -> Linear "In Review"
  Jira "Done"        -> Linear "Done"
---

# Issue Sync

Synchronize issues and tasks across GitHub, Jira, and Linear in real-time.

**Integrations:** GitHub, Jira, Linear

## When to Use

- Teams use multiple project management tools and need consistent tracking
- The user wants to sync issues between Jira and Linear or GitHub
- The user mentions "issue sync", "cross-tool", or "sync tasks"

## Steps

### Step 1: Map Fields

Define status, priority, and assignee mappings between tools.

### Step 2: Perform Initial Sync

Sync all existing issues with conflict resolution rules.

### Step 3: Enable Continuous Sync

Set up webhooks or polling for ongoing synchronization.

## Output

Deliver:
- Field mapping configuration
- Sync report with counts and conflicts
- Continuous sync setup instructions
