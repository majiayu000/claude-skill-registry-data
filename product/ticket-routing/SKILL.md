---
name: ticket-routing
displayName: Ticket Routing
tagline: Automatically route support tickets to the right team based on category, priority, and skills.
description: |
  Routes incoming support tickets to the appropriate team or agent based
  on ticket content analysis, category detection, priority assessment,
  and agent skill matching. Reduces response time by eliminating manual
  triage and ensures tickets reach the right person on the first try.
department:
  - Customer Support
  - Operations
use_cases:
  - Ticket Management
  - Support Automation
  - Customer Experience
tools_required:
  - Zendesk MCP
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
  Set up ticket routing for our support team.
  Categories: Billing, Technical, Account, Feature Request.
  Priority: P1 (outage), P2 (broken feature), P3 (general), P4 (question).
exampleOutput: |
  Ticket Routing Configuration

  ROUTING RULES
  Billing Issues    -> Billing Team (avg response: 2h)
  Technical Bugs    -> Engineering Support (avg response: 4h)
  Account Issues    -> Account Management (avg response: 1h)
  Feature Requests  -> Product Team (weekly review batch)

  PRIORITY ESCALATION
  P1 (Outage):      Immediate Slack alert #incidents + page on-call
  P2 (Broken):      Route to senior agent, 4h SLA
  P3 (General):     Standard queue, 24h SLA
  P4 (Question):    Knowledge base suggestion first, 48h SLA

  LAST WEEK STATS
  Total Tickets:     284
  Auto-routed:       256 (90%)
  Misrouted:         8 (3%) — rules updated
  Avg First Response: 3.2h (SLA target: 4h)
---

# Ticket Routing

Automatically route support tickets to the right team based on category, priority, and skills.

**Integrations:** Zendesk, Slack

## When to Use

- Support tickets need automated triage and routing
- Response times are slow due to manual ticket assignment
- The user mentions "ticket routing", "triage", or "support queue"

## Steps

### Step 1: Define Categories and Rules

Set up ticket categories with routing destinations.

### Step 2: Configure Priority Levels

Define priority tiers with SLA targets and escalation rules.

### Step 3: Enable Auto-routing

Activate content-based routing with skill matching.

## Output

Deliver:
- Routing rules configuration
- Priority escalation policies
- Routing performance metrics
