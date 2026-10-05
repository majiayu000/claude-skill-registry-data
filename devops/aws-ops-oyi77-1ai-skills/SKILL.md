---
name: aws-ops
description: Use when aWS operations — EC2, S3, Lambda, RDS, ECS, IAM, CloudFormation.
  Infrastructure and cost optimization. Use when working with aws ops.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- aws
- ci-cd
- devops
- infrastructure
- ops
version: 1.0.0
category: devops
---



## Overview

AWS infrastructure management covering core services (EC2, S3, Lambda, RDS), IAM security, CloudFormation IaC, and cost optimization strategies.

## Capabilities

- EC2 instance management and auto-scaling
- S3 bucket policies and lifecycle
- Lambda function deployment
- IAM policy design
- CloudFormation templates
- Cost optimization (Spot, Reserved, Savings Plans)
- CloudWatch monitoring

## When to Use
**Trigger phrases:**
- "aws ops"
- "AWS operations — EC2, S3, Lambda, RDS, ECS, IAM, CloudFormation"


- Cloud infrastructure management
- Web application hosting
- Data processing pipelines
- Cost optimization reviews

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The aws-ops workflow follows a standard pipeline pattern.

Core flow:
```
# aws-ops primary flow
input = prepare(raw_data)
result = process(input, config={aws, cloudformation, cost, infrastructure, lambda})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### CloudFormation EC2
```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t3.micro
      ImageId: ami-0abcdef1234567890
      SecurityGroupIds: [!Ref WebSG]
      Tags:
        - Key: Name
          Value: WebServer
```

## Common Patterns

- Tag everything for cost tracking
- Use IAM roles, not access keys
- Enable CloudTrail for audit
- S3 lifecycle rules for cost

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |