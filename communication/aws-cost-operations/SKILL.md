---
name: aws-cost-operations
description: AWS cost/ops quick guide for budgeting, monitoring, and optimization with standard guardrails.
---

# AWS Cost & Operations (Concise)

Use for: FinOps reviews, budget/alerts, right-sizing, and ops hygiene on AWS.

## Core steps
- Accounts/guardrails: org SCPs, SSO, budgets per OU; tag standards (owner, env, cost-center, app).
- Budgets/alerts: AWS Budgets + SNS/Email/Chat; anomaly detection on Cost Explorer; set % thresholds.
- Right-size: compute (EC2/ASG/Fargate/Lambda) based on utilization; S3/Glacier lifecycle; RDS/Aurora rightsizing; turn off idle.
- Pricing levers: Savings Plans/RIs, Graviton preference, spot where safe, data transfer minimization (VPC endpoints, regional design).
- Storage: S3 IA/Glacier policies; EBS GP3; snapshots lifecycle; DynamoDB autoscaling + TTL.
- Networking: prune NAT gateways, use private links/endpoints, limit cross-AZ and inter-region flows.
- Observability: tag propagation to logs/metrics; cost per service/app dashboards; alarms on spend and on disabled logging.

## Ops hygiene
- Enable CloudTrail, Config, GuardDuty, Security Hub; centralize logs (KMS, retention).
- IaC: use CDK/Terraform with reviews and drift checks.
- Backup/DR: retention policies, periodic recovery tests.

## Quick checks
- `aws ce get-cost-and-usage` for recent spikes; check untagged spend.
- S3 `storage-lens`, `s3 ls --summarize`; EBS snapshot list/age; idle load balancers; idle RDS/ElastiCache.

## References
- AWS Well-Architected Cost pillar; AWS Budgets/CE docs; FinOps best practices.
