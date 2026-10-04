---
name: infra-kit.domain.iac
description: Create, review, validate, refactor, or troubleshoot Infrastructure-as-Code using Terraform and/or Terragrunt (modules, stacks, layouts, remote state, dependency wiring).
---

# IaC (Terraform + Terragrunt)

Use this skill when the work item will be implemented in Terraform and/or orchestrated via Terragrunt.

This is the unified IaC entrypoint for Terraform and Terragrunt.

## Outcomes

- Scaffold or refactor readable, reusable Terraform modules and stacks
- Design or fix Terragrunt layouts, includes, dependencies, and remote state conventions
- Review IaC for correctness, destructive change risk, and security gaps
- Fix validation failures and broken wiring across environments

## Workflow

1. Inspect the repository layout before changing files.
2. Identify what is actually in use:
   - Terraform-only
   - Terragrunt orchestrating Terraform/OpenTofu modules
3. Establish constraints:
   - cloud/provider(s)
   - environment model (dev/stage/prod)
   - backend/remote state strategy
   - naming + tag/label contract
4. Implement with the smallest correct change.
5. Validate with the strongest deterministic checks available.

## Terraform Authoring Notes

- Prefer explicit `required_version` and `required_providers`.
- Keep modules reusable: typed variables, useful descriptions, stable outputs.
- Use `locals` for repeated naming/tagging.
- Default IAM to least privilege unless the user explicitly accepts broader rights.
- Avoid secrets in code or example tfvars.

## Terragrunt Authoring Notes

- Inspect `include`/`find_in_parent_folders`/`read_terragrunt_config` paths from the caller’s file.
- Keep shared config centralized (often `root.hcl`) and push env-specific values to env layers.
- Use `dependency` blocks for real data flow and ordering.
- Treat `run --all` blast radius as a first-class risk.

## Hallucination Guardrails

- Don’t guess provider args, module outputs, or Terragrunt paths. Inspect files and cite them.
- When provider/module docs are needed, look up the official documentation (and mention version).
- List every command you actually ran; if skipped, state the blocker.

## Validation Loop

Prefer repo tooling first. Otherwise use the strongest available subset:

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan

terragrunt hcl fmt
terragrunt init
terragrunt validate
terragrunt plan
```

Bundled helpers:

```bash
bash scripts/validate_iac.sh <path>
```

## Delivery Standard

Always leave the user with:

- the files changed (or the recommended layout)
- key assumptions (backend/state, accounts/regions, env model)
- validation commands run
- unresolved risks (especially destructive changes and state interactions)
