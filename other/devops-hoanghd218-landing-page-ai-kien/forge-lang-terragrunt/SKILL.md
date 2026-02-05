---
name: forge-lang-terragrunt
description: Terragrunt wrapper for Terraform with DRY configurations. Enforces plan-before-apply workflow. Use when working with terragrunt.hcl files.
---

# Terragrunt Development

## Safety Rules

**NEVER run without user confirmation:**
- `terragrunt apply`
- `terragrunt destroy`
- `terragrunt run-all apply`
- `terragrunt run-all destroy`

**ALWAYS run first:**
- `terragrunt plan`
- `terragrunt validate`

## Workflow

```
┌────────────────────────────────────────────────────────┐
│  VALIDATE → PLAN → REVIEW → APPLY                     │
└────────────────────────────────────────────────────────┘
```

### Step 1: Validate

```bash
terragrunt validate
terragrunt hclfmt --check
```

### Step 2: Plan

```bash
# Single module
terragrunt plan

# All modules (be careful!)
terragrunt run-all plan
```

**Show plan to user and wait for confirmation.**

### Step 3: Apply (only after explicit approval)

```bash
terragrunt apply
```

## Linting

```bash
# Format check
terragrunt hclfmt --check

# Format and fix
terragrunt hclfmt

# Validate all
terragrunt run-all validate
```

## Project Structure

```
infrastructure/
├── terragrunt.hcl              # Root config
├── _envcommon/                 # Shared configs
│   └── vpc.hcl
├── prod/
│   ├── env.hcl
│   ├── vpc/
│   │   └── terragrunt.hcl
│   └── eks/
│       └── terragrunt.hcl
├── staging/
│   ├── env.hcl
│   └── vpc/
│       └── terragrunt.hcl
└── modules/                    # Terraform modules
    └── vpc/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

## Root terragrunt.hcl Template

```hcl
# Root terragrunt.hcl

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "my-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = var.aws_region
}
EOF
}
```

## Pre-Apply Checklist

```
Terragrunt Checklist:
- [ ] terragrunt validate passed
- [ ] terragrunt hclfmt --check passed
- [ ] terragrunt plan reviewed
- [ ] Dependencies understood
- [ ] User confirmed changes
- [ ] Ready to apply
```

## run-all Safety

When using `run-all`:
- Always review dependency graph first
- Use `--terragrunt-parallelism 1` for safer execution
- Consider `--terragrunt-exclude-dir` for sensitive paths

```bash
# Show dependency graph
terragrunt graph-dependencies

# Plan all with limited parallelism
terragrunt run-all plan --terragrunt-parallelism 1
```
