---
name: devops-patterns
description: >
  DevOps and cloud infrastructure patterns for Terraform, Kubernetes, Docker, and CI/CD.
  Use when writing infrastructure code, configuring deployments, or setting up pipelines.
---

# devops-patterns

DevOps and cloud infrastructure patterns.

## how to use

- `/devops-patterns`
  Apply these infrastructure patterns to all DevOps work in this conversation.

- `/devops-patterns <context>`
  Review the context against rules below and suggest improvements.

## when to apply

Reference these guidelines when:
- writing Terraform modules or managing state
- configuring Kubernetes resources
- writing Dockerfiles or Docker Compose
- setting up CI/CD pipelines (GitHub Actions)
- managing secrets in infrastructure
- configuring monitoring and alerting

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | infrastructure as code | critical |
| 2 | container best practices | critical |
| 3 | Kubernetes patterns | high |
| 4 | CI/CD pipelines | high |
| 5 | secrets management | critical |
| 6 | monitoring | medium |

## quick reference

### 1. infrastructure as code (critical)

**Terraform**:
- use modules for reusable components; keep modules small and focused
- remote state with locking (S3 + DynamoDB, Terraform Cloud)
- separate state per environment (dev/staging/prod)
- use `terraform plan` before every `apply`; review changes
- pin provider versions: `required_providers { aws = { version = "~> 5.0" } }`
- use `data` sources to reference existing resources; never hardcode IDs
- tag all resources with: environment, project, owner, managed-by
- use `terraform fmt` and `terraform validate` in CI
- keep sensitive values in `terraform.tfvars` (gitignored) or secrets manager
- use workspaces sparingly; prefer separate state files per environment

**Structure**:
```
modules/
  <module-name>/
    main.tf
    variables.tf
    outputs.tf
environments/
  dev/
    main.tf      # calls modules
    terraform.tfvars
  prod/
    main.tf
    terraform.tfvars
```

### 2. container best practices (critical)

- use multi-stage builds to minimize image size
- pin base image versions with SHA digest
- run as non-root user (`USER 1001`)
- one process per container
- use `.dockerignore` to exclude unnecessary files
- order Dockerfile layers for cache efficiency (dependencies before code)
- scan images for vulnerabilities in CI (trivy, snyk)
- set resource limits (memory, CPU)
- use health checks
- prefer COPY over ADD
- never store secrets in images; use runtime injection

**Multi-stage template**:
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER 1001
EXPOSE 3000
HEALTHCHECK CMD wget -q --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### 3. Kubernetes patterns (high)

- always set resource requests AND limits
- use liveness, readiness, and startup probes
- use namespaces for environment separation
- use RBAC with least-privilege service accounts
- store config in ConfigMaps, secrets in Secrets (or external secrets operator)
- use Deployments for stateless, StatefulSets for stateful workloads
- set Pod Disruption Budgets for availability
- use horizontal pod autoscaler (HPA) for scaling
- use network policies to restrict pod-to-pod traffic
- prefer rolling updates; set maxSurge and maxUnavailable

**Resource template**:
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 4. CI/CD pipelines (high)

**GitHub Actions**:
- pin action versions with SHA: `uses: actions/checkout@<sha>`
- use `concurrency` to cancel outdated runs
- cache dependencies (node_modules, pip cache, Docker layers)
- separate build, test, and deploy jobs
- use environment protection rules for production deploys
- store secrets in GitHub Secrets; never in workflow files
- use matrix builds for multi-version testing
- fail fast on lint/type errors before running tests
- use OIDC for cloud provider authentication (no long-lived keys)

**Pipeline stages**:
1. Lint + format check
2. Type check
3. Unit tests
4. Build
5. Integration tests
6. Security scan
7. Deploy to staging
8. E2E tests on staging
9. Deploy to production (manual approval)

### 5. secrets management (critical)

**Hierarchy** (most to least preferred):
1. Cloud secrets manager (AWS Secrets Manager, GCP Secret Manager)
2. External secrets operator (K8s)
3. CI/CD platform secrets (GitHub Secrets)
4. Encrypted files (SOPS, age)
5. Environment variables (acceptable for non-sensitive config)
6. Hardcoded values (NEVER for secrets)

- rotate secrets regularly; automate rotation where possible
- audit secret access
- separate secrets by environment
- use short-lived credentials (OIDC, STS) over long-lived keys

### 6. monitoring (medium)

- instrument with metrics (Prometheus), logs (structured JSON), and traces (OpenTelemetry)
- define SLIs and SLOs for critical services
- alert on symptoms (error rate, latency), not causes
- use dashboards for context, not primary alerting
- implement health check endpoints for all services
- monitor resource utilization and cost
- set up on-call rotation and escalation policies

## common fixes

| problem | fix |
|---------|-----|
| Terraform state drift | `terraform plan` to detect, `terraform import` for unmanaged resources |
| Large Docker image | use multi-stage build, alpine base, .dockerignore |
| Pod CrashLoopBackOff | check logs, verify resource limits, check probes |
| Slow CI pipeline | cache dependencies, parallelize jobs, fail fast |
| Secret in git history | rotate immediately, use git-filter-repo to purge |
| OOM killed pod | increase memory limit or optimize application |

## CI/CD best practices (from CI/CD handbook patterns)

### GitHub Actions Advanced Patterns

**Reusable Workflows**:
```yaml
# .github/workflows/reusable-deploy.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      AWS_ROLE_ARN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    permissions:
      id-token: write  # OIDC
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@<sha>
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
```

**Composite Actions** (reusable steps):
```yaml
# .github/actions/setup-project/action.yml
name: Setup Project
runs:
  using: composite
  steps:
    - uses: actions/setup-python@<sha>
      with:
        python-version: '3.11'
    - run: pip install uv && uv sync
      shell: bash
```

**Matrix Strategies**:
```yaml
strategy:
  fail-fast: false
  matrix:
    python: ['3.10', '3.11', '3.12']
    os: [ubuntu-latest, macos-latest]
    exclude:
      - python: '3.10'
        os: macos-latest
```

### Pipeline Optimization Techniques
| Technique | Savings | How |
|-----------|---------|-----|
| Dependency caching | 30-60s | `actions/cache` with hash key |
| Docker layer caching | 1-3min | `docker/build-push-action` with cache |
| Parallel jobs | 40-60% | Split tests, lint independently |
| Conditional runs | Variable | `if: github.event_name == 'push'` |
| Artifact reuse | 30-60s | Build once, deploy to multiple envs |
| Path filters | Variable | Only run when relevant files change |

## cross-references

- **security-review** skill: CI/CD security rules
- **DEVOPS_TOOLKIT.md**: Infrastructure tools reference
- **SECURITY_ARSENAL.md**: CI/CD security checklist
