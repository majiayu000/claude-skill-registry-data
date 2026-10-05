---
name: ai-governance-framework-generator
displayName: AI Governance Framework Generator
tagline: Create a governance framework defining approval workflows, risk tiers, and escalation paths.
description: |
  Generates a complete AI governance framework tailored to your organization's
  structure and regulatory requirements. Defines a five-tier risk classification
  system, designs approval workflows with SLAs for each tier, establishes a
  governance board with RACI matrix, creates escalation paths, and produces
  all supporting artifacts including charter, decision tree, and meeting templates.
department:
  - Security & Compliance
  - AI Enablement Leaders
use_cases:
  - Compliance Audit
  - Documentation
  - Workflow Automation
tools_required:
  - Google Drive MCP
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
  Organization: Mid-market SaaS company, 400 employees
  Structure: Federated teams with central IT
  Existing governance: ITIL change management, SOC2 certified
  Decision makers: CISO, CTO, VP Engineering, General Counsel
  Current state: Ad-hoc AI adoption, no formal process
exampleOutput: |
  AI Governance Framework — [Company Name]

  RISK TIERS
  Tier 0 (Unrestricted): Local AI tools, offline models → Auto-approved
  Tier 1 (Standard):     SOC2 vendors, internal data  → Manager approval (1 day)
  Tier 2 (Elevated):     API integrations, data export → Security review (5 days)
  Tier 3 (Restricted):   PII/customer data             → Governance board (15 days)
  Tier 4 (Prohibited):   Autonomous decisions           → Executive + legal (30 days)

  GOVERNANCE BOARD
  Chair: CISO | Members: CTO, VP Eng, General Counsel, Privacy Officer
  Meeting: Bi-weekly (2nd & 4th Thursday, 30 min)
  Quorum: 3 of 5 members

  RACI MATRIX (sample)
  | Activity              | CISO | CTO | VP Eng | Legal | Champions |
  |-----------------------|------|-----|--------|-------|-----------|
  | Tier classification   | A    | C   | R      | C     | I         |
  | Vendor assessment     | A    | I   | C      | C     | R         |
  | Policy updates        | R    | C   | C      | A     | I         |
  | Incident response     | A    | I   | R      | C     | R         |

  Generated: Google Drive folder with 7 documents (Charter, Decision Tree,
  Workflow Diagrams, RACI Matrix, Policy Templates, Meeting Agenda, Exception Process)
---

# AI Governance Framework Generator

Create a governance framework defining approval workflows, risk tiers, and escalation paths for AI tool adoption.

**Integrations:** Google Drive

## When to Use

- The user needs to establish AI governance in their organization
- Leadership requires a formal framework for AI tool decisions
- The user mentions "AI governance", "approval framework", "risk tiers", or "escalation paths"
- Compliance or legal teams need a structured approach to AI oversight

## Steps

### Step 1: Assess Governance Needs

Ask the user for:

1. **Organization structure** — Centralized IT, federated teams, or hybrid
2. **Existing governance** — Any current IT governance or change management frameworks
3. **Regulatory landscape** — Industry regulations that apply (SOC2, HIPAA, GDPR, etc.)
4. **Decision makers** — Who are the key stakeholders (CISO, CTO, VP Eng, Legal)
5. **Current state** — Is AI adoption ad-hoc, partially managed, or not started

### Step 2: Define Risk Tiers

Create a tiered classification system:

| Tier | Risk Level | Criteria | Examples |
|------|-----------|----------|---------|
| **Tier 0: Unrestricted** | Minimal | No data access, offline tools, open-source local models | Local code formatters with AI, offline autocomplete |
| **Tier 1: Standard** | Low | Internal data only, established vendors, SOC2 certified | GitHub Copilot, Cursor with SSO |
| **Tier 2: Elevated** | Medium | Confidential data, API integrations, data leaves the org | Custom MCP servers, AI APIs in production |
| **Tier 3: Restricted** | High | PII/PHI data, regulatory scope, customer-facing AI | AI chatbots handling customer data, ML models in healthcare |
| **Tier 4: Prohibited** | Critical | Classified data, high-risk autonomous decisions | Fully autonomous AI making financial/medical decisions |

### Step 3: Design Approval Workflows

For each tier, define the approval process:

**Tier 0 — Auto-Approved:**
- No approval needed
- Logged for inventory purposes

**Tier 1 — Manager Approval:**
- Manager approves via Jira/ServiceNow
- Security team notified (no action required)
- SLA: 1 business day

**Tier 2 — Security Review:**
- Manager approval + Security team review
- Vendor security assessment required
- Data flow documentation required
- SLA: 5 business days

**Tier 3 — Governance Board:**
- Full governance board review (CISO, Legal, CTO, Privacy Officer)
- Third-party security audit may be required
- Privacy Impact Assessment (PIA) required
- SLA: 15 business days

**Tier 4 — Executive Approval:**
- Governance board + C-level sign-off
- External legal review
- Board notification (if applicable)
- SLA: 30 business days

### Step 4: Define Escalation Paths

| Trigger | Escalation Path |
|---------|----------------|
| SLA breach | Reviewer's manager notified, then skip-level after 2x SLA |
| Data incident | Immediate escalation to CISO and Legal |
| Policy violation | Manager + HR + Security notified |
| Tool outage/downtime | IT Operations + Vendor management |
| Cost overrun | Finance + Budget owner + CTO |
| Regulatory inquiry | Legal + Compliance + CISO |

### Step 5: Create Governance Artifacts

Generate in Google Drive:

1. **Governance Charter** — Mission, scope, authority, membership of the AI governance body
2. **Risk Tier Decision Tree** — Flowchart for classifying new AI tools into the correct tier
3. **Approval Workflow Diagrams** — Visual process flows for each tier
4. **RACI Matrix** — Responsible, Accountable, Consulted, Informed for each governance activity
5. **Policy Templates** — Reusable templates for tool-specific policies
6. **Meeting Cadence** — Governance board meeting schedule, agenda template, decision log
7. **Exception Process** — How to handle cases that don't fit standard tiers

### Step 6: Define Review Cadence

| Review Type | Frequency | Scope |
|-------------|-----------|-------|
| Tool inventory audit | Monthly | All approved tools still compliant |
| Risk tier reassessment | Quarterly | Re-evaluate tool classifications |
| Policy review | Semi-annually | Update policies for new regulations |
| Framework review | Annually | Full governance framework effectiveness |

## Output

Deliver:
- Complete governance framework document
- Risk tier classification guide with decision tree
- Approval workflow diagrams for each tier
- RACI matrix
- Escalation path documentation
- Meeting templates and review calendar
