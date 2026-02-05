---
name: delivery-and-infra
description: Use when designing cloud infrastructure, CI/CD pipelines, or deployment strategies
---

# Delivery & Infrastructure

Guidelines for cloud architecture, CI/CD, and deployment engineering.

## When to Use

- Designing cloud infrastructure (AWS/Azure/GCP)
- Setting up CI/CD pipelines
- Container orchestration (Kubernetes)
- Infrastructure as Code (Terraform)
- Deployment strategy selection

## Core Principles

1. **Automate Everything** - No manual deployment steps
2. **Infrastructure as Code** - Version-controlled, reproducible
3. **Build Once, Deploy Anywhere** - Immutable artifacts
4. **Fast Feedback** - Fail fast, fix fast
5. **Security by Design** - Embedded throughout lifecycle
6. **GitOps as Truth** - Git is single source of truth
7. **Zero-Downtime** - All deployments without user impact

## CI/CD Pipeline

### Standard Stages
```
Lint → Test → Security Scan → Build → Deploy (staging) → Deploy (prod)
```

### Pipeline Checklist
- [ ] Parallel execution where possible
- [ ] Caching for faster builds
- [ ] Environment-based deployment gates
- [ ] Automated rollback on failure
- [ ] Security scanning (SAST/DAST)
- [ ] Artifact versioning and signing

### GitHub Actions Example
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test -- --coverage

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.IMAGE }}:${{ github.sha }}
```

## Container Best Practices

### Dockerfile Checklist
- [ ] Multi-stage builds for minimal size
- [ ] Non-root user for runtime
- [ ] No secrets in image layers
- [ ] Minimal base image (alpine, distroless)
- [ ] Health checks defined
- [ ] Resource limits configured

### Example Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine
RUN adduser -S app -u 1001
WORKDIR /app
COPY --from=builder --chown=app /app/dist ./dist
COPY --from=builder --chown=app /app/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK CMD node healthcheck.js
CMD ["node", "dist/main.js"]
```

## Deployment Strategies

| Strategy | Use Case | Rollback |
|----------|----------|----------|
| Rolling | Default, gradual | `kubectl rollout undo` |
| Blue-Green | Quick switch, validation period | Switch service back |
| Canary | Risk mitigation, A/B testing | Route 100% to stable |

## Kubernetes Essentials

### Production Deployment Checklist
- [ ] Resource requests and limits defined
- [ ] Liveness and readiness probes
- [ ] Security context (non-root, read-only)
- [ ] Pod anti-affinity for HA
- [ ] HPA for auto-scaling
- [ ] PDB for availability during updates
- [ ] Secrets from external manager

### Key Resources
```yaml
# Deployment with probes
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 10
```

## Infrastructure as Code

### Terraform Best Practices
- Use modules for reusable components
- Remote state with locking
- Input validation on variables
- Semantic versioning for modules
- Consistent naming conventions
- Document all outputs

### Module Structure
```
modules/
  vpc/
    main.tf
    variables.tf
    outputs.tf
```

## Cloud Architecture

### Design Principles
1. **Design for Failure** - Self-healing mechanisms
2. **Security by Design** - Least privilege, encryption
3. **Cost-Conscious** - Right-size, savings plans
4. **Managed Services** - Reduce operational overhead

### HA/DR Patterns
- Multi-AZ for availability
- Multi-region for disaster recovery
- Cross-region backup replication
- DNS-based failover

### Cost Optimization
- Right-sizing based on usage
- Reserved instances/savings plans
- Lifecycle policies for storage
- Auto-scaling to match demand
- Regular unused resource cleanup

## Security Checklist

- [ ] VPC with private subnets
- [ ] Security groups (least privilege)
- [ ] IAM roles (minimal permissions)
- [ ] Encryption at rest and in transit
- [ ] Secrets in dedicated manager
- [ ] Audit logging enabled
- [ ] DDoS protection configured

## Observability

### Metrics to Track
- **RED**: Rate, Errors, Duration
- **USE**: Utilization, Saturation, Errors

### Key Dashboards
- Application performance (latency, errors)
- Infrastructure health (CPU, memory, disk)
- Business metrics (transactions, users)

### Alerting Rules
```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  annotations:
    summary: "Error rate > 5%"
```

## Runbook Template

```markdown
## Deployment Runbook

### Prerequisites
- kubectl access, valid kubeconfig
- Registry credentials
- Monitoring access

### Deploy
1. Merge to main → pipeline triggers
2. Monitor pipeline in CI
3. Verify in monitoring dashboard

### Rollback
kubectl rollout undo deployment/app -n production

### Troubleshooting
- Pods not starting: `kubectl logs -f deployment/app`
- High errors: Check app logs and metrics
```
