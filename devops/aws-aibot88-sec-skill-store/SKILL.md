---
name: aws
description: AWS infrastructure management — EKS, ECR, VPC, RDS, ElastiCache, S3, Route53, ACM, Secrets Manager, CloudWatch, IAM
version: 1.0.0
author: veekunth217
tags: [aws, eks, ecr, vpc, rds, s3, route53, acm, cloudwatch, iam, secrets-manager, elasticache]
platforms: [claude-code, cursor, codex]
---

# AWS Skill

Expert-level AWS infrastructure management. Covers the full stack from networking to observability.

**RULE: Always show what will be created/changed and wait for GO before executing.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### EKS Cluster Setup & Management
<!-- TODO: Step-by-step EKS cluster creation, node group configs, OIDC provider, kubectl access setup -->
<!-- TODO: Cluster upgrades, managed add-ons, Fargate profiles -->

### ECR Image Push/Pull Workflows
<!-- TODO: ECR auth, lifecycle policies, cross-account access, image scanning -->
<!-- TODO: docker build → tag → push pipeline, pull-through cache -->

### VPC, Subnets, Security Groups
<!-- TODO: Multi-AZ VPC design, public/private/isolated subnet tiers -->
<!-- TODO: Security group rules, NACLs, VPC flow logs, peering -->

### RDS, ElastiCache, S3
<!-- TODO: RDS parameter groups, Multi-AZ, read replicas, snapshots -->
<!-- TODO: ElastiCache Redis cluster, node types, failover -->
<!-- TODO: S3 bucket policies, versioning, lifecycle, static hosting, presigned URLs -->

### Route53, ACM SSL
<!-- TODO: Hosted zone setup, A/CNAME/alias records -->
<!-- TODO: ACM certificate request, DNS validation, wildcard certs -->
<!-- TODO: Health checks, failover routing, latency routing -->

### Secrets Manager Integration
<!-- TODO: Secret creation, rotation, cross-account access -->
<!-- TODO: App integration patterns (Node, Python, Go) -->

### CloudWatch + Alerting
<!-- TODO: Log groups, metric filters, dashboards -->
<!-- TODO: Alarms, SNS notifications, composite alarms -->
<!-- TODO: Container Insights for EKS -->

### IAM Roles & Policies
<!-- TODO: Least-privilege policy design, IRSA for EKS, permission boundaries -->
<!-- TODO: Cross-account role assumption, service-linked roles -->

---

## Common Workflows

### Authenticate to EKS
```bash
aws eks update-kubeconfig --name [cluster-name] --region [region]
kubectl get nodes
```

### Authenticate to ECR and push
```bash
aws ecr get-login-password --region [region] | \
  docker login --username AWS --password-stdin \
  [account-id].dkr.ecr.[region].amazonaws.com

docker build -t [app] .
docker tag [app]:latest [account-id].dkr.ecr.[region].amazonaws.com/[app]:latest
docker push [account-id].dkr.ecr.[region].amazonaws.com/[app]:latest
```

### Check CloudWatch logs
```bash
aws logs tail /aws/eks/[cluster]/cluster --follow
aws logs tail /ecs/[service] --follow --filter-pattern "ERROR"
```

---

## Quick Reference

| Service | Console shortcut | CLI prefix |
|---------|-----------------|------------|
| EKS     | eks.console.aws.amazon.com | `aws eks` |
| ECR     | ecr.console.aws.amazon.com | `aws ecr` |
| RDS     | rds.console.aws.amazon.com | `aws rds` |
| S3      | s3.console.aws.amazon.com  | `aws s3`  |
| IAM     | iam.console.aws.amazon.com | `aws iam` |

<!-- TODO: Add full interactive workflows for each capability section above -->
