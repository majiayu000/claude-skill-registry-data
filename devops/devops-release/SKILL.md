---
name: devops-release
description: DevOps and Release Engineering from Netflix (8000+ deployments/day, 260M+ subscribers). Use when setting up CI/CD pipelines (GitHub Actions), containerizing with Docker, deploying to Kubernetes, configuring monitoring/alerting (Datadog, Prometheus), implementing canary/blue-green deployments, writing operations runbooks, or managing production releases. Triggers on CI/CD, deployment, pipeline, Docker, release, monitoring, alerting, rollback, or infrastructure automation.
---

# DevOps & Release Engineering - Netflix-Grade Infrastructure

**Purpose**: Complete DevOps and release management procedures from Netflix

**Agent**: Netflix DevOps Engineer
**Use When**: Phase 5 (Packaging) & Phase 6 (Deployment) - need CI/CD, infrastructure, and deployment automation

---

## Overview

This skill module provides comprehensive DevOps procedures used at Netflix to handle 8,000+ deployments/day serving 260M+ subscribers with 99.999% uptime.

**Core Philosophy**:
- Automate everything
- Deploy often (small changes = lower risk)
- Monitor proactively
- Rollback easily
- Zero-downtime deployments

---

## Available Reference Guides

### 1. CI/CD Pipelines
**File**: `references/ci-cd-pipelines.md`

**Covers**:
- GitHub Actions pipeline setup (Netflix standard)
- Automated testing integration (unit, integration, E2E)
- Code quality gates (linting, type-checking, coverage)
- Security scanning (Snyk, npm audit)
- Docker image building and pushing
- Multi-environment deployment (staging → production)
- Canary deployment automation

**When to Use**: Phase 3 (Development) - setup early

**Example Pipeline**:
```yaml
Jobs:
1. Quality Gates (lint, type-check, security scan)
2. Test (unit, integration, E2E)
3. Build (Docker image)
4. Deploy Staging (auto)
5. Performance Test (auto)
6. Deploy Production (manual approval + canary)
```

---

### 2. Infrastructure as Code
**File**: `references/infrastructure-as-code.md`

**Covers**:
- Terraform for AWS/GCP/Azure
- VPC, subnets, security groups
- EKS/GKE/AKS cluster setup
- RDS/Cloud SQL database provisioning
- ElastiCache/Memorystore (Redis)
- S3/Cloud Storage + CDN (CloudFront)
- Load balancers and auto-scaling

**When to Use**: Phase 2 (Design) - infrastructure planning
Phase 5 (Packaging) - provision infrastructure

**Example Terraform Structure**:
```
infrastructure/
├── modules/
│   ├── vpc/
│   ├── eks/
│   ├── rds/
│   └── redis/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── main.tf
```

---

### 3. Kubernetes Deployment
**File**: `references/kubernetes-deployment.md`

**Covers**:
- Deployment manifests (replicas, resources, health checks)
- Service configuration (ClusterIP, LoadBalancer)
- Horizontal Pod Autoscaler (HPA)
- ConfigMaps and Secrets management
- Ingress configuration (routing, TLS)
- Rolling updates and rollback
- Namespace management

**When to Use**: Phase 6 (Deployment)

**Example Manifests**:
- Deployment (with liveness/readiness probes)
- Service (load balancing)
- HPA (auto-scaling 3-20 pods)
- Ingress (HTTPS + routing)

---

### 4. Monitoring & Alerting
**File**: `references/monitoring-alerting.md`

**Covers**:
- Datadog/New Relic setup
- Application metrics (request rate, error rate, latency)
- Infrastructure metrics (CPU, memory, network)
- Database metrics (connections, query performance)
- Alert rules (error rate, high latency, pod crashes)
- Dashboards creation
- On-call setup (PagerDuty/Opsgenie)

**When to Use**: Phase 6 (Deployment) - before production

**Key Alerts**:
- Error rate > 5%
- P95 latency > 1s
- Pod crash looping
- Memory usage > 90%
- Database connection pool > 80%

---

### 5. Release Management
**File**: `references/release-management.md`

**Covers**:
- Release planning and scheduling
- Canary deployment strategy (10% → 50% → 100%)
- Blue-green deployment
- Feature flags
- Rollback procedures
- Release notes generation
- Post-release monitoring

**When to Use**: Phase 7 (Release & Distribution)

**Netflix Canary Process**:
```
1. Deploy canary (10% traffic)
2. Monitor 5-10 min (error rate, latency)
3. If healthy: Promote to 50%
4. Monitor 5-10 min
5. If healthy: Promote to 100%
6. If issues: Instant rollback
```

---

### 6. Operations Runbooks
**File**: `references/operations-runbooks.md`

**Covers**:
- Architecture overview
- Deployment procedures
- Health check verification
- Common issues and solutions
- Rollback procedures
- Scaling procedures
- Disaster recovery
- Contact information and escalation

**When to Use**: Phase 6 (Handover) - training ops team

**Runbook Sections**:
- Deployment
- Monitoring
- Common Issues (high error rate, high latency, pod crashes)
- Rollback
- Scaling
- Disaster Recovery

---

## Quick Start

### For DevOps Engineer (you):

```bash
# Phase 3: CI/CD Setup
Read: references/ci-cd-pipelines.md
Create: .github/workflows/ci-cd.yml
Test: Run pipeline on test branch

# Phase 2-5: Infrastructure
Read: references/infrastructure-as-code.md
Write: Terraform for AWS/GCP/Azure
Provision: dev, staging, prod environments

# Phase 5: Kubernetes Config
Read: references/kubernetes-deployment.md
Write: k8s manifests (deployment, service, HPA, ingress)
Test: Deploy to staging

# Phase 6: Monitoring
Read: references/monitoring-alerting.md
Setup: Datadog/New Relic
Create: Dashboards and alerts

# Phase 6: Deployment
Read: references/release-management.md
Deploy: Canary to production
Monitor: Post-deployment metrics

# Phase 6: Handover
Read: references/operations-runbooks.md
Create: Operations runbook
Train: Operations team
```

### For Other Agents:

**PM**: Review deployment timeline, coordinate releases
**QA**: Use staging environment for testing
**Developers**: Understand CI/CD pipeline, fix build failures
**BA**: Use staging for UAT

---

## Deployment Strategies (Netflix-Proven)

### Canary Deployment (Recommended)
```
Advantages:
✅ Gradual rollout (10% → 50% → 100%)
✅ Early issue detection (affects only 10% initially)
✅ Easy rollback (revert traffic routing)

Process:
1. Deploy new version alongside old
2. Route 10% traffic to new version
3. Monitor metrics (5-10 min)
4. If healthy: Increase to 50%
5. If healthy: Increase to 100%
6. If issues: Route 100% back to old version
```

### Blue-Green Deployment
```
Advantages:
✅ Instant switchover
✅ Easy rollback (switch back to blue)
✅ Zero downtime

Process:
1. Blue (v1.0) = 100% traffic
2. Deploy Green (v1.1) = 0% traffic
3. Test Green thoroughly
4. Switch 100% traffic to Green
5. Keep Blue for rollback (24h)
```

### Rolling Update (Default Kubernetes)
```
Advantages:
✅ Simple, built-in
✅ Gradual replacement

Process:
1. Kubernetes replaces pods one-by-one
2. Waits for new pod to be ready
3. Then replaces next pod
4. maxSurge: 1, maxUnavailable: 0 (zero downtime)
```

---

## Infrastructure Stack (Netflix-Style)

### AWS Stack (Recommended)
```
Frontend:
- CloudFront CDN (global distribution)
- S3 (static assets)

Application:
- EKS (Kubernetes cluster)
- ALB (Application Load Balancer)
- Auto Scaling Groups

Data:
- RDS PostgreSQL (primary database)
- ElastiCache Redis (caching)
- S3 (file storage)

Monitoring:
- CloudWatch (logs, metrics)
- Datadog (APM)
```

### GCP Stack (Alternative)
```
Frontend:
- Cloud CDN
- Cloud Storage

Application:
- GKE (Kubernetes cluster)
- Cloud Load Balancing

Data:
- Cloud SQL PostgreSQL
- Memorystore Redis
- Cloud Storage

Monitoring:
- Cloud Monitoring
- Cloud Logging
```

---

## Quality Gates Checklist

Before production deployment:

```markdown
## Build & Tests ✅
- [ ] All tests passing in CI/CD
- [ ] Code coverage ≥ 80%
- [ ] No linting errors
- [ ] Type check passed

## Security ✅
- [ ] Security scan passed (no critical)
- [ ] Dependencies updated
- [ ] Secrets in vault (not code)
- [ ] TLS configured

## Performance ✅
- [ ] Load test passed
- [ ] API latency benchmarks met
- [ ] Database queries optimized

## Deployment ✅
- [ ] Staging deployment successful
- [ ] Smoke tests passed
- [ ] Rollback tested
- [ ] Runbook updated

## Monitoring ✅
- [ ] Application metrics configured
- [ ] Alert rules active
- [ ] Dashboards created
- [ ] On-call rotation setup

**DevOps Sign-Off**: _______________
**Date**: _______________
```

---

## DevOps Tools (Netflix Tech Stack)

### CI/CD
- **GitHub Actions** (recommended): Native GitHub integration
- **Jenkins**: Traditional, powerful
- **GitLab CI**: All-in-one platform
- **Spinnaker**: Netflix-created, multi-cloud

### Infrastructure as Code
- **Terraform**: Multi-cloud, declarative
- **CloudFormation**: AWS-native
- **Pulumi**: Code-based (TypeScript, Python)

### Containers & Orchestration
- **Docker**: Container runtime
- **Kubernetes**: Orchestration
- **Helm**: Kubernetes package manager
- **Kustomize**: Kubernetes templating

### Monitoring & Observability
- **Datadog**: APM, metrics, logs, traces
- **New Relic**: APM, real-user monitoring
- **Prometheus + Grafana**: Open-source metrics
- **ELK Stack**: Elasticsearch, Logstash, Kibana (logs)

### Cloud Platforms
- **AWS**: Most mature, comprehensive
- **GCP**: Great for AI/ML, Kubernetes
- **Azure**: Enterprise, Microsoft ecosystem

---

## Netflix DevOps Standards

**Automation**: 100% - no manual deployments
**Deployment Frequency**: Multiple per day (small changes)
**Lead Time**: < 1 hour (commit to production)
**MTTR**: < 30 min (mean time to recovery)
**Change Failure Rate**: < 5%

**Key Principles**:
- **Cattle, not pets**: Servers are disposable
- **Immutable infrastructure**: Never modify, always replace
- **Everything as code**: Repeatable, version-controlled
- **Fail fast**: Detect issues early, rollback immediately

---

## Communication Templates

### Deployment Notification (Slack)
```
🚀 *PRODUCTION DEPLOYMENT STARTED*

• Version: v1.2.3
• Commit: abc123def
• Strategy: Canary (10% → 50% → 100%)
• ETA: 30 minutes
• Deployed by: Marcus Chen
• Monitoring: https://datadog.com/dashboard/abc

*Canary Status*:
[⏳] 10% deployed, monitoring...
```

### Incident Alert (PagerDuty)
```
🚨 *INCIDENT: High Error Rate*

• Service: todo-app-production
• Error rate: 12% (threshold: 5%)
• Started: 2026-02-04 14:23 UTC
• Impact: 12% of users affected
• Assigned: On-call DevOps

*Actions*:
1. Rollback to v1.2.2 (in progress)
2. Investigate error logs
3. Post-mortem scheduled
```

---

## Remember

🚀 **Automate everything** - Manual processes don't scale to 8000 deploys/day
📊 **Monitor proactively** - Know about issues before customers
🔄 **Deploy often** - Small changes = lower risk, easier to debug
⏪ **Rollback easily** - Always have escape hatch (< 30 seconds)
📖 **Document everything** - Runbooks save hours during incidents

---

**For detailed procedures, read the reference guides in `references/` folder**

**Created**: 2026-02-04
**Maintained By**: Netflix DevOps Engineer
**Review Cycle**: After each major deployment
