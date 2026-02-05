---
name: azure-basics
description: Azure cloud services, resource management, and Azure CLI patterns. Use when working with Azure resources, resource groups, ARM templates, az commands (az vm, az network, az storage, az aks), Azure naming conventions, RBAC policies, networking (VNet, NSG, Application Gateway), or implementing Azure best practices for resource organization, cost management, and security.
---

# Azure Basics Skill

## Purpose

Provide Azure cloud platform best practices, CLI command patterns, and resource organization strategies for reliable, secure, and cost-effective cloud infrastructure.

**Key Capabilities**:
- Azure CLI command patterns
- Resource organization and naming
- Networking fundamentals (VNet, NSG, routing)
- RBAC and security
- Cost management
- ARM template patterns

---

## When to Use This Skill

Auto-activates when:
- Working with Azure resources (VMs, storage, databases, AKS)
- Running Azure CLI commands (`az` commands)
- Creating ARM templates or Bicep files
- Managing Azure resource groups
- Configuring Azure networking (VNets, subnets, NSGs)
- Implementing Azure RBAC policies
- Optimizing Azure costs

---

## Quick Start

### New Azure Project Checklist

- [ ] **Subscription Setup**: Verify subscription access and limits
- [ ] **Naming Convention**: Define resource naming standard
- [ ] **Resource Groups**: Organize by environment/workload
- [ ] **Networking**: Plan IP addressing (VNet, subnets)
- [ ] **RBAC**: Configure least-privilege access
- [ ] **Tagging Strategy**: Define required tags
- [ ] **Cost Budgets**: Set spending alerts
- [ ] **Monitoring**: Enable Azure Monitor and Log Analytics

### Resource Deployment Checklist

- [ ] **Resource Group**: Create or select target RG
- [ ] **Location**: Choose Azure region
- [ ] **SKU Selection**: Right-size resources for workload
- [ ] **Networking**: Configure VNet integration
- [ ] **Security**: Apply NSG rules, enable managed identity
- [ ] **Tags**: Apply environment, owner, cost center tags
- [ ] **Backup**: Configure backup policies (if applicable)
- [ ] **Monitoring**: Enable diagnostics and alerts

---

## Core Principles (7 Key Rules)

### 1. Use Resource Groups for Organization

**Resource groups are lifecycle boundaries - group resources by lifecycle.**

```bash
✅ GOOD - Organized by lifecycle
az group create --name prod-app-rg --location eastus
az group create --name prod-data-rg --location eastus
az group create --name shared-network-rg --location eastus

# App resources in app RG
# Data resources in data RG (longer lifecycle)
# Network resources in network RG (shared)

❌ BAD - All resources in one RG
az group create --name everything-rg --location eastus
# Deleting one resource risks deleting everything
```

**Why**: Simplifies resource management, enables batch operations, clear ownership.

### 2. Follow Azure Naming Conventions

**Use consistent, descriptive naming patterns.**

```bash
✅ GOOD - Consistent naming
# Pattern: {environment}-{workload}-{resource-type}-{region}
prod-webapp-vm-eastus
prod-webapp-storage-eastus
dev-api-aks-westus

❌ BAD - Inconsistent naming
vm1
storage-account-production
my-kubernetes
```

**Recommended Pattern**:
```
{env}-{workload}-{resource-type}[-{instance}]

env: dev, test, stage, prod
workload: webapp, api, data
resource-type: vm, vnet, storage, aks
instance: 01, 02 (for multiple instances)
```

### 3. Apply Tags for Cost Management

**Tag all resources for cost tracking and organization.**

```bash
✅ GOOD - Comprehensive tagging
az resource tag \
  --resource-group prod-app-rg \
  --name prod-webapp-vm \
  --resource-type Microsoft.Compute/virtualMachines \
  --tags \
    Environment=production \
    CostCenter=engineering \
    Owner=team-platform \
    Project=customer-portal

❌ BAD - No tags or inconsistent tags
# No visibility into cost allocation
```

**Required Tags**:
- Environment (dev/test/prod)
- CostCenter (billing allocation)
- Owner (team/email)
- Project (initiative/product)

### 4. Use Managed Identities (No Credentials)

**Never store credentials - use Azure managed identities.**

```bash
✅ GOOD - Managed identity
# Create VM with system-assigned identity
az vm create \
  --name prod-webapp-vm \
  --resource-group prod-app-rg \
  --assign-identity

# Grant access to Key Vault
az keyvault set-policy \
  --name prod-keyvault \
  --object-id $IDENTITY_ID \
  --secret-permissions get list

# Application uses identity (no credentials in code)

❌ BAD - Hardcoded credentials
# Connection strings in app config
# Service principal credentials in environment variables
```

**Why**: Eliminates credential rotation, reduces security risk, simplifies access management.

### 5. Implement Network Security Groups (NSGs)

**Control traffic with NSGs - default deny, explicit allow.**

```bash
✅ GOOD - Explicit NSG rules
az network nsg create --name frontend-nsg --resource-group prod-network-rg

# Allow HTTPS from internet
az network nsg rule create \
  --nsg-name frontend-nsg \
  --name allow-https \
  --priority 100 \
  --source-address-prefixes Internet \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp

# Deny all other inbound
# (Default rule: DenyAllInbound at priority 65500)

❌ BAD - No NSG or overly permissive
az network nsg rule create \
  --name allow-all \
  --source-address-prefixes '*' \
  --destination-port-ranges '*' \
  --access Allow
# Security nightmare!
```

### 6. Use Azure Regions Strategically

**Choose regions based on latency, compliance, cost.**

```bash
✅ GOOD - Region strategy
# Primary: East US (closest to users)
# Secondary: West US (disaster recovery)
# Data residency: North Europe (GDPR compliance)

az group create --name prod-primary-rg --location eastus
az group create --name prod-dr-rg --location westus

❌ BAD - Random region selection
# No disaster recovery plan
# High latency for users
# Compliance violations
```

### 7. Right-Size Resources (Cost Optimization)

**Start small, scale up - not reverse.**

```bash
✅ GOOD - Right-sized VM
az vm create \
  --name prod-webapp-vm \
  --size Standard_B2s \  # 2 vCPU, 4 GB RAM
  --resource-group prod-app-rg

# Monitor, scale up if needed

❌ BAD - Oversized VM
az vm create \
  --size Standard_D16s_v3 \  # 16 vCPU, 64 GB RAM
  # For workload needing 2 vCPU
  # Wasting 87.5% of capacity
```

**Cost Optimization**:
- Use Reserved Instances (1-3 year commit = 40-60% discount)
- Auto-shutdown for dev/test VMs
- Use Azure Advisor recommendations
- Right-size based on actual metrics

---

## Common Azure CLI Commands

| Command | Purpose |
|---------|---------|
| `az login` | Authenticate to Azure |
| `az account list` | List subscriptions |
| `az account set` | Switch subscription |
| `az group create` | Create resource group |
| `az group delete` | Delete resource group |
| `az resource list` | List resources |
| `az vm create` | Create virtual machine |
| `az network vnet create` | Create virtual network |
| `az storage account create` | Create storage account |
| `az aks create` | Create AKS cluster |

---

## Quick Reference

### Resource Naming Patterns

| Resource Type | Pattern | Example |
|---------------|---------|---------|
| Resource Group | `{env}-{workload}-rg` | `prod-webapp-rg` |
| Virtual Machine | `{env}-{workload}-vm[-{instance}]` | `prod-api-vm-01` |
| Storage Account | `{env}{workload}storage` | `prodwebappstorage` |
| Virtual Network | `{env}-{region}-vnet` | `prod-eastus-vnet` |
| Subnet | `{purpose}-subnet` | `frontend-subnet` |
| NSG | `{purpose}-nsg` | `frontend-nsg` |
| AKS Cluster | `{env}-{workload}-aks` | `prod-api-aks` |

### Common Azure Regions

| Region | Location | Use Case |
|--------|----------|----------|
| eastus | East US | General purpose, low cost |
| westus2 | West US 2 | West coast users |
| centralus | Central US | Central location |
| northeurope | North Europe | GDPR compliance |
| westeurope | West Europe | European users |
| southeastasia | Southeast Asia | APAC users |

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Single Resource Group for Everything

**Problem**: All resources in one RG
**Issue**: Cannot manage lifecycle independently
**Fix**: Separate by environment, workload, or lifecycle

### ❌ Anti-Pattern 2: No Tagging Strategy

**Problem**: Resources without tags
**Issue**: Cannot track costs or ownership
**Fix**: Enforce required tags via Azure Policy

### ❌ Anti-Pattern 3: Overprivileged RBAC

**Problem**: Everyone has Contributor role
**Issue**: Security risk, accidental deletions
**Fix**: Least-privilege access (Reader, specific roles)

### ❌ Anti-Pattern 4: No Cost Budgets

**Problem**: No spending alerts
**Issue**: Surprise bills, cost overruns
**Fix**: Set budgets and alerts in Azure Cost Management

### ❌ Anti-Pattern 5: Public IP on Everything

**Problem**: All VMs have public IPs
**Issue**: Increased attack surface
**Fix**: Private networking with VPN/Bastion access

---

## Common Workflows

### Workflow 1: Create VNet with Subnets

```bash
# 1. Create resource group
az group create --name prod-network-rg --location eastus

# 2. Create VNet
az network vnet create \
  --name prod-eastus-vnet \
  --resource-group prod-network-rg \
  --address-prefix 10.0.0.0/16

# 3. Create frontend subnet
az network vnet subnet create \
  --vnet-name prod-eastus-vnet \
  --name frontend-subnet \
  --resource-group prod-network-rg \
  --address-prefix 10.0.1.0/24

# 4. Create backend subnet
az network vnet subnet create \
  --vnet-name prod-eastus-vnet \
  --name backend-subnet \
  --resource-group prod-network-rg \
  --address-prefix 10.0.2.0/24

# 5. Create NSG for frontend
az network nsg create \
  --name frontend-nsg \
  --resource-group prod-network-rg

# 6. Associate NSG with subnet
az network vnet subnet update \
  --vnet-name prod-eastus-vnet \
  --name frontend-subnet \
  --resource-group prod-network-rg \
  --network-security-group frontend-nsg
```

### Workflow 2: Deploy VM with Managed Identity

```bash
# 1. Create VM with system-assigned identity
az vm create \
  --name prod-webapp-vm-01 \
  --resource-group prod-app-rg \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --vnet-name prod-eastus-vnet \
  --subnet frontend-subnet \
  --assign-identity \
  --tags Environment=production Owner=platform-team

# 2. Get identity principal ID
IDENTITY_ID=$(az vm identity show \
  --name prod-webapp-vm-01 \
  --resource-group prod-app-rg \
  --query principalId -o tsv)

# 3. Grant access to Key Vault
az keyvault set-policy \
  --name prod-keyvault \
  --object-id $IDENTITY_ID \
  --secret-permissions get list

# 4. Application can now access secrets without credentials
```

---

## Navigation Guide

| Need to... | Read this |
|------------|-----------|
| Organize Azure resources | [resource-groups.md](resources/resource-groups.md) |
| Create ARM templates | [arm-templates.md](resources/arm-templates.md) |
| Master Azure CLI | [cli-patterns.md](resources/cli-patterns.md) |

---

## Resource Files

### [resource-groups.md](resources/resource-groups.md)
Resource organization strategies, naming conventions, tagging policies, RBAC patterns

### [arm-templates.md](resources/arm-templates.md)
ARM template structure, parameter patterns, outputs, deployment strategies

### [cli-patterns.md](resources/cli-patterns.md)
Azure CLI automation, scripting patterns, JMESPath queries, output formatting

---

## Related Skills

- **terraform-basics** - Infrastructure-as-code for Azure provisioning
- **task-management** - Dependency analysis for Azure resource ordering

---

**Skill Status**: COMPLETE ✅
**Line Count**: 458 ✅
**Progressive Disclosure**: 3 resource files ✅
