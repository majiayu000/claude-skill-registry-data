---
name: cloud-iam-privesc
description: >
  Escalate privileges in cloud IAM (AWS/GCP/Azure) from a low-priv set of credentials. Load when
  you hold cloud creds/keys/a role and want higher privilege or new resources. Signals: leaked
  AWS keys, an assumed role, a service-account token, "escalate in AWS/GCP/Azure", enumerated permissions.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A01:2021-Broken-Access-Control]
cwe: [CWE-269]
mitre: [T1078.004, T1548]
tools: [awscli, pacu, scoutsuite, enumerate-iam]
schema_version: 1
---

# Cloud IAM privilege escalation

## When it applies
You have some cloud identity (leaked keys, an SSRF-obtained role — `cloud-imds-ssrf`, a
compromised service account) and want to escalate to admin or reach more resources.

## Why it works
IAM is complex and permissions are over-granted. A handful of seemingly-minor permissions form
known escalation paths — creating a policy version, attaching a policy, passing a role, updating a
function's code/role — that promote a low-priv identity to admin.

## Method
1. **Identify & enumerate**: `aws sts get-caller-identity`; enumerate your effective permissions
   (`enumerate-iam`, `pacu`, or read attached policies). GCP: `gcloud ... get-iam-policy`; Azure: `az role assignment list`.
2. **Find an escalation primitive** (AWS examples):
   - `iam:CreatePolicyVersion` / `SetDefaultPolicyVersion` → grant yourself `*`.
   - `iam:AttachUserPolicy` / `PutUserPolicy` → attach AdministratorAccess.
   - `iam:PassRole` + `lambda:CreateFunction`/`ec2:RunInstances`/`glue`/`cloudformation` → run code as a privileged role.
   - `iam:CreateAccessKey` on another user; `sts:AssumeRole` on an over-trusting role.
   GCP: `iam.serviceAccounts.actAs`, `setIamPolicy`, editor→owner via `deploymentmanager`.
3. **Execute the path** (in scope), then confirm elevated access with a read-only admin call.
4. **Automate discovery** with `pacu` (AWS) escalation modules / ScoutSuite for the landscape.

## Gotchas
- Enumerate permissions first — escalation depends entirely on which ones you hold.
- Prove escalation with a minimal, reversible action; don't create lasting admin backdoors on a live account (RoE).
- Temp creds expire — capture `get-caller-identity` before and after as proof.

## Verify success
You gain permissions/resources beyond your starting identity (e.g. an admin-only call now
succeeds, or you assume a higher-priv role), demonstrated with before/after identity.

## References
Rhino Security "AWS IAM privilege escalation" methods; Pacu; GCP/Azure privesc guides; ScoutSuite.
