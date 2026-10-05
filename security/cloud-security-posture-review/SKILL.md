---
name: cloud-security-posture-review
displayName: Cloud Security Posture Review
tagline: Run a structured review of your cloud environment against CIS benchmarks and generate a findings report.
description: |
  Performs a comprehensive cloud security posture review against CIS benchmarks
  for AWS, GCP, or Azure. Checks identity, networking, logging, encryption,
  and compute configurations, then produces a scored findings report with
  prioritized remediation steps in a Google Sheet.
department:
  - Cloud Security
  - Security & Compliance
use_cases:
  - Compliance Audit
  - Documentation
tools_required:
  - AWS MCP
  - Google Sheets MCP
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
  We need a cloud security posture review of our AWS environment.
  3 accounts (dev, staging, prod), 12 VPCs, 50+ EC2 instances, RDS,
  S3 buckets. Goal: align with CIS AWS Foundations Benchmark before
  our SOC2 audit. Output findings to a Google Sheet for tracking.
exampleOutput: |
  Cloud Security Posture Review — AWS | CIS Benchmark Alignment
  Scope: 3 accounts, 12 VPCs | Review date: 2026-02-18

  CIS BENCHMARK SCORES BY CATEGORY
  | Category         | Pass | Fail | N/A | Score  |
  |------------------|------|------|-----|-------|
  | Identity & Access| 12   | 3    | 1   | 80%   |
  | Logging          | 8    | 4    | 0   | 67%   |
  | Networking       | 15   | 2    | 2   | 88%   |
  | Data Protection  | 6    | 5    | 1   | 55%   |
  | Monitoring       | 4    | 2    | 0   | 67%   |
  | OVERALL          | 45   | 16   | 4   | 74%   |

  TOP FAILURES (prioritized)
  1. 1.4 – MFA not enabled for root (Critical)
  2. 2.1.1 – S3 buckets not versioned (High)
  3. 3.1 – CloudTrail not enabled in all regions (High)
  ... 13 more

  Generated: Google Sheet with Findings, Remediation, Owner columns
---

# Cloud Security Posture Review

Run a structured review of your cloud environment against CIS benchmarks and generate a findings report.

**Integrations:** AWS MCP, Google Sheets MCP

## When to Use

- The user needs to prepare for a compliance audit (SOC2, ISO 27001, HIPAA) and wants CIS alignment
- The user mentions "cloud security posture", "CIS benchmark", "security review", or "compliance check"
- After a significant infrastructure change, to validate security configuration
- When leadership requests a scored security posture report with prioritized findings

## Steps

### Step 1: Select Benchmark and Scope

Choose the appropriate CIS benchmark and scope:

| Cloud Provider | Benchmark | Scope Options |
|----------------|-----------|---------------|
| AWS | CIS AWS Foundations Benchmark v3.x | Single account, OU, or Organization |
| GCP | CIS Google Cloud Computing Platform | Project, folder, or org |
| Azure | CIS Microsoft Azure Foundations | Subscription or management group |

Confirm with the user: account IDs, regions to include, and any exclusions (e.g., sandbox accounts).

### Step 2: Identity & Access Review

Review IAM and identity configurations:

| Control Area | Checks |
|--------------|--------|
| Root account | MFA enabled, no access keys, unused |
| IAM users | MFA, password policy, unused credentials |
| IAM policies | Least privilege, no inline policies where avoidable |
| Service accounts | Scoped permissions, no long-lived keys where possible |
| Federated access | SAML/SCIM, conditional access, session duration |

Document pass/fail for each applicable CIS control. Use AWS MCP to query IAM configuration.

### Step 3: Network Review

Review VPC and network security:

| Control Area | Checks |
|--------------|--------|
| VPC design | Subnet segmentation, NACLs, flow logs |
| Security groups | Minimal ingress, no 0.0.0.0/0 on sensitive ports |
| Network access | VPC endpoints for AWS services, private subnets for data |
| Perimeter | WAF, DDoS protection, exposed management interfaces |

Map findings to CIS networking controls.

### Step 4: Logging, Encryption & Compute Review

Review remaining control areas:

| Control Area | Checks |
|--------------|--------|
| Logging | CloudTrail enabled, multi-region, S3 access logs, VPC flow logs |
| Encryption | S3 default encryption, EBS encryption, RDS encryption, KMS usage |
| Compute | EC2/VM hardened images, patch status, instance metadata service (IMDSv2) |
| Secrets | Secrets Manager/Parameter Store, no secrets in code or config |

Record pass/fail and evidence (e.g., control IDs, resource ARNs).

### Step 5: Generate Findings Report

Create a Google Sheet with:

- **Tab 1: Summary** — Overall score, pass/fail counts by category, trend vs. prior review
- **Tab 2: Findings** — Control ID, title, status (Pass/Fail/N/A), description, evidence
- **Tab 3: Remediation** — Per finding: owner, priority, steps, target date
- **Tab 4: Raw Data** — Exported checks for audit trail

Use Google Sheets MCP to create and populate the spreadsheet. Format with conditional formatting (e.g., red for fail, green for pass).

## Output

Deliver:
- CIS benchmark scores by category with pass/fail/N/A counts
- Findings report with control ID, status, and evidence
- Prioritized remediation plan with owners and target dates
- Google Sheet with all findings and remediation tracking
