---
name: bicep
description: "Covers Azure Bicep and ARM templates: Bicep DSL, modules, parameters, resource declarations, deployment scopes, template specs, and migration from ARM JSON. WHEN: \"Bicep\", \".bicep\", \"ARM template\", \"Azure Resource Manager\", \"az deployment\", \"Bicep module\", \"deployment stack\", \"template spec\", \"Azure IaC\"."
license: MIT
---

# Azure Bicep / ARM Expert

This skill covers Azure Bicep and ARM templates. Bicep is Azure's domain-specific language (DSL) for deploying Azure resources declaratively. It transpiles to ARM JSON templates. Bicep is a managed tool with continuous updates — no traditional versioning.

For foundational IaC concepts (state, drift, idempotency), refer to the parent IaC agent.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md`
   - **Architecture** -- Load `references/architecture.md`
   - **Best practices** -- Load `references/best-practices.md`
   - **ARM to Bicep migration** -- Cover decompilation and refactoring

2. **Default to Bicep** -- Always recommend Bicep over raw ARM JSON for new projects. Bicep is simpler, type-safe, and transpiles to ARM.

3. **Recommend** -- Provide Bicep code examples with `az deployment` CLI commands.

## Core Concepts

### Bicep File Structure

```bicep
// main.bicep
targetScope = 'resourceGroup'  // or subscription, managementGroup, tenant

@description('Environment name')
@allowed(['dev', 'staging', 'production'])
param environment string

@description('Azure region')
param location string = resourceGroup().location

@secure()
param sqlAdminPassword string

// Variables
var prefix = '${environment}-myapp'

// Resources
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: '${replace(prefix, '-', '')}stor'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: '${prefix}-web'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: '${prefix}-plan'
  location: location
  sku: {
    name: environment == 'production' ? 'P1v3' : 'B1'
  }
}

// Outputs
output storageAccountName string = storageAccount.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
```

### Resource Declaration

```bicep
// Symbolic name     Resource type                          API version
resource myVnet      'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'prod-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: ['10.0.0.0/16']
    }
    subnets: [
      {
        name: 'web-subnet'
        properties: {
          addressPrefix: '10.0.1.0/24'
        }
      }
    ]
  }
}

// Child resource (nested)
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = {
  parent: myVnet
  name: 'db-subnet'
  properties: {
    addressPrefix: '10.0.2.0/24'
  }
}

// Existing resource (reference without creating)
resource existingVnet 'Microsoft.Network/virtualNetworks@2024-05-01' existing = {
  name: 'existing-vnet-name'
}
```

### Modules

```bicep
// modules/storage.bicep
param name string
param location string
param sku string = 'Standard_LRS'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  sku: { name: sku }
  kind: 'StorageV2'
}

output id string = storageAccount.id
output name string = storageAccount.name
```

```bicep
// main.bicep — consuming a module
module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'
  params: {
    name: 'myappstorage'
    location: location
  }
}

// Use module output
output storageId string = storage.outputs.id
```

### Module Sources

```bicep
// Local file
module local 'modules/storage.bicep' = { ... }

// Bicep Registry (ACR)
module registry 'br:myregistry.azurecr.io/bicep/modules/storage:v1.0' = { ... }

// Template Spec
module templateSpec 'ts:subscriptionId/resourceGroup/templateSpecName:v1.0' = { ... }

// Public Module Registry
module publicModule 'br/public:avm/res/storage/storage-account:0.8.0' = { ... }
```

### Deployment Scopes

```bicep
// Resource group (default)
targetScope = 'resourceGroup'

// Subscription level (create resource groups, policies)
targetScope = 'subscription'

// Management group level (policies, blueprints)
targetScope = 'managementGroup'

// Tenant level (management groups)
targetScope = 'tenant'
```

### Loops and Conditions

```bicep
// Loop
param subnetNames array = ['web', 'api', 'db']

resource subnets 'Microsoft.Network/virtualNetworks/subnets@2024-05-01' = [for (name, i) in subnetNames: {
  parent: vnet
  name: name
  properties: {
    addressPrefix: '10.0.${i + 1}.0/24'
  }
}]

// Conditional
param deployRedis bool = false

resource redis 'Microsoft.Cache/redis@2024-03-01' = if (deployRedis) {
  name: '${prefix}-redis'
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 1
    }
  }
}
```

### Deployment Stacks

Deployment stacks manage resource lifecycle across deployments:

```bash
# Create a deployment stack (prevents orphaned resources)
az stack group create \
  --name my-stack \
  --resource-group my-rg \
  --template-file main.bicep \
  --deny-settings-mode denyDelete \
  --action-on-unmanage deleteAll
```

## CLI Reference

```bash
# Deploy to resource group
az deployment group create \
  --resource-group my-rg \
  --template-file main.bicep \
  --parameters environment=production

# Deploy to subscription
az deployment sub create \
  --location eastus \
  --template-file main.bicep

# What-if (preview changes)
az deployment group what-if \
  --resource-group my-rg \
  --template-file main.bicep

# Validate template
az bicep build --file main.bicep
az deployment group validate --resource-group my-rg --template-file main.bicep

# Decompile ARM JSON to Bicep
az bicep decompile --file template.json

# Publish module to registry
az bicep publish --file module.bicep --target br:myregistry.azurecr.io/bicep/modules/storage:v1.0
```

## Reference Files

- `references/architecture.md` — Bicep compilation, ARM deployment engine, deployment scopes, template spec and registry architecture, deployment stacks
- `references/best-practices.md` — Module design, naming conventions, parameter validation, Bicep linting, CI/CD integration, AVM (Azure Verified Modules)
- `references/diagnostics.md` — Deployment failures, what-if analysis, resource errors, decompilation issues, API version compatibility
