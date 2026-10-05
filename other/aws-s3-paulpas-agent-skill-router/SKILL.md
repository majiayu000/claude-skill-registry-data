---




name: aws-s3
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Configures S3 object storage with versioning, lifecycle policies, encryption"
  and access controls for durable, scalable data storage with cost optimization in
  AWS.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-cloudformation, aws-cloudfront, aws-iam, aws-kms
  role: reference
  scope: infrastructure
  triggers: s3, object storage, bucket, versioning, lifecycle policy, s3 access, static
    website, object expiration
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




# S3 (Simple Storage Service)

Configure durable, scalable object storage with versioning, lifecycle management, and encryption. S3 provides unlimited, cost-effective storage for any data type with sophisticated access controls.

## TL;DR Checklist

- [ ] Enable versioning for data protection and rollback
- [ ] Configure lifecycle policies to transition old objects to cheaper storage classes
- [ ] Enable encryption at rest (SSE-S3, SSE-KMS, or client-side)
- [ ] Implement bucket policies with principle of least privilege
- [ ] Enable block public access for all buckets by default
- [ ] Enable MFA delete for critical buckets
- [ ] Configure access logging to CloudWatch or another bucket
- [ ] Use S3 Object Lock for compliance requirements
- [ ] Enable CloudTrail logging for API audit trail
- [ ] Configure intelligent tiering for automatic cost optimization

---

## When to Use

Use S3 when:

- Storing large files or unstructured data (images, videos, documents, backups)
- Requiring highly durable, geographically distributed storage (11 9's of durability)
- Hosting static websites or serving content via CloudFront
- Storing application backups, database snapshots, or disaster recovery data
- Building data lakes or data warehouses
- Needing versioning and point-in-time recovery
- Sharing objects with fine-grained access control

---

## When NOT to Use

Avoid S3 when:

- Requiring microsecond latency (use ElastiCache or DynamoDB instead)
- Building highly structured relational databases (use RDS instead)
- Needing file system semantics with POSIX permissions (use EFS instead)
- Working with streaming data requiring low latency (use Kinesis instead)

---

## Purpose and Use Cases

**Primary Purpose:** Provide infinitely scalable, durable object storage with automatic data protection, lifecycle management, and sophisticated access controls.

**Common Use Cases:**

1. **Backup and Disaster Recovery** — Store database backups, EC2 snapshots, and recovery data
2. **Data Lake** — Centralized repository for structured and unstructured data
3. **Static Website Hosting** — Host HTML, CSS, JavaScript with CloudFront integration
4. **Log Storage** — Aggregate application, security, and access logs
5. **Content Distribution** — Source for CloudFront CDN
6. **Data Archival** — Long-term storage with Glacier for compliance
7. **Application Data** — User uploads, generated reports, processed outputs

---

## Architecture Design Patterns

### Pattern 1: Versioned Bucket with Lifecycle Management

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket-unique-name
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          # Transition to Intelligent-Tiering after 30 days
          - Id: TransitionToIntelligentTiering
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: INTELLIGENT_TIERING
          # Transition to Glacier after 90 days
          - Id: TransitionToGlacier
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER
          # Expire (delete) after 365 days
          - Id: ExpireOldVersions
            Status: Enabled
            ExpirationInDays: 365
            NoncurrentVersionExpirationInDays: 90
          # Delete incomplete multipart uploads after 7 days
          - Id: CleanupIncompleteUploads
            Status: Enabled
            AbortIncompleteMultipartUpload:
              DaysAfterInitiation: 7
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
            BucketKeyEnabled: true
      LoggingConfiguration:
        DestinationBucketName: !Ref LogBucket
        LogFilePrefix: data-bucket-logs/
      Tags:
        - Key: Environment
          Value: production
        - Key: DataClassification
          Value: sensitive

  LogBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-data-bucket-logs-unique-name
      AccessControl: LogDeliveryWrite
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  DataBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref DataBucket
      PolicyText:
        Version: '2012-10-17'
        Statement:
          # Deny unencrypted uploads
          - Sid: DenyUnencryptedObjectUploads
            Effect: Deny
            Principal: '*'
            Action: s3:PutObject
            Resource: !Sub '${DataBucket.Arn}/*'
            Condition:
              StringNotEquals:
                s3:x-amz-server-side-encryption: AES256
          # Deny insecure transport
          - Sid: DenyInsecureTransport
            Effect: Deny
            Principal: '*'
            Action: s3:*
            Resource:
              - !GetAtt DataBucket.Arn
              - !Sub '${DataBucket.Arn}/*'
            Condition:
              Bool:
                aws:SecureTransport: 'false'
          # Allow specific IAM role to access
          - Sid: AllowApplicationAccess
            Effect: Allow
            Principal:
              AWS: arn:aws:iam::123456789012:role/ApplicationRole
            Action:
              - s3:GetObject
              - s3:PutObject
              - s3:DeleteObject
            Resource: !Sub '${DataBucket.Arn}/*'

  BucketNotification:
    Type: AWS::S3::Bucket
    Properties:
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: arn:aws:lambda:us-east-1:123456789012:function/ProcessS3Upload
            Filter:
              Key:
                FilterRules:
                  - Name: prefix
                    Value: uploads/
                  - Name: suffix
                    Value: .jpg
```

**Key Elements:**
- Versioning enabled for data protection
- Lifecycle rules transition objects through storage classes
- Intelligent-Tiering automatically optimizes costs
- Glacier for long-term retention
- Complete public access blocking
- Server-side encryption with bucket keys
- Access logging to separate bucket
- Bucket policy enforces encrypted transport and uploads
- Event notifications trigger Lambda processing

### Pattern 2: Static Website Hosting with CloudFront

```yaml
Resources:
  WebsiteBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-website-bucket-unique-name
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: 404.html
      PublicAccessBlockConfiguration:
        BlockPublicAcls: false
        BlockPublicPolicy: false
        IgnorePublicAcls: false
        RestrictPublicBuckets: false

  WebsiteBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref WebsiteBucket
      PolicyText:
        Version: '2012-10-17'
        Statement:
          - Sid: PublicReadGetObject
            Effect: Allow
            Principal: '*'
            Action: s3:GetObject
            Resource: !Sub '${WebsiteBucket.Arn}/*'

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        DefaultRootObject: index.html
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt WebsiteBucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub 'origin-access-identity/cloudfront/${CloudFrontOAI}'
        DefaultCacheBehavior:
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          Compress: true
          DefaultTTL: 86400
          MaxTTL: 31536000
        HttpVersion: http2and3

  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: OAI for S3 website bucket
```

**Key Elements:**
- S3 bucket configured as static website
- CloudFront Origin Access Identity restricts direct bucket access
- Only CloudFront can read objects (OAI-based access)
- HTTP/2 and HTTP/3 support for performance
- Compression enabled for text content
- Long TTL for static assets

### Pattern 3: Multi-Region Replication with Compliance Lock

```yaml
Resources:
  PrimaryBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-primary-bucket-unique-name
      VersioningConfiguration:
        Status: Enabled
      ReplicationConfiguration:
        Role: !GetAtt ReplicationRole.Arn
        Rules:
          - Id: ReplicateAll
            Status: Enabled
            Priority: 1
            DeleteMarkerReplication:
              Status: Enabled
            Filter:
              Prefix: ''
            Destination:
              Bucket: !GetAtt ReplicaBucket.Arn
              ReplicationTime:
                Status: Enabled
                Time:
                  Minutes: 15
              Metrics:
                Status: Enabled
                EventThreshold:
                  Minutes: 15
              StorageClass: STANDARD_IA

  ReplicaBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-replica-bucket-unique-name
      VersioningConfiguration:
        Status: Enabled
      ObjectLockEnabled: true
      ObjectLockConfiguration:
        ObjectLockEnabled: Enabled
        Rule:
          DefaultRetention:
            Mode: GOVERNANCE
            Years: 7

  ReplicationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: S3Replication
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetReplicationConfiguration
                  - s3:ListBucket
                Resource: !GetAtt PrimaryBucket.Arn
              - Effect: Allow
                Action:
                  - s3:GetObjectVersionForReplication
                  - s3:GetObjectVersionAcl
                Resource: !Sub '${PrimaryBucket.Arn}/*'
              - Effect: Allow
                Action:
                  - s3:ReplicateObject
                  - s3:ReplicateDelete
                Resource: !Sub '${ReplicaBucket.Arn}/*'
```

**Key Elements:**
- Multi-region replication with RTC (Replication Time Control)
- Object Lock for compliance (immutable backups)
- GOVERNANCE mode allows authorized users to modify lock
- Metrics track replication status
- Replica bucket in different region for disaster recovery

---

## Integration Approaches

### 1. Integration with CloudFront

S3 + CloudFront provides:
- Global content distribution with edge caching
- Reduced S3 API costs (CloudFront caches responses)
- DDoS protection via CloudFront
- Origin Access Identity for secure bucket access

### 2. Integration with Lambda

S3 events trigger Lambda functions for:
- Image resizing and transformation
- Document processing (PDF conversion, OCR)
- Log analysis and alerts
- Data transformation pipelines

### 3. Integration with Athena and Glue

Query S3 data directly via SQL:
- Athena for ad-hoc SQL queries on CSV, JSON, Parquet
- Glue Crawler to auto-discover schema
- No data movement required (query in-place)

### 4. Integration with CloudTrail

Enable CloudTrail for S3 API auditing:
- Track all API calls (GetObject, PutObject, DeleteObject)
- Compliance and forensics investigations
- Unauthorized access detection

### 5. Integration with IAM and KMS

Fine-grained access control:
- IAM policies for user/role permissions
- Bucket policies for public/cross-account access
- KMS encryption with customer-managed keys
- Resource-based policies for least privilege

---

## Common Pitfalls

### ❌ Pitfall 1: Buckets Not Versioned

**Problem:** Accidental deletions or overwrites are permanent; no rollback possible.

**Solution:**
- Enable versioning on all production buckets
- Combine with lifecycle rules to manage version storage costs
- Use Object Lock for compliance requirements

### ❌ Pitfall 2: No Lifecycle Management

**Problem:** All data stored in S3 Standard costs $0.023/GB/month; old data accumulates.

**Solution:**
- Transition to Intelligent-Tiering after 30 days (automatic optimization)
- Move to Glacier/Deep Archive after 90 days for long-term retention
- Set expiration policies for temporary data
- Regular cost analysis via S3 Storage Lens

### ❌ Pitfall 3: Public Buckets Exposing Sensitive Data

**Problem:** Bucket misconfiguration exposes credentials, keys, or PII.

**Solution:**
- Enable block public access on all buckets by default
- Use bucket policies to restrict access
- Never use public ACLs
- Regular security audits via S3 Block Public Access

### ❌ Pitfall 4: No Encryption

**Problem:** Data at rest is unencrypted; fails compliance requirements.

**Solution:**
- Enable default encryption (SSE-S3 or SSE-KMS)
- Use bucket policies to deny unencrypted uploads
- Use customer-managed KMS keys for sensitive data
- Enable encryption for snapshots and replicas

### ❌ Pitfall 5: Not Monitoring Access

**Problem:** Unauthorized access goes undetected; compliance violations.

**Solution:**
- Enable access logging to CloudWatch
- Configure S3 Storage Lens for analytics
- Enable CloudTrail for API audit trail
- Set up CloudWatch alarms for suspicious patterns

### ❌ Pitfall 6: Missing Multi-Region Replication

**Problem:** Regional outage loses all data; no disaster recovery.

**Solution:**
- Enable S3 replication to secondary region for critical data
- Use Object Lock in replica bucket for immutability
- Test failover procedures regularly

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Durability** | Enable versioning; replicate to secondary region |
| **Cost** | Use Intelligent-Tiering; expire old versions |
| **Security** | Block public access; enforce encrypted transport; use KMS |
| **Compliance** | Enable CloudTrail; use Object Lock; implement retention policies |
| **Performance** | Use CloudFront for distribution; S3 Transfer Acceleration for large uploads |
| **Monitoring** | Enable access logging; configure CloudWatch alarms |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-cloudfront` | Distribute S3 content globally |
| `cncf-aws-kms` | Encrypt S3 objects with customer-managed keys |
| `cncf-aws-iam` | Control S3 bucket and object access |
| `cncf-aws-cloudformation` | Infrastructure as code for S3 resources |
| `cncf-aws-cloudwatch` | Monitor S3 access and performance |
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
