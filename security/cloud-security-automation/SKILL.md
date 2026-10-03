---
name: cloud-security-automation
description: Cloud security posture skill for AWS, Azure, GCP, and multi-cloud. Covers IAM least-privilege, key and secret hygiene, network exposure, data protection, logging coverage, IaC scanning (Terraform, CloudFormation, Bicep, Pulumi), CSPM remediation, and landing-zone hardening. Use for misconfig discovery, IaC review, and automated drift-and-fix workflows on cloud accounts you own.
---

# Cloud Security Automation

## Authorization Boundary

- Require account IDs, role ARNs/principals, and read-only credentials in scope before any live query.
- Default to read-only APIs and `--dry-run`/plan mode for any change.
- Do not exfiltrate customer data; redact resource names if shared outside the engagement.

## Posture Workflow

1. Inventory: accounts, subscriptions, projects, regions, services in use, owners, tags.
2. Baseline: pull config via `aws configservice`, `az resource graph`, `gcloud asset`, plus `prowler`, `scout-suite`, `cloudsploit`, `steampipe`.
3. Score: map findings to CIS, NIST 800-53, Well-Architected, and CSA CCM.
4. IaC pre-flight: `checkov`, `tfsec`, `kics`, `terrascan`, `cfn-nag` on PRs; block on critical.
5. Remediate: produce least-privilege IAM diffs, network restrictions, encryption defaults, and logging fixes as code, not console clicks.
6. Drift watch: compare desired state to live; alert on out-of-band changes.

## Focus Areas

- IAM: wildcard actions, cross-account trust, unused roles, long-lived keys, OIDC federation.
- Network: public S3/Blob/GCS, 0.0.0.0/0 ingress, exposed databases, lateral paths.
- Data: encryption at rest, KMS key policies, backup posture, PII tagging.
- Logging: CloudTrail/Activity Logs/Audit Logs coverage, retention, SIEM ingestion.
- Identity: MFA, conditional access, SCP/Org Policy guardrails, break-glass accounts.

## Output Contract

- `inventory.json`, `findings.csv` (with severity, control, evidence, fix).
- `iac-patches/`: ready-to-PR diffs.
- `runbooks/`: incident-grade response for each top finding.
- `posture-trend.md`: weekly delta with regressions called out.
