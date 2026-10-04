---
type: skill
name: iam
description: AWS Identity and Access Management for users, roles, policies, and permissions. Use when creating IAM policies, configuring cross-account access, setting up service roles, troubleshooting permission errors, or managing access control.
last_updated: "2026-01-07"
doc_source: https://docs.aws.amazon.com/IAM/latest/UserGuide/
---

# AWS IAM

AWS Identity and Access Management (IAM) enables secure access control to AWS services and resources. IAM is foundational to AWS security—every AWS API call is authenticated and authorized through IAM.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Common Patterns](#common-patterns)
- [CLI Reference](#cli-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Service-Linked Role (SLR) Security](#service-linked-role-slr-security)
- [References](#references)

## Core Concepts

### Principals

Entities that can make requests to AWS: IAM users, roles, federated users, and applications.

### Policies

JSON documents defining permissions. Types:
- **Identity-based**: Attached to users, groups, or roles
- **Resource-based**: Attached to resources (S3 buckets, SQS queues)
- **Permission boundaries**: Maximum permissions an identity can have
- **Service control policies (SCPs)**: Organization-wide limits

### Roles

Identities with permissions that can be assumed by trusted entities. No permanent credentials—uses temporary security tokens.

### Trust Relationships

Define which principals can assume a role. Configured via the role's trust policy.

## Common Patterns

### Create a Service Role for Lambda

**AWS CLI:**

```bash
# Create the trust policy
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name MyLambdaRole \
  --assume-role-policy-document file://trust-policy.json

# Attach a managed policy
aws iam attach-role-policy \
  --role-name MyLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**boto3:**

```python
import boto3
import json

iam = boto3.client('iam')

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# Create role
iam.create_role(
    RoleName='MyLambdaRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)

# Attach managed policy
iam.attach_role_policy(
    RoleName='MyLambdaRole',
    PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
)
```

### Create Custom Policy with Least Privilege

```bash
cat > policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/MyTable"
    }
  ]
}
EOF

aws iam create-policy \
  --policy-name MyDynamoDBPolicy \
  --policy-document file://policy.json
```

### Cross-Account Role Assumption

```bash
# In Account B (trusted account), create role with trust for Account A
cat > cross-account-trust.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::111111111111:root" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": { "sts:ExternalId": "unique-external-id" }
      }
    }
  ]
}
EOF

# From Account A, assume the role
aws sts assume-role \
  --role-arn arn:aws:iam::222222222222:role/CrossAccountRole \
  --role-session-name MySession \
  --external-id unique-external-id
```

## CLI Reference

### Essential Commands

| Command | Description |
|---------|-------------|
| `aws iam create-role` | Create a new IAM role |
| `aws iam create-policy` | Create a customer managed policy |
| `aws iam attach-role-policy` | Attach a managed policy to a role |
| `aws iam put-role-policy` | Add an inline policy to a role |
| `aws iam get-role` | Get role details |
| `aws iam list-roles` | List all roles |
| `aws iam simulate-principal-policy` | Test policy permissions |
| `aws sts assume-role` | Assume a role and get temporary credentials |
| `aws sts get-caller-identity` | Get current identity |

### Useful Flags

- `--query`: Filter output with JMESPath
- `--output table`: Human-readable output
- `--no-cli-pager`: Disable pager for scripting

## Best Practices

### Security

- **Never use root account** for daily tasks
- **Enable MFA** for all human users
- **Use roles** instead of long-term access keys
- **Apply least privilege** — grant only required permissions
- **Use conditions** to restrict access by IP, time, or MFA
- **Rotate credentials** regularly
- **Use permission boundaries** for delegated administration

### Policy Design

- Start with AWS managed policies, customize as needed
- Use policy variables (`${aws:username}`) for dynamic policies
- Prefer explicit denies for sensitive actions
- Group related permissions logically

### Monitoring

- Enable **CloudTrail** for API auditing
- Use **IAM Access Analyzer** to identify overly permissive policies
- Review **credential reports** regularly
- Set up alerts for root account usage

## Troubleshooting

### Access Denied Errors

**Symptom:** `AccessDeniedException` or `UnauthorizedAccess`

**Debug steps:**
1. Verify identity: `aws sts get-caller-identity`
2. Check attached policies: `aws iam list-attached-role-policies --role-name MyRole`
3. Simulate the action:
   ```bash
   aws iam simulate-principal-policy \
     --policy-source-arn arn:aws:iam::123456789012:role/MyRole \
     --action-names dynamodb:GetItem \
     --resource-arns arn:aws:dynamodb:us-east-1:123456789012:table/MyTable
   ```
4. Check for explicit denies in SCPs or permission boundaries
5. Verify resource-based policies allow the principal

### Role Cannot Be Assumed

**Symptom:** `AccessDenied` when calling `AssumeRole`

**Causes:**
- Trust policy doesn't include the calling principal
- Missing `sts:AssumeRole` permission on the caller
- ExternalId mismatch (for cross-account roles)
- Session duration exceeds maximum

**Fix:** Review and update the role's trust relationship.

### Policy Size Limits

- Managed policy: 6,144 characters
- Inline policy: 2,048 characters (user), 10,240 characters (role/group)
- Trust policy: 2,048 characters

**Solution:** Use multiple policies, reference resources by prefix/wildcard, or use tags-based access control.

## Service-Linked Role (SLR) Security

Service-linked roles are IAM roles managed by AWS services. Their permissions are
AWS-defined and cannot be modified, but they introduce indirect privilege escalation
paths that must be audited. SLR abuse is an **indirect** attack vector — always
report it even when exploitation requires a second step.

Reference: https://www.plerion.com/blog/about-aws-service-linked-roles

### What Makes SLRs Different

- **AWS-managed permissions** — you cannot edit the SLR's policy, but you can create or delete the role
- **Implicit trust** — SLRs trust their service principal without confused deputy protections (`aws:SourceAccount`/`aws:SourceArn` conditions are absent)
- **Fixed naming** — all SLRs live under `/aws-service-role/` path

### Enumeration

```bash
# List all existing SLRs
aws iam list-roles \
  --query 'Roles[?starts_with(Path, `/aws-service-role/`)].{RoleName:RoleName,Arn:Arn,Service:AssumeRolePolicyDocument.Statement[0].Principal.Service}' \
  --output json

# Discover all AWS services that support SLRs
curl -s https://servicereference.us-east-1.amazonaws.com/v1/service-list.json | \
  jq -r '.[].service + ".amazonaws.com"'

# Check who can create SLRs (scan policies for this action)
# Look for: iam:CreateServiceLinkedRole with Resource: arn:aws:iam::*:role/aws-service-role/*
```

### Indirect Privilege Escalation Paths

An attacker who can create or trigger a service using an SLR can inherit
the SLR's AWS-defined permissions. Key high-risk SLRs:

| Service | SLR Risk | Escalation Path | Severity |
|:--------|:---------|:-----------------|:---------|
| Application Migration (mgn) | `ec2:ModifyInstanceAttribute` + `ec2:StartInstances` | Inject user data script → restart instance → code runs as instance role | CRITICAL |
| Directory Service (ds) | `ssm:SendCommand` | Send SSM command to any instance → executes as that instance's role | CRITICAL |
| Kafka / MSK | `secretsmanager:PutResourcePolicy` on `AmazonMSK_*` | Modify secret resource policy → grant self access to secret values | HIGH |
| License Manager | `secretsmanager:GetSecretValue` on `Resource: *` | Direct read access to any secret in the account | HIGH |
| RDS | Unrestricted EC2 permissions (`Resource: *`) | Broad EC2 control without resource scoping | HIGH |
| Transfer Family | Broad EC2 control (`Resource: *`) | EC2 network and instance manipulation | MEDIUM |

### SLR Creation as Reconnaissance

Even when SLR permissions are not directly exploitable, the ability to create
SLRs reveals which services are in use. An attacker can:

1. Attempt to create SLRs for all AWS services
2. Services already in use return "role already exists"
3. Services not in use create the SLR successfully
4. This maps the account's service footprint without CloudTrail noise

**Defensive measure:** Pre-create all available SLRs to prevent this enumeration.

### Tag and Namespace Collisions

Some SLRs use **unreserved tags** (e.g., `Owner`, `DeployedBy`, `Application`)
that can collide with customer ABAC (tag-based access control) policies. If your
policies grant access based on `aws:ResourceTag/Owner`, an SLR that sets that
tag on resources it manages could inadvertently grant access.

**Reserved S3 bucket prefixes** — AWS services reserve bucket name patterns
(e.g., `aws-*`, `elasticbeanstalk-*`). Creating buckets with these prefixes
can intercept service data flows.

### Audit Checklist

1. Enumerate existing SLRs and cross-reference with high-risk list above
2. Identify all principals with `iam:CreateServiceLinkedRole` — flag if `Resource` is wildcarded
3. Check if high-risk SLRs exist that are not required by active services
4. Review ABAC policies for tag conditions that overlap SLR-reserved tags
5. Verify no S3 buckets use reserved service prefixes

## References

- [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
- [IAM API Reference](https://docs.aws.amazon.com/IAM/latest/APIReference/)
- [IAM CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/iam/)
- [Policy Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html)
- [boto3 IAM](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html)
- [SLR Abuse Research (Plerion)](https://www.plerion.com/blog/about-aws-service-linked-roles)
