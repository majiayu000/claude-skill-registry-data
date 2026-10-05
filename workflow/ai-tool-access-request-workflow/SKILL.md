---
name: ai-tool-access-request-workflow
displayName: AI Tool Access Request Workflow
tagline: Standardized workflow for employees to request AI tool access with auto-routing to security review.
description: |
  Sets up a complete intake-to-approval pipeline for AI tool access requests.
  Creates a Jira issue type with structured fields, configures automation rules
  for risk-based tier assignment and reviewer routing, adds Slack notifications
  for transparency, and includes a security review runbook with decision templates.
department:
  - Security & Compliance
  - DevOps & Platform
use_cases:
  - Workflow Automation
  - Compliance Audit
  - Task Management
tools_required:
  - Jira MCP
  - Slack MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  Tool: Claude Team
  Requester: Jane Smith, Backend Engineering
  Business justification: Accelerate API development and code review
  Data types: Internal source code (no PII)
  Seats requested: 12
  Estimated cost: $240/month
exampleOutput: |
  [JIRA] AI-ACCESS-47: Claude Team — Backend Engineering (12 seats)
  Status: IN REVIEW | Tier: 2 (Standard Review) | SLA: 3 business days

  Auto-assigned reviewers:
  - Manager: @john.doe (notified via Slack DM)
  - Security: @security-team (added to #ai-tool-requests queue)

  Checklist:
  ✅ Vendor SOC2 compliance verified
  ✅ Data retention policy reviewed (30-day, no training on data)
  ⬜ SSO integration confirmed
  ⬜ Security team sign-off

  [SLACK] #ai-tool-requests:
  "New request: Claude Team for Backend Engineering (12 seats, $240/mo)
   Tier 2 — Standard Review | Due: March 5, 2026
   Reviewers: @john.doe @security-team"
---

# AI Tool Access Request Workflow

Standardized workflow for employees to request AI tool access with auto-routing to security review.

**Integrations:** Jira, Slack

## When to Use

- The user wants to set up an approval process for AI tool requests
- An organization needs to standardize how employees get access to AI tools
- The user mentions "tool access request", "approval workflow", or "AI tool provisioning"
- Security or IT teams need a structured intake process

## Steps

### Step 1: Define Approval Tiers

Help the user define risk-based tiers:

| Tier | Risk Level | Examples | Approval Required |
|------|-----------|---------|------------------|
| **Tier 1: Pre-Approved** | Low | GitHub Copilot, Cursor (with SSO) | Auto-approved, manager notification |
| **Tier 2: Standard Review** | Medium | ChatGPT Team, Claude, custom MCP servers | Manager + Security review (SLA: 3 days) |
| **Tier 3: Extended Review** | High | Tools handling PII/PHI, self-hosted LLMs, fine-tuned models | Manager + Security + Legal + CISO (SLA: 10 days) |

### Step 2: Create Jira Request Template

Set up a Jira issue type "AI Tool Access Request" with these fields:

| Field | Type | Required |
|-------|------|----------|
| Tool Name | Short text | Yes |
| Tool URL/Vendor | URL | Yes |
| Business Justification | Long text | Yes |
| Data Types Involved | Multi-select (None, Internal, Confidential, PII, PHI) | Yes |
| Team/Department | Select | Yes |
| Number of Seats | Number | Yes |
| Estimated Monthly Cost | Number | No |
| Urgency | Select (Standard, Expedited) | No |

### Step 3: Configure Jira Automation

Set up automation rules:

1. **Auto-assign tier** — Based on "Data Types Involved" selection, auto-label the tier
2. **Route to reviewers** — Tier 1: auto-approve and notify manager. Tier 2: assign to security team queue. Tier 3: create sub-tasks for each reviewer
3. **SLA tracking** — Set due dates based on tier SLA
4. **Escalation** — Auto-escalate if SLA is breached (notify reviewer's manager)

### Step 4: Set Up Slack Notifications

Configure Slack integration:

- **#ai-tool-requests** channel: Post new requests and status updates
- **DM to requester**: Notify when status changes (approved, needs more info, denied)
- **DM to reviewers**: Alert when a new request needs their review
- **Weekly digest**: Summary of pending requests to the security team channel

### Step 5: Create Runbook

Provide a runbook for the security review team:

1. **Vendor assessment checklist** — SOC2 compliance, data retention policy, encryption, subprocessors
2. **Data flow diagram template** — Where does data go when using this tool?
3. **Decision matrix** — Standard criteria for approve/deny/conditional approval
4. **Conditional approval template** — Approved with restrictions (e.g., no PII, VPN required)
5. **Denial template** — Professional denial with alternative tool suggestions

## Output

The workflow produces:
- A Jira project board with the request intake process
- Slack channel integration for visibility
- Automation rules for routing and SLA tracking
- Templates for security review decisions
