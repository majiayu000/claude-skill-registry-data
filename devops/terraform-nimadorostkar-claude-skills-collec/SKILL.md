---
name: terraform
description: Use when managing infrastructure as code with Terraform or OpenTofu. Covers module design, state management, drift, plan review, secrets, and applying changes without destroying production.
metadata:
  category: devops
  version: 1.0.0
  tags: [terraform, iac, opentofu, state, modules]
---

# Terraform

## Purpose

Manage infrastructure declaratively without the two events that define bad Terraform experiences: a plan nobody read that destroyed a database, and a state file that no longer matches reality.

## When to Use

- Writing or reviewing Terraform configuration.
- Structuring modules and environments.
- Reviewing a plan before an apply that touches production.
- Recovering from state drift or a corrupted state file.

## Capabilities

- Module design with clear inputs, outputs, and versioning.
- Remote state with locking, and workspace or directory-based environment separation.
- Plan review, including recognizing a destructive change before it runs.
- Import and drift reconciliation.
- Secrets handling that keeps values out of state where possible.

## Inputs

- The existing configuration and state.
- The target environment and its blast radius.
- The plan output — always read before an apply.

## Outputs

- Modules that are reusable and versioned.
- Remote state, locked, encrypted, and backed up.
- A reviewed plan with any resource replacement explicitly acknowledged.

## Workflow

1. **Separate environments physically** — Separate state files and separate directories or workspaces. A single state containing dev and prod is one typo away from an incident.
2. **Write modules with a narrow interface** — Inputs that are actually variable, outputs that consumers need. A module with forty variables is a wrapper, not an abstraction.
3. **Plan and read the plan** — Every `-/+` is a destroy and recreate. On a database, a load balancer, or anything holding state, that is an outage. Never approve a plan you have not read line by line.
4. **Lock the state** — Remote backend with locking (S3 + DynamoDB, or the equivalent). Two concurrent applies against unlocked state will corrupt it.
5. **Pin everything** — Provider versions, module versions, and the Terraform version itself. An unpinned provider will change behavior underneath you on an unrelated day.
6. **Reconcile drift explicitly** — Manual changes happen. `terraform plan` shows them; decide to import, adopt, or revert. Ignoring drift means the next apply reverts someone's emergency fix.

## Best Practices

- `prevent_destroy` on stateful resources — databases, buckets, DNS zones. It converts a catastrophic mistake into an error message.
- Never commit `.tfstate`. It contains secrets in plaintext, regardless of how they entered.
- `terraform apply` without a saved plan file re-plans, which means what you apply is not necessarily what you reviewed. Use `terraform plan -out=tfplan` and apply the file.
- Avoid `count` for resources that may be reordered; use `for_each` with a stable key. `count` reindexes, and reindexing destroys and recreates.
- Do not use Terraform to manage application deployment. It is a poor fit for anything that changes more than a few times a day.
- Secrets belong in a secret manager, referenced by ARN or path. Anything passed as a variable ends up in state.

## Examples

**A module interface that is actually reusable:**

```hcl
# modules/postgres/variables.tf
variable "name"              { type = string }
variable "environment"       { type = string }
variable "instance_class"    { type = string, default = "db.t4g.medium" }
variable "allocated_storage" { type = number, default = 50 }
variable "subnet_ids"        { type = list(string) }

# modules/postgres/main.tf
resource "aws_db_instance" "this" {
  identifier            = "${var.name}-${var.environment}"
  engine                = "postgres"
  engine_version        = "16.3"
  instance_class        = var.instance_class
  allocated_storage     = var.allocated_storage
  storage_encrypted     = true
  deletion_protection   = var.environment == "prod"
  backup_retention_period = var.environment == "prod" ? 30 : 1

  # Password comes from Secrets Manager; it never appears in a .tfvars file.
  manage_master_user_password = true

  lifecycle {
    prevent_destroy = true            # a plan that would destroy this now fails
    ignore_changes  = [engine_version] # minor upgrades are applied by AWS, not us
  }
}
```

**Reading a plan for the change that matters:**

```text
# aws_db_instance.this must be replaced
-/+ resource "aws_db_instance" "this" {
      ~ availability_zone = "eu-west-1a" -> "eu-west-1b" # forces replacement
```

`forces replacement` on a database means: destroy the database, create a new empty one. This plan must never be applied. The correct response is to revert the change, not to approve and hope.

## Notes

- `terraform state mv` and `terraform import` are the tools for reconciling reality with configuration. Both are safe operations on the state file — but back the state up first, always.
- OpenTofu is a drop-in fork of Terraform 1.5 and diverges gradually. Configuration written for either works on the other today; pin the binary and be explicit about which you use.
- A `terraform destroy` in the wrong directory has ended careers. `prevent_destroy` and separate credentials per environment are cheap insurance.
