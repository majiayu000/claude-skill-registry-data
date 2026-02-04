---
name: terraform-plan
description: Review Terraform plans and configurations for safety and best practices. Use when the user says "review terraform", "terraform plan", "what will this destroy", "check my infrastructure code", or asks about Terraform changes.
allowed-tools: Bash, Read, Glob, Grep
---

# Terraform Plan Review

Analyze Terraform plans and configurations to prevent destructive changes and ensure best practices.

## Instructions

1. Read relevant `.tf` files to understand the configuration
2. Run `terraform plan` if not already provided
3. Identify destructive operations (destroy, replace)
4. Check for security and best practice issues
5. Summarize changes with risk assessment

## Plan analysis

```bash
# Generate plan
terraform plan -out=tfplan

# Show plan in detail
terraform show tfplan

# JSON output for parsing
terraform show -json tfplan
```

## Critical alerts - MUST flag

- Any `destroy` operations on stateful resources (databases, storage)
- Any `replace` operations (forces new resource)
- Changes to `prevent_destroy` lifecycle settings
- Modifications to IAM policies or security groups
- Changes to encryption settings
- Removal of backup configurations

## Security checks

- No hardcoded secrets in `.tf` files
- Sensitive variables marked as `sensitive = true`
- S3 buckets have encryption and versioning
- Security groups not open to 0.0.0.0/0
- RDS/databases not publicly accessible
- KMS keys have rotation enabled

## Best practices

- Remote state with locking (S3+DynamoDB, Terraform Cloud)
- State encryption enabled
- Provider versions pinned
- Module versions pinned
- Variables have descriptions and validation
- Resources properly tagged

## Output format

```
## Destructive Changes (REVIEW CAREFULLY)
- aws_db_instance.main will be DESTROYED

## Modifications
- aws_security_group.web: ingress rules changing

## Additions
- aws_instance.new_server

## Risk Assessment: HIGH/MEDIUM/LOW
```

## Rules

- MUST highlight all destroy/replace operations prominently
- MUST warn about stateful resource changes
- Never run `terraform apply` without explicit user approval
- Never run `terraform destroy`
- Always recommend `terraform plan` before apply
