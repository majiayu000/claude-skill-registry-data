---
name: cloud-security
description: Assess cloud environments (AWS, GCP, Azure) for authorized security review — public storage and snapshot exposure, IAM over-permissioning and privilege-escalation paths, exposed metadata/credentials, misconfigured serverless and networking, and public-facing managed services. Covers both external bug-bounty-style discovery and authenticated configuration review. Use whenever the user mentions AWS/GCP/Azure, S3/GCS/Blob buckets, IAM roles/policies, 169.254.169.254 or cloud metadata, cloud keys, serverless/Lambda, or asks to review a cloud account's security posture.
license: Apache-2.0
metadata:
  layer: specialist
  status: under-review
  coverage: cloud-iam
---

# Cloud Security Reviewer (AWS · GCP · Azure)

Two modes, different authorization:
- **External** (bug-bounty / attack-surface): only in-scope assets, unauthenticated or
  with your own account. No enumerating a third party's private resources.
- **Authenticated review** (your/engagement account): read-only config audit with
  least-privilege credentials you were given.

Confirm which mode and the authorization basis before anything. Credentials are sensitive
— never print, log, or commit them; never use discovered credentials to pivot without
explicit authorization (on bug bounty: report, don't use). See `docs/SAFETY.md`.

## Inputs
- Mode + authorization basis + provider(s).
- External: in-scope domains/IPs/bucket names.
- Authenticated: read-only credentials/role, and the account/project/subscription id.

## Highest-signal checks (map, don't spray)

### 1. Public storage & data exposure
- **S3 / GCS / Azure Blob**: unauthenticated list/read; bucket-name enumeration from the
  org's naming pattern (only names tied to in-scope assets). Check ACLs, public policy,
  and `response-content-type` serve-side issues (→ `bb-upload`).
- Public snapshots/images: EBS/AMI, RDS snapshots, GCP images, Azure disks shared public.
- Exposed artifact stores, backups, logs, `.git`, CI caches on public storage.

### 2. Credential & metadata exposure
- Keys in public buckets, repos, JS bundles (→ `js-audit`), container layers.
- **Metadata service** via SSRF (→ `bb-ssrf`): AWS IMDS `169.254.169.254` (prefer proving
  IMDSv1 reachability; IMDSv2 needs the token hop), GCP `metadata.google.internal` with
  `Metadata-Flavor: Google`, Azure IMDS `169.254.169.254/metadata` with
  `Metadata:true`. Demonstrate reachability; **do not exfiltrate or use** the creds.

### 3. IAM over-permissioning & privilege escalation (authenticated mode)
- Enumerate principals, policies, roles, trust relationships.
- Flag wildcards (`Action:"*"`, `Resource:"*"`), `iam:PassRole` + a compute service,
  `iam:CreatePolicyVersion`/`SetDefaultPolicyVersion`, `lambda:UpdateFunctionCode` on a
  privileged role, `sts:AssumeRole` chains, GCP `iam.serviceAccounts.actAs` /
  `setIamPolicy`, Azure role-assignment write / `Owner` sprawl.
- Describe the **escalation path** as a graph; prove only read-level enumeration unless
  explicitly authorized to demonstrate escalation in a lab/engagement.

### 4. Network & service exposure
- Security groups / firewall rules open to `0.0.0.0/0` on sensitive ports (DB, RDP, SSH,
  k8s API, admin UIs), public RDS/Redis/Elastic, exposed management consoles.
- Public serverless endpoints (Lambda URLs, Cloud Functions, API Gateway) with weak authz.

### 5. Logging/monitoring gaps (detection posture)
- CloudTrail/Config/GuardDuty, GCP Audit Logs, Azure Monitor disabled or not org-wide —
  a finding in itself and a hand-off to `detection-engineering`.

## Decisions requiring judgment
- A bucket/snapshot is public but does it belong to an in-scope asset? Verify before access.
- Reachable metadata endpoint — stop at reachability proof; do not read/use credentials.
- IAM escalation path — graph it; demonstrate only within explicit authorization.

## Evidence vs hypothesis
Record to `schemas/finding.schema.json`. A public bucket needs the unauthenticated read
response (own/in-scope data). An IAM path is a hypothesis until each permission is
confirmed present; mark unconfirmed hops clearly. Never present "could escalate" as proven.

## Tools (check availability; none bundled; use read-only creds)
- Provider CLIs: `aws`, `gcloud`, `az` (read/describe/list only).
- Posture/enum: `ScoutSuite`, `Prowler`, `cloudsplaining`, `pmapper` (AWS IAM graph),
  `cartography`; external bucket checks via provider APIs. Confirm each is installed;
  otherwise use the provider CLI's describe/list calls.
- Never run a tool that writes/changes state in review mode.

## Failure handling
No credentials → external mode only. A CLI/tool missing → state it and use the REST/CLI
read equivalent. Access denied on an enumeration call → record as "not assessable with
provided permissions," don't assume secure.

## Output
A posture table (service · exposure · severity · evidence) + finding records + the IAM
escalation graph (if authenticated). Calibrate/report via `bb-disclosures`, `bb-chains`,
`bb-report`.

## Acceptance criteria (for `validated`)
- POS: given read-only creds, produces the posture table and an IAM finding with the
  confirmed permission set. NEG: refuses to mark an IAM escalation "confirmed" with an
  unverified hop. SAFE: proves metadata reachability without using creds; read-only in
  review mode; in-scope only externally. INC: access-denied enumeration → not-assessable,
  not "secure."

## References
AWS/GCP/Azure IAM docs; cloud provider security best-practice guides; MITRE ATT&CK Cloud.
Siblings: `bb-ssrf`, `js-audit`, `bb-upload`, `container-k8s-security`,
`detection-engineering`.
