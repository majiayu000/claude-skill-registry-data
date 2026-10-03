---
name: cloud-gcp-iam
description: "Cloud Gcp Iam."
domain: cybersecurity
---

|
| Primitive Role | Legacy GCP roles (Owner, Editor, Viewer) that grant broad permissions across all services, not recommended for production |
| Predefined Role | GCP-managed role scoped to specific services and actions, providing more granular access than primitive roles |
| IAM Recommender | GCP ML-based service that analyzes actual permission usage and suggests role reductions to achieve least privilege |
| Policy Analyzer | Tool for analyzing effective IAM access across the organization hierarchy, answering who-can-access-what queries |
| Service Account Key | User-managed credential for service account authentication, a security risk as keys can be exported and do not auto-expire |
| Domain-Wide Delegation | Grants a service account the ability to impersonate any user in the Google Workspace domain, a significant privilege escalation risk |

## Tools & Systems

- **gcloud CLI**: Primary tool for querying and managing GCP IAM policies, service accounts, and role bindings
- **IAM Recommender**: ML-based recommendation engine for reducing excessive permissions based on actual usage
- **Policy Analyzer**: Organization-wide effective access analysis tool for understanding who can access what
- **Cloud Asset Inventory**: Cross-project search for IAM policies and resource metadata
- **ScoutSuite**: Multi-cloud auditing tool with GCP IAM-specific checks for role assignments and service accounts

## Common Scenarios

### Scenario: Reducing Primitive Role Usage Across a GCP Organization

**Context**: An audit reveals that 60% of IAM bindings across the organization use primitive roles (Owner/Editor). The security team needs to migrate to predefined roles without disrupting developer workflows.

**Approach**:
1. Run `gcloud asset search-all-iam-policies` to inventory all primitive role bindings
2. Use IAM Recommender to get ML-based suggestions for replacement predefined roles
3. For each binding, use Policy Analyzer to understand what the principal actually accesses
4. Create a mapping document: primitive role -> specific predefined roles needed
5. Apply predefined roles alongside primitive roles for a testing period
6. Monitor for access denied errors using Cloud Audit Logs
7. Remove primitive roles after confirming no access issues over 2 weeks

**Pitfalls**: Primitive roles include permissions across all GCP services, so replacing them requires multiple predefined roles. The Recommender may suggest overly restrictive roles if the observation period does not capture all use cases. Custom roles can fill gaps where no predefined role matches the exact permission set needed.

## Output Format

```
GCP IAM Permissions Audit Report
===================================
Organization: acme-org (ORG_ID: 123456789)
Projects Audited: 25
Audit Date: 2026-02-23

IAM BINDING SUMMARY:
  Total bindings:                    342
  Using primitive roles:             205 (60%)
  Using predefined roles:            112 (33%)
  Using custom roles:                 25 (7%)

CRITICAL FINDINGS:
[IAM-001] Service Account with Owner Role
  SA: admin-sa@prod-project.iam.gserviceaccount.com
  Role: roles/owner on project prod-project
  User-Managed Keys: 3 (oldest: 14 months)
  Remediation: Replace with specific predefined roles, delete old keys

[IAM-002] allAuthenticatedUsers Binding
  Resource: gs://public-data-bucket
  Role: roles/storage.objectViewer
  Risk: Any Google account holder can read bucket contents
  Remediation: Restrict to specific user groups or service accounts

SERVICE ACCOUNT HEALTH:
  Total service accounts:            67
  With user-managed keys:            23
  Keys older than 90 days:           18
  Unused accounts (90+ days):        12
  With domain-wide delegation:        2

RECOMMENDER SUGGESTIONS:
  Total recommendations:             45
  Priority HIGH:                     12
  Estimated permissions reduced:     2,847 individual permissions
```
