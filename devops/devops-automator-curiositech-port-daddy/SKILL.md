---
license: Apache-2.0
name: devops-automator
description: 'Expert DevOps engineer for CI/CD, IaC, Kubernetes, and deployment automation. Activate on: CI/CD, GitHub Actions, Terraform, Docker, Kubernetes, Helm, ArgoCD, GitOps, deployment pipeline, infrastructure as code, container orchestration. NOT for: application code (use language skills), database schema (use data-pipeline-engineer), API design (use api-architect).'
allowed-tools: Read,Write,Edit,Bash(docker:*,kubectl:*,terraform:*,helm:*,gh:*)
category: DevOps & Infrastructure
tags:
  - ci-cd
  - terraform
  - docker
  - kubernetes
  - gitops
pairs-with:
  - skill: site-reliability-engineer
    reason: Ensure deployed code is healthy
  - skill: security-auditor
    reason: Secure the deployment pipeline
---

# DevOps Automator

Expert DevOps engineer for CI/CD pipelines, infrastructure as code, and deployment automation.

## DECISION POINTS

### Deployment Strategy Selection

**IF production service with >1000 RPS AND downtime SLA <1min:**
→ Blue/Green deployment (zero downtime, instant rollback, 2x resources)

**ELSE IF gradual rollout required OR resource constraints exist:**
→ Canary deployment (5%→25%→100%, traffic-based validation, cost-efficient)

**ELSE IF simple application OR development environment:**
→ Rolling update (sequential replacement, K8s default, minimal resources)

### Infrastructure Provisioning Choice

**IF cloud resources (VPC, RDS, ELB) needed:**
→ Use Terraform with remote state backend
  ├─ IF team <5 people: Terraform Cloud free tier
  └─ IF enterprise: S3 + DynamoDB state locking

**ELSE IF only Kubernetes applications:**
→ Use Helm charts with ArgoCD GitOps
  ├─ IF complex config variations: Kustomize overlays
  └─ IF simple deployments: Plain K8s manifests

### CI Pipeline Architecture

**IF monorepo with multiple services:**
→ Path-based triggers with parallel jobs
```
changes:
  - 'frontend/**' → frontend-ci.yml
  - 'backend/**' → backend-ci.yml
  - 'shared/**' → full-rebuild.yml
```

**ELSE IF frequent commits (>10/day per service):**
→ Matrix builds with aggressive caching
```
strategy:
  matrix:
    service: [api, web, worker]
    include:
      - service: api
        dockerfile: ./api/Dockerfile
        context: ./api
```

**ELSE IF infrequent updates (<5/week):**
→ Simple linear pipeline with full build

## FAILURE MODES

### Schema Bloat
**Detection:** Terraform plan shows >50 resources for simple app deployment
**Symptom:** `terraform plan` takes >2min, state file >500KB for basic infrastructure
**Fix:** Split into focused modules (network, compute, storage), use data sources to reference existing resources

### Rubber Stamp Review
**Detection:** CI passes but deployment fails with "connection refused" or "image not found"
**Symptom:** Green checkmarks everywhere but service is down in production
**Fix:** Add smoke tests after deployment, implement health check validation gates

### Secret Sprawl
**Detection:** `grep -r "password\|api_key" .` returns hits in committed files
**Symptom:** Secrets hardcoded in YAML, env files committed to git
**Fix:** External secret operators (ESO), sealed-secrets, or cloud secret managers

### Pipeline Deadlock
**Detection:** Multiple commits queued, jobs stuck in "pending" state >10min
**Symptom:** `github.event_name == 'push'` triggers overlapping workflow runs
**Fix:** Add concurrency groups with auto-cancel-in-progress

### Resource Starvation
**Detection:** `kubectl top pods` shows pods with no CPU/memory limits consuming >80% node capacity
**Symptom:** Pod evictions, OOMKilled containers, slow application response
**Fix:** Set requests/limits for all containers, implement LimitRanges

## WORKED EXAMPLES

### Example 1: E-commerce API Canary Deployment

**Context:** Production API serving 500 RPS, needs feature flag rollout

**Decision Tree Navigation:**
- Traffic volume (500 RPS) → Canary deployment chosen
- Critical service → Blue/Green rejected (too expensive for gradual test)
- Need traffic analysis → Istio traffic splitting selected

**Implementation:**
```yaml
# ArgoCD Rollout with traffic analysis
spec:
  strategy:
    canary:
      steps:
      - setWeight: 5
      - analysis:
          templates:
          - templateName: error-rate
          args:
          - name: service-name
            value: api-service
      - setWeight: 25
      - pause: duration: 10m
      - setWeight: 100
```

**Trade-off Analysis:**
- Cost: 105-125% of baseline (vs 200% for blue/green)
- Risk: Gradual exposure limits blast radius
- Rollback: 30s vs 5s for blue/green
- Complexity: Requires service mesh + monitoring

### Example 2: Multi-Environment Terraform Module

**Context:** Need identical infrastructure for dev/staging/prod with different sizing

**Decision Process:**
- Shared configuration patterns → Terraform modules
- Environment-specific values → workspace variables
- State isolation required → Separate backends per env

**Module Structure:**
```hcl
# modules/eks-cluster/main.tf
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  version  = var.k8s_version
  
  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# environments/prod/main.tf
module "eks" {
  source = "../../modules/eks-cluster"
  
  cluster_name = "prod-cluster"
  instance_type = "m5.large"  # vs t3.micro for dev
  min_size = 3                # vs 1 for dev
}
```

**Validation Gates:**
- `terraform validate` passes
- `checkov` security scan clean
- Cost estimation under budget threshold

### Example 3: GitHub Actions Security Pipeline

**Context:** Node.js app needs security scanning before production deploy

**Pipeline Design Decision:**
```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run Trivy scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        exit-code: '1'  # Fail on high/critical vulnerabilities
        
  deploy:
    needs: [security, test]  # Block deployment on security issues
    if: github.ref == 'refs/heads/main'
```

**Trade-offs Considered:**
- Block vs warn: Chose block for prod, warn for feature branches
- Scan scope: Full filesystem vs dependencies only (chose dependencies for speed)
- Vulnerability threshold: High/Critical vs Medium+ (chose High/Critical to reduce noise)

## QUALITY GATES

- [ ] All container images use specific version tags (no :latest in production)
- [ ] Every Kubernetes workload has resource requests and limits defined
- [ ] CI pipeline fails if security scan finds high/critical vulnerabilities
- [ ] Terraform state is stored in remote backend with state locking enabled
- [ ] All secrets are externalized (no hardcoded values in manifests)
- [ ] Health checks (liveness/readiness probes) configured for all services
- [ ] Deployment strategy supports rollback within 5 minutes
- [ ] Infrastructure changes require successful `terraform plan` before merge
- [ ] Container images run as non-root user (securityContext.runAsNonRoot: true)
- [ ] Monitoring alerts are configured for deployment success/failure rates

## NOT-FOR BOUNDARIES

**This skill should NOT be used for:**
- **Application code development** → Use language-specific skills (typescript-expert, python-developer)
- **Database schema design** → Use `data-pipeline-engineer` for data modeling
- **API endpoint design** → Use `api-architect` for REST/GraphQL specification
- **Frontend build optimization** → Use `frontend-architect` for webpack/bundling
- **Performance testing** → Use `site-reliability-engineer` for load testing strategies
- **Security vulnerability remediation** → Use `security-auditor` for code-level security fixes

**Delegation patterns:**
- Infrastructure setup (DevOps) → Application logic (language skills)
- CI/CD pipeline (DevOps) → Code review/testing (language skills)  
- Deployment automation (DevOps) → Performance monitoring (SRE)