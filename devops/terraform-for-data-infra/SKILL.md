---
name: terraform-for-data-infra
description: Provision data infrastructure with Terraform — warehouses, buckets, IAM/roles, orchestration, and streaming resources — using modules, remote state, workspaces/environments, and safe plan/apply workflows. Use when writing Terraform for Snowflake/BigQuery/Redshift, S3/GCS, IAM, Airflow/MWAA, or Kafka, or structuring reusable data-infra modules across environments.
---

# Terraform for Data Infrastructure

## When to use

- Provisioning data platform resources as code (warehouses, buckets, IAM,
  orchestration, streaming).
- Structuring reusable modules and multiple environments (dev/staging/prod).
- Setting up remote state and safe plan/apply workflows.
- Do NOT use for in-warehouse data modeling (use dbt) or app infra unrelated to
  data.

## Workflow

```
- [ ] Use remote state with locking (S3+DynamoDB / GCS / Terraform Cloud)
- [ ] Factor reusable pieces into modules; parameterize per environment
- [ ] Separate environments via workspaces or per-env state, not copy-paste
- [ ] Always review terraform plan before apply
- [ ] Manage least-privilege IAM/roles as code; keep secrets out of state
```

1. **Remote state + locking.** Never keep state locally on a team; use a locked
   remote backend so concurrent applies can't corrupt it.
2. **Modules.** Encapsulate a warehouse, bucket+lifecycle, or role set as a module
   and instantiate it per environment with variables.
3. **Environments.** Use workspaces or separate state per env; keep one codebase,
   varying only inputs — mirrors the "same code, different target" data-CI/CD rule.
4. **Plan before apply.** Review the plan; data resources (warehouses, roles,
   buckets) are high-blast-radius.
5. **Least privilege as code.** Define IAM/roles/grants in Terraform; avoid
   embedding secrets in state.

## Patterns

**Environment via variables + module:**

```hcl
module "warehouse" {
  source        = "./modules/snowflake-warehouse"
  name          = "etl_${var.env}"
  size          = var.env == "prod" ? "LARGE" : "XSMALL"
  auto_suspend  = 60
  auto_resume   = true
}
```

**Remote state backend (S3 + lock table):**

```hcl
terraform {
  backend "s3" {
    bucket         = "acme-tfstate"
    key            = "data/${terraform.workspace}/terraform.tfstate"
    dynamodb_table = "tf-locks"
  }
}
```

**Keep secrets out of state** — source them from a secrets manager
(`aws_secretsmanager_secret_version`, Vault) at apply time; treat state as
sensitive and encrypt the backend.

## Common pitfalls

- **Local state on a team** — lost/corrupted state and drift; use a locked remote
  backend.
- **Copy-pasting per environment** — configs drift; use modules + variables.
- **`apply` without reviewing `plan`** — accidental warehouse resize or role
  deletion.
- **Secrets in variables/state** — plaintext credentials leak; use a secrets
  manager and mark values sensitive.
- **Over-broad IAM** — grant least privilege; wildcards become audit findings.
- **Managing data content in Terraform** — it manages infrastructure, not rows;
  keep data transformations in dbt/pipelines.
