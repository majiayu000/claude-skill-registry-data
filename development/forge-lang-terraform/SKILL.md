---
name: forge-lang-terraform
description: Terraform infrastructure-as-code safety practices. Enforces plan-before-apply workflow. Use when working with .tf files or infrastructure commands.
---

# Terraform Development

## Safety Rules

**NEVER run without user confirmation:**
- `terraform apply`
- `terraform destroy`
- `terraform import`

**ALWAYS run first:**
- `terraform plan`
- `terraform validate`

## Workflow

```
┌────────────────────────────────────────────────┐
│  VALIDATE → PLAN → REVIEW → APPLY             │
└────────────────────────────────────────────────┘
```

### Step 1: Validate

```bash
terraform init
terraform validate
terraform fmt -check
```

### Step 2: Plan

```bash
terraform plan -out=tfplan
```

**Show plan to user and wait for confirmation.**

### Step 3: Apply (only after explicit approval)

```bash
terraform apply tfplan
```

## Linting

```bash
# Format check
terraform fmt -check -recursive

# TFLint
tflint --recursive

# Checkov security scanning
checkov -d .
```

## Project Structure

```
project/
├── main.tf
├── variables.tf
├── outputs.tf
├── versions.tf
├── terraform.tfvars.example
├── modules/
│   └── module_name/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── README.md
```

## Pre-Apply Checklist

```
Terraform Checklist:
- [ ] terraform init completed
- [ ] terraform validate passed
- [ ] terraform fmt -check passed
- [ ] tflint passed (if available)
- [ ] terraform plan reviewed
- [ ] User confirmed changes
- [ ] Ready to apply
```

## State Safety

- Never edit terraform.tfstate manually
- Always use `terraform state` commands
- Back up state before imports
- Use remote state with locking

## Scripts

Validate before plan:

```bash
~/.claude/skills/languages/terraform/scripts/plan-check.sh
```
