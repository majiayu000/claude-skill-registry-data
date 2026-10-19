---
name: cloud-gcp
description: >
  Attack Google Cloud Platform — metadata/SA token theft, IAM privilege escalation, and storage/
  function misconfig. Load when the target runs on GCP, you hold a GCP SA key/token, or see
  gcp/gcloud/GCE/GKE/appspot. Signals: metadata.google.internal, service-account.json, storage.googleapis.com,
  cloudfunctions, gcloud.
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A01:2021-Broken-Access-Control, A05:2021-Security-Misconfiguration]
cwe: [CWE-269, CWE-732]
mitre: [T1078.004, T1552.005]
tools: [gcloud, gcloud-iam, ScoutSuite]
schema_version: 1
---

# GCP attacks

## When it applies
The target is on GCP and you have some access — an SSRF into a GCE/GKE instance, a leaked service
account (SA) key, or a foothold in a workload. Goal: steal credentials, escalate IAM, reach data.

## Why it works
GCP identity centers on **service accounts** and IAM bindings that are frequently over-granted. The
metadata server hands SA tokens to anything on the instance, and a small set of permissions
(`actAs`, `setIamPolicy`, deploy roles) form known escalation paths to owner.

## Method
1. **Metadata → SA token** (via SSRF, or on the host): `GET metadata.google.internal/computeMetadata/v1/
   instance/service-accounts/default/token` with header `Metadata-Flavor: Google` (→ `cloud-imds-ssrf`).
   Also grab `.../scopes` and project info.
2. **Authenticate & enumerate**: `gcloud auth activate-service-account --key-file=sa.json`;
   `gcloud projects get-iam-policy`, list what the SA can do; ScoutSuite for the landscape.
3. **IAM privesc paths**: `iam.serviceAccounts.actAs` + deploy (Cloud Functions/Run/Compute) to run
   as a higher-priv SA; `iam.serviceAccounts.getAccessToken`/`signJwt`/`implicitDelegation`;
   `setIamPolicy` (editor→owner); `deploymentmanager` running as the default SA.
4. **Data & services**: enumerate GCS buckets (→ `cloud-s3-exposure` equivalents), Cloud SQL,
   secrets in Secret Manager, and GKE (→ `cloud-kubernetes`).
5. **Prove impact** with a read-only call as the escalated identity; don't create lasting bindings.

## Gotchas
- SA **scopes** (legacy) can restrict a token even with broad IAM — check both scope and IAM.
- `actAs` + a deploy permission is the classic privesc — hunt for it specifically.
- Org policies/VPC-SC may block exfil paths; note them rather than forcing.

## Verify success
Escalated access proven — a call succeeding as a higher-priv SA, secret/data read you shouldn't
have, or `gcloud` acting with permissions beyond your starting identity.

## References
GCP IAM docs; Rhino Security GCP privesc research; ScoutSuite; "hacking GCP" guides.
