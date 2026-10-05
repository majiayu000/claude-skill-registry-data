---
name: compliance-evidence-collector
displayName: Compliance Evidence Collector
tagline: Gather and organize evidence for SOC2, ISO 27001, or HIPAA audits from your cloud environment and tools.
description: |
  Automates the collection and organization of compliance evidence for SOC2, ISO 27001,
  or HIPAA audits. Pulls evidence from AWS configurations, Google Drive policies, and
  Jira tickets, then organizes findings into a structured evidence package with control
  mappings and gap identification.
department:
  - Security & Compliance
use_cases:
  - Compliance Audit
  - Documentation
  - Task Management
tools_required:
  - AWS MCP
  - Google Drive MCP
  - Jira MCP
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
  Context: Preparing for SOC2 Type II audit
  Company: 200-person SaaS company, B2B product
  Environment: AWS (production, staging), Google Workspace, Jira/Confluence
  Timeline: Audit in 8 weeks, need evidence package by week 4
  Controls in scope: CC6.1 (Logical access), CC6.6 (Change management), A1.2 (Risk assessment)
exampleOutput: |
  Compliance Evidence Collection Summary — SOC2 Type II

  FRAMEWORK: SOC2 Trust Services Criteria
  SCOPE: CC6 (Logical and Physical Access), A1 (Risk Assessment)
  EVIDENCE SOURCES: AWS, Google Drive, Jira
  COLLECTION DATE: 2026-02-12

  CONTROLS MAPPED
  | Control   | Description              | Evidence Gathered      | Status   |
  |-----------|--------------------------|------------------------|----------|
  | CC6.1     | Logical access controls  | IAM policies, MFA config | Complete |
  | CC6.6     | Change management        | Jira change tickets    | Complete |
  | A1.2      | Risk assessment          | Risk register, findings | Partial  |

  EVIDENCE GATHERED (by source)
  AWS:  IAM user list (12), MFA status (100% enabled), S3 bucket policies (8), CloudTrail config
  G Drive: Access control matrix, sharing settings audit, DLP policy exports
  Jira:  45 change tickets (last 90 days), approval workflows, release process docs

  GAPS IDENTIFIED
  1. A1.2 — Risk register missing 2 quarterly reviews (Q3, Q4 2025)
  2. CC6.1 — 3 contractors have console access; recommend bastion + SSO
  3. CC6.6 — 12% of changes lacked formal approval ticket

  REMEDIATION TICKETS CREATED
  Jira: COMP-101, COMP-102, COMP-103 with due dates and assignees
---

# Compliance Evidence Collector

Gather and organize evidence for SOC2, ISO 27001, or HIPAA audits from your cloud environment and tools.

**Integrations:** AWS, Google Drive, Jira

## When to Use

- The user is preparing for a SOC2, ISO 27001, or HIPAA audit and needs evidence collection
- An auditor has requested an evidence package with control mappings
- The user mentions "compliance audit", "SOC2 evidence", "audit readiness", or "control mapping"
- Teams need to identify gaps before an audit and create remediation tickets

## Steps

### Step 1: Select Compliance Framework

Identify the framework and controls in scope:

| Framework | Common Controls / Domains | Evidence Sources |
|-----------|---------------------------|------------------|
| **SOC2** | CC6 (Logical Access), CC6.6 (Change Mgmt), A1 (Risk), CC7 (System Ops) | AWS IAM, Jira, Drive, monitoring tools |
| **ISO 27001** | A.9 (Access Control), A.12 (Ops Security), A.14 (Acquisition) | Same + asset inventory, policies |
| **HIPAA** | Access Control, Audit Controls, Integrity, Transmission Security | AWS, EHR configs, BAA docs, audit logs |

Ask the user for: framework, controls in scope (or control IDs), audit timeline, and what evidence sources they have (AWS, GDrive, Jira, etc.).

### Step 2: Map Controls to Evidence Sources

Create a control-to-evidence mapping:

| Control ID | Control Name | Evidence Type | Source | Collection Method |
|------------|--------------|---------------|--------|-------------------|
| CC6.1 | Logical access | IAM policies, MFA config | AWS | IAM list-users, GetAccountPasswordPolicy, MFA status |
| CC6.6 | Change management | Change tickets, approval workflow | Jira | JQL for change-type tickets, workflow config |
| A1.2 | Risk assessment | Risk register, findings | Google Drive | Search for "risk register", "risk assessment" |
| CC7.1 | System monitoring | Config, alerts, logs | AWS | CloudWatch, CloudTrail, Config rules |

Document which MCP tools will pull from which sources and what queries or APIs to use.

### Step 3: Collect Evidence from Cloud Environment

Execute evidence collection:

**AWS (via AWS MCP):**
- IAM users, roles, and policies (with MFA status)
- S3 bucket policies, encryption settings
- CloudTrail configuration and logging status
- Security group and NACL summaries
- Config rules and compliance status
- KMS key policies

**Google Drive (via Google Drive MCP):**
- Access control matrix (who has access to what)
- Sharing settings for sensitive folders
- DLP policy exports (if applicable)
- Policy documents (acceptable use, security policy)
- Risk register, incident reports

**Jira (via Jira MCP):**
- Change management tickets (JQL: project = INFRA AND type = Change)
- Approval workflows and custom fields
- Release process documentation
- Incident tickets and post-mortems

For each piece of evidence, record: source, collection date, control it supports, and any redaction needed.

### Step 4: Organize Evidence Package

Structure the evidence into an audit-ready package:

| Folder / Section | Contents |
|------------------|----------|
| **Control Mapping** | Table linking each control to evidence IDs |
| **Evidence by Control** | Subfolder per control (e.g., CC6.1/) with screenshots, exports, configs |
| **Evidence by Source** | AWS/, GDrive/, Jira/ with raw exports |
| **Gap Analysis** | Spreadsheet or doc listing gaps per control |
| **Narrative** | Summary document describing the control environment |

Ensure file names are descriptive (e.g., `CC6.1-IAM-users-export-2026-02-12.csv`) and include collection timestamps.

### Step 5: Identify Gaps and Create Remediation Tickets

Analyze evidence against control requirements:

| Gap Type | Example | Remediation |
|----------|---------|-------------|
| Missing evidence | No risk assessment for Q4 | Schedule and document risk review |
| Incomplete control | MFA not enforced for 2 users | Enable MFA, document exception process |
| Policy gap | No formal change approval | Document approval workflow, add Jira workflow |
| Configuration issue | S3 bucket unencrypted | Enable encryption, document exception |

For each gap:
1. **Document** — Control ID, gap description, risk level
2. **Remediation** — Specific actions needed
3. **Create ticket** — Use Jira MCP to create remediation tickets with assignees and due dates
4. **Prioritize** — Mark critical gaps for immediate action before audit

## Output

Deliver:
- A structured evidence package with control mapping and evidence by control/source
- A summary report showing controls covered, evidence gathered, and gaps identified
- Remediation tickets in Jira (or equivalent) for each gap with due dates
- A collection log (what was pulled, when, from where) for auditor reference
- Recommendations for closing gaps before the audit date
