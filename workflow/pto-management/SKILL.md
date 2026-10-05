---
name: pto-management
displayName: PTO Management
tagline: Manage paid time off requests, balances, and team coverage across your organization.
description: |
  Automates PTO request workflows including approval routing, balance
  tracking, and team coverage analysis. Checks for conflicts with
  critical deadlines or low team coverage before approving. Provides
  managers with visibility into team availability and PTO trends.
department:
  - HR
  - People Operations
use_cases:
  - Time Off Management
  - Team Coverage
  - HR Automation
tools_required:
  - BambooHR MCP
  - Slack MCP
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
  Process PTO request: @alice wants June 16-20 off.
  Check team coverage and approve if no conflicts.
exampleOutput: |
  PTO Request — Alice Johnson

  REQUEST
  Dates:        June 16-20 (5 days)
  Type:         Vacation
  Balance:      18 days remaining (after: 13 days)

  COVERAGE CHECK
  Team Size:    6 engineers
  Already Off:  None during June 16-20
  Coverage:     83% (5/6) — Above minimum (60%)
  Conflicts:    No release deadlines or on-call shifts

  STATUS: ✅ Auto-approved
  - Slack notification sent to #platform
  - Calendar updated
  - BambooHR balance adjusted
---

# PTO Management

Manage paid time off requests, balances, and team coverage across your organization.

**Integrations:** BambooHR, Slack

## When to Use

- An employee submits a PTO request
- Managers need team coverage visibility
- The user mentions "PTO", "time off", "vacation request", or "team coverage"

## Steps

### Step 1: Validate Request

Check PTO balance and request validity.

### Step 2: Check Coverage

Analyze team availability for the requested dates.

### Step 3: Process Approval

Route for approval or auto-approve based on coverage rules.

### Step 4: Notify Team

Update calendars and notify the team of upcoming absences.

## Output

Deliver:
- PTO request status with coverage analysis
- Calendar and system updates
- Team notifications
