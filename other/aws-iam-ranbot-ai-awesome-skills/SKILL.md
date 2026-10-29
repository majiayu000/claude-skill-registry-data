---
name: aws-iam
description: Manage IAM users, roles, and policies. Implement least-privilege access and security best practices. Use when configuring AWS identity and access management. 
category: Document Processing
source: antigravity
tags: [api, ai, agent, workflow, template, design, document, security, aws, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/aws-iam
---


# AWS IAM

Manage identity and access in AWS with least-privilege policies, roles, federation, and permission boundaries.

## When to Use This Skill

- Creating roles for EC2 instances, Lambda functions, or ECS tasks
- Writing custom IAM policies with least-privilege access
- Setting up OIDC federation for GitHub Actions or other CI/CD systems
- Implementing permission boundaries for delegated administration
- Auditing access with IAM Access Analyzer and credential reports
- Configuring cross-account access with assume-role patterns
- Enforcing MFA and session policies

## Prerequisites

- AWS CLI v2 installed and configured
- Least-privilege IAM actions for the chosen roles/policies; iam:* is not a prerequisite
- For OIDC: ability to create identity providers (`iam:CreateOpenIDConnectProvider`)
- AWS Organizations access for Service Control Policies (SCPs)

## IAM Policy Structure

Every IAM policy follows the same JSON structure. Always specify the minimum actions and resources required.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadWrite",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    },
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-app-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }
  ]
}
```

## Create and Manage Roles

```bash
# Create an EC2 instance role with trust policy
aws iam create-role \
  --role-name EC2AppRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }' \
  --tags '[{"Key":"Team","Value":"platform"},{"Key":"Environment","Value":"production"}]'

# Create and attach an inline policy
aws iam put-role-policy \
  --role-name EC2AppRole \
  --policy-name s3-access \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    }]
  }'

# Attach a managed policy
aws iam attach-role-policy \
  --role-name EC2AppRole \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

# Create instance profile and associate the role
aws iam create-instance-profile --instance-profile-name EC2AppProfile
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2AppProfile \
  --role-name EC2AppRole

# Create a Lambda execution role
aws iam create-role \
  --role-name LambdaExecRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name LambdaExecRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

## Cross-Account Access

```bash
# In Account B: create role that Account A can assume
aws iam create-role \
  --role-name CrossAccountReadRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::111111111111:root"},
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {"sts:ExternalId": "unique-external-id-12345"}
      }
    }]
  }'

# In Account A: assume the role
aws sts assume-role \
  --role-arn arn:aws:iam::222222222222:role/CrossAccountReadRole \
  --role-session-name cross-account-session \
  --external-id unique-external-id-12345

# Use the temporary credentials
export AWS_ACCESS_KEY_ID="ASIAXXX"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_SESSION_TOKEN="xxx"
```

## OIDC Federation for GitHub Actions

```bash
# Create the GitHub OIDC identity provider
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list "6938fd4d98bab03faadb97b34396831e3780aea1"

# Create a role for GitHub Actions with repo-scoped trust
aws iam create-role \
  --role-name GitHubActionsDeployRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:ref:refs/heads/main"
        }
      }
    }]
  }'

# Attac
