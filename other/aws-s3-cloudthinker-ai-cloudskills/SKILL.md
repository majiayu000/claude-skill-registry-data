---
name: aws-s3
description: |
  Use when working with Aws S3 — aWS S3 bucket analysis, storage class
  distribution, lifecycle policies, access patterns, and cost optimization.
  Covers bucket inventory, object metrics, versioning status, encryption audit,
  public access analysis, and intelligent tiering evaluation.
connection_type: aws
preload: false
---

# AWS S3 Skill

Analyze AWS S3 buckets with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-s3/` → S3-specific analysis (buckets, storage classes, lifecycle, access)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for bucket in $buckets; do
  get_bucket_info "$bucket" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List all buckets
list_buckets() {
  aws s3api list-buckets --output text --query 'Buckets[].[Name,CreationDate]'
}

# Get bucket region
get_bucket_region() {
  local bucket=$1
  aws s3api get-bucket-location --bucket "$bucket" \
    --output text --query 'LocationConstraint' 2>/dev/null || echo "us-east-1"
}

# Get bucket size from CloudWatch (S3 metrics have 1-day delay)
get_bucket_size() {
  local bucket=$1
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "3 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-3d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 --metric-name BucketSizeBytes \
    --dimensions Name=BucketName,Value="$bucket" Name=StorageType,Value=StandardStorage \
    --start-time "$start_time" --end-time "$end_time" \
    --period 86400 --statistics Average \
    --output text --query 'Datapoints[-1].[Average]'
}

# Get bucket object count from CloudWatch
get_object_count() {
  local bucket=$1
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "3 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-3d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/S3 --metric-name NumberOfObjects \
    --dimensions Name=BucketName,Value="$bucket" Name=StorageType,Value=AllStorageTypes \
    --start-time "$start_time" --end-time "$end_time" \
    --period 86400 --statistics Average \
    --output text --query 'Datapoints[-1].[Average]'
}

# Get bucket encryption status
get_encryption() {
  local bucket=$1
  aws s3api get-bucket-encryption --bucket "$bucket" \
    --output text \
    --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.[SSEAlgorithm,KMSMasterKeyID]' 2>/dev/null || echo "NONE"
}

# Get public access block
get_public_access() {
  local bucket=$1
  aws s3api get-public-access-block --bucket "$bucket" \
    --output text \
    --query 'PublicAccessBlockConfiguration.[BlockPublicAcls,IgnorePublicAcls,BlockPublicPolicy,RestrictPublicBuckets]' 2>/dev/null || echo "NOT_SET"
}
```

## Common Operations

### 1. Bucket Inventory with Security Posture

```bash
#!/bin/bash
export AWS_PAGER=""
BUCKETS=$(aws s3api list-buckets --output text --query 'Buckets[].Name')
for bucket in $BUCKETS; do
  {
    enc=$(aws s3api get-bucket-encryption --bucket "$bucket" \
      --output text --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' 2>/dev/null || echo "NONE")
    pub=$(aws s3api get-public-access-block --bucket "$bucket" \
      --output text --query 'PublicAccessBlockConfiguration.BlockPublicAcls' 2>/dev/null || echo "NOT_SET")
    ver=$(aws s3api get-bucket-versioning --bucket "$bucket" \
      --output text --query 'Status' 2>/dev/null || echo "Disabled")
    printf "%s\tEnc:%s\tPubBlock:%s\tVersioning:%s\n" "$bucket" "$enc" "$pub" "${ver:-Disabled}"
  } &
done
wait
```

### 2. Storage Class Distribution (sampled)

```bash
#!/bin/bash
export AWS_PAGER=""
BUCKET=$1
aws s3api list-objects-v2 --bucket "$BUCKET" --max-items 1000 \
  --output text --query 'Contents[].[StorageClass]' \
  | sort | uniq -c | sort -rn
```

### 3. Lifecycle Policy Review

```bash
#!/bin/bash
export AWS_PAGER=""
BUCKETS=$(aws s3api list-buckets --output text --query 'Buckets[].Name')
for bucket in $BUCKETS; do
  {
    rules=$(aws s3api get-bucket-lifecycle-configuration --bucket "$bucket" \
      --output text \
      --query 'Rules[].[ID,Status,Transitions[0].Days,Transitions[0].StorageClass,Expiration.Days]' 2>/dev/null || echo "NO_LIFECYCLE")
    printf "%s\t%s\n" "$bucket" "$rules"
  } &
done
wait
```

### 4. Access Logging and Metrics Status

```bash
#!/bin/bash
export AWS_PAGER=""
BUCKETS=$(aws s3api list-buckets --output text --query 'Buckets[].Name')
for bucket in $BUCKETS; do
  {
    logging=$(aws s3api get-bucket-logging --bucket "$bucket" \
      --output text --query 'LoggingEnabled.TargetBucket' 2>/dev/null || echo "DISABLED")
    printf "%s\tLogging:%s\n" "$bucket" "${logging:-DISABLED}"
  } &
done
wait
```

### 5. Large Object Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
BUCKET=$1
aws s3api list-objects-v2 --bucket "$BUCKET" --max-items 5000 \
  --output text --query 'Contents[?Size>`1073741824`].[Key,Size,StorageClass,LastModified]' \
  | sort -k2 -rn | head -20
```

## Anti-Hallucination Rules

1. **S3 metrics have 1-day delay** - BucketSizeBytes and NumberOfObjects are reported daily. Do not expect real-time data.
2. **No server-side filtering for list-objects** - S3 does not support filtering by storage class or size at the API level. Use `--prefix` for key filtering, then post-process.
3. **LocationConstraint null = us-east-1** - `get-bucket-location` returns null/None for us-east-1 buckets. Handle this case explicitly.
4. **Storage class defaults to STANDARD** - Objects without an explicit StorageClass are STANDARD. The API may return null for these.
5. **Versioning cannot be disabled** - Once enabled, versioning can only be suspended (not disabled). Suspended buckets still retain existing versions.

## Output Format

Present results as a structured report:
```
Aws S3 Report
═════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **list-objects-v2 pagination**: Default max is 1000 objects per page. Use `--page-size` and `--max-items` for large buckets. Never attempt to list all objects in buckets with millions of keys.
- **Cross-region requests**: S3 API calls for bucket configuration go to the bucket's region. Use `--region` if the bucket is in a different region than your default.
- **Requester pays**: Some buckets have requester-pays enabled. Calls may fail without `--request-payer requester`.
- **ACLs vs bucket policy vs public access block**: All three control access. Check all of them for a complete picture.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
