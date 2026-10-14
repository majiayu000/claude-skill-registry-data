---
name: aws-foundations
description: "Operate AWS pragmatically: VPC/IAM least privilege, compute choice, managed data, observability, cost guards. Use for infra decisions and deploys. GCP/Azure: same principles, provider docs."
---

# aws-foundations

Boring infrastructure: managed services first, least privilege always, cost alarms before the bill.

## Activate when

- Choosing compute (Lambda/ECS/EKS/EC2), data (RDS/DynamoDB/ElastiCache), CDN (S3+CloudFront), queues (SQS/SNS), or wiring observability.

## Do NOT activate for

- Local containers (see devops/docker-compose) or CI config (see devops/github-actions).

## Procedure

1. Network: VPC with public/private subnets, security groups as narrow allowlists; no public data stores.
2. Identity: IAM roles per workload, no long-lived keys; MFA on humans; audit with CloudTrail.
3. Compute: serverless-first for spiky, containers for steady; autoscaling + health-checked load balancers; staged rollouts with rollback.
4. Data: RDS with backups + pooling, DynamoDB with explicit access patterns, ElastiCache for hot reads; SQS/SNS decouple slow work.
5. Observe: CloudWatch metrics/alarms, structured logs, tracing; SLOs with error budgets (see `../../architecture/observability/`).
6. Cost: budgets + anomaly alerts, lifecycle rules on S3/logs, right-size monthly.
7. Verify: deploy to a scratch env, kill-and-recover drill, restore-from-backup drill, cost report reviewed.

## References
- GCP/Azure: apply the same procedure against provider docs; do not invent service behavior.
