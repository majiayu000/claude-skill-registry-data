---
name: aws-specialist
description: AWS cloud infrastructure, services, and architecture including CloudFormation,
  CDK, and the AWS Well-Architected Framework. Use when asked to deploy to AWS, set
  up EC2 or ECS or EKS, configure IAM roles or policies, create Lambda functions,
  set up S3 buckets or CloudFront, design a VPC, write CloudFormation or CDK code,
  optimize AWS costs, configure CloudWatch alarms, scan AWS account resources, or
  audit AWS security posture.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-cloud
  tags:
  - aws
  - cloud
  - iac
  - cloudformation
  - cdk
  - lambda
  - ec2
  - ecs
  - eks
  - iam
  - s3
---

# AWS Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `deploy to AWS`, `set up EC2`, `configure IAM`.
- The requested work fits this skill's lane: EC2, ECS, EKS, Lambda, RDS, S3, CloudWatch, IAM, VPC, cost optimization, AWS security.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Azure or GCP work; Terraform HCL writing (use terraform-specialist); application code.

## First actions
1. `Glob('**/*.tf', '**/*.cfn.yml', '**/*.cfn.json', '**/cdk.json', '**/samconfig.toml')` — find existing IaC
2. `Glob('**/.aws/config', '**/aws-config*')` — find AWS config files that reveal region and profile context
3. Read any existing CloudFormation templates or CDK stacks to understand current resource patterns
4. Identify: target region, whether this is greenfield or existing infrastructure, AWS account structure (single vs multi-account)

## Decision rules
- If IaC tooling is already established (Terraform files present): use terraform-specialist for provisioning; use this skill for AWS-specific service knowledge
- If asked about IAM: default to least-privilege; never recommend wildcard (`*`) actions in production policies
- If the task requires cross-account access: use IAM roles with trust policies, not access keys
- If cost optimization is involved: check for Reserved Instance/Savings Plan opportunities, right-sizing, and S3 lifecycle policies
- If multi-cloud scope appears: route Azure to azure-specialist, GCP to gcp-specialist

## Steps

### Step 1: Assess current AWS context
Understand what already exists: existing VPCs, IAM structure, compute patterns, and IaC approach in use.

### Step 2: Design the solution
Apply Well-Architected Framework pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization.

### Step 3: Write the code
For CloudFormation: write YAML with proper `Outputs` and `Parameters`. For CDK: use TypeScript or Python constructs with L2+ where available. For CLI-based tasks: write bash scripts using `aws` CLI with proper error handling.

### Step 4: Validate
For CloudFormation: `aws cloudformation validate-template`. For CDK: `cdk synth`. For IAM policies: use IAM policy simulator logic to check permissions.

## Output contract
- Primary artifact: CloudFormation YAML, CDK stack file, or AWS CLI bash script
- Required: IAM least-privilege analysis for any IAM resources created; cost estimate note for significant resources
- Security: all S3 buckets must have `BlockPublicAcls: true` by default; all IAM roles must have scoped conditions

## Constraints
- NEVER create IAM users with long-lived access keys for workloads — use IAM roles
- NEVER use `Effect: Allow, Action: *, Resource: *` in production
- NEVER hardcode AWS credentials in any file
- Scope boundary: application code belongs to language-specific skills; Terraform module writing belongs to terraform-specialist

## Examples

### Example 1: Lambda + API Gateway setup
User says: "Set up a Lambda function with an API Gateway endpoint for a Python REST API"
Actions:
1. Glob for existing CloudFormation/SAM templates
2. Write SAM template with Lambda function, API Gateway, and IAM execution role
3. Include environment variables, memory/timeout configuration, and CloudWatch log group
Result: Complete SAM template with deployment instructions

### Example 2: AWS account scan
User says: "Scan my AWS account for security issues"
Actions:
1. Write Python script using boto3 to check: public S3 buckets, overly permissive security groups, IAM users without MFA, unencrypted EBS volumes, CloudTrail status
2. Output findings as JSON grouped by severity
Result: Security audit script with prioritized findings

## Troubleshooting
**"Access Denied" on AWS API calls**
Cause: IAM permissions missing or wrong region
Fix: Check effective permissions with `aws iam simulate-principal-policy`; verify `--region` flag matches resource location

**CloudFormation stack stuck in UPDATE_ROLLBACK_FAILED**
Cause: Manual resource changes outside CloudFormation
Fix: Use `aws cloudformation continue-update-rollback --skip-resources` to skip conflicting resources

## Reference
- `references/legacy-agent.md`: full service reference — EC2, ECS, EKS, Lambda, RDS, S3, CloudWatch, IAM, VPC, cost optimization patterns, MCP code examples (note: MCP stubs are non-functional)
