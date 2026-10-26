---
name: aws-cloud-practitioner
description: Use when preparing for AWS Certified Cloud Practitioner (CLF-C02) — the exam domains and weights, cloud concepts, the shared responsibility model, core services by category, security and identity basics, pricing models and support plans, and practising with scenario questions checked against AWS documentation. Also use when writing or verifying practice questions at this level.
---

# AWS Certified Cloud Practitioner (CLF-C02)

Bottom line: **this exam tests recognition — which service or concept fits a business scenario — not configuration**. Learn categories and the "why" of each core service, and the shared responsibility split.

## Exam shape (confirm on the official exam page)

- Multiple choice and multiple response; 90 minutes; scaled score with a passing mark of 700/1000; some unscored questions are included.
- Domains: Cloud Concepts, Security and Compliance, Cloud Technology and Services (largest), Billing, Pricing, and Support. Use the official exam guide for exact weights and task statements.

Primary sources: AWS Certification (https://aws.amazon.com/certification/), the official exam guide, AWS documentation, the Well-Architected Framework, and AWS Skill Builder's free practice question set.

## What to know cold

| Area | Core points |
|---|---|
| Cloud value | Elasticity, pay-as-you-go, economies of scale, global reach, CapEx → OpEx |
| Global infrastructure | Regions, Availability Zones, edge locations; choosing a Region (compliance, latency, service availability, price) |
| Shared responsibility | AWS: security *of* the cloud; customer: security *in* the cloud — and how the split shifts between EC2, RDS and Lambda |
| Identity | IAM users, groups, roles, policies, least privilege, MFA, root user protection, IAM Identity Center |
| Compute | EC2 (instance families, purchase options: On-Demand, Savings Plans, Reserved, Spot), Lambda, containers (ECS, EKS, Fargate) |
| Storage | S3 (storage classes, lifecycle), EBS, EFS, Glacier tiers |
| Databases | RDS, Aurora, DynamoDB, ElastiCache, Redshift — relational vs key-value vs analytics |
| Networking | VPC, subnets, security groups vs network ACLs, Route 53, CloudFront, Direct Connect, VPN |
| Security services | Shield, WAF, GuardDuty, Inspector, Macie, KMS, Secrets Manager, Artifact, Security Hub |
| Operations | CloudWatch, CloudTrail, Config, Trusted Advisor, Systems Manager |
| Cost | Pricing Calculator, Cost Explorer, Budgets, Cost and Usage Report, consolidated billing in Organizations |
| Support | Basic, Developer, Business, Enterprise On-Ramp, Enterprise — what each adds (response times, TAM) |

## Study loop

1. Read the exam guide's task statements; turn each into one question you can answer.
2. For each service, write one line: "use it when ... / not when ...".
3. Practise scenario questions; for every option, say why it is right or wrong.
4. Check doubtful answers in AWS documentation, not in third-party dumps.

## Writing practice questions

- Ground each option's explanation in an AWS documentation page.
- Prefer scenarios ("a company needs ...") over definitions; keep wording varied.
- Re-check facts that change (service names, support plan features) before publishing.

## Pitfalls

- **Security groups are stateful, network ACLs stateless.**
- **CloudTrail (who did what) vs CloudWatch (metrics/logs) vs Config (resource configuration history).**
- **Savings Plans vs Reserved Instances vs Spot** — commitment and interruption trade-offs.
- **Trusted Advisor checks** available depend on the support plan.
- Old names in study material (services get renamed) — use current documentation.

## Self-check

- A full practice set under 90 minutes with comfortable margin above the passing line.
- Explain the shared responsibility model for EC2, RDS and Lambda without notes.
- Name the right service for 20 random business needs in under 10 seconds each.
