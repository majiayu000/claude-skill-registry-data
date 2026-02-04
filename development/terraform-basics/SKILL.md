---
name: terraform-basics
description: Terraform infrastructure-as-code patterns for AWS and Azure provisioning. Use when creating or modifying .tf files, writing Terraform modules, managing remote state (S3, Azure Storage), working with terraform commands (init, plan, apply, destroy), configuring providers (AWS, Azure, Google Cloud), or implementing infrastructure best practices like module design, workspace strategies, and state locking.
---

# Terraform Basics Skill

## Purpose

Provide infrastructure-as-code best practices, command workflows, and module design patterns for Terraform-based AWS and Azure provisioning.

**Key Capabilities**:
- Terraform command workflows
- Module design patterns
- Remote state management
- Provider configuration
- Security and compliance
- Troubleshooting

---

## When to Use This Skill

Auto-activates when:
- Creating or modifying `.tf` files (main.tf, variables.tf, outputs.tf)
- Writing Terraform modules (`modules/*/`)
- Managing state files (terraform.tfstate)
- Running terraform commands (init, plan, apply, destroy)
- Configuring cloud providers (AWS, Azure, GCP)
- Implementing infrastructure patterns (VPC, networking, compute)

---

## Quick Start

### New Terraform Project Checklist

- [ ] **Provider Configuration**: Define required providers with version constraints
- [ ] **Backend Configuration**: Configure remote state (S3, Azure Storage, Terraform Cloud)
- [ ] **Module Structure**: Organize into reusable modules
- [ ] **Variables**: Define input variables with validation
- [ ] **Outputs**: Export values for other modules/projects
- [ ] **Version Pinning**: Lock provider and module versions
- [ ] **State Locking**: Enable state locking (DynamoDB, Azure Storage)
- [ ] **Pre-commit Hooks**: Add terraform fmt, validate, tflint

### New Module Checklist

- [ ] **Module Directory**: `modules/{module-name}/`
- [ ] **Required Files**: main.tf, variables.tf, outputs.tf, README.md
- [ ] **Input Validation**: Validate variable inputs
- [ ] **Documentation**: Document inputs, outputs, examples
- [ ] **Versioning**: Tag module releases (v1.0.0)
- [ ] **Testing**: Write tests (terraform test, terratest)

---

## Core Principles (7 Key Rules)

### 1. State Files Are Sacred - Always Use Remote State

**Never commit terraform.tfstate to git. Always use remote backend.**

```hcl
✅ GOOD - Remote state with locking
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

❌ BAD - Local state (no locking, no collaboration)
# No backend configuration = local state
# terraform.tfstate in .gitignore but risky
```

**Why**: State locking prevents concurrent modifications, remote state enables team collaboration.

### 2. Always Plan Before Apply

**Review changes before applying to production.**

```bash
✅ GOOD - Plan → Review → Apply workflow
terraform plan -out=tfplan
# Review plan output carefully
terraform show tfplan
# If approved:
terraform apply tfplan

❌ BAD - Direct apply without review
terraform apply -auto-approve  # DANGEROUS in production!
```

**Why**: Prevents accidental resource deletion, cost overruns, security misconfigurations.

### 3. Use Modules for Reusability (DRY Principle)

**Don't repeat infrastructure code. Create reusable modules.**

```hcl
✅ GOOD - Reusable module
# modules/azure-vnet/main.tf
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name
}

# Root module usage
module "vnet_prod" {
  source              = "./modules/azure-vnet"
  vnet_name           = "prod-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = "eastus"
  resource_group_name = azurerm_resource_group.prod.name
}

❌ BAD - Copy-pasted resource blocks
resource "azurerm_virtual_network" "vnet_prod" { ... }
resource "azurerm_virtual_network" "vnet_staging" { ... }
resource "azurerm_virtual_network" "vnet_dev" { ... }
# Same code repeated 3 times
```

**Why**: Maintainability, consistency, reduced errors.

### 4. Pin Provider and Module Versions

**Lock versions for reproducibility.**

```hcl
✅ GOOD - Version constraints
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.70.0"  # Locked to 3.70.x
    }
  }
}

module "network" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"  # Exact version
}

❌ BAD - No version constraints
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      # No version = latest (unpredictable)
    }
  }
}
```

**Why**: Prevents breaking changes, ensures consistent deployments.

### 5. Use Data Sources Over Hardcoded Values

**Query existing resources instead of hardcoding.**

```hcl
✅ GOOD - Data source
data "azurerm_resource_group" "existing" {
  name = "existing-rg"
}

resource "azurerm_storage_account" "storage" {
  resource_group_name = data.azurerm_resource_group.existing.name
  location            = data.azurerm_resource_group.existing.location
}

❌ BAD - Hardcoded values
resource "azurerm_storage_account" "storage" {
  resource_group_name = "existing-rg"  # Hardcoded
  location            = "eastus"       # Hardcoded
}
```

**Why**: Flexibility, environment portability, reduced duplication.

### 6. Validate Inputs and Outputs

**Add validation rules and output documentation.**

```hcl
✅ GOOD - Input validation
variable "environment" {
  type        = string
  description = "Environment name (dev, staging, prod)"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

output "vnet_id" {
  description = "Azure Virtual Network ID for use in other modules"
  value       = azurerm_virtual_network.vnet.id
}

❌ BAD - No validation or documentation
variable "environment" {
  type = string
  # No validation, no description
}

output "vnet_id" {
  value = azurerm_virtual_network.vnet.id
  # No description
}
```

**Why**: Prevents invalid configurations, improves documentation.

### 7. Use Workspaces for Environments (When Appropriate)

**Workspaces for environment isolation (dev, staging, prod).**

```bash
✅ GOOD - Workspace strategy
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch to environment
terraform workspace select prod
terraform plan -var-file=prod.tfvars

❌ BAD - Single workspace for all environments
# No isolation, risk of mixing dev/prod resources
```

**Why**: Environment isolation, reduced accidental cross-environment changes.

---

## Common Terraform Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `terraform init` | Initialize backend, download providers | First time, after adding providers/modules |
| `terraform validate` | Check syntax validity | After editing .tf files |
| `terraform fmt` | Format code to standard style | Before committing |
| `terraform plan` | Preview changes | Before apply, during review |
| `terraform apply` | Apply changes | After plan approval |
| `terraform destroy` | Delete all resources | Tearing down environments |
| `terraform state list` | List resources in state | Debugging, auditing |
| `terraform state show` | Show resource details | Inspecting specific resources |
| `terraform import` | Import existing resources | Adopting existing infrastructure |
| `terraform output` | Display output values | Retrieving module outputs |

---

## Quick Reference

### File Naming Conventions

| File | Purpose |
|------|---------|
| `main.tf` | Primary resource definitions |
| `variables.tf` | Input variable declarations |
| `outputs.tf` | Output value definitions |
| `providers.tf` | Provider configurations |
| `backend.tf` | Backend configuration (remote state) |
| `terraform.tfvars` | Variable values (environment-specific) |
| `versions.tf` | Terraform and provider version constraints |

### Module Structure

```
modules/azure-vnet/
├── main.tf          # Resource definitions
├── variables.tf     # Input variables
├── outputs.tf       # Outputs
├── README.md        # Module documentation
├── examples/        # Usage examples
│   └── basic/
│       └── main.tf
└── tests/           # Module tests
    └── basic_test.go
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Monolithic Configuration

**Problem**: Single main.tf with 1000+ lines
**Issue**: Hard to maintain, understand, and collaborate
**Fix**: Split into modules and logical files

### ❌ Anti-Pattern 2: Hardcoded Credentials

**Problem**: AWS keys or Azure credentials in .tf files
**Issue**: Security risk, credential leakage
**Fix**: Use environment variables, managed identities, or credential helpers

### ❌ Anti-Pattern 3: No State Locking

**Problem**: Multiple users applying changes simultaneously
**Issue**: State corruption, race conditions
**Fix**: Enable state locking (DynamoDB for S3, blob lease for Azure)

### ❌ Anti-Pattern 4: Auto-Approve in Production

**Problem**: `terraform apply -auto-approve` in CI/CD
**Issue**: No human review, risky changes
**Fix**: Require manual approval for production applies

### ❌ Anti-Pattern 5: Ignoring Plan Output

**Problem**: Running apply without reviewing plan
**Issue**: Accidental deletions, unexpected changes
**Fix**: Always review `terraform plan` output before apply

---

## Common Workflows

### Workflow 1: Initial Project Setup

```bash
# 1. Create project directory
mkdir -p terraform/modules

# 2. Initialize Terraform
cd terraform
terraform init

# 3. Create backend configuration
cat > backend.tf <<EOF
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate"
    container_name       = "tfstate"
    key                  = "project.tfstate"
  }
}
EOF

# 4. Initialize backend
terraform init -backend-config=backend.hcl

# 5. Create workspace
terraform workspace new dev
```

### Workflow 2: Daily Development

```bash
# 1. Pull latest state
terraform refresh

# 2. Make changes to .tf files
# Edit main.tf, variables.tf, etc.

# 3. Format code
terraform fmt -recursive

# 4. Validate syntax
terraform validate

# 5. Plan changes
terraform plan -out=tfplan

# 6. Review plan
terraform show tfplan

# 7. Apply changes
terraform apply tfplan
```

### Workflow 3: Multi-Environment Deployment

```bash
# Deploy to dev
terraform workspace select dev
terraform plan -var-file=dev.tfvars -out=dev.tfplan
terraform apply dev.tfplan

# Deploy to staging
terraform workspace select staging
terraform plan -var-file=staging.tfvars -out=staging.tfplan
terraform apply staging.tfplan

# Deploy to prod (with approval)
terraform workspace select prod
terraform plan -var-file=prod.tfvars -out=prod.tfplan
# Manual review and approval
terraform apply prod.tfplan
```

---

## Navigation Guide

| Need to... | Read this |
|------------|-----------|
| Learn terraform commands | [terraform-commands.md](resources/terraform-commands.md) |
| Manage state files | [state-management.md](resources/state-management.md) |
| Design reusable modules | [module-patterns.md](resources/module-patterns.md) |

---

## Resource Files

### [terraform-commands.md](resources/terraform-commands.md)
Complete command reference with examples, flags, and troubleshooting

### [state-management.md](resources/state-management.md)
Remote state backends, locking, migration, disaster recovery

### [module-patterns.md](resources/module-patterns.md)
Module design, composition, testing, versioning, registry publishing

---

## Related Skills

- **azure-basics** - Azure-specific resource patterns and CLI commands
- **task-management** - Dependency analysis for infrastructure ordering

---

**Skill Status**: COMPLETE ✅
**Line Count**: 435 ✅
**Progressive Disclosure**: 3 resource files ✅
