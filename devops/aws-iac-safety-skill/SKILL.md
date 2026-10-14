---
name: aws-iac-safety-skill
description: >-
  AWS IaC safety patterns — resource count gating, SSM CI passthrough, ECR
  lifecycle ownership, SSM_SECRETS_REFERENCE, Lambda Web Adapter dual-target.
license: Apache-2.0
compatibility: opencode
category: DevOps
---

<!-- Provenance: canvastekk-devops + canvastekk-floor-flatness-app LEARNINGS. PLAN-GIT-312. Excludes: Lambda CNAME, GHA artifact mismatch, Lambda public auth, ECR lowercase, local TF state, no-rollback (all in other skills). -->

## What I do

I provide safety patterns for AWS Infrastructure-as-Code (Terraform/OpenTofu) and GitHub Actions CI/CD, extracted from production incidents. Each pattern caused a real outage or security issue.

## When to use me

Use this skill when:
- Writing or reviewing Terraform/OpenTofu modules managing GitHub or AWS resources
- Setting up multi-environment CI/CD with SSM parameters
- Managing ECR repositories across multiple modules
- Deploying the same Docker image to both EC2 and Lambda
- Auditing IaC for cross-module ownership violations

## Related Skills

- **civiltekk-opentofu-skill** (route `explore`, AWS section): AWS resource discovery (Lambda Function URL CNAME pattern).
- **security-audit-skill**: Security auditing (Lambda public-without-auth, local Terraform state patterns).
- **docker-containerization-skill**: Docker patterns (no-rollback-on-deploy pattern).

---

## A. GitHub Resource Management

### A1. Repo-Level GitHub Resources Without Count Gating

GitHub repo-level variables/secrets are **singular** — one per name, shared across environments. Without `count` gating, non-dev environments attempt to create resources that already exist, triggering HTTP 422 conflicts.

```hcl
# BAD — creates in ALL environments, 422 on non-dev
resource "github_actions_variable" "registry_token" {
  repository = var.repo_name
  variable_name  = "REGISTRY_TOKEN"
  variable_value = var.registry_token
}

# GOOD — only dev creates repo-level resources
resource "github_actions_variable" "registry_token" {
  count          = var.environment == "dev" ? 1 : 0
  repository     = var.repo_name
  variable_name  = "REGISTRY_TOKEN"
  variable_value = var.registry_token
}
```

**Gotcha:** The CI `cleanup-resources` mechanism uses `tofu state rm` (not `import`). After `state rm`, OpenTofu sees no state for the resource and attempts `CREATE` on the next plan — triggering the 422 again. The fix is count-gating, not state manipulation.

---

## B. SSM Parameter Management

### B1. Hardcoded Dev SSM Path via CI Variable

Passing the full SSM path as a `TF_VAR_*` via GitHub Actions CI hardcodes the dev path. All environments receive the dev token, causing cross-env auth failures (HTTP 401 in UAT/prod).

```hcl
# BAD — CI passes TF_VAR_registry_ssm_parameter="/<org>/<service>/dev/..."
variable "registry_ssm_parameter" {
  type = string
}
data "aws_ssm_parameter" "registry_token" {
  name = var.registry_ssm_parameter
}

# GOOD — derive path locally from var.environment; remove the variable + CI TF_VAR line
locals {
  ssm_path = "/<org>/<service>/${var.environment}/registry-service-token"
}
data "aws_ssm_parameter" "registry_token" {
  name = local.ssm_path
}
```

**Detection:** Search for modules with both `variable "*_ssm_parameter"` AND `TF_VAR_*_ssm_parameter` in CI workflows.

### B2. Update SSM_SECRETS_REFERENCE.md on New Parameters

Every new `aws_ssm_parameter` resource must be documented in `docs/SSM_SECRETS_REFERENCE.md` under the appropriate service section. SSM is the single source of truth for secrets; the reference doc is the human-readable index.

```markdown
<!-- docs/SSM_SECRETS_REFERENCE.md -->

## Workflow Engine

| Parameter | Environment | Description |
|-----------|-------------|-------------|
| `/<org>/<service>/dev/registry-service-token` | dev | ECR auth token |
| `/<org>/<service>/uat/registry-service-token` | uat | ECR auth token |
```

---

## C. ECR Lifecycle Management

### C1. Cross-Module ECR Lifecycle Policy Ownership

AWS allows **only one** lifecycle policy per ECR repo. Creating `aws_ecr_lifecycle_policy` in a consumer module on a repo owned by another module causes silent overwrites and state divergence across environments.

```hcl
# BAD — consumer module manages lifecycle on a repo it doesn't own
data "aws_ecr_repository" "shared" {
  name = var.shared_repo_name
}

resource "aws_ecr_lifecycle_policy" "shared" {
  repository = data.aws_ecr_repository.shared.name
  policy     = jsonencode({ ... })
}

# GOOD — manage lifecycle where the repo is created (owning module)
# Consumer modules use data sources for READ-ONLY references only
```

---

## D. Lambda Deployment

### D1. Lambda Web Adapter for Dual-Target Deployment

Use AWS Lambda Web Adapter (Rust-based extension) over Mangum (Python ASGI wrapper) for zero-code-change deployment of the same FastAPI Docker image to both EC2 (docker-compose) and Lambda. The adapter is inert outside the Lambda runtime environment.

```dockerfile
# Dockerfile — same image works for EC2 and Lambda
FROM python:3.12-slim

# Lambda Web Adapter (harmless on EC2, activated on Lambda)
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 \
     /lambda-adapter /opt/extensions/lambda-adapter

# Standard FastAPI setup
COPY . /app
WORKDIR /app
RUN pip install fastapi uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Operational prerequisites for Lambda:**
- `/tmp` storage: minimum 5 GB
- Timeout: minimum 60s (recommended 120s)
- Memory: minimum 2 GB (recommended 4 GB)
- Provisioned concurrency for production traffic
