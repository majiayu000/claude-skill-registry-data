---
type: skill
name: s3
description: AWS S3 object storage for bucket management, object operations, and access control. Use when creating buckets, uploading files, configuring lifecycle policies, setting up static websites, managing permissions, or implementing cross-region replication.
last_updated: "2026-01-07"
doc_source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/
---

# AWS S3

Amazon Simple Storage Service (S3) provides scalable object storage with industry-leading durability (99.999999999%). S3 is fundamental to AWS—used for data lakes, backups, static websites, and as storage for many other AWS services.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Common Patterns](#common-patterns)
- [CLI Reference](#cli-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [S3 Security Edge Cases](#s3-security-edge-cases)
- [References](#references)

## Core Concepts

### Buckets

Containers for objects. Bucket names are globally unique across all AWS accounts.

### Objects

Files stored in S3, consisting of data, metadata, and a unique key (path). Maximum size: 5 TB.

### Storage Classes

| Class | Use Case | Durability | Availability |
|-------|----------|------------|--------------|
| Standard | Frequently accessed | 99.999999999% | 99.99% |
| Intelligent-Tiering | Unknown access patterns | 99.999999999% | 99.9% |
| Standard-IA | Infrequent access | 99.999999999% | 99.9% |
| Glacier Instant | Archive with instant retrieval | 99.999999999% | 99.9% |
| Glacier Flexible | Archive (minutes to hours) | 99.999999999% | 99.99% |
| Glacier Deep Archive | Long-term archive | 99.999999999% | 99.99% |

### Versioning

Keeps multiple versions of an object. Essential for data protection and recovery.

## Common Patterns

### Create a Bucket with Best Practices

**AWS CLI:**

```bash
# Create bucket (us-east-1 doesn't need LocationConstraint)
aws s3api create-bucket \
  --bucket my-secure-bucket-12345 \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-secure-bucket-12345 \
  --versioning-configuration Status=Enabled

# Block public access
aws s3api put-public-access-block \
  --bucket my-secure-bucket-12345 \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-secure-bucket-12345 \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
  }'
```

**boto3:**

```python
import boto3

s3 = boto3.client('s3', region_name='us-west-2')

# Create bucket
s3.create_bucket(
    Bucket='my-secure-bucket-12345',
    CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
)

# Enable versioning
s3.put_bucket_versioning(
    Bucket='my-secure-bucket-12345',
    VersioningConfiguration={'Status': 'Enabled'}
)

# Block public access
s3.put_public_access_block(
    Bucket='my-secure-bucket-12345',
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
)
```

### Upload and Download Objects

```bash
# Upload a single file
aws s3 cp myfile.txt s3://my-bucket/path/myfile.txt

# Upload with metadata
aws s3 cp myfile.txt s3://my-bucket/path/myfile.txt \
  --metadata "environment=production,version=1.0"

# Download a file
aws s3 cp s3://my-bucket/path/myfile.txt ./myfile.txt

# Sync a directory
aws s3 sync ./local-folder s3://my-bucket/prefix/ --delete

# Copy between buckets
aws s3 cp s3://source-bucket/file.txt s3://dest-bucket/file.txt
```

### Generate Presigned URL

```python
import boto3
from botocore.config import Config

s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

# Generate presigned URL for download (GET)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'path/to/file.txt'},
    ExpiresIn=3600  # URL valid for 1 hour
)

# Generate presigned URL for upload (PUT)
upload_url = s3.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'my-bucket',
        'Key': 'uploads/newfile.txt',
        'ContentType': 'text/plain'
    },
    ExpiresIn=3600
)
```

### Configure Lifecycle Policy

```bash
cat > lifecycle.json << 'EOF'
{
  "Rules": [
    {
      "ID": "MoveToGlacierAfter90Days",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    },
    {
      "ID": "DeleteOldVersions",
      "Status": "Enabled",
      "Filter": {},
      "NoncurrentVersionExpiration": {"NoncurrentDays": 30}
    }
  ]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
```

### Event Notifications to Lambda

```bash
aws s3api put-bucket-notification-configuration \
  --bucket my-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [
      {
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:ProcessS3Upload",
        "Events": ["s3:ObjectCreated:*"],
        "Filter": {
          "Key": {
            "FilterRules": [
              {"Name": "prefix", "Value": "uploads/"},
              {"Name": "suffix", "Value": ".jpg"}
            ]
          }
        }
      }
    ]
  }'
```

## CLI Reference

### High-Level Commands (aws s3)

| Command | Description |
|---------|-------------|
| `aws s3 ls` | List buckets or objects |
| `aws s3 cp` | Copy files |
| `aws s3 mv` | Move files |
| `aws s3 rm` | Delete files |
| `aws s3 sync` | Sync directories |
| `aws s3 mb` | Make bucket |
| `aws s3 rb` | Remove bucket |

### Low-Level Commands (aws s3api)

| Command | Description |
|---------|-------------|
| `aws s3api create-bucket` | Create bucket with options |
| `aws s3api put-object` | Upload with full control |
| `aws s3api get-object` | Download with options |
| `aws s3api delete-object` | Delete single object |
| `aws s3api put-bucket-policy` | Set bucket policy |
| `aws s3api put-bucket-versioning` | Enable versioning |
| `aws s3api list-object-versions` | List all versions |

### Useful Flags

- `--recursive`: Process all objects in prefix
- `--exclude/--include`: Filter objects
- `--dryrun`: Preview changes
- `--storage-class`: Set storage class
- `--acl`: Set access control (prefer policies instead)

## Best Practices

### Security

- **Block public access** at account and bucket level
- **Enable versioning** for data protection
- **Use bucket policies** over ACLs
- **Enable encryption** (SSE-S3 or SSE-KMS)
- **Enable access logging** for audit
- **Use VPC endpoints** for private access
- **Enable MFA Delete** for critical buckets

### Performance

- **Use Transfer Acceleration** for distant uploads
- **Use multipart upload** for files > 100 MB
- **Randomize key prefixes** for high-throughput (less relevant with 2024 improvements)
- **Use byte-range fetches** for large file downloads

### Cost Optimization

- **Use lifecycle policies** to transition to cheaper storage
- **Enable Intelligent-Tiering** for unpredictable access
- **Delete incomplete multipart uploads**:
  ```json
  {
    "Rules": [{
      "ID": "AbortIncompleteMultipartUpload",
      "Status": "Enabled",
      "Filter": {},
      "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}
    }]
  }
  ```
- **Use S3 Storage Lens** to analyze storage patterns

## Troubleshooting

### Access Denied Errors

**Causes:**
1. Bucket policy denies access
2. IAM policy missing permissions
3. Public access block preventing access
4. Object owned by different account
5. VPC endpoint policy blocking

**Debug steps:**

```bash
# Check your identity
aws sts get-caller-identity

# Check bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# Check public access block
aws s3api get-public-access-block --bucket my-bucket

# Check object ownership
aws s3api get-object-attributes \
  --bucket my-bucket \
  --key myfile.txt \
  --object-attributes ObjectOwner
```

### CORS Errors

**Symptom:** Browser blocks cross-origin request

**Fix:**

```bash
aws s3api put-bucket-cors --bucket my-bucket --cors-configuration '{
  "CORSRules": [{
    "AllowedOrigins": ["https://myapp.com"],
    "AllowedMethods": ["GET", "PUT", "POST"],
    "AllowedHeaders": ["*"],
    "ExposeHeaders": ["ETag"],
    "MaxAgeSeconds": 3600
  }]
}'
```

### Slow Uploads

**Solutions:**
- Use multipart upload for large files
- Enable Transfer Acceleration
- Use `aws s3 cp` with `--expected-size` for large files
- Check network throughput to the region

### 403 on Presigned URL

**Causes:**
- URL expired
- Signer lacks permissions
- Bucket policy blocks access
- Region mismatch (v4 signatures are region-specific)

**Fix:** Ensure signer has permissions and use correct region.

## External Accessibility Probe

Use when the question is "is this bucket publicly accessible?" Tests from outside the account with no credentials — what an attacker would see.

**Step 1 — Discover endpoint:**
```bash
aws s3api get-bucket-location --bucket {{bucket}} --region {{region}}
# Confirms bucket exists and reveals its region
```

**Step 2 — External probe (no credentials):**
```bash
curl -s https://{{bucket}}.s3.amazonaws.com/
```

**Interpreting the response:**

| Response body | Meaning |
|:---------|:--------|
| Contains `ListBucketResult` or `<Key>` | Fully public — bucket contents readable by anyone |
| Contains `<Code>AccessDenied</Code>` | Bucket reachable but access denied — **must evaluate WHY** (see below) |
| Contains `<Code>NoSuchBucket</Code>` or connection refused | Bucket not publicly reachable |

**CRITICAL — 403 AccessDenied requires root-cause analysis, not a blanket finding:**

A 403 can mean two very different things:
1. **No Block Public Access override** → bucket is on the public internet, policy could be misconfigured to allow access. This IS a finding.
2. **`RestrictPublicBuckets = true`** → S3 is actively blocking anonymous access at the API enforcement layer, regardless of what the bucket policy says. This is NOT a finding — the bucket is mitigated.

**You MUST cross-reference the Public Access Block before concluding:**
```bash
aws s3api get-public-access-block --bucket {{bucket}} --output json
```

| `RestrictPublicBuckets` | `IsPublic` (policy status) | Actual state | Finding? |
|:------------------------|:---------------------------|:-------------|:---------|
| `true` | `true` | Policy says public but **override blocks anonymous access** | **NO** — mitigated by RestrictPublicBuckets |
| `true` | `false` | Not public | NO |
| `false` | `true` | Policy is public AND no override — **actually exposed** | **YES** — real finding |
| `false` | `false` | Not public | NO |

**Do NOT rely on `get-bucket-policy-status` alone.** `IsPublic: true` only evaluates the policy text in isolation — it does NOT account for Block Public Access overrides. See "Block Public Access Enforcement Hierarchy" below for the full evaluation order.

**Step 3 — Extended probes (check edge case exposure):**

If the base probe returns AccessDenied, also test hidden enumeration and metadata endpoints:
```bash
# Version listing (bypasses ListBucket deny):
curl -s "https://{{bucket}}.s3.amazonaws.com/?versions"

# Multipart uploads (leaks uploader ARNs):
curl -s "https://{{bucket}}.s3.amazonaws.com/?uploads"

# Metadata probes:
curl -s "https://{{bucket}}.s3.amazonaws.com/?tagging"
curl -s "https://{{bucket}}.s3.amazonaws.com/?logging"
curl -s "https://{{bucket}}.s3.amazonaws.com/?encryption"
```

If any return data instead of AccessDenied, the bucket is leaking information
even though the base listing is denied. See S3 Security Edge Cases below for details.

**Scoring:** See `agents/roles.md` → Scoring Rubric. S3-specific:
- Unauthenticated curl HTTP 200 (ListBucketResult) → Score 5 CRITICAL
- Unauthenticated curl HTTP 403 **with `RestrictPublicBuckets = false`** → Score 5 (reachable, auth-dependent)
- Unauthenticated curl HTTP 403 **with `RestrictPublicBuckets = true`** → **FALSE_POSITIVE** (override blocks access)
- `IsPublic: true` alone (without checking Block Public Access) → **INSUFFICIENT** — must cross-reference `get-public-access-block`
- Raw policy JSON inference only → Score 3

---

## S3 Security Edge Cases

Advanced S3 attack vectors and misconfigurations that standard tools often miss.
These MUST be checked during audits when S3 buckets are in scope.

Reference: https://www.plerion.com/blog/things-you-wish-you-didnt-need-to-know-about-s3

### Anonymous API Access

Buckets with `Principal: "*"` and broad actions (e.g., `s3:*`) allow unauthenticated
destructive operations including bucket deletion:

```bash
# An attacker can delete an unprotected bucket anonymously:
curl -X DELETE https://[bucketname].s3.[region].amazonaws.com
```

**Audit check:** Any policy with `Principal: "*"` and actions beyond `s3:GetObject`
is a critical finding. Anonymous requests appear in CloudTrail with
`"accountId": "anonymous"` and empty `principalId` — no attribution possible.

```bash
# Check for overly permissive policies:
aws s3api get-bucket-policy --bucket {{bucket}} --output json
# Flag: Principal "*" with actions other than s3:GetObject
```

### Hidden Enumeration Paths (Beyond ListBucket)

Denying `s3:ListBucket` does NOT prevent object enumeration. Two alternative
listing APIs exist that are often left unprotected:

| API | Permission Required | What It Reveals |
|:----|:-------------------|:----------------|
| `GET /?versions` | `s3:ListBucketVersions` | All object versions including deleted objects |
| `GET /?uploads` | `s3:ListMultipartUploads` | In-progress uploads + uploader's principal ARN |

```bash
# Check if versions listing is accessible:
curl -s "https://{{bucket}}.s3.amazonaws.com/?versions"

# Check if multipart uploads are visible:
curl -s "https://{{bucket}}.s3.amazonaws.com/?uploads"
```

**Audit check:** If `s3:ListBucket` is denied but `s3:ListBucketVersions` or
`s3:ListMultipartUploads` are not explicitly denied, the listing protection is
incomplete. Report as a finding.

### Multipart Upload Information Disclosure

Incomplete multipart uploads are invisible in the AWS console but remain
accessible via API. They:

- Consume storage indefinitely (cost impact)
- Expose the uploader's principal ARN in the XML response (`<Owner>` element)
- Can reveal sensitive file names and upload patterns

```bash
# Enumerate incomplete uploads:
aws s3api list-multipart-uploads --bucket {{bucket}}

# Mitigation: lifecycle rule to auto-abort incomplete uploads
# (already in Best Practices → Cost Optimization section above)
```

### Account Enumeration via fetch-owner

The `fetch-owner` parameter on listing requests returns canonical user IDs
(64-char hex strings) for each object owner. These can be used to enumerate
AWS account IDs:

```bash
# Returns canonical user IDs in response:
curl "https://{{bucket}}.s3.amazonaws.com?fetch-owner=true"
```

The `x-amz-expected-bucket-owner` header enables direct account ID testing —
correct IDs proceed normally, incorrect ones return access denied. This turns
any accessible bucket into an account ID oracle.

### Uploader-Controlled Object Properties

When a policy allows `s3:PutObject`, the uploader controls more than just the
object data. They can set:

| Property | Risk | Mitigation |
|:---------|:-----|:-----------|
| **Storage Class** | Uploader can select expensive tiers (Glacier Deep Archive → costly retrieval); bucket owner pays | Condition key: `s3:x-amz-storage-class` |
| **Tags** | Tag-based automation can be spoofed; ABAC policies may grant unintended access | Condition key: `s3:RequestObjectTagKeys` |
| **Object Lock** | Compliance mode lets uploader set retention dates — objects become undeletable | Restrict `s3:PutObjectRetention` |
| **Website Redirect** | `x-amz-website-redirect-location` header enables open redirect attacks on static-hosted buckets | Deny `s3:PutObject` with redirect header |

```json
// Example: restrict storage class to STANDARD only
{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:PutObject",
    "Resource": "arn:aws:s3:::{{bucket}}/*",
    "Condition": {
        "StringNotEquals": {
            "s3:x-amz-storage-class": "STANDARD"
        }
    }
}
```

**Audit check:** If a bucket allows `s3:PutObject` from external principals,
check whether storage class, tags, object lock, and redirect headers are
restricted via conditions.

### Block Public Access Enforcement Hierarchy

**MANDATORY — evaluate this hierarchy before reporting any S3 public access finding.**

S3 has a layered access control model. A permissive bucket policy does NOT mean the
bucket is actually publicly accessible. The Block Public Access settings act as
**hard overrides** at the API enforcement layer, evaluated AFTER the policy:

```
Evaluation order (request from anonymous principal):
  1. Account-level Block Public Access  → if RestrictPublicBuckets=true → DENY
  2. Bucket-level Block Public Access   → if RestrictPublicBuckets=true → DENY
  3. Bucket policy                      → evaluated only if no override blocked it
```

**Key settings and what they actually do:**

| Setting | Effect |
|:--------|:-------|
| `BlockPublicAcls` | Rejects PUT requests that include a public ACL |
| `IgnorePublicAcls` | Ignores existing public ACLs when evaluating access |
| `BlockPublicPolicy` | Rejects PUT bucket policy calls if the policy is public |
| `RestrictPublicBuckets` | **Overrides public policies at access time** — anonymous/cross-account access is denied even if the policy allows it |

**The critical insight:** `RestrictPublicBuckets = true` makes a `Principal: "*"` policy
**inert for anonymous access**. The policy text still says public, `get-bucket-policy-status`
still returns `IsPublic: true`, but S3 **blocks the access at evaluation time**.

**Common Terraform pattern:** `BlockPublicPolicy = false` (so Terraform can apply the policy)
+ `RestrictPublicBuckets = true` (so the policy is neutralized at runtime). This is a
deliberate, secure configuration — NOT a finding.

**Audit check:**
```bash
# ALWAYS run this before concluding a bucket is publicly accessible:
aws s3api get-public-access-block --bucket {{bucket}} --output json

# If RestrictPublicBuckets = true:
#   → Principal:"*" policy is MITIGATED — do NOT report as public access finding
#   → Report BlockPublicPolicy=false as INFORMATIONAL only if relevant
#
# If RestrictPublicBuckets = false AND policy has Principal:"*":
#   → Bucket IS actually publicly accessible — report as finding
```

### Public Access Block Blind Spots

The four Public Access Block settings do NOT catch all public exposure:

| Exposure Method | Detected by Public Access Block? |
|:----------------|:--------------------------------|
| Bucket policy with `Principal: "*"` | Yes (when `BlockPublicPolicy` is true) |
| ACL grants to `AllUsers` / `AuthenticatedUsers` | Yes (when `BlockPublicAcls` is true) |
| CloudFront distribution serving bucket content | **No** — `get-bucket-policy-status` returns `IsPublic: false` |
| Cognito Identity Pool granting S3 access | **No** — credentials are valid AWS credentials, not "public" |
| Presigned URLs | **No** — generated by authenticated principals |

```bash
# Check for CloudFront distributions serving from this bucket:
aws cloudfront list-distributions \
  --query 'DistributionList.Items[?Origins.Items[?DomainName==`{{bucket}}.s3.amazonaws.com`]].{Id:Id,Domain:DomainName,Enabled:Enabled}' \
  --output json

# Check for Cognito identity pools with S3 access:
aws cognito-identity list-identity-pools --max-results 60 --output json
```

**Audit check:** Never rely solely on `get-bucket-policy-status` to determine
if a bucket is publicly accessible. Always check CloudFront distributions and
Cognito identity pools as additional exposure paths.

### Anonymous Metadata Operations

Even without `s3:ListBucket`, anonymous users can probe accessible buckets for
metadata via these operations:

```bash
# Bucket existence:
curl -sI "https://{{bucket}}.s3.amazonaws.com/" | head -1

# Object tags:
curl -s "https://{{bucket}}.s3.amazonaws.com/{{key}}?tagging"

# Logging config:
curl -s "https://{{bucket}}.s3.amazonaws.com/?logging"

# Encryption config:
curl -s "https://{{bucket}}.s3.amazonaws.com/?encryption"
```

**Audit check:** If any of these return data instead of AccessDenied, the bucket
is leaking configuration metadata to anonymous users.

### Case-Sensitive Key Exploitation

S3 object keys are case-sensitive but many applications treat them as
case-insensitive. This creates exploitation opportunities:

- `file.txt`, `File.txt`, and `FILE.txt` are three different objects
- Applications that check existence with one case but read with another can be bypassed
- Example: signup checks `users/john`, but password reset lowercases to `users/john` — attacker creates `users/John` to hijack

**Audit check:** If an application uses S3 keys for identity or access control
decisions, verify case-handling is consistent across all code paths.

### Audit Checklist

When S3 buckets are in scope, check all of the following:

1. **Block Public Access enforcement hierarchy (MANDATORY FIRST STEP)** — run `get-public-access-block` and evaluate `RestrictPublicBuckets` BEFORE concluding any bucket is public. If `RestrictPublicBuckets = true`, a `Principal: "*"` policy is mitigated. See "Block Public Access Enforcement Hierarchy" above.
2. Bucket policy — flag `Principal: "*"` with anything beyond `s3:GetObject`, BUT only report as public access if `RestrictPublicBuckets = false`
3. Public Access Block — verify all four settings are `true`. If `BlockPublicPolicy = false` but `RestrictPublicBuckets = true`, this is a common Terraform pattern (not a finding for public access, but note the configuration)
4. CloudFront distributions — check if bucket is served publicly via CDN
5. Cognito identity pools — check for guest/self-signup access to bucket
6. ListBucketVersions / ListMultipartUploads — verify these are denied if ListBucket is denied
7. Incomplete multipart uploads — check for orphaned uploads leaking ARNs and consuming storage
8. PutObject conditions — verify storage class, tags, object lock, redirects are restricted
9. Anonymous metadata probes — test `?tagging`, `?logging`, `?encryption` endpoints

---

## References

- [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [S3 API Reference](https://docs.aws.amazon.com/AmazonS3/latest/API/)
- [S3 CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [boto3 S3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [S3 Security Edge Cases (Plerion)](https://www.plerion.com/blog/things-you-wish-you-didnt-need-to-know-about-s3)
