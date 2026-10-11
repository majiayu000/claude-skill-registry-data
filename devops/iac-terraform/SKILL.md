---
name: iac-terraform
description: Terraform/OpenTofu — remote state, modules, CI/CD, drift detection.
---

# Infrastructure as Code — Terraform / OpenTofu

## Core Principle

IaC is code. It lives in git, gets reviewed in PRs, runs in CI, and never has secrets hardcoded in it. State is shared and locked.

> OpenTofu is a drop-in open-source alternative to Terraform. All patterns here apply to both.

---

## Detection Signals

| Signal | Location |
|--------|----------|
| `*.tf` files | `infra/` or repo root |
| `terraform.tfvars` | environment directories |
| `.terraform.lock.hcl` | environment directories |
| `hashicorp/setup-terraform` | CI/CD pipeline files |
| `TF_VAR_*` env vars | `.env`, CI secrets |

---

## Core Workflow

```bash
terraform init      # initialize backend and download providers
terraform validate  # check syntax and provider references
terraform plan      # preview changes — always review before apply
terraform apply     # apply changes (never skip plan in production)
terraform destroy   # destroy resources (requires explicit approval)
```

**Never run `apply` without reviewing `plan` output in production.**

---

## Key Rules (apply always)

| Rule | Detail |
|------|--------|
| Remote state | Always use remote backend with locking — never local state in teams |
| Secrets | Use cloud secret manager data sources — never in `.tfvars` or `-var` flags |
| Modules | Create when same resources used in 2+ environments |
| Version pins | Pin module versions via git tags; pin provider versions in `required_providers` |
| `for_each` over `count` | Use `for_each` with maps for resources that differ significantly |
| CI apply gates | Manual approval required for production environments |

Load `references/patterns.md` for: full project structure, remote state backend configs (AWS/GCP/Azure), module patterns, variable validation, secrets data sources, import commands, and anti-patterns.

Load `references/ci-cd.md` for: GitHub Actions plan/apply/drift-detection workflows, GitLab CI plan+apply pipeline, environment promotion pattern.

---

## `.gitignore` Requirements

```
*.tfstate
*.tfstate.backup
.terraform/
*.tfplan
```

---

## Before Declaring Done

- [ ] Remote backend configured with state locking (S3+DynamoDB, GCS, or Azure Blob)
- [ ] State bucket has versioning enabled (allows rollback)
- [ ] No secrets in `.tfvars` or passed via `-var` — all secrets use data sources
- [ ] `terraform validate` passes in CI on every PR
- [ ] `terraform plan` output posted to PR for review
- [ ] `terraform apply` requires manual approval for production environment
- [ ] Drift detection scheduled (weekly minimum)
- [ ] `.gitignore` includes `*.tfstate`, `.terraform/`, `*.tfplan`
- [ ] Modules versioned via git tags if shared across repos
