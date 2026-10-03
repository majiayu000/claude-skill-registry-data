---
name: using-terraform-azure
description: Provision Azure infrastructure with Terraform (azurerm 4.x) — Key Vault, Managed Identity, App Service, AVM modules.
when_to_use: Reach for this when writing Terraform HCL to provision Azure resources (provider "azurerm", *.tf). For Azure CI/CD pipelines use managing-azure-devops; for serverless function code use using-azure-functions; for AWS infra use aws-cloud. IaC-provisioning skill, Azure-specific.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/*.tf"
  - "**/*.tfvars"
  - "terraform.tfstate*"
---

# Terraform Azure Infrastructure Skill

**Version**: 1.0.0 | **Target**: <500 lines | **Purpose**: Fast reference for Azure infrastructure with Terraform azurerm 4.x

---

## When to Use

**Auto-Detection Triggers**:
- `*.tf` files containing `azurerm` provider references
- `terraform.tfvars` with Azure-specific variables
- `backend "azurerm"` configuration blocks
- User mentions Azure, Terraform, or azurerm

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **[REFERENCE.md](REFERENCE.md)**: Multi-environment patterns, networking, App Service, SQL, Service Bus, state management

---

## CRITICAL: azurerm 4.0 Breaking Changes

> **WARNING**: The azurerm 4.x provider introduces several breaking changes from 3.x.
> Base models frequently generate 3.x code. Apply these corrections every time.

| Breaking Change | Old (3.x) | New (4.x) |
|----------------|-----------|-----------|
| **subscription_id** | Optional in provider | **MANDATORY in provider block** |
| **skip_provider_registration** | `skip_provider_registration = true` | **REMOVED** -- use `resource_provider_registrations = "none"` |
| **SQL resources** | `azurerm_sql_server`, `azurerm_sql_database` | `azurerm_mssql_server`, `azurerm_mssql_database` |
| **MySQL resources** | `azurerm_mysql_server`, `azurerm_mysql_database` | `azurerm_mysql_flexible_server`, `azurerm_mysql_flexible_database` |
| **Key Vault access** | Access policies by default | Use `enable_rbac_authorization = true` |
| **State backend auth** | Storage access keys | Use `use_azuread_auth = true` |
| **Provider functions** | Not available | `provider::azurerm::normalise_resource_id()`, `parse_resource_id()` |

**Resource renames (partial list)**:
- `azurerm_sql_firewall_rule` -> `azurerm_mssql_firewall_rule`
- `azurerm_sql_virtual_network_rule` -> `azurerm_mssql_virtual_network_rule`
- `azurerm_mysql_firewall_rule` -> `azurerm_mysql_flexible_server_firewall_rule`
- `azurerm_postgresql_server` -> `azurerm_postgresql_flexible_server`

---

## Provider Configuration

```hcl
terraform {
  required_version = ">= 1.8.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  # MANDATORY in 4.x -- omitting this causes a fatal error
  subscription_id = var.subscription_id

  # Replaces removed skip_provider_registration
  # "none" = register nothing; "core" = default set; "extended" = all common
  resource_provider_registrations = "none"

  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

variable "subscription_id" {
  description = "Azure Subscription ID (mandatory for azurerm 4.x)"
  type        = string
  sensitive   = true
}
```

---

## State Backend

**azurerm backend with Entra ID authentication** (recommended over storage access keys):

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "tfstateaccount"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"

    # Use Entra ID (Azure AD) auth -- NOT storage access keys
    use_azuread_auth = true
  }
}
```

---

## Key Vault with RBAC

> **CRITICAL**: When `enable_rbac_authorization = true`, access policies are **completely ignored**.
> Use Azure role assignments instead of `azurerm_key_vault_access_policy`.

```hcl
resource "azurerm_key_vault" "main" {
  name                = "kv-${var.project}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # RBAC mode -- access policies are IGNORED when this is true
  enable_rbac_authorization = true

  soft_delete_retention_days = 90
  purge_protection_enabled   = true

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
    ip_rules       = var.allowed_ip_ranges
  }
}

# Role assignments for Key Vault access
resource "azurerm_role_assignment" "kv_secrets_reader" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}

resource "azurerm_role_assignment" "kv_secrets_officer" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}
```

**Key Vault RBAC roles quick reference**:

| Role | Secrets | Keys | Certificates |
|------|---------|------|--------------|
| Key Vault Secrets User | Read | - | - |
| Key Vault Secrets Officer | Full | - | - |
| Key Vault Crypto User | - | Encrypt/Decrypt/Wrap/Unwrap | - |
| Key Vault Crypto Officer | - | Full | - |
| Key Vault Certificates Officer | - | - | Full |
| Key Vault Administrator | Full | Full | Full |

---

## Managed Identity Patterns

### System-Assigned Identity

```hcl
resource "azurerm_linux_web_app" "api" {
  name                = "app-${var.project}-api-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack { dotnet_version = "8.0" }
  }
}

resource "azurerm_role_assignment" "app_kv_secrets" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.api.identity[0].principal_id
}
```

### User-Assigned Identity

```hcl
resource "azurerm_user_assigned_identity" "app" {
  name                = "id-${var.project}-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
}

# Attach to resources via identity block
resource "azurerm_linux_web_app" "api" {
  # ...
  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.app.id]
  }
}

# Grant roles to the identity
resource "azurerm_role_assignment" "app_storage_blob" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
}
```

**When to use which**:
- **System-assigned**: Single resource, lifecycle tied to parent, simpler
- **User-assigned**: Shared across resources, survives resource recreation, pre-provisioned roles

---

## Azure Verified Modules (AVM)

Microsoft-maintained Terraform modules. Use for standard patterns with built-in best practices.

**Naming convention**: `Azure/avm-res-{provider}-{resource}/azurerm`

```hcl
module "vnet" {
  source  = "Azure/avm-res-network-virtualnetwork/azurerm"
  version = "~> 0.4"

  name                = "vnet-${var.project}-${var.environment}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.0.0.0/16"]

  subnets = {
    app  = { name = "snet-app",  address_prefixes = ["10.0.1.0/24"] }
    data = { name = "snet-data", address_prefixes = ["10.0.2.0/24"] }
  }
}

module "key_vault" {
  source  = "Azure/avm-res-keyvault-vault/azurerm"
  version = "~> 0.9"

  name                      = "kv-${var.project}-${var.environment}"
  resource_group_name       = azurerm_resource_group.main.name
  location                  = azurerm_resource_group.main.location
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  enable_rbac_authorization = true
}
```

**Common AVM modules**: `avm-res-network-virtualnetwork`, `avm-res-keyvault-vault`, `avm-res-storage-storageaccount`, `avm-res-web-site`, `avm-res-sql-server`

---

## Provider-Defined Functions (4.x)

New in azurerm 4.x -- provider-scoped functions:

```hcl
locals {
  # Normalise resource ID to consistent casing
  normalised_id = provider::azurerm::normalise_resource_id(
    "/subscriptions/xxx/resourceGroups/MyRG/providers/Microsoft.KeyVault/vaults/myKV"
  )

  # Parse resource ID into components
  parsed = provider::azurerm::parse_resource_id(
    "/subscriptions/xxx/resourceGroups/my-rg/providers/Microsoft.Web/sites/my-app"
  )
  # parsed.subscription_id, parsed.resource_group_name, parsed.resource_name
}
```

---

## Module Patterns

### Variables with Validation

```hcl
variable "project" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9-]{3,20}$", var.project))
    error_message = "Project must be 3-20 lowercase alphanumeric or hyphens."
  }
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Local Values and Naming

```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = merge(
    { Project = var.project, Environment = var.environment, ManagedBy = "terraform" },
    var.tags,
  )
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}
```

### Module Composition

```hcl
module "networking" {
  source      = "./modules/networking"
  project     = var.project
  environment = var.environment
  location    = var.location
  tags        = local.common_tags
}

module "security" {
  source            = "./modules/security"
  project           = var.project
  environment       = var.environment
  resource_group_id = module.networking.resource_group_id
  tags              = local.common_tags
}

module "application" {
  source              = "./modules/application"
  resource_group_name = module.networking.resource_group_name
  app_subnet_id       = module.networking.app_subnet_id
  key_vault_id        = module.security.key_vault_id
  identity_id         = module.security.identity_id
  tags                = local.common_tags
}
```

---

## Quick Reference Card

### Common Commands

```bash
terraform init -backend-config="env/prod.backend.hcl"
terraform plan -var-file="env/prod.tfvars" -out=plan.tfplan
terraform apply plan.tfplan
terraform state list
terraform state show azurerm_resource_group.main
terraform import azurerm_resource_group.main /subscriptions/.../resourceGroups/rg-name
terraform fmt -recursive
terraform validate
```

### Azure Resource Naming Conventions

| Resource | Pattern | Example |
|----------|---------|---------|
| Resource Group | `rg-{project}-{env}` | `rg-myapp-prod` |
| Virtual Network | `vnet-{project}-{env}` | `vnet-myapp-prod` |
| Subnet | `snet-{purpose}` | `snet-app`, `snet-data` |
| Key Vault | `kv-{project}-{env}` | `kv-myapp-prod` |
| Storage Account | `st{project}{env}` | `stmyappprod` |
| App Service | `app-{project}-{role}-{env}` | `app-myapp-api-prod` |
| Managed Identity | `id-{project}-{env}` | `id-myapp-prod` |
| SQL Server | `sql-{project}-{env}` | `sql-myapp-prod` |
| Service Bus | `sb-{project}-{env}` | `sb-myapp-prod` |
| NSG | `nsg-{subnet}` | `nsg-snet-app` |
| Private Endpoint | `pe-{target}-{env}` | `pe-sql-prod` |

---

**See Also**: [REFERENCE.md](REFERENCE.md) for multi-environment patterns, networking (VNet, subnets, NSGs, private endpoints), App Service/Functions infrastructure, Azure SQL with private endpoints, Service Bus, and state management best practices.

**Terraform Compatibility**: >= 1.8.0 | **azurerm Provider**: ~> 4.0 | **Last Updated**: 2026-02-23
