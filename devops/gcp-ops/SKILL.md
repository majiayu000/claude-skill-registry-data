---
name: gcp-ops
description: Use when google Cloud operations — Compute Engine, Cloud Run, BigQuery,
  Cloud Functions, GKE, IAM. Use when working with gcp ops.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- gcp
- infrastructure
- ops
version: 1.0.0
category: devops
---



## Overview

Google Cloud operations covering Compute Engine, Cloud Run for containers, BigQuery for analytics, Cloud Functions, and GKE for Kubernetes.

## Capabilities

- Compute Engine VM management
- Cloud Run container deployment
- BigQuery SQL analytics
- Cloud Functions serverless
- GKE cluster management
- IAM and service accounts
- Cost management and committed use

## When to Use
**Trigger phrases:**
- "gcp ops"
- "Google Cloud operations — Compute Engine, Cloud Run, BigQuery, Cloud Functions, "


- GCP infrastructure management
- Data analytics with BigQuery
- Container workloads on GKE
- Serverless with Cloud Run

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The gcp-ops workflow follows a standard pipeline pattern.

Core flow:
```
# gcp-ops primary flow
input = prepare(raw_data)
result = process(input, config={bigquery, cloud, compute, engine, functions})
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


### Cloud Run Deploy
```bash
gcloud run deploy my-service   --image gcr.io/project/image   --region us-central1   --allow-unauthenticated   --memory 512Mi
```

## Common Patterns

- Use service accounts with least privilege
- Preemptible VMs for batch work
- BigQuery slots for predictable cost
- Cloud Run concurrency tuning

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