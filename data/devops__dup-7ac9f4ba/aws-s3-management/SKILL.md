---
name: aws-s3-management
description: Configure S3 buckets with security, lifecycle, and replication policies
sasmp_version: "1.3.0"
bonded_agent: 03-aws-storage
bond_type: PRIMARY_BOND
---

# AWS S3 Management Skill

Manage S3 buckets with enterprise security and cost optimization.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | S3 |
| Complexity | Low-Medium |
| Est. Time | 5-15 min |
| Prerequisites | AWS account |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| bucket_name | string | Globally unique name | ^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$ |
| region | string | AWS region | Valid region code |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| versioning | bool | false | Enable versioning |
| encryption | string | AES256 | SSE-S3, SSE-KMS, or none |
| public_access_block | bool | true | Block public access |
| lifecycle_rules | array | [] | Lifecycle configurations |
| cors_rules | array | [] | CORS configuration |

## Execution Flow

```
1. Validate bucket name availability
2. Create bucket with region
3. Configure Block Public Access
4. Enable encryption
5. Set versioning (if enabled)
6. Apply lifecycle rules
7. Configure logging
```

## Implementation

### Create Secure Bucket
```bash
# Create bucket
aws s3api create-bucket \
  --bucket my-secure-bucket \
  --region us-east-1

# Block public access
aws s3api put-public-access-block \
  --bucket my-secure-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-secure-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-secure-bucket \
  --versioning-configuration Status=Enabled
```

### Lifecycle Rule Example
```json
{
  "Rules": [
    {
      "ID": "MoveToGlacier",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }
  ]
}
```

## Retry Logic

```python
def s3_operation_with_retry(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation()
        except s3.exceptions.SlowDown:
            wait = 2 ** attempt
            time.sleep(wait)
        except s3.exceptions.ServiceUnavailable:
            time.sleep(2 ** attempt)
    raise Exception("Max retries exceeded")
```

## Observability

### CloudWatch Metrics
- `BucketSizeBytes` - Total bucket size
- `NumberOfObjects` - Object count
- `AllRequests` - Request count
- `4xxErrors` / `5xxErrors` - Error rates

### Access Logs
```
bucket_owner bucket [time] remote_ip requester request_id operation key
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| BucketAlreadyExists | Name taken globally | Choose unique name |
| AccessDenied | IAM or bucket policy | Check both policies |
| SlowDown | Request rate exceeded | Add random prefix to keys |
| NoSuchBucket | Bucket deleted | Verify bucket exists |

### Debug Checklist
- [ ] Bucket name globally unique?
- [ ] Block Public Access enabled?
- [ ] Bucket policy not overly permissive?
- [ ] Encryption enabled?
- [ ] Versioning enabled for critical data?
- [ ] Lifecycle rules not conflicting?

### Access Denied Resolution
```
Check order:
1. IAM user/role policy (s3:GetObject, etc.)
2. Bucket policy (Principal, Resource)
3. Block Public Access settings
4. Object ACL (if ACLs enabled)
5. VPC Endpoint policy (if using)
```

## Cost Optimization

| Storage Class | Cost | Retrieval | Use Case |
|--------------|------|-----------|----------|
| Standard | $$$ | Instant | Frequent access |
| Intelligent-Tiering | $$ | Instant | Unknown pattern |
| Standard-IA | $ | Instant | Infrequent |
| Glacier Instant | ¢ | Milliseconds | Archive, quick access |
| Glacier Flexible | ¢ | Minutes-hours | Archive |
| Glacier Deep Archive | ¢ | Hours | Long-term |

## Test Template

```python
def test_s3_bucket_creation():
    # Arrange
    bucket_name = f"test-bucket-{uuid.uuid4().hex[:8]}"

    # Act
    s3.create_bucket(Bucket=bucket_name)
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )

    # Assert
    response = s3.get_public_access_block(Bucket=bucket_name)
    assert response['PublicAccessBlockConfiguration']['BlockPublicAcls']

    # Cleanup
    s3.delete_bucket(Bucket=bucket_name)
```

## Assets

- `assets/s3-lifecycle.json` - Lifecycle configuration template

## References

- [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
