---
name: do-terraform
version: 1.0.0
description: Write or review Terraform with clean versioned modules, locked remote state, drift detection, and disciplined plan review before apply.
author: matrixx0070
tags: [terraform, iac, devops, cloud, review, state]
capabilities: []
---

# do-terraform

## When to use

You need to author infrastructure-as-code, refactor sprawling configs into modules, set up remote state, investigate drift, or review a `terraform plan` before apply.

**Not for:** Kubernetes workload manifests (use do-kubernetes), CI that runs the plan/apply (use do-ci-pipeline), or the production cutover procedure (use do-release-checklist).

## Method

1. Structure code: reusable modules with explicit `variables.tf`/`outputs.tf`, thin root configs per environment, and pinned provider and module versions.
2. Configure remote state with locking (S3+DynamoDB, GCS, or Terraform Cloud). Decision: isolate state per environment to limit blast radius; never commit state or secrets.
3. Keep resources declarative and idempotent. Decision: prefer `for_each` over `count` so removing one element does not re-index and recreate the others; use `data` sources instead of hardcoded IDs.
4. Detect drift with `terraform plan -detailed-exitcode` on a schedule. Decision: reconcile by `import` or by correcting config — never by manual console edits, which re-introduce drift.
5. Review every plan: read `+`/`~`/`-` symbols, flag any destroy-then-create on stateful resources, check for unintended replacements, and confirm secret values are not printed.
6. Gate apply behind CI with a saved plan artifact so the reviewed plan is the applied plan.

## Example

```hcl
# for_each gives stable addressing: removing "web" leaves "api" untouched
variable "buckets" {
  type    = set(string)
  default = ["web", "api"]
}

resource "aws_s3_bucket" "this" {
  for_each = var.buckets
  bucket   = "acme-${terraform.workspace}-${each.key}"
}

terraform {
  required_version = ">= 1.6"
  backend "s3" {
    bucket         = "acme-tfstate"
    key            = "prod/app.tfstate"   # isolated per env
    dynamodb_table = "tf-locks"           # state locking
    encrypt        = true
  }
}
```

## Pitfalls

- `count` on a list where you delete a middle element — Terraform re-indexes and destroys/recreates every resource after it.
- Local or committed state, so two engineers apply concurrently and corrupt it (no lock).
- Fixing drift by hand in the cloud console; the next plan wants to revert your fix, or silently overwrites it.
- Skimming a plan and missing a `-/+` replacement on a database or volume — that is data loss, not an update.

## Output format

```
Layout: module/ and root file tree, key .tf snippets.
Backend: remote state + locking config.

Plan review:
- adds:      <n>
- changes:   <n>
- destroys:  <n>
- HIGH RISK: <resource> replaced (destroy-then-create on stateful) — call out explicitly
```
