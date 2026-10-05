---




name: aws-ecr
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Manages container image repositories with ECR for secure storage, scanning"
  replication, and integration with EKS, ECS, and Lambda for container deployments.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-eks, aws-iam, aws-kms, cubefs
  role: reference
  scope: infrastructure
  triggers: container registry, container security, containers, docker images, ecr,
    image repository, image scanning, vulnerability scanning
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




# ECR (Elastic Container Registry)

Manage container images securely with vulnerability scanning, lifecycle policies, replication, and integration with container orchestration services.

## TL;DR Checklist

- [ ] Enable image scanning for vulnerability detection
- [ ] Configure lifecycle policies to manage image versions
- [ ] Use image tags for versioning (not latest)
- [ ] Enable cross-region replication for disaster recovery
- [ ] Implement pull-through cache for upstream registries
- [ ] Encrypt images at rest with KMS
- [ ] Use repository policies to control access
- [ ] Monitor image push/pull with CloudTrail
- [ ] Set up resource cleanup for untagged images
- [ ] Implement image signing for integrity verification

---

## When to Use

Use ECR when:

- Running container workloads on AWS (ECS, EKS, Lambda)
- Needing private container registry
- Requiring vulnerability scanning
- Building CI/CD pipelines with containers
- Needing image lifecycle management

---

## When NOT to Use

Avoid ECR for:

- Public open-source images (Docker Hub is fine)
- Non-AWS container deployments (use Docker Hub, Quay)

---

## Purpose and Use Cases

**Primary Purpose:** Provide secure, managed container image registry with vulnerability scanning, lifecycle management, and AWS service integration.

**Common Use Cases:**

1. **Container Storage** — Store application images for ECS/EKS
2. **CI/CD Pipelines** — Build and push images automatically
3. **Vulnerability Scanning** — Automatic security assessment
4. **Image Replication** — Multi-region disaster recovery
5. **Access Control** — Fine-grained permission management

---

## Architecture Design Patterns

### Pattern 1: Secure ECR Repository with Scanning

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # ECR Repository
  ApplicationRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: application-images
      EncryptionConfiguration:
        EncryptionType: KMS
        KmsKey: !GetAtt RepositoryEncryptionKey.Arn
      ImageScanningConfiguration:
        ScanOnPush: true
      LifecyclePolicy:
        LifecyclePolicyText: |
          {
            "rules": [
              {
                "rulePriority": 1,
                "description": "Keep last 10 images tagged, expire untagged",
                "selection": {
                  "tagStatus": "tagged",
                  "tagPrefixList": ["v"],
                  "countType": "imageCountMoreThan",
                  "countNumber": 10
                },
                "action": {
                  "type": "expire"
                }
              },
              {
                "rulePriority": 2,
                "description": "Expire untagged images after 7 days",
                "selection": {
                  "tagStatus": "untagged",
                  "countType": "sinceImagePushed",
                  "countUnit": "days",
                  "countNumber": 7
                },
                "action": {
                  "type": "expire"
                }
              }
            ]
          }
      RepositoryPolicyText:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowECSTaskPull
            Effect: Allow
            Principal:
              AWS: arn:aws:iam::123456789012:role/ecsTaskRole
            Action:
              - ecr:GetAuthorizationToken
              - ecr:GetDownloadUrlForLayer
              - ecr:BatchGetImage
              - ecr:BatchCheckLayerAvailability
          - Sid: AllowEKSNodesPull
            Effect: Allow
            Principal:
              AWS: arn:aws:iam::123456789012:role/nodeGroupRole
            Action:
              - ecr:GetAuthorizationToken
              - ecr:GetDownloadUrlForLayer
              - ecr:BatchGetImage
              - ecr:BatchCheckLayerAvailability
          - Sid: DenyUnencryptedTransport
            Effect: Deny
            Principal: '*'
            Action: 'ecr:*'
            Condition:
              Bool:
                aws:SecureTransport: 'false'
      Tags:
        - Key: Application
          Value: main

  # KMS Key for Image Encryption
  RepositoryEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for ECR repository encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow ECR to use key
            Effect: Allow
            Principal:
              Service: ecr.amazonaws.com
            Action:
              - 'kms:Decrypt'
              - 'kms:GenerateDataKey'
            Resource: '*'

  # ECR Lifecycle Policy for Cleanup
  ImageCleanupFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: ecr-image-cleanup
      Runtime: python3.11
      Handler: index.handler
      Role: !GetAtt CleanupRole.Arn
      Code:
        ZipFile: |
          import boto3
          import json
          from datetime import datetime, timedelta
          
          ecr = boto3.client('ecr')
          
          def handler(event, context):
              repo_name = 'application-images'
              max_age_days = 30
              
              # List images
              response = ecr.list_images(repositoryName=repo_name)
              
              to_delete = []
              for image in response.get('imageIds', []):
                  if 'imageTag' not in image:  # Untagged
                      image_detail = ecr.describe_images(
                          repositoryName=repo_name,
                          imageIds=[image]
                      )
                      push_time = image_detail['imageDetails'][0]['imagePushedAt']
                      age = datetime.now(push_time.tzinfo) - push_time
                      
                      if age > timedelta(days=max_age_days):
                          to_delete.append(image)
              
              if to_delete:
                  ecr.batch_delete_image(
                      repositoryName=repo_name,
                      imageIds=to_delete
                  )
              
              return {
                  'statusCode': 200,
                  'deleted': len(to_delete)
              }

  CleanupRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: ECRAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ecr:ListImages
                  - ecr:DescribeImages
                  - ecr:BatchDeleteImage
                Resource: !GetAtt ApplicationRepository.RepositoryUri

  # CloudWatch Alarms
  ScanFailuresAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: ecr-scan-failures
      MetricName: ImageScanFailures
      Namespace: AWS/ECR
      Statistic: Sum
      Period: 3600
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: RepositoryName
          Value: !Ref ApplicationRepository

Outputs:
  RepositoryUri:
    Value: !GetAtt ApplicationRepository.RepositoryUri
    Description: ECR repository URI
  RepositoryName:
    Value: !Ref ApplicationRepository
    Description: ECR repository name
```

**Key Elements:**
- ECR repository with KMS encryption
- Image scanning enabled on push
- Lifecycle policy for version management
- Repository policy for fine-grained access
- Lambda for automated cleanup
- CloudWatch alarms for scan failures

### Pattern 2: Cross-Region Replication

```yaml
Resources:
  # Replication Configuration
  RegistryReplicationConfig:
    Type: AWS::ECR::RegistryReplicationConfig
    Properties:
      Rules:
        - Destinations:
            - Region: eu-west-1
              RegistryId: !Ref 'AWS::AccountId'
            - Region: ap-southeast-1
              RegistryId: !Ref 'AWS::AccountId'
          RepositoryFilters:
            - Filter: PREFIX_LIST
              FilterValue:
                - prod
          Destinations:
            - Region: eu-west-1
              RegistryId: !Ref 'AWS::AccountId'
            - Region: ap-southeast-1
              RegistryId: !Ref 'AWS::AccountId'
```

**Key Elements:**
- Automatic replication to secondary regions
- Disaster recovery for container images
- All regions stay in sync

---

## Integration Approaches

### 1. Integration with ECS

ECR + ECS enables:
- Task definitions pull images from ECR
- No credentials needed (IAM roles)
- Automatic image updates

### 2. Integration with EKS

ECR + EKS enables:
- Pods pull images from ECR
- IRSA for access without credentials
- Multi-region replication for HA

### 3. Integration with CodePipeline

CodePipeline + ECR enables:
- CI/CD automated image builds
- Image scanning in pipeline
- Deployment to production

### 4. Integration with Lambda

Lambda + ECR enables:
- Container images for Lambda functions
- Vulnerability scanning
- Secure image storage

---

## Common Pitfalls

### ❌ Pitfall 1: No Image Tagging Strategy

**Problem:** Cannot track versions; hard to rollback.

**Solution:**
- Tag with semantic versioning (v1.0.0)
- Tag with commit SHA for traceability
- Never use 'latest' in production

### ❌ Pitfall 2: Unbounded Image Growth

**Problem:** Repository grows indefinitely; storage costs.

**Solution:**
- Implement lifecycle policies
- Expire untagged images (7-30 days)
- Limit tagged image count (keep last N)

### ❌ Pitfall 3: No Vulnerability Scanning

**Problem:** Deploy vulnerable images; security breaches.

**Solution:**
- Enable image scanning on push
- Block deployment of high-severity images
- Regular scans of existing images

### ❌ Pitfall 4: No Encryption

**Problem:** Images stored unencrypted; data exposure risk.

**Solution:**
- Enable KMS encryption at rest
- Use customer-managed keys
- Enforce secure transport

### ❌ Pitfall 5: Overly Permissive Repository Policy

**Problem:** Unauthorized users can pull/push images.

**Solution:**
- Use least-privilege repository policies
- Separate policies for pull vs. push
- Audit access via CloudTrail

---

## Best Practices Summary

| Category | Best Practice |
|---|---|
| **Tagging** | Semantic versioning; commit SHA; no 'latest' |
| **Scanning** | Enable on push; block high-severity |
| **Cleanup** | Lifecycle policies; regular maintenance |
| **Security** | KMS encryption; secure transport only |
| **Replication** | Multi-region for disaster recovery |

---

## Related Skills

| Skill | Purpose |
|---|---|
| `cncf-aws-eks` | Container orchestration with images |
| `cncf-aws-iam` | Repository access control |
| `cncf-aws-kms` | Image encryption |
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

---

## Live References

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/AmazonECR/latest/userguide/images-tags.html)
- [Configuration Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html)
- [Best Practices](https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security_iam_id-based-policy-examples.html)

