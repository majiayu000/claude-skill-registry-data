---
name: iam-policy-analyzer
displayName: IAM Policy Analyzer
tagline: Analyze AWS/GCP/Azure IAM policies for over-permissive access, unused roles, and privilege escalation paths.
description: |
  Reviews IAM policies across cloud providers to identify over-permissive access,
  unused roles, cross-account trust issues, and privilege escalation paths.
  Generates a risk-scored findings report with specific remediation recommendations
  for each policy violation.
department:
  - Security & Compliance
  - Cloud Security
use_cases:
  - Compliance Audit
  - Threat Modeling
tools_required:
  - AWS MCP
  - GitHub MCP
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
  We need to review IAM policies for our 50-person engineering org on AWS.
  We have 200+ IAM roles, a mix of human users, service accounts, and
  CI/CD pipelines. Concern: possible over-permissive policies from rapid
  onboarding. We use Organization SCPs and need cross-account trust review.
exampleOutput: |
  IAM Policy Findings Report — [Account ID] | Generated: 2026-02-20

  OVER-PERMISSIVE POLICIES (Risk: High)
  | Role/Policy           | Violation                         | Risk | Remediation                    |
  |-----------------------|-----------------------------------|------|-------------------------------|
  | prod-deploy-role      | s3:* on all buckets               | 9.2  | Scope to specific bucket ARNs  |
  | dev-admin-assume      | iam:* attached to assume role     | 8.8  | Remove iam:*; use least priv  |
  | lambda-exec-*         | dynamodb:GetItem resource: *      | 6.5  | Restrict to required table     |

  UNUSED ROLES (Last used >90 days)
  | Role Name             | Last Used   | Action   |
  |-----------------------|-------------|----------|
  | legacy-migration-2019 | 2024-03-12  | Decommission |
  | temp-intern-role-1    | 2025-08-01  | Review & remove |
  | ... 12 more           |             |          |

  PRIVILEGE ESCALATION PATHS
  | Path                  | Steps | Severity |
  |-----------------------|-------|----------|
  | dev-user → admin      | 2 (AssumeRole + PassRole) | Critical |
  | cicd-role → root      | 3 (CreateUser + AttachPolicy)     | High   |

  Total findings: 28 | Critical: 2 | High: 8 | Medium: 12 | Low: 6
---

# IAM Policy Analyzer

Analyze AWS/GCP/Azure IAM policies for over-permissive access, unused roles, and privilege escalation paths.

**Integrations:** AWS MCP, GitHub MCP

## When to Use

- The user needs to audit IAM policies before a compliance review or security assessment
- The user mentions "IAM review", "over-permissive policies", "least privilege", or "privilege escalation"
- After a breach or suspected credential compromise, to identify exposure scope
- When consolidating or migrating IAM roles and need to understand current state and risks

## Steps

### Step 1: Inventory IAM Policies

Gather a complete inventory of IAM entities:

| Entity Type | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| Roles | IAM roles, instance profiles | IAM roles, service accounts | RBAC roles, managed identities |
| Users | IAM users (if any) | — | Entra ID users |
| Policies | Inline + managed policies | IAM policy bindings | Role assignments |
| Cross-account | AssumeRole trust policies | — | Cross-tenant/app registrations |

Use AWS MCP to list roles, policies, and trust relationships. Export Terraform/CloudFormation if available via GitHub MCP for version history.

### Step 2: Analyze Permission Scope

Check for over-permissive patterns:

| Pattern | Risk | Example |
|---------|------|---------|
| Wildcard actions (`*:Get*`, `s3:*`) | High | Allows unintended operations |
| Resource `*` | High | Applies to all resources in scope |
| PassRole + broad IAM | Critical | Enables privilege escalation |
| Cross-account trust without conditions | Medium | Overly broad federation |
| Long-lived keys on service accounts | Medium | Prefer workload identity |

Flag policies that violate least privilege or exceed documented use cases.

### Step 3: Detect Privilege Escalation Paths

Identify chains that allow a low-privilege identity to gain higher privileges:

| Escalation Type | Common Triggers |
|-----------------|-----------------|
| AssumeRole chain | Role A can assume Role B that has admin |
| PassRole abuse | Role can pass admin role to itself or another |
| IAM self-modification | iam:PutUserPolicy, iam:AttachUserPolicy on self |
| Resource creation | ec2:RunInstances with instance profile that has admin |

Document each path with source role, intermediate steps, and target privilege level.

### Step 4: Generate Findings Report

Produce a risk-scored findings table:

| Finding | Risk (1–10) | Description | Remediation |
|---------|-------------|-------------|-------------|
| Over-permissive policy | 6–10 | Policy exceeds documented need | Scope actions and resources |
| Unused role | 3–5 | No activity in 90+ days | Decommission or justify |
| Privilege escalation path | 7–10 | Chain to elevated access | Break chain, add conditions |
| Cross-account trust issue | 5–8 | Overly permissive trust | Add conditions, MFA, scoping |
| Service account key | 4–6 | Long-lived key in use | Migrate to workload identity |

Include pass/fail counts by category and a prioritized remediation order.

### Step 5: Create Remediation Plan

For each finding, provide:

1. **Immediate actions** — Critical and high-risk fixes (e.g., remove wildcards, break escalation paths)
2. **Short-term** — Unused role cleanup, trust policy tightening
3. **Long-term** — Process for future reviews, automated checks, policy guardrails

Output a remediation checklist with owners and target dates.

## Output

Deliver:
- Risk-scored findings report with over-permissive policies, unused roles, and privilege escalation paths
- Specific remediation recommendations for each finding
- Prioritized remediation plan (immediate, short-term, long-term)
- Summary of pass/fail counts by risk category
