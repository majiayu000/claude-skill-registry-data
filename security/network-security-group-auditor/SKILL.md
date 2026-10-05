---
name: network-security-group-auditor
displayName: Network Security Group Auditor
tagline: Review cloud firewall rules and security groups for overly permissive ingress/egress and public exposure.
description: |
  Audits AWS Security Groups, NACLs, and firewall rules for overly permissive configurations.
  Identifies rules allowing unrestricted ingress (0.0.0.0/0), unnecessary open ports, unused
  security groups, and public-facing resources that should be private. Generates a prioritized
  remediation report with specific rule changes.
department:
  - Cloud Security
use_cases:
  - Compliance Audit
  - Threat Modeling
tools_required:
  - AWS MCP
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
  We need to audit our security groups across 3 AWS accounts with 45 VPCs.
  Focus on: public-facing rules (0.0.0.0/0), overly broad ports (e.g., 22, 3389
  wide open), unused security groups, and resources attached to overly permissive SGs.
exampleOutput: |
  Network Security Group Audit — 3 Accounts, 45 VPCs

  FINDINGS SUMMARY
  | Finding Type              | Count |
  |---------------------------|-------|
  | Rules with 0.0.0.0/0      | 23    |
  | Overly broad ports (22,3389)| 18  |
  | Unused security groups    | 41    |
  | Resources with public SG  | 156   |
  | NACLs with 0.0.0.0/0      | 7     |

  CRITICAL: 23 ingress rules allow 0.0.0.0/0
  - sg-abc123: port 22, 443 (web tier — review 443, restrict 22)
  - sg-def456: port 3389 (app tier — restrict to jump host)
  - sg-ghi789: port 5432 (DB — CRITICAL: restrict immediately)

  UNUSED GROUPS: 41 security groups with zero attachments
  Top 5 by age: sg-old1 (340d), sg-old2 (301d), sg-old3 (287d)...
---

# Network Security Group Auditor

Review cloud firewall rules and security groups for overly permissive ingress/egress and public exposure.

**Integrations:** AWS MCP

## When to Use

- The user needs to audit security groups, NACLs, or firewall rules before a compliance review
- The user mentions "security group audit", "open ports", "0.0.0.0/0", or "public exposure"
- After a security incident or pentest that identified network misconfigurations
- When preparing for SOC2, ISO 27001, or similar audits requiring network control documentation

## Steps

### Step 1: Inventory Security Groups

Enumerate all security groups across the specified accounts and regions:

| Attribute | Description |
|-----------|-------------|
| Group ID | sg-xxxxxxxx |
| Name | User-defined or auto-generated |
| VPC | Default or custom VPC |
| Inbound rules | Port, protocol, source CIDR/security group |
| Outbound rules | Port, protocol, destination CIDR/security group |
| Attachments | Count of ENIs/resources using the group |

Use AWS MCP to list security groups, describe rules, and optionally NACLs. Build a normalized inventory table.

### Step 2: Analyze Ingress Rules

Identify high-risk ingress rules:

| Risk Level | Criteria | Example |
|------------|----------|---------|
| Critical | 0.0.0.0/0 to DB ports (3306, 5432, 27017, 6379) | MySQL/Postgres/MongoDB/Redis exposed |
| High | 0.0.0.0/0 to SSH (22) or RDP (3389) | Management ports publicly open |
| High | 0.0.0.0/0 to application ports (80, 443) | May be intentional; verify use case |
| Medium | Overly broad CIDR (e.g., /8, /16) | Internal sweep; consider VPC CIDR |
| Low | Unusual ports open | Custom apps; document justification |

Produce a table: Security Group, Port, Protocol, Source, Risk Level, Recommendation.

### Step 3: Analyze Egress Rules

Identify overly permissive egress:

| Risk Level | Criteria | Recommendation |
|------------|----------|----------------|
| High | 0.0.0.0/0 on all ports | Restrict to required destinations (e.g., NTP, package repos) |
| Medium | 0.0.0.0/0 on 443 only | Acceptable for outbound HTTPS; consider VPC endpoints |
| Low | Scoped egress | Document for compliance |

Note: Egress 0.0.0.0/0 is common but increases data exfiltration risk. Flag for review where data sensitivity is high.

### Step 4: Identify Unused and Redundant Groups

Detect security groups with no attachments or redundant rules:

| Finding | Definition | Action |
|---------|------------|--------|
| Unused SG | Zero ENI/resource attachments | Candidate for deletion (verify no Lambda, etc.) |
| Redundant rules | Duplicate or overlapping rules | Consolidate to simplify |
| Orphaned references | Referenced by another SG but unused | Clean up references before deletion |

Cross-reference with EC2, Lambda, RDS, and other services. Report age of unused groups to prioritize cleanup.

### Step 5: Generate Remediation Report

Produce a prioritized remediation report:

| Section | Contents |
|---------|----------|
| Executive Summary | Total SGs, critical/high/medium/low counts, top risks |
| Critical Findings | Rules with 0.0.0.0/0 to sensitive ports, specific changes |
| High Findings | Broad management ports, recommended CIDR restrictions |
| Unused Groups | List with group ID, name, age, suggested action |
| Remediation Steps | Concrete changes (e.g., "Revoke sg-xxx rule: 0.0.0.0/0:22 → 10.0.1.0/24:22") |

Include a summary table suitable for compliance evidence (finding type, count, status).

## Output

Deliver:

- Findings summary table: Finding Type, Count
- Critical/high risk rules table: SG, Port, Protocol, Source, Risk, Recommendation
- Unused security groups list with IDs, names, and age
- Prioritized remediation report with specific rule changes
- Optional: CSV export for ticket creation or compliance documentation
