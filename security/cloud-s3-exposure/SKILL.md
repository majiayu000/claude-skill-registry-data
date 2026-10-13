---
name: cloud-s3-exposure
description: >
  Find and prove misconfigured cloud object storage (S3/GCS/Azure Blob). Load when assets load
  from *.s3.amazonaws.com, storage.googleapis.com, *.blob.core.windows.net, bucket-looking
  hostnames, or "bucket". Signals: public-read/list, unauthenticated writes, predictable bucket names.
domain: cloud
type: technique
stability: learning
modes: [bugbounty]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-732]
mitre: [T1530]
tools: [awscli, s3scanner, gcpbucketbrute]
schema_version: 1
---

# Cloud object-storage misconfiguration

## When it applies
The app stores files in S3/GCS/Azure Blob and the bucket's ACL/policy is too open — public
listing, public read of private objects, or (worst) unauthenticated write.

## Why it works
Object-storage ACLs are easy to get wrong: "public" gets applied at the bucket level, or an
IAM policy grants `s3:ListBucket`/`GetObject`/`PutObject` to `*`. Predictable names
(`companyname-backups`, `-assets`, `-dev`) make discovery trivial.

## Method
1. **Find bucket names**: from asset URLs, JS, DNS CNAMEs, and permutations of the org name
   (`company`, `company-prod`, `company-backups`, region suffixes).
2. **Test list/read (S3)**: `aws s3 ls s3://bucket --no-sign-request` (list) and
   `aws s3 cp s3://bucket/file . --no-sign-request` (read). `--no-sign-request` = anonymous.
3. **Test write** (high impact, do carefully & in scope): `aws s3 cp poc.txt s3://bucket/
   --no-sign-request` — a successful anonymous write is critical (defacement/malware hosting).
4. **GCS/Azure**: `gsutil ls gs://bucket` / anonymous HTTPS `GET`; Azure `?comp=list` on the container.
5. **Scale carefully** with `s3scanner`/`gcpbucketbrute` on name lists — respect scope & rate.

## Gotchas
- 403 on the bucket root ≠ safe — individual objects may still be public; test known object paths.
- Anonymous write is the crown jewel but easy to over-test — upload one harmless marker, then stop.
- Region matters for the endpoint; a wrong region gives misleading 301/403.

## Verify success
Anonymous listing/read of non-public objects, or a successful anonymous write of a harmless
proof file (then remove it). Capture the exact command + response.

## References
AWS S3 security docs; "hacking the cloud" S3 guides; s3scanner README.
