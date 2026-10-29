---
name: aws-s3
description: Configure S3 buckets, policies, and lifecycle rules. Implement versioning, replication, and security. Use when managing object storage on AWS. 
category: Document Processing
source: antigravity
tags: [pdf, api, ai, agent, template, document, security, aws, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-s3
---


# AWS S3

Manage Amazon S3 object storage with production-grade security, lifecycle policies, replication, and access controls.

## When to Use This Skill

- Creating S3 buckets with security hardening (encryption, public access block, versioning)
- Writing bucket policies to enforce HTTPS, restrict IP ranges, or grant cross-account access
- Setting up lifecycle rules to transition objects between storage classes
- Configuring cross-region replication for disaster recovery
- Generating presigned URLs for temporary access to private objects
- Setting up static website hosting or CloudFront origins
- Troubleshooting access denied errors or policy conflicts

## Prerequisites

- AWS CLI v2 installed and configured
- Least-privilege IAM permissions for the selected bucket/object operations; grant only the required KMS actions for SSE-KMS. Do not grant wildcard service permissions as a default.
- For replication: IAM role with replication permissions and destination bucket in target region
- For logging: a separate logging bucket with appropriate ACL

## Create and Secure a Bucket

```bash
# Create a bucket (us-east-1 does not need LocationConstraint)
aws s3api create-bucket \
  --bucket my-app-data-prod \
  --region us-east-1

# Create a bucket in another region
aws s3api create-bucket \
  --bucket my-app-data-dr \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Block ALL public access (always do this first)
aws s3api put-public-access-block \
  --bucket my-app-data-prod \
  --public-access-block-configuration '{
    "BlockPublicAcls": true,
    "IgnorePublicAcls": true,
    "BlockPublicPolicy": true,
    "RestrictPublicBuckets": true
  }'

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-app-data-prod \
  --versioning-configuration Status=Enabled

# Enable server-side encryption with SSE-KMS
aws s3api put-bucket-encryption \
  --bucket my-app-data-prod \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "alias/s3-key"
      },
      "BucketKeyEnabled": true
    }]
  }'

# Enable access logging
aws s3api put-bucket-logging \
  --bucket my-app-data-prod \
  --bucket-logging-status '{
    "LoggingEnabled": {
      "TargetBucket": "my-access-logs-bucket",
      "TargetPrefix": "s3-logs/my-app-data-prod/"
    }
  }'

# Add tags
aws s3api put-bucket-tagging \
  --bucket my-app-data-prod \
  --tagging '{
    "TagSet": [
      {"Key": "Environment", "Value": "production"},
      {"Key": "Team", "Value": "platform"},
      {"Key": "DataClassification", "Value": "confidential"}
    ]
  }'
```

## Bucket Policies

```bash
# Apply a bucket policy (enforce HTTPS and restrict to VPC endpoint)
aws s3api put-bucket-policy \
  --bucket my-app-data-prod \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "DenyInsecureTransport",
        "Effect": "Deny",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": [
          "arn:aws:s3:::my-app-data-prod",
          "arn:aws:s3:::my-app-data-prod/*"
        ],
        "Condition": {
          "Bool": {"aws:SecureTransport": "false"}
        }
      },
      {
        "Sid": "RestrictToVPCEndpoint",
        "Effect": "Deny",
        "Principal": "*",
        "Action": "s3:*",
        "Resource": [
          "arn:aws:s3:::my-app-data-prod",
          "arn:aws:s3:::my-app-data-prod/*"
        ],
        "Condition": {
          "StringNotEquals": {
            "aws:sourceVpce": "vpce-abc123"
          }
        }
      }
    ]
  }'
```

Cross-account access policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CrossAccountRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::987654321098:role/DataAnalystRole"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-data-prod",
        "arn:aws:s3:::my-app-data-prod/shared/*"
      ]
    }
  ]
}
```

## Lifecycle Rules

```bash
# Apply a comprehensive lifecycle configuration
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-app-data-prod \
  --lifecycle-configuration '{
    "Rules": [
      {
        "ID": "TierDownOldData",
        "Status": "Enabled",
        "Filter": {"Prefix": "data/"},
        "Transitions": [
          {"Days": 30, "StorageClass": "STANDARD_IA"},
          {"Days": 90, "StorageClass": "GLACIER_IR"},
          {"Days": 180, "StorageClass": "GLACIER"},
          {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
        ]
      },
      {
        "ID": "ExpireLogs",
        "Status": "Enabled",
        "Filter": {"Prefix": "logs/"},
        "Expiration": {"Days": 90},
        "Transitions": [
          {"Days": 7, "StorageClass": "STANDARD_IA"},
          {"Days": 30, "StorageClass": "GLACIER"}
        ]
      },
      {
        "ID": "CleanupOldVersions"
