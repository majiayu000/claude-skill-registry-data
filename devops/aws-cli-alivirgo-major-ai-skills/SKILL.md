---
name: aws-cli
description: "Use AWS CLI profiles and SSO to inspect and manage S3, EC2, Lambda, IAM, and CloudWatch resources with explicit account and region selection."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["aws", "aws-cli", "iam", "s3", "cloudwatch", "lambda", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# AWS CLI & Cloud APIs AI Skill Guide

## Overview & Engine Architecture

The AWS CLI v2 calls AWS service APIs using a credential chain (environment, SSO/profile, instance role). Every mutating call is account- and region-scoped. Agents always print caller identity and region before deletes, prefer least-privilege IAM, and keep long-lived access keys out of git and chat.

```
User / CI
  -> aws CLI v2
      -> credential chain (SSO / env / role)
          -> service APIs (S3, EC2, Lambda, IAM, Logs, ...)
```

## When to use this skill

- Imperative debugging alongside Terraform/CDK
- S3 sync, log tails, Lambda invoke, IAM policy simulation
- Confirming which account a pipeline is acting on
- One-off safe read operations during incidents

## Operational directives

1. Start with `aws sts get-caller-identity` and confirm account/ARN.
2. Prefer IAM Identity Center (SSO) over permanent access keys for humans.
3. Use `--dry-run` where the API supports it (notably EC2).
4. Never log `AWS_SECRET_ACCESS_KEY`, session tokens, or pre-signed URL query secrets in full.
5. Scope IAM policies to resources and conditions (`aws:RequestedRegion`, source IP, MFA) when designing roles.

## Identity and config

```bash
aws sts get-caller-identity
aws configure list
aws configure list-profiles
# SSO example:
aws sso login --profile prod-admin
export AWS_PROFILE=prod-admin
```

## High-value command patterns

```bash
# S3
aws s3 ls s3://my-bucket/prefix/
aws s3 sync ./dist s3://my-bucket/app/ --delete --dryrun

# Logs
aws logs tail /aws/lambda/my-fn --follow --since 30m

# Lambda
aws lambda get-function --function-name my-fn
aws lambda invoke --function-name my-fn --payload '{}' out.json

# IAM sanity
aws iam get-role --role-name gha-deploy
```

## Incident hygiene table

| Task | Safe first step | Dangerous if blind |
| --- | --- | --- |
| Clear a bucket | `ls` + versioning check | `rb --force` |
| Stop an instance | `describe-instances` | terminate vs stop mixup |
| Rotate keys | create new + update consumers | deactivate last key early |
| Fix Lambda | check CloudWatch errors | raising memory without need |

## Best practices

- Tag resources for cost and ownership (`Owner`, `Service`, `Env`).
- Prefer instance/task roles over embedding keys in compute.
- Use CloudTrail when investigating who changed what.
- Keep CLI version current; auth and SSO flows improve over time.

## Limitations

- Service quotas, SCPs, and permission boundaries can deny valid CLI calls.
- Some older services have inconsistent pagination and dry-run support.
- This skill does not replace Well-Architected reviews for new architectures.

## Related skills

- `@terraform` - durable infrastructure changes
- `@kubernetes` - EKS workload debugging after node/IAM issues
- `@docker` - images pushed to ECR
