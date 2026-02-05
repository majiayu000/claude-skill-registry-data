---
name: devops-architect
description: Expert DevOps architecture including CI/CD, infrastructure as code, containerization, and observability
version: 1.0.0
author: USER
tags: [devops, cicd, docker, kubernetes, terraform, observability]
---

# DevOps Architect

## Purpose
Design robust DevOps architectures including CI/CD pipelines, infrastructure as code, containerization, and observability strategies.

## Activation Keywords
- DevOps, CI/CD, pipeline
- Docker, Kubernetes, container
- Terraform, infrastructure as code
- monitoring, observability, logging
- deployment, release

## Core Capabilities

### 1. CI/CD Design
- Pipeline architecture
- Build optimization
- Test automation
- Deployment strategies
- Release management

### 2. Infrastructure as Code
- Terraform patterns
- Module design
- State management
- Environment parity
- Drift detection

### 3. Containerization
- Dockerfile optimization
- Multi-stage builds
- Image security
- Registry management
- Orchestration

### 4. Kubernetes
- Cluster architecture
- Workload patterns
- Service mesh
- Resource management
- RBAC design

### 5. Observability
- Metrics (Prometheus)
- Logging (ELK/Loki)
- Tracing (Jaeger/Tempo)
- Alerting strategy
- Dashboards

## CI/CD Pipeline Design

```yaml
# Standard pipeline stages
stages:
  - lint        # Code quality
  - test        # Unit + Integration
  - security    # SAST, dependency scan
  - build       # Container image
  - deploy-dev  # Dev environment
  - e2e         # End-to-end tests
  - deploy-stg  # Staging
  - deploy-prd  # Production (manual gate)
```

## Deployment Strategies

| Strategy | Use Case |
|----------|----------|
| Rolling | Standard, zero-downtime |
| Blue-Green | Instant rollback needed |
| Canary | Risk mitigation, A/B |
| Feature Flag | Gradual rollout |

## Infrastructure Patterns

```hcl
# Terraform module structure
modules/
├── networking/
│   ├── vpc/
│   └── security-groups/
├── compute/
│   ├── eks/
│   └── ec2/
└── data/
    ├── rds/
    └── elasticache/

environments/
├── dev/
├── staging/
└── production/
```

## Observability Stack

```
Metrics → Prometheus → Grafana
Logs → Fluent Bit → Loki → Grafana
Traces → OpenTelemetry → Tempo → Grafana
Alerts → Alertmanager → PagerDuty/Slack
```

## Example Usage

```
User: "Design CI/CD for microservices deployment"

DevOps Architect Response:
1. Pipeline design
   - Monorepo vs polyrepo strategy
   - Shared pipeline templates
   - Service-specific customizations

2. Infrastructure
   - Kubernetes cluster design
   - Namespace per environment
   - Resource quotas

3. Deployment strategy
   - Canary releases
   - Automated rollback
   - Feature flags integration

4. Observability
   - Service mesh for tracing
   - Centralized logging
   - SLO-based alerting
```
