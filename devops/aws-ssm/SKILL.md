---




name: aws-ssm
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Manages EC2 instances and on-premises servers with AWS Systems Manager"
  for configuration management, patch management, and secure shell access without
  SSH keys.'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  related-skills: aws-ec2, aws-iam, aws-secrets-manager
  role: reference
  scope: infrastructure
  triggers: configuration management, parameter store, patch management, session manager,
    ssm, systems manager, ansible, automation
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




# SSM (AWS Systems Manager)

Manage configuration, patches, and secure shell access for EC2 instances and on-premises servers without SSH keys or bastion hosts.

## TL;DR Checklist

- [ ] Install SSM agent on all instances (pre-installed on recent AMIs)
- [ ] Create IAM role with AmazonSSMManagedInstanceCore policy
- [ ] Use Session Manager for secure shell access (no SSH keys)
- [ ] Enable CloudTrail logging of Session Manager sessions
- [ ] Use Parameter Store for application configuration
- [ ] Enable Patch Manager for automated patching
- [ ] Implement maintenance windows for patch deployment
- [ ] Use State Manager for configuration compliance
- [ ] Monitor session and patch activity
- [ ] Configure session recording to S3 for audit

---

## When to Use

Use SSM when:

- Managing EC2 instance configuration
- Patching operating systems and applications
- Enabling secure shell access without SSH
- Storing application parameters/secrets
- Running commands across multiple instances
- Auditing compliance and configuration drift

---

## When NOT to Use

Avoid SSM for:

- Stateless container deployments (use ECS instead)
- Development-only environments (SSH acceptable)

---

## Purpose and Use Cases

**Primary Purpose:** Provide unified management and secure access to EC2 instances and on-premises servers without SSH keys or bastion hosts.

**Common Use Cases:**

1. **Secure Shell Access** — Session Manager for secure remote access
2. **Patch Management** — Automated OS and application patching
3. **Configuration Management** — Parameter Store for app config
4. **Compliance** — Track configuration state and drift
5. **Remote Commands** — Run scripts across instance fleet
6. **Inventory** — Track software and configurations

---

## Architecture Design Patterns

### Pattern 1: Secure Instance Management with Session Manager

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # IAM Role for EC2 with SSM permissions
  EC2SSMRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: ec2-ssm-role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
      Policies:
        - PolicyName: ParameterStoreAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ssm:GetParameter
                  - ssm:GetParameters
                  - ssm:GetParametersByPath
                Resource: !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/app/*'
              - Effect: Allow
                Action:
                  - kms:Decrypt
                Resource: !GetAtt ParameterEncryptionKey.Arn

  # Instance Profile
  EC2InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref EC2SSMRole

  # KMS Key for Parameter Encryption
  ParameterEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for SSM Parameter Store encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow SSM to use key
            Effect: Allow
            Principal:
              Service: ssm.amazonaws.com
            Action:
              - 'kms:Decrypt'
              - 'kms:GenerateDataKey'
            Resource: '*'

  # Session Manager Configuration Document
  SessionManagerDocument:
    Type: AWS::SSM::Document
    Properties:
      Name: SSM-SessionManagerRunShell
      DocumentType: Session
      DocumentFormat: JSON
      Content:
        schemaVersion: '1.0'
        description: SSM Session Manager configuration
        sessionType: Standard_Stream
        inputs:
          s3BucketName: !Ref SessionLoggingBucket
          s3KeyPrefix: session-logs/
          s3EncryptionEnabled: true
          cloudWatchLogGroupName: /aws/ssm/sessions
          cloudWatchEncryptionEnabled: true
          idleSessionTimeout: '20'
          maxSessionDuration: '60'
          cloudWatchStreamingEnabled: true
          kmsKeyId: !GetAtt SessionEncryptionKey.Arn

  # S3 Bucket for Session Logs
  SessionLoggingBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'ssm-session-logs-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # KMS Key for Session Encryption
  SessionEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for SSM session encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM permissions
            Effect: Allow
            Principal:
              AWS: !Ref 'AWS::AccountId'
            Action: 'kms:*'
            Resource: '*'

  # Application Parameters
  DatabaseHost:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/prod/db-host
      Type: String
      Value: prod-db.c9akciq32.us-east-1.rds.amazonaws.com
      Description: Database host

  DatabasePassword:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/prod/db-password
      Type: SecureString
      Value: !Sub '{{resolve:secretsmanager:db-password:SecretString:password}}'
      Description: Database password (encrypted)
      KmsKeyId: !Ref ParameterEncryptionKey

  ApiKey:
    Type: AWS::SSM::Parameter
    Properties:
      Name: /app/prod/api-key
      Type: SecureString
      Value: !Sub '{{resolve:secretsmanager:api-key:SecretString:api-key}}'
      Description: API key (encrypted)
      KmsKeyId: !Ref ParameterEncryptionKey

  # CloudWatch Log Group for Session Logs
  SessionLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/ssm/sessions
      RetentionInDays: 30

Outputs:
  InstanceProfileArn:
    Value: !GetAtt EC2InstanceProfile.Arn
    Description: Instance profile ARN for EC2 instances
  ParameterStorePath:
    Value: /app/prod/
    Description: Parameter Store path for application config
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

- [Primary Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-managing-instances.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [Configuration Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-get-parameter-value-api.html)
- [Best Practices](https://docs.aws.amazon.com/systems-manager/latest/userguide/install-ssm-agent.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-state-runcommands.html)

