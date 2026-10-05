---
name: security-alert-triage
displayName: Security Alert Triage
tagline: Auto-triage security alerts from cloud providers, classify severity, and suggest response actions.
description: |
  Automatically triages security alerts from AWS GuardDuty, CloudTrail, and other cloud security
  services. Classifies each alert by severity and type, correlates related events, filters false
  positives, suggests response actions, and routes critical alerts to the appropriate team via
  Slack and PagerDuty.
department:
  - Cloud Security
  - Security & Compliance
use_cases:
  - Incident Response
  - Workflow Automation
tools_required:
  - Slack MCP
  - AWS MCP
  - PagerDuty MCP
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
  We have 340 GuardDuty findings from the last 24 hours across 5 AWS accounts.
  Need help triaging: classify severity, flag false positives (we have known
  pentest IPs and dev sandbox activity), and route critical/high to our
  security-oncall Slack channel and PagerDuty.
exampleOutput: |
  Security Alert Triage Summary — Last 24h

  | Severity  | Count | Auto-Resolved | Action Required |
  |-----------|-------|---------------|-----------------|
  | Critical  | 2     | 0             | 2               |
  | High      | 12    | 1             | 11              |
  | Medium    | 85    | 42            | 43              |
  | Low/Info  | 241   | 198           | 43              |
  |-----------|-------|---------------|-----------------|
  | Total     | 340   | 241           | 99              |

  False Positive Rate: ~28% (pentest IPs, known dev sandbox)
  Routed to Slack: 14 alerts (Critical + High)
  PagerDuty incidents created: 2 (Critical only)

  Top Critical Alerts:
  1. [GuardDuty] UnauthorizedAccess:EC2/SSHBruteForce — i-0abc123, us-east-1
  2. [GuardDuty] Backdoor:EC2/C&CActivity.B!DNS — i-0def456, eu-west-1
---

# Security Alert Triage

Auto-triage security alerts from cloud providers, classify severity, and suggest response actions.

**Integrations:** Slack MCP, AWS MCP, PagerDuty MCP

## When to Use

- The user has a large batch of security alerts (GuardDuty, CloudTrail, etc.) and needs help triaging
- The user wants to automate alert classification, false positive filtering, or routing
- The user mentions "alert fatigue", "triage", "GuardDuty findings", or "security alert overload"
- After a pentest or during known high-volume periods (e.g., dev sandbox activity)

## Steps

### Step 1: Ingest Security Alerts

Pull alerts from the specified sources:

| Source | Method | Fields to Extract |
|--------|--------|-------------------|
| AWS GuardDuty | AWS MCP / API | Finding type, severity, resource, timestamp, account |
| CloudTrail | CloudTrail Insights / Event history | Anomalous events, unusual API calls |
| Other | User-provided CSV/JSON | Same fields where available |

Collect: finding type, severity, affected resource (ARN, instance ID), account/region, timestamp, and raw event details. Normalize into a common schema for analysis.

### Step 2: Classify and Score Alerts

Map each finding to a severity level and response priority:

| Finding Category | Typical Severity | Examples |
|------------------|------------------|----------|
| Credential compromise, backdoor, malware | Critical | SSH brute force, C&C activity, crypto mining |
| Privilege escalation, data exfil, persistent access | High | IAM policy changes, S3 GetObject spikes |
| Reconnaissance, policy violations | Medium | Port scan, unrestricted security group |
| Informational, expected behavior | Low/Info | New region, known tool usage |

| Severity | Response SLA |
|----------|--------------|
| Critical | Immediate (PagerDuty) |
| High | Within 4 hours (Slack + ticket) |
| Medium | Within 24 hours (ticket only) |
| Low | Batch review weekly |

### Step 3: Correlate Related Events

Group related findings to reduce noise:

| Correlation Rule | Logic | Action |
|------------------|-------|--------|
| Same resource | Multiple findings on same instance/ARN | Merge into single incident |
| Same source IP | Multiple findings from one IP | Treat as one campaign |
| Same finding type | Repeated identical finding | Deduplicate, count occurrences |
| Timeline clustering | Findings within 15 min window | Link as potential chain |

Output: deduplicated incident list with primary finding and related IDs.

### Step 4: Filter False Positives

Apply user-provided or inferred suppression rules:

| Rule Type | Example | Implementation |
|-----------|---------|----------------|
| IP allowlist | Pentest IPs, dev VPN | Exclude findings from these IPs |
| Resource allowlist | Dev sandbox, test accounts | Exclude specific accounts/ARNs |
| Finding type | Known noisy findings | Exclude or downgrade severity |
| Time-based | Maintenance windows | Exclude during known windows |

Tag each alert as: **Action Required**, **False Positive**, or **Informational**. Report false positive rate in summary.

### Step 5: Route and Notify

Route alerts to the appropriate channels:

| Severity | Slack | PagerDuty | Ticket |
|----------|-------|-----------|--------|
| Critical | #security-oncall | Create incident | Auto-create |
| High | #security-oncall | No (or optional) | Auto-create |
| Medium | — | — | Auto-create |
| Low | — | — | Optional batch ticket |

Use Slack MCP to post to the specified channel with alert summary and links. Use PagerDuty MCP to create incidents for critical alerts. Include suggested response actions in each notification.

## Output

Deliver:

- Triage summary table: Severity, Count, Auto-Resolved, Action Required
- False positive rate and count
- List of critical/high alerts with finding type, resource, account, and suggested action
- Slack messages posted for critical/high (if Slack MCP configured)
- PagerDuty incidents created for critical (if PagerDuty MCP configured)
- Optional: CSV or JSON export of all triaged findings for audit
