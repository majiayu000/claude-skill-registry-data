---
name: linear
description: Manage issues, projects, and team workflows in Linear via the Linear MCP server. Create, update, organize, and track work without leaving the terminal.
compatibility:
  use-case: Project management, issue tracking, team coordination
  frameworks: Linear MCP, issue management, workflow automation
---

# Linear Issue Management

## Use This Skill When

- Creating or updating Linear issues programmatically
- Managing projects and team workflows in Linear
- Reading issue status and project information
- Bulk-updating issues or labels
- Assigning work and tracking progress
- Organizing sprints and cycles

## When NOT to Use

- Real-time planning via Linear UI (faster there)
- Complex workflow logic beyond CRUD
- Issues involving authentication setup

## Context: Issue Management Maturity

**Undeveloped**: Manual UI clicking, slow issue creation.

**Target**: Programmatic issue creation/update, read project status, manage cycles.

**Optimized**: Automated workflows, bulk operations, integrated with CI/CD and external systems.

## Core Principle

**Programmatic issue management scales.** Direct API access enables batch operations, automation, and integration that's impossible via UI alone.

## Instructions

### Step 1: Set Up Linear MCP

**If not already configured:**

```bash
codex mcp add linear --url https://mcp.linear.app/mcp
codex --enable rmcp_client
codex mcp login linear  # OAuth login
# Restart codex after login
```

### Step 2: Clarify Goal and Scope

**Determine what you're working with:**

- **Team**: Which team owns this work?
- **Project**: Which project are issues in?
- **Labels**: Standard labels in this workspace?
- **Cycles**: Current sprint/cycle?

### Step 3: Execute Issue Operations

**List issues:**
```bash
composio execute LIST_ISSUES -d '{
  "team_key": "ENG",
  "status": "todo",
  "limit": 20
}'
```

**Create issue:**
```bash
composio execute CREATE_ISSUE -d '{
  "team_id": "team-123",
  "title": "Fix login bug",
  "description": "Users report 500 error on login page",
  "priority": 1,
  "estimate": 3
}'
```

**Update issue:**
```bash
composio execute UPDATE_ISSUE -d '{
  "issue_id": "ENG-123",
  "status": "in_progress",
  "assignee_id": "user-456"
}'
```

### Step 4: Organize Work

**Use labels and projects to organize:**
- Assign to cycles (sprints)
- Add labels (bug, feature, tech-debt)
- Link related issues
- Set priorities

### Step 5: Summary and Next Actions

**After operations, confirm:**
- Issues created/updated
- Team visibility into work
- Cycle assignments

## Output

**Deliver issue operations summary and any created/updated issues with tracking links.**