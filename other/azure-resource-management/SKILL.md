---
name: azure-resource-management
description: Manage Azure resources effectively using CLI, Portal, Bicep, and ARM templates. Use for provisioning, organizing, and maintaining cloud infrastructure.
triggers:
- /azure resources
- /azure manage
---

# Azure Resource Management

This skill provides comprehensive guidance for managing Azure resources including provisioning, organizing, securing, and optimizing cloud infrastructure.

## When to use this skill

Use this skill when you need to:
- Create, update, or delete Azure resources
- Organize resources using resource groups and tags
- Implement infrastructure as code using Bicep or ARM templates
- Manage resource lifecycle and governance
- Optimize resource costs and performance

## Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed (az --version)
- Or Azure PowerShell module (optional)
- Understanding of resource hierarchy (Subscription → Resource Groups → Resources)

## Guidelines

### Resource Organization

Follow these principles for organizing Azure resources:

**Resource Groups**
- Group resources by lifecycle (e.g., all resources for a single application)
- Name consistently: `rg-<app>-<env>-<region>` (e.g., `rg-webapp-prod-westus`)
- Tag all resources with: Environment, Owner, Project, CostCenter

**Naming Conventions**
- Use lowercase with hyphens for resource names
- Include environment indicator: dev, staging, prod
- Keep names descriptive but concise (max 24 chars for storage accounts)

### Resource Provisioning Methods

**Azure CLI (Recommended for ad-hoc operations)**
```bash
# Login and set subscription
az login
az account set --subscription "Your Subscription"

# Create resource group
az group create \
  --name rg-myapp-prod \
  --location westus \
  --tags Environment=Production Owner=TeamA Project=MyApp

# Create resources
az storage account create \
  --name myappprodstorage \
  --resource-group rg-myapp-prod \
  --sku Standard_LRS \
  --kind StorageV2
```

**Bicep (Recommended for production)**
- Use Bicep for all production deployments
- Store templates in version control
- Parameterize environment-specific values
- See `examples/resource-deployment.bicep` for a complete example

### Resource Management Best Practices

**Locks and Security**
- Apply resource locks to prevent accidental deletion
- Use Azure Policy to enforce organizational standards
- Implement RBAC with least privilege principle

**Cost Management**
- Enable Cost Alerts at 80% of budget
- Use Reserved Instances for predictable workloads
- Regularly review and delete unused resources
- Tag resources for cost allocation

**Monitoring**
- Enable Azure Monitor for all resources
- Configure Diagnostic Settings to send logs to Log Analytics
- Set up alerts for critical metrics

## Examples

See the `examples/` directory for:
- `resource-deployment.bicep` - Complete Bicep template
- `resource-cleanup.ps1` - Resource cleanup script
- `tagging-strategy.md` - Comprehensive tagging guide

## References

- [Azure Resource Manager documentation](https://docs.microsoft.com/azure/azure-resource-manager/)
- [Bicep documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- [Azure naming conventions](https://docs.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- [Azure Policy samples](https://docs.microsoft.com/azure/governance/policy/samples/)
