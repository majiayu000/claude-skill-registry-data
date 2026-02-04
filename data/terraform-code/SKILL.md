---
name: terraform-code
description: Write HashiCorp-compliant Terraform infrastructure code for Azure with automated style validation. Optimized for azurerm and azapi providers. Use when implementing Terraform resources, modules, or configurations. Triggers include "write terraform", "create tf module", "terraform code", "implement infrastructure as code", or working with .tf files. ALWAYS uses Terraform MCP tools to query provider documentation before implementation.
---

# Terraform Code (Azure)

Write production-ready Terraform code for Azure following HashiCorp's official style conventions with automated validation and quality checks. Optimized for **azurerm** and **azapi** providers.

## Workflow

### 1. Research Phase (Use Task Tool with Parallel Agents)

**ALWAYS launch parallel research agents to gather comprehensive information.** This ensures high-quality implementation based on official documentation and best practices.

#### Launch Parallel Research Agents

Use the Task tool to launch TWO agents in parallel (single message with multiple Task calls):

**Agent 1: Azure Service Research**
```
Task tool configuration:
- subagent_type: "general-purpose"
- description: "Research Azure service documentation"
- prompt: "Research Azure {service_name} using Azure MCP tools:
  1. Use mcp__Azure__documentation('{service_name}') for official documentation
  2. Use mcp__Azure__azureterraformbestpractices('{service_name}') for Terraform patterns
  3. Use mcp__Azure__get_bestpractices('{service_name}') for Well-Architected Framework
  4. Summarize: Key configuration requirements, security best practices, common patterns"

Example services: "Front Door", "App Service", "Virtual Network", "Storage Account"
```

**Agent 2: Terraform Provider Research**
```
Task tool configuration:
- subagent_type: "general-purpose"
- description: "Research Terraform provider details"
- prompt: "Research Terraform providers using Terraform MCP tools:
  1. Use mcp__Terraform__get_provider_details('hashicorp', 'azurerm') for azurerm resources
  2. Use mcp__Terraform__get_provider_details('azure', 'azapi') for azapi resources
  3. Use mcp__Terraform__get_latest_provider_version() for both providers
  4. Identify relevant resource types for {resource_description}
  5. List required arguments and optional configurations"

Example: resource_description = "Azure Front Door with WAF"
```

#### Parallel Execution Pattern

**Critical: Launch both agents in a SINGLE message:**

```markdown
I'm launching two research agents in parallel to gather comprehensive information:

<Agent 1: Azure MCP Research>
<Agent 2: Terraform MCP Research>
```

Wait for both agents to complete, then synthesize findings before implementation.

#### Expected Research Output

After agents complete, you should have:

✅ **From Azure MCP Agent:**
- Official Azure service documentation
- Security and compliance requirements
- Terraform-specific implementation patterns
- Well-Architected Framework best practices

✅ **From Terraform MCP Agent:**
- Available azurerm/azapi resource types
- Required vs optional arguments
- Latest provider versions
- Data source options

**See [research_workflow.md](references/research_workflow.md) for detailed agent orchestration patterns.**

### 2. Structure Files According to Standards

Create the following file structure:

**Core files (always create):**
- `terraform.tf` - Version constraints and required providers
- `providers.tf` - Provider configuration blocks
- `main.tf` - Resources and data sources
- `variables.tf` - Input variable declarations (alphabetically ordered)
- `outputs.tf` - Output declarations (alphabetically ordered)

**Optional files (create as needed):**
- `locals.tf` - Local value definitions
- `backend.tf` - Backend configuration
- Logical splits: `network.tf`, `compute.tf`, `storage.tf`, etc.

**Use template files from `assets/templates/` as starting points.**

### 3. Implement Resources Following Style Guide

#### Naming Conventions
- **Use underscores**, not hyphens: `web_server` ✅, `web-server` ❌
- **No type redundancy**: `azurerm_virtual_network.main` ✅, `azurerm_virtual_network.vnet_main` ❌
- **Descriptive nouns**: Clear, meaningful names
- **Azure resource naming**: Follow Azure naming conventions in `name` arguments

#### Formatting Rules
- **2-space indentation** (never tabs)
- **Align equals signs** for consecutive arguments at same nesting level
- **Blank lines** between top-level blocks
- **Meta-arguments first**: `count`, `for_each`, then regular arguments, then nested blocks

#### Block Organization
```hcl
resource "azurerm_virtual_machine" "web" {
  count = 3  # Meta-arguments first

  # Regular arguments (aligned)
  name                = "${var.prefix}-vm-${count.index}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  vm_size             = "Standard_B2s"

  # Nested blocks
  storage_os_disk {
    # ...
  }

  # lifecycle at end
  lifecycle {
    create_before_destroy = true
  }
}
```

#### Variable Requirements
Every variable MUST have:
- `type` - Explicit type declaration
- `description` - Clear explanation
- `default` (optional) - Reasonable default when appropriate
- `validation` (optional) - For constrained values

```hcl
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

#### Output Requirements
Every output should have:
- `description` - Explain the output's purpose
- `sensitive = true` - For passwords, keys, secrets

```hcl
output "database_password" {
  description = "Master password for RDS database"
  value       = aws_db_instance.main.password
  sensitive   = true
}
```

#### Comments
- Use `#` for comments (not `//` or `/* */`)
- Comment **sparingly** - write self-explanatory code
- Add comments only when logic is complex or non-obvious

**See [style_guide.md](references/style_guide.md) for complete style conventions.**

### 4. Validate Code Quality

Run validation scripts before completion:

#### Format Check and Auto-Fix
```bash
bash scripts/validate_terraform.sh <terraform_directory>
```

This runs:
- `terraform fmt -recursive` - Auto-format code
- `terraform validate` - Syntax and logic validation

#### Style Compliance Check
```bash
python3 scripts/check_style.py <terraform_directory>
```

This checks:
- Naming conventions (underscores, no type redundancy)
- Indentation (2 spaces)
- Variable type and description requirements
- Output descriptions
- File organization

**Fix all errors before marking implementation complete.**

### 5. Best Practices

#### Data Sources Before Resources
Define data sources before the resources that reference them:

```hcl
# Data sources first
data "aws_ami" "ubuntu" {
  most_recent = true
  # ...
}

# Then resources that use them
resource "aws_instance" "web" {
  ami = data.aws_ami.ubuntu.id
  # ...
}
```

#### Use Locals for Common Values
```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_instance" "web" {
  # ...
  tags = merge(local.common_tags, { Name = "web-server" })
}
```

#### Prefer for_each Over count
```hcl
resource "aws_instance" "server" {
  for_each = toset(["web", "api", "worker"])

  ami           = var.ami_id
  instance_type = "t2.micro"

  tags = {
    Name = "${each.key}-server"
  }
}
```

#### Implicit Dependencies Over Explicit
```hcl
# Preferred: implicit dependency
resource "aws_eip" "example" {
  instance = aws_instance.web.id
}

# Use depends_on only when necessary
resource "aws_instance" "web" {
  # ...
  depends_on = [aws_security_group.allow_web]
}
```

## Azure Implementation Patterns

### Resource Group and Virtual Network (azurerm)
```hcl
data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-${var.environment}-rg"
  location = var.location

  tags = local.common_tags
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = var.vnet_address_space

  tags = local.common_tags
}

resource "azurerm_subnet" "private" {
  for_each = var.private_subnets

  name                 = each.key
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [each.value.address_prefix]

  service_endpoints = each.value.service_endpoints
}
```

### Front Door with WAF (azurerm)
```hcl
resource "azurerm_cdn_frontdoor_profile" "main" {
  name                = "${var.project_name}-fd"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "Premium_AzureFrontDoor"

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_firewall_policy" "main" {
  name                = "${var.project_name}fdwaf"
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = azurerm_cdn_frontdoor_profile.main.sku_name
  mode                = "Prevention"

  managed_rule {
    type    = "Microsoft_DefaultRuleSet"
    version = "2.1"
  }

  tags = local.common_tags
}

resource "azurerm_cdn_frontdoor_security_policy" "main" {
  name                     = "${var.project_name}-security-policy"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.main.id

  security_policies {
    firewall {
      cdn_frontdoor_firewall_policy_id = azurerm_cdn_frontdoor_firewall_policy.main.id

      association {
        domain {
          cdn_frontdoor_domain_id = azurerm_cdn_frontdoor_endpoint.main.id
        }

        patterns_to_match = ["/*"]
      }
    }
  }
}
```

### Using azapi Provider for Preview Features
```hcl
# Use azapi for resources not yet available in azurerm
resource "azapi_resource" "storage_account" {
  type      = "Microsoft.Storage/storageAccounts@2023-01-01"
  name      = "${var.project_name}st${var.environment}"
  parent_id = azurerm_resource_group.main.id
  location  = var.location

  body = jsonencode({
    sku = {
      name = "Standard_LRS"
    }
    kind = "StorageV2"
    properties = {
      minimumTlsVersion = "TLS1_2"
      allowBlobPublicAccess = false
      networkAcls = {
        defaultAction = "Deny"
        bypass        = "AzureServices"
      }
    }
  })

  tags = local.common_tags
}

# Data source for azapi resource
data "azapi_resource" "storage_account" {
  type      = "Microsoft.Storage/storageAccounts@2023-01-01"
  name      = azapi_resource.storage_account.name
  parent_id = azurerm_resource_group.main.id

  response_export_values = ["properties.primaryEndpoints"]
}
```

### App Service with Private Endpoint
```hcl
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-asp"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "P1v3"

  tags = local.common_tags
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.project_name}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_service_plan.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = true

    application_stack {
      node_version = "18-lts"
    }
  }

  tags = local.common_tags
}

resource "azurerm_private_endpoint" "app" {
  name                = "${var.project_name}-app-pe"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  subnet_id           = azurerm_subnet.private["app"].id

  private_service_connection {
    name                           = "${var.project_name}-app-psc"
    private_connection_resource_id = azurerm_linux_web_app.main.id
    is_manual_connection           = false
    subresource_names              = ["sites"]
  }

  tags = local.common_tags
}
```

## Resources

### scripts/
- **validate_terraform.sh** - Runs `terraform fmt` and `terraform validate`
- **check_style.py** - Validates HashiCorp style compliance

### references/
- **research_workflow.md** - Parallel agent orchestration for Azure + Terraform MCP research (START HERE)
- **style_guide.md** - Complete HashiCorp style conventions and best practices
- **terraform_mcp_usage.md** - Terraform MCP tools workflow and patterns (Azure-focused)
- **azure_patterns.md** - Azure-specific patterns, best practices, and common implementations

### assets/templates/
- **terraform.tf** - Version constraints template
- **providers.tf** - Provider configuration template
- **main.tf** - Resources template
- **variables.tf** - Variables template
- **outputs.tf** - Outputs template
- **locals.tf** - Locals template

## Quick Reference

### Style Checklist
- ✅ 2-space indentation (no tabs)
- ✅ Underscores in names (no hyphens)
- ✅ No resource type in resource names
- ✅ Aligned equals signs for consecutive arguments
- ✅ Meta-arguments before regular arguments
- ✅ Blank lines between top-level blocks
- ✅ All variables have `type` and `description`
- ✅ Sensitive outputs marked with `sensitive = true`
- ✅ Data sources before dependent resources
- ✅ Run `terraform fmt` before completion
- ✅ Run `terraform validate` before completion

### Required Research Pattern (Parallel Agents)
```
1. Launch TWO agents in PARALLEL (single message):

   Agent 1: Azure MCP Research
   - mcp__Azure__documentation(service)
   - mcp__Azure__azureterraformbestpractices(service)
   - mcp__Azure__get_bestpractices(service)

   Agent 2: Terraform MCP Research
   - mcp__Terraform__get_provider_details("hashicorp", "azurerm")
   - mcp__Terraform__get_provider_details("azure", "azapi")
   - mcp__Terraform__get_latest_provider_version() for both

2. Wait for both agents to complete

3. Synthesize findings:
   - Cross-validate Azure requirements with Terraform capabilities
   - Create implementation plan
   - Identify required resources and variables

4. Implement resources using synthesized research

5. Validate with scripts
```

### Azure-Specific Best Practices
- **Always create resource group first** - All Azure resources require a resource group
- **Use data source for client config** - `data "azurerm_client_config" "current" {}`
- **azapi for preview features** - Use azapi provider for resources not yet in azurerm
- **Consistent naming** - Use `${var.project_name}-${var.environment}-${resource_type}` pattern
- **Location from resource group** - Reference `azurerm_resource_group.main.location`
- **Private endpoints** - Use for secure connectivity to PaaS services
- **Service endpoints** - Configure on subnets for Azure service access
