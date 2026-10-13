---
name: defense-cloud-detection
description: >
  Detect and respond to attacks in cloud control planes — credential abuse, IMDS theft, persistence,
  and privilege escalation — from audit logs. Load for "detect cloud attacks", "CloudTrail/GuardDuty",
  "someone used our keys", AWS/Azure/GCP monitoring, or cloud IR. The defensive counterpart to the
  cloud-* offensive skills.
domain: defense
type: technique
stability: learning
modes: [defense]
severity: info
mitre: [T1078.004, T1552.005, T1078, T1098]
tools: [cloudtrail, guardduty, athena, azure-monitor, gcp-audit-logs]
schema_version: 1
---

# Cloud detection & response

## When it applies
Your assets live in AWS/Azure/GCP and you need to catch control-plane abuse — stolen keys, a role
assumed from a strange place, new persistence — using the provider's audit logs.

## Why it works
Every cloud API call is logged (CloudTrail / Azure Activity / GCP Admin Activity). Attacks that are
invisible on the host (assuming a role, reading a secret, adding a key) are loud in the control
plane — if you're actually reading it. The identity *and* the calling context are in every event.

## Method
1. **Guarantee the telemetry**: CloudTrail (all regions + management & data events), Azure Activity
   + Entra sign-in logs, GCP audit logs — centralised and immutable. No logs → no detection.
2. **Credential-theft tells**: an IAM user/role key used from a new ASN/region/UA, especially
   `sts:GetCallerIdentity` then enumeration bursts — classic stolen-key triage. IMDS-sourced role
   creds used off the instance (compare the session's source IP to the instance).
3. **Persistence**: `CreateAccessKey`, `CreateUser`, new login profile, `CreateRole` with a broad
   trust policy, new identity provider — alert on these in prod accounts.
4. **Privilege escalation**: `AttachUserPolicy`/`PutUserPolicy` granting `*`, `iam:PassRole` +
   service launch, `AssumeRole` chains that cross accounts.
5. **Managed signals**: enable GuardDuty / Defender for Cloud / SCC as a baseline, then tune and
   layer custom queries (Athena over CloudTrail) on top.
6. **Respond**: disable the key/session, revoke role sessions, snapshot for forensics, rotate, and
   review what the identity could reach (`tradecraft-attack-path-mapping`).

## Gotchas
- CloudTrail data events (S3 object-level, Lambda) are off by default — you miss exfil without them.
- Roles blur "who did it" — correlate the session name and source, not just the principal.
- Automation (CI/CD, Terraform) generates the same API calls; baseline service identities first.

## Verify success
A simulated key-abuse / privilege-escalation sequence (e.g. via a lab) surfaces from the audit logs
with the identity, source, and action, and the response revokes access and preserves evidence.

## References
AWS CloudTrail & GuardDuty; Azure Monitor / Entra sign-in logs; GCP audit logs; MITRE ATT&CK Cloud matrix.
