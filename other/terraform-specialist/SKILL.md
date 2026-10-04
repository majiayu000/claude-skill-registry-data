---
name: terraform-specialist
description: Terraform configuration writing, module development, state management,
  and multi-cloud infrastructure provisioning. Use when asked to write Terraform code,
  create a reusable Terraform module, manage Terraform state (local, S3, Terraform
  Cloud), import existing infrastructure, set up workspaces for multi-environment
  management, or troubleshoot a Terraform plan or apply error.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure-iac
  tags:
  - terraform
  - iac
  - infrastructure
  - modules
  - state
  - aws
  - azure
  - gcp
  - multi-cloud
---

# Terraform Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write Terraform`, `Terraform module`, `terraform plan error`.
- The requested work fits this skill's lane: Terraform HCL writing, module development, state management, workspace strategy, import.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Cloud service selection (use cloud specialist for that context); application code.

## First actions
1. `Glob('**/*.tf', '**/*.tfvars', '**/terraform.lock.hcl', '**/.terraform.lock.hcl')` — find existing Terraform code
2. `Read` main.tf, variables.tf, and backend configuration to understand current structure
3. Identify: provider(s), backend type (local, S3, Terraform Cloud), workspace strategy, Terraform version

## Decision rules
- Backend: never use local state for anything beyond local dev/testing — use remote backend (S3 + DynamoDB lock, or Terraform Cloud)
- Modules: write reusable modules for any resource pattern used more than once; one module per logical unit
- Variables: all variables need `description` and `type`; sensitive vars get `sensitive = true`
- For importing existing resources: use `terraform import` and generate the config; verify with `terraform plan` showing no changes
- If cloud-specific service knowledge is needed: use this skill for Terraform HCL; route service questions to aws/azure/gcp-specialist

## Steps

### Step 1: Read existing code
Understand provider versions, module structure, variable patterns, and naming conventions in use.

### Step 2: Write Terraform code
File structure: `main.tf` (resources), `variables.tf` (input vars), `outputs.tf` (output values), `versions.tf` (required_providers block).

### Step 3: Validate
```bash
terraform fmt -recursive
terraform validate
terraform plan
```
All three must pass cleanly before handing back.

## Output contract
- File structure: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` minimum
- All resources: use consistent naming convention (`<env>-<service>-<type>`, e.g., `prod-api-sg`)
- All sensitive outputs: marked `sensitive = true`
- `terraform plan` shows only the intended changes - no unexpected destroys

## Constraints
- NEVER commit `.tfstate` files or `.terraform/` directories
- NEVER use `terraform apply -auto-approve` in production environments without a review step
- NEVER hardcode credentials in `.tf` files - use provider-level auth (IAM roles, env vars, Vault)
- Scope boundary: cloud service selection and architecture belongs to cloud specialist skills; this skill handles HCL and Terraform mechanics

## Examples

### Example 1: New AWS infrastructure module
User says: "Write a Terraform module for an ECS service with ALB and auto-scaling"
Actions:
1. Glob for existing Terraform modules to match conventions
2. Write module with: ECS cluster, task definition, service, ALB, target group, security groups, auto-scaling policy
3. Write variables.tf with all configurable parameters; outputs.tf with service URL and ARN
Result: Complete Terraform module directory passing `terraform validate`

## Troubleshooting
**"Error: Error acquiring the state lock"**
Cause: Previous run crashed holding DynamoDB lock
Fix: `terraform force-unlock <LOCK_ID>` - verify no other apply is running first

**Plan shows unexpected resource destroy**
Cause: Resource name changed, moved to a module, or provider upgrade changed resource behavior
Fix: Use `terraform state mv` to rename in state; or use `moved {}` block (Terraform 1.1+)

## Reference
- `references/legacy-agent.md`: module patterns, state management strategies, workspace management, provider configuration, import workflows, Terraform Cloud/Enterprise patterns
