---
name: cloud-imds-ssrf
description: >
  Escalate SSRF to cloud credential theft via the instance metadata service (IMDS). Load when
  SSRF is confirmed AND the target runs on AWS/GCP/Azure. Signals: 169.254.169.254 reachable,
  cloud-hosted app, SSRF that can set arbitrary Host/headers, "metadata".
domain: cloud
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A10:2021-SSRF]
cwe: [CWE-918]
mitre: [T1552.005]
tools: [curl, awscli]
schema_version: 1
---

# SSRF → cloud metadata → IAM credential theft

## When it applies
You have SSRF and the app runs on a cloud VM/container with an attached role. The metadata
endpoint hands out temporary credentials to anything that can reach it from the instance.

## Why it works
IMDS lives at a link-local IP (`169.254.169.254`) and trusts *network position*, not identity.
SSRF gives you that position, so the app fetches the instance's role credentials for you —
then you use them against the cloud API with the app's permissions.

## Method
1. **AWS IMDSv1** (no token): SSRF to
   `http://169.254.169.254/latest/meta-data/iam/security-credentials/` → role name →
   `.../security-credentials/<role>` returns `AccessKeyId`, `SecretAccessKey`, `Token`.
2. **AWS IMDSv2** (token required): needs a PUT to get a token, then a header on the GET —
   possible only if the SSRF can set method + `X-aws-ec2-metadata-token` header. Many SSRFs can't;
   note IMDSv2 as the mitigation if it blocks you.
3. **GCP**: `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`
   with header `Metadata-Flavor: Google` (needs header-setting SSRF).
4. **Azure**: `http://169.254.169.254/metadata/identity/oauth2/token?...` with `Metadata: true`.
5. **Use the creds** (in scope only): configure the CLI with the temp key/secret/token and run
   read-only calls (`aws sts get-caller-identity`, `s3 ls`) to prove impact — don't touch data.

## Gotchas
- IMDSv2/`Metadata` header requirements defeat header-less SSRF — that's a finding (says v2 is on), not a dead end.
- Temp creds expire fast; grab `sts get-caller-identity` immediately as proof.
- Containers may hit the ECS task metadata (`169.254.170.2`) instead of EC2 IMDS.

## Verify success
`aws sts get-caller-identity` (or GCP/Azure equivalent) returns the instance role identity
using credentials pulled through the SSRF.

## References
PortSwigger SSRF labs; AWS IMDSv2 docs; "SSRF to cloud takeover" write-ups.
