---
name: gcp-expert
description: Google Cloud Platform expertise from Google engineers. Master GCP services, GKE, BigQuery, Vertex AI, and cloud-native architecture. Use when working with Google Cloud services, deploying to GCP, or designing GCP architectures. Learn from the company that runs Google Search, YouTube, and Gmail on their own infrastructure.
expert_level: 10/10
source_company: Google
specialist: google-ai-researcher, google-sre-devops
requires:
  - kubernetes-expert
related:
  - deep-learning
  - sre-practices
---

# GCP Expert - Google Cloud Platform Mastery

**Experts**: Emily Rodriguez (Google AI, 10 years), Alex Kim (Google SRE, 11 years)
**Level**: 10/10 - Google's own cloud platform

## Overview

Google Cloud Platform from Google engineers - the infrastructure powering Search, YouTube, Gmail, Maps. This is cloud expertise from the source.

## When to Use GCP Services

**Compute needs:**
- Containers/Kubernetes → GKE (see references/compute.md)
- Serverless containers → Cloud Run (see references/compute.md)
- VMs → Compute Engine (see references/compute.md)

**Data & Analytics:**
- Data warehouse → BigQuery (see references/data.md)
- Streaming pipelines → Dataflow (see references/data.md)

**Databases:**
- Relational → Cloud SQL or Cloud Spanner (see references/databases.md)
- NoSQL → Firestore (see references/databases.md)

**AI & ML:**
- Machine learning → Vertex AI (see references/ai-ml.md)

**Messaging:**
- Pub/Sub, event-driven → See references/messaging.md

## Core Workflow

1. **Design**: Choose appropriate services for requirements
2. **Provision**: Use Terraform or gcloud CLI
3. **Deploy**: GKE for containers, Cloud Run for serverless
4. **Monitor**: Cloud Monitoring + Cloud Logging
5. **Optimize**: Cost optimization + performance tuning

## Best Practices

### Security
- IAM: Least privilege access
- VPC Service Controls: Perimeter security
- Secret Manager: Never hardcode secrets
- Workload Identity: For GKE pods

### Cost Optimization
- Committed Use Discounts: Save 57% on VMs
- Preemptible VMs: Save 80% for batch jobs
- BigQuery slots: Reserve for predictable costs

### Reliability
- Multi-region for critical services
- Health checks on all services
- Auto-scaling for traffic spikes

### Monitoring
- Cloud Monitoring: Metrics + alerts
- Cloud Logging: Centralized logs
- Cloud Trace: Distributed tracing

## Google's Production Scale

GCP powers:
- **Google Search**: 8.5 billion searches/day
- **YouTube**: 2 billion users, 1 billion hours/day
- **Gmail**: 1.8 billion users
- **Google Maps**: 1 billion users

## Related Skills

- **[kubernetes-expert](../kubernetes-expert/SKILL.md)** - GKE foundation
- **[deep-learning](../deep-learning/SKILL.md)** - Vertex AI ML
- **[sre-practices](../sre-practices/SKILL.md)** - Google SRE on GCP

---

**Last Updated**: 2026-02-03
**Experts**: Emily Rodriguez, Alex Kim (Google, 10-11 years each)
