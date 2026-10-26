---
name: aws-solutions-architect-associate
description: Use when preparing for AWS Certified Solutions Architect – Associate (SAA-C03) — designing secure, resilient, high-performing and cost-optimised architectures, choosing between similar services from requirement keywords, networking and identity details, and practising long scenario questions verified against AWS documentation. Also use when writing or verifying architecture practice questions at associate level.
---

# AWS Certified Solutions Architect – Associate (SAA-C03)

Bottom line: **every question is a trade-off hidden in the wording**. Find the deciding requirement ("lowest cost", "least operational overhead", "highly available", "near real-time", "without code changes") and eliminate options that violate it.

## Exam shape (confirm on the official exam page)

- Multiple choice and multiple response; 130 minutes; scaled score with a passing mark of 720/1000; some unscored questions.
- Domains: Design Secure Architectures (largest), Design Resilient Architectures, Design High-Performing Architectures, Design Cost-Optimized Architectures. Use the official exam guide for weights and task statements.

Primary sources: AWS Certification (https://aws.amazon.com/certification/), the exam guide, AWS documentation and FAQs, the Well-Architected Framework and its lenses.

## Decision tables to build yourself

| Need | Typical choice | Watch for |
|---|---|---|
| Decouple components | SQS (queue), SNS (fan-out), EventBridge (event routing) | FIFO ordering and exactly-once needs |
| Stream processing | Kinesis Data Streams / Firehose, MSK | Firehose is near real-time delivery, not custom processing |
| Relational, high availability | RDS Multi-AZ (failover) vs read replicas (scale reads) vs Aurora | Multi-AZ standby does not serve reads (classic deployments) |
| Key-value at scale | DynamoDB (+ DAX for microsecond reads, global tables for multi-Region) | Partition key design |
| Shared file system | EFS (Linux), FSx for Windows / Lustre / NetApp ONTAP | Protocols and performance modes |
| Static content, global | S3 + CloudFront with origin access control | Signed URLs/cookies for private content |
| Hybrid connectivity | Site-to-Site VPN (fast to set up) vs Direct Connect (consistent, private) | Redundancy: DX + VPN backup |
| Many VPCs | Transit Gateway vs VPC peering (non-transitive) vs PrivateLink | CIDR overlap |
| Disaster recovery | Backup/restore → pilot light → warm standby → multi-site | RTO/RPO wording |
| Encryption | KMS (keys, grants, key policies), SSE-S3 / SSE-KMS, ACM for TLS | Cross-account key access |

## Security essentials

- IAM roles for services and cross-account access; resource policies vs identity policies; permission boundaries and SCPs in Organizations.
- Private subnets with NAT gateways for outbound access; VPC endpoints (gateway for S3/DynamoDB, interface for others) to avoid the internet.
- Least privilege, encryption at rest and in transit, logging with CloudTrail.

## Study loop

1. Read each task statement in the exam guide and list the services it implies.
2. Practise long scenarios: underline the deciding requirement before reading options.
3. For each wrong option, write the requirement it fails.
4. Verify every uncertain point in documentation; build small labs for networking and IAM if possible.

## Writing practice questions

- Base each explanation on a documentation page and cite it.
- Keep distractors plausible (right service, wrong mode).
- Avoid copying question banks; create your own scenarios.

## Pitfalls

- **"Least operational overhead"** favours managed and serverless options even when another option also works.
- **Auto Scaling + ALB health checks** vs EC2 status checks.
- **S3 storage classes:** retrieval times and minimum storage durations matter for cost answers.
- **Global vs regional** services (IAM, Route 53, CloudFront are global; most others regional).
- **Spot for stateful workloads** is a trap.

## Self-check

- A full practice exam in 130 minutes with margin above the passing line.
- Fill the decision table from memory.
- Explain the RTO/RPO of each DR strategy and its cost order.
