---
name: recon-cloud-assets
description: >
  Discover an organization's cloud footprint — buckets, blobs, apps, IP ranges, and services across
  AWS/GCP/Azure. Load during recon on a company target, on "cloud recon", finding storage/assets, or
  before cloud testing. Signals: an org name/domain in scope, assets on cloud CDNs, wildcard program.
domain: recon
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: info
mitre: [T1596, T1590]
tools: [cloud_enum, s3scanner, amass, dnsx]
schema_version: 1
---

# Cloud asset discovery

## When it applies
Recon on an org where a lot of surface lives in the cloud. Mapping the cloud footprint surfaces
storage exposure, forgotten apps, and IP ranges that feed the cloud-specific skills.

## Why it works
Cloud resources use predictable naming and public namespaces (S3 bucket names are global; app
services use `*.azurewebsites.net`, `*.appspot.com`, etc.). Permuting the org name across providers
reveals assets that aren't linked from the main site.

## Method
1. **Permutation sweep**: `cloud_enum -k <company> -k <company>-prod -k <brand>` to check AWS S3,
   Azure blobs/apps, and GCP buckets/apps for names derived from the org.
2. **From existing assets**: resolve subdomains/CNAMEs (→ `recon-subdomain-enum`, `recon-dns-analysis`)
   for cloud endpoints (`*.s3.amazonaws.com`, `*.blob.core.windows.net`, `*.cloudfront.net`).
3. **IP ranges / ASN**: find the org's ASN and cloud IP ranges; identify origin IPs behind CDNs.
4. **Storage exposure**: feed discovered buckets/containers to `cloud-s3-exposure` (list/read/write test).
5. **Certificate transparency + favicon/Shodan** (→ `recon-osint`) to catch cloud-hosted apps.

## Gotchas
- Stay in scope — cloud recon surfaces third-party SaaS and unrelated tenants; verify ownership.
- Shared CDNs (Cloudflare/CloudFront) are not the org's infra — don't attack the CDN; find origin.
- Anonymous bucket testing must be minimal (list/read a marker) — see `cloud-s3-exposure` for care.

## Verify success
A map of in-scope cloud assets (buckets, apps, IP ranges) with any exposed storage flagged for
follow-up by the cloud skills.

## References
cloud_enum; s3scanner; "cloud recon" methodology; provider public-namespace docs.
