---
name: devops
description: CI/CD pipeline design and DevOps practices — GitHub Actions workflows, deployment strategies, infrastructure-as-code patterns, and observability basics.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# devops

CI/CD pipeline design and DevOps practices — GitHub Actions workflows, deployment strategies, infrastructure-as-code patterns, and observability basics.

## Instructions

Apply these DevOps practices when building pipelines and infrastructure:

### CI/CD Pipeline Design

Every repository should have at minimum:
1. **CI pipeline** (on every push/PR): lint → test → build → security scan
2. **CD pipeline** (on merge to main): build image → push to registry → deploy to staging → (manual gate) → deploy to production

**GitHub Actions CI template:**
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build

      - name: Scan for vulnerabilities
        run: npx audit-ci --moderate
```

### Deployment Strategies

**Rolling deployment** (default for Kubernetes): gradually replace old pods with new ones. Zero downtime; easy rollback.

**Blue/Green deployment**: two identical environments; switch traffic atomically. Instant rollback; requires 2x infrastructure.

**Canary deployment**: route a small % of traffic to the new version first. Validate metrics before full rollout. Best for high-traffic, risk-sensitive services.

**Feature flags**: deploy code without activating features. Decouple deployment from release.

### Environment Promotion

```
dev → staging → production
```

- `dev`: every merge to `main`; auto-deploy; no manual gate
- `staging`: every merge to `main` or release branch; smoke tests; auto-deploy
- `production`: tagged release or manual approval; requires staging green

### Infrastructure as Code

- Manage all infrastructure with code (Terraform, Pulumi, CDK)
- Store state remotely (S3 + DynamoDB lock, Terraform Cloud)
- Review infrastructure changes in PRs just like application code
- Use modules/components for reusable patterns

```hcl
# Terraform: always pin provider versions
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

### Secrets in CI/CD

- Store secrets in GitHub Actions secrets or the `copilot` environment
- Never echo secrets in logs — mask with `::add-mask::`
- Use OIDC-based authentication (not long-lived credentials) for cloud providers:

```yaml
- name: Configure AWS credentials via OIDC
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
    aws-region: eu-west-1
```

### Observability

Every service should expose:
- **Metrics**: request rate, error rate, latency (RED metrics); resource usage (CPU, memory)
- **Logs**: structured JSON logs with `timestamp`, `level`, `service`, `trace_id`
- **Traces**: distributed tracing via OpenTelemetry

**Alerting rules:**
- Error rate > 1% for 5 minutes → PagerDuty alert
- P99 latency > 2s for 10 minutes → Slack warning
- Pod restarts > 3 in 15 minutes → incident

### Healthchecks

Every service must expose:
- `GET /healthz` (liveness) – returns 200 if process is running
- `GET /readyz` (readiness) – returns 200 only when ready to serve traffic

## Examples

```bash
# Run a GitHub Actions workflow locally with act
act push -j ci

# Terraform plan with remote state
terraform init && terraform plan -out=tfplan

# Deploy a Helm chart with a canary strategy
helm upgrade --install myapp ./charts/myapp \
  --set image.tag=a1b2c3d \
  --set canary.enabled=true \
  --set canary.weight=10

# Check rollout status
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp  # rollback
```

## References

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [OpenTelemetry](https://opentelemetry.io/)
- [Terraform best practices](https://www.terraform-best-practices.com/)
- [The Twelve-Factor App](https://12factor.net/)
- [DORA metrics](https://dora.dev/)
