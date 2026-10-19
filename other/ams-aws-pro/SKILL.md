---
name: aws-pro
description: AWS guidance — core services, IAM least privilege, networking, cost control, and production architecture patterns.
category: development
---

## Overview

AWS is the broadest cloud platform — 200+ services, with a core set (EC2, S3, RDS, IAM, VPC, Lambda, CloudFront, Route53, EKS/ECS) covering most architectures. Its breadth is the challenge: there are five ways to do everything, pricing is complex, and IAM misconfigurations are the leading cause of cloud incidents.

The disciplines that matter: IAM least privilege, VPC networking fundamentals, choosing the right compute/storage per workload, and cost awareness from day one. This skill covers the core services, the security baseline, and architecture patterns that work — plus the cost traps to avoid.

## When to use

- Designing architecture on AWS (choosing services).
- Setting up IAM (users, roles, policies, least privilege).
- Building VPC networking (subnets, routing, security groups).
- Choosing compute (EC2, Lambda, ECS, EKS, Fargate).
- Controlling AWS costs (finding waste, budgets, alerts).
- Securing an AWS account (baseline, auditing, incident response).
- Preparing for production (multi-AZ, backups, DR).

## Core concepts

- **IAM: least privilege, always.** Roles for workloads (never long-lived access keys for apps), policies scoped to specific actions and resources, no `*` on production policies. IAM Access Analyzer finds unused permissions; credential reports find stale keys.
- **VPC fundamentals.** Your private network: public subnets (load balancers, NAT) + private subnets (apps, databases) across 2-3 AZs; route tables, internet gateway, NAT gateway. Security groups (stateful instance firewalls) + NACLs (stateless subnet firewalls) — security groups do most of the work.
- **Compute choices.** EC2 (control, steady workloads), Lambda (event-driven, spiky, short tasks), ECS/Fargate (containers without managing servers), EKS (Kubernetes when you need it). Match the abstraction to the team's operational capacity — EKS without K8s expertise is pain.
- **S3.** Object storage for everything static: versioning on, encryption on, block public access on (use CloudFront OAC for public content), lifecycle policies to Glacier for old data. S3 is also the Terraform-state, backup, and log-archive default.
- **RDS/Aurora.** Managed Postgres/MySQL: Multi-AZ for HA, read replicas for scale, automated backups + point-in-time recovery, Performance Insights for query tuning. Never run production databases on EC2 unless you have a very good reason.
- **CloudFront + Route53.** CDN for global latency and caching; Route53 for DNS with health-checked routing. CloudFront in front of S3/ALB is the standard public-web pattern.
- **Lambda well.** Small functions, right-sized memory (CPU scales with memory), VPC only when needed (it adds cold-start latency), reserved concurrency to bound blast radius, DLQs for async failures.
- **SQS/SNS/EventBridge.** Queues (SQS) for decoupling, topics (SNS) for fan-out, EventBridge for event routing between services. Prefer managed messaging over self-hosted brokers unless you need the protocol.
- **CloudWatch.** Metrics, logs, alarms — the default observability. Structured JSON logs, metric filters, composite alarms; but know its costs (custom metrics, log ingestion) and supplement with purpose-built tools at scale.
- **Organizations and accounts.** Multi-account strategy (prod/staging/dev, security, logging) with SCPs for guardrails. One account for everything is how incidents become company-wide.
- **Pricing model.** On-demand vs reserved/savings plans (steady workloads), spot (interruptible batch), graviton (ARM — cheaper and faster for many workloads). Right-size before committing to reservations.
- **Backups and DR.** AWS Backup for centralized policies; cross-region replication for S3 and RDS snapshots; define RTO/RPO per workload and test restores — untested backups are rumors.
- **Tagging.** Cost allocation tags (team, environment, service) enforced by policy — without tags, cost attribution is impossible.
- **Security baseline.** CloudTrail on (all regions, log file validation), GuardDuty for threat detection, Security Hub for posture, Config for compliance rules. Enable these before you need them.
- **Secrets Manager / Parameter Store.** Never env-var secrets into containers or bake them into AMIs; fetch at runtime with IAM-scoped access and rotation.
- **VPC endpoints.** PrivateLink endpoints for S3, DynamoDB, and other AWS services — keeps traffic off the internet and avoids NAT data-processing charges.
- **Auto Scaling done right.** Target-tracking policies on meaningful metrics (request count per target, custom app metrics) — not just CPU; warm pools for spiky workloads.

## Practical workflow

1. **Set up the account foundation.** Organizations with separate accounts (prod/staging/dev/security), CloudTrail everywhere, GuardDuty + Security Hub enabled, IAM Identity Center for human access (no IAM users for people).
2. **Build the VPC.** Public/private subnets across 3 AZs, NAT gateways (or NAT instances for dev cost savings), security groups with least-privilege rules, VPC flow logs for debugging.
   ```hcl
   # sketch: public ALB -> private app -> private RDS, 3 AZs
   module "vpc" {
     source = "terraform-aws-modules/vpc/aws"
     azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
     public_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
     private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
   }
   ```
3. **Lock down IAM.** Roles per workload with scoped policies; no static keys for apps (IRSA for EKS, instance profiles for EC2, OIDC for CI); MFA for humans; regular access reviews.
4. **Choose compute per workload.** Steady API → ECS/Fargate or EC2 ASG; spiky events → Lambda; need K8s → EKS; batch → spot fleets. Right-size with Compute Optimizer, prefer Graviton.
5. **Put data on managed services.** RDS Multi-AZ with automated backups, ElastiCache for Redis, S3 with versioning + lifecycle. Test restore procedures quarterly.
6. **Front with CloudFront + WAF.** CDN caching, TLS, WAF rules for common attacks; Route53 health checks with failover routing for multi-region.
   - Cache static aggressively, dynamic selectively; invalidate deliberately — invalidations cost and signal a design smell if constant.
7. **Observe and alarm.** CloudWatch dashboards for golden signals; alarms on error rates, latency, and saturation; structured logs with correlation IDs; trace with X-Ray or OpenTelemetry.
8. **Control costs.** Budgets with alerts, Cost Explorer reviews, kill idle resources (unattached EBS, old snapshots, idle NAT/LBs), S3 lifecycle policies, compute savings plans after right-sizing.

## Common pitfalls

- **`AdministratorAccess` everywhere** — wildcard IAM is the #1 cloud security failure; least privilege from the start.
- **Long-lived access keys** — leaked in repos and logs; roles + OIDC, rotate what remains.
- **Single AZ deployments** — one AZ failure = outage; multi-AZ for everything production.
- **Public S3 buckets** — data exposure; block public access, serve via CloudFront OAC.
- **Unencrypted everything** — EBS, RDS, S3 without encryption; enable by default (it's free).
- **No CloudTrail** — flying blind after an incident; enable in all regions with log validation.
- **Oversized instances** — paying for idle CPU; right-size, then commit to savings plans.
- **Idle resource sprawl** — unattached volumes, old AMIs/snapshots, forgotten load balancers; audit regularly.
- **NAT gateway cost surprise** — per-GB data processing charges; budget for it or architect around it.
- **Lambda in VPC by default** — cold-start latency and ENI management for no benefit; only when accessing VPC resources.
- **No backups tested** — snapshots exist but restores never tried; test quarterly.
- **One account for everything** — blast radius of a compromise; multi-account with SCPs.
- **Ignoring GuardDuty findings** — threat detection enabled but unmonitored; findings need a response runbook.
- **Secrets in user-data / env vars** — visible in console and snapshots; use Secrets Manager with runtime retrieval.
- **Default VPC for production** — the default VPC's flat open design; build purpose-specific VPCs instead.
- **Cross-AZ data transfer blindness** — chatty cross-AZ traffic racking up charges; keep data-local where possible.
