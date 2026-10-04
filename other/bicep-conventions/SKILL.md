---
name: bicep-conventions
description: 'Best practices for Azure Bicep Infrastructure as Code covering naming conventions (lowerCamelCase for identifiers, descriptive prefixes for resource names), parameter design with decorators and safe defaults, resource references using symbolic names and the existing keyword, import/export for shared types and user-defined functions, modularization patterns with versioned modules and ACR publishing, loadJsonContent for external configuration, .bicepparam parameter files, subscription-scoped deployments, @batchSize for loop control, security practices (@secure, Key Vault references, no secrets in outputs), and documentation standards. Apply this skill whenever writing, reviewing, modifying, or refactoring .bicep files -- including when the user asks about Bicep parameter design, resource naming, module structure, deployment templates, or Azure IaC patterns, even if they do not explicitly mention "Bicep conventions."'
user-invocable: false
---

# Azure Bicep Conventions and Best Practices

Follow these conventions when writing, reviewing, or refactoring Bicep templates to produce secure, maintainable, and idiomatic Infrastructure as Code.

## File Structure

Organize every Bicep file in a consistent top-to-bottom order so readers always know where to look:

1. `import` statements (for shared types and functions from other files)
2. `targetScope` (if not the default `resourceGroup`)
3. `metadata` (optional -- file-level description)
4. `type` definitions (user-defined types)
5. `func` declarations (user-defined functions)
6. `param` declarations
7. `var` declarations
8. `resource` and `module` statements
9. `output` declarations

```bicep
import { environment as env, resourceName } from '../modules/naming.1.0.bicep'

targetScope = 'subscription'

metadata description = 'Deploys the core networking stack for the production environment.'

// Types and functions
@export()
type environment = 'DEV' | 'UAT' | 'PROD'

// Parameters
@description('The Azure region for all resources.')
param location string

// Variables
var vnetName = resourceName(environment, 'network', 'vnet')

// Resources
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = { ... }

// Outputs
output vnetId string = vnet.id
```

## Naming Conventions

### Symbolic Names

Symbolic names are identifiers used only within the Bicep file -- they never appear in Azure. They should be optimized for readability.

- Use **lowerCamelCase** for all symbolic names: parameters, variables, resources, modules, and outputs.
- Choose descriptive names that convey purpose: `storageAccount` rather than `sa`, `appServicePlan` rather than `asp`.
- Do not include the word `name` in a symbolic name that represents the resource itself -- `storageAccount` is the resource, `storageAccountName` is a string holding its Azure name.

```bicep
// Good
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = { ... }
param deploymentEnvironment string

// Avoid
resource sa 'Microsoft.Storage/storageAccounts@2023-05-01' = { ... }
param env string
```

### Azure Resource Names

Azure resource names (the `name` property) must be globally or regionally unique depending on the service. Use `uniqueString()` seeded with the resource group ID and a descriptive prefix to guarantee uniqueness while remaining identifiable.

```bicep
var storageAccountName = 'st${uniqueString(resourceGroup().id)}' // st + 13-char hash
var keyVaultName = 'kv-${workloadName}-${uniqueString(resourceGroup().id)}'
```

- Use consistent, short prefixes that identify the resource type (e.g., `st` for storage accounts, `kv-` for Key Vault, `vnet-` for virtual networks).
- Keep names within the service-specific length and character constraints.

## Parameters

Parameters are the public interface of a Bicep file or module. Design them for clarity and safety.

### Decorators

Always annotate parameters with `@description()` so that consumers and documentation generators understand each parameter's purpose:

```bicep
@description('The Azure region where resources will be deployed.')
param location string = resourceGroup().location

@description('The name of the workload, used as a prefix in resource names.')
@minLength(2)
@maxLength(10)
param workloadName string
```

Use validation decorators (`@minLength`, `@maxLength`, `@minValue`, `@maxValue`) to catch invalid input early. Use `@allowed()` sparingly -- it is appropriate for genuinely constrained sets (SKU names, Azure regions), but over-constraining makes templates brittle when new options become available.

### Defaults

Provide defaults that produce a safe, low-cost deployment suitable for test environments. This lets developers deploy without specifying every parameter while keeping production deployments explicit.

```bicep
@description('The SKU for the App Service plan.')
param appServicePlanSku string = 'B1'

@description('Whether to enable zone redundancy.')
param zoneRedundant bool = false
```

### Object and Array Parameters

When a resource requires several related settings, group them into an object parameter with a user-defined type rather than declaring many individual parameters:

```bicep
type networkConfig = {
  vnetAddressPrefix: string
  subnetAddressPrefix: string
  enableDdosProtection: bool
}

@description('Network configuration for the deployment.')
param network networkConfig = {
  vnetAddressPrefix: '10.0.0.0/16'
  subnetAddressPrefix: '10.0.1.0/24'
  enableDdosProtection: false
}
```

### Settings that Vary by Deployment

Use parameters for values that genuinely change between deployments: environment names, SKUs, region, feature flags. Values that are derived or constant belong in variables.

## Variables

Variables hold values that are computed from parameters or that simplify repeated expressions. Bicep auto-infers variable types, so do not annotate them.

```bicep
var appServiceName = 'app-${workloadName}-${environment}'
var isProduction = environment == 'prod'
var tags = {
  workload: workloadName
  environment: environment
  managedBy: 'bicep'
}
```

Use variables to avoid repeating complex expressions and to give meaningful names to intermediate values.

## Resource References

### Symbolic Names over Functions

Prefer symbolic references over `reference()`, `resourceId()`, or string-interpolated resource IDs. Symbolic references let Bicep infer dependencies automatically and catch errors at compile time.

```bicep
// Good -- symbolic reference
output storageEndpoint string = storageAccount.properties.primaryEndpoints.blob

// Avoid -- manual reference
output storageEndpoint string = reference(resourceId('Microsoft.Storage/storageAccounts', storageAccountName)).properties.primaryEndpoints.blob
```

### The existing Keyword

Use the `existing` keyword to reference resources that are already deployed rather than passing around resource IDs as strings:

```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
  scope: resourceGroup(keyVaultResourceGroupName)
}

resource secret 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'my-secret'
  properties: {
    value: secretValue
  }
}
```

### Child Resources

Use the `parent` property to declare child resources. Avoid deeply nested resource declarations because they reduce readability:

```bicep
// Good -- parent property
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' = {
  parent: vnet
  name: 'snet-app'
  properties: {
    addressPrefix: '10.0.1.0/24'
  }
}

// Avoid -- deeply nested inline
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' = {
  name: vnetName
  properties: {
    subnets: [
      {
        name: 'snet-app'
        properties: { addressPrefix: '10.0.1.0/24' }
      }
      // More subnets nested here become hard to maintain
    ]
  }
}
```

## API Versions

Always use the **latest stable** API version for each resource type. Avoid preview API versions in production templates unless you need a feature that is only available in preview. Pin to a specific date rather than a floating reference so builds are reproducible.

```bicep
// Good -- latest stable at time of writing
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = { ... }

// Avoid -- outdated
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-02-01' = { ... }
```

## Modularization

Break large templates into focused modules. Each module should represent a logical unit (a single resource with its supporting resources, or a pattern like "web app with monitoring").

### Module Design Principles

- **Consistent interface**: accept parameters for anything that varies, expose outputs for anything the caller needs.
- **Minimal surface**: pass only the parameters the module requires -- do not forward the entire parent parameter set.
- **Reusability**: a well-designed module works across environments without modification.

```bicep
// main.bicep
module webApp 'modules/web-app.bicep' = {
  name: 'deploy-web-app'
  params: {
    location: location
    appServicePlanId: appServicePlan.id
    appName: appName
    tags: tags
  }
}

// modules/web-app.bicep
@description('Resource ID of the App Service plan.')
param appServicePlanId string

@description('Name for the App Service.')
param appName string

@description('Azure region.')
param location string

@description('Tags to apply to all resources.')
param tags object

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  tags: tags
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
  }
}

output webAppHostName string = webApp.properties.defaultHostName
```

### Resource Loops

Use `for` loops to deploy multiple instances of a resource from an array or range. This avoids copy-paste and keeps the template declarative:

```bicep
param subnetConfigs array = [
  { name: 'snet-app', addressPrefix: '10.0.1.0/24' }
  { name: 'snet-data', addressPrefix: '10.0.2.0/24' }
]

resource subnets 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' = [
  for config in subnetConfigs: {
    parent: vnet
    name: config.name
    properties: {
      addressPrefix: config.addressPrefix
    }
  }
]
```

## Language Features

Use modern Bicep features to keep templates concise and readable:

- **String interpolation** over `concat()`:
  ```bicep
  var name = 'app-${workloadName}-${environment}'   // Good
  var name = concat('app-', workloadName, '-', environment)  // Avoid
  ```

- **Ternary operator** for conditional values:
  ```bicep
  var sku = isProduction ? 'P1v3' : 'B1'
  ```

- **Null-coalescing operator** (`??`) for fallback values:
  ```bicep
  var region = customRegion ?? resourceGroup().location
  ```

- **Spread operator** (`...`) for merging objects:
  ```bicep
  var allTags = { ...baseTags, ...environmentTags }
  ```

## Security

Bicep templates often handle credentials, connection strings, and other sensitive values. Mishandling them creates security vulnerabilities that persist in deployment history and logs.

### Sensitive Parameters

Mark parameters that accept secrets with `@secure()` so their values are never logged or displayed in deployment history:

```bicep
@secure()
@description('The administrator password for the SQL server.')
param sqlAdminPassword string
```

### Key Vault References

For production deployments, reference secrets from Azure Key Vault in parameter files rather than passing them as plain text. This keeps secrets out of source control entirely:

```json
{
  "sqlAdminPassword": {
    "reference": {
      "keyVault": { "id": "/subscriptions/.../providers/Microsoft.KeyVault/vaults/myVault" },
      "secretName": "sql-admin-password"
    }
  }
}
```

### Outputs

Never expose secrets, connection strings, passwords, or keys in outputs. Outputs are stored in plaintext in the deployment history and are visible to anyone with read access to the resource group. If a downstream resource needs a secret, pass it through Key Vault or use the `existing` keyword to look it up directly.

```bicep
// Good -- output only non-sensitive identifiers
output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name

// Dangerous -- never do this
output storageKey string = storageAccount.listKeys().keys[0].value
```

### HTTPS by Default

When deploying web-facing resources, enable HTTPS-only settings:

```bicep
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  properties: {
    httpsOnly: true
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
  }
}
```

## Tagging

Apply consistent tags to all resources for cost tracking, ownership, and operational purposes. Define tags as a variable or parameter and spread them onto every resource:

```bicep
var tags = {
  workload: workloadName
  environment: environment
  managedBy: 'bicep'
  costCenter: costCenter
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  tags: tags
  ...
}
```

## Dependencies

Bicep automatically infers deployment dependencies from symbolic references. Use explicit `dependsOn` only when there is an implicit ordering requirement that Bicep cannot detect (e.g., a role assignment must complete before a resource tries to access a storage account). Over-using `dependsOn` slows deployments by serializing operations that could run in parallel.

```bicep
// Implicit dependency -- Bicep infers that webApp depends on appServicePlan
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  properties: {
    serverFarmId: appServicePlan.id  // Bicep detects this reference
  }
}

// Explicit dependsOn -- only when necessary
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  dependsOn: [storageAccount]
  ...
}
```

## Imports, Exports, and User-Defined Functions

### Sharing Types and Functions Across Files

Use `@export()` to expose types and functions from a file, and `import` to consume them elsewhere. This is the primary mechanism for sharing naming conventions, custom types, and utility functions across a Bicep project.

```bicep
// modules/naming.1.0.bicep -- shared naming module

@export()
type environment = 'DEV' | 'UAT' | 'PROD'

@export()
@description('Get a resource name using the organizational naming convention')
func resourceName(
  environment environment,
  function string,
  resourceTypeAbbreviation string) string =>
  toLower(join([ 'org', 'platform', environment, function, resourceTypeAbbreviation, '01' ], '-'))

@export()
func resourceGroupName(environment environment) string =>
  'org-platform-${toLower(environment)}-rg'
```

```bicep
// environment/main.bicep -- consumer
import { environment as env, resourceName, resourceGroupName } from '../modules/naming.1.0.bicep'

param environment env

resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName(environment)
  location: location
}
```

### User-Defined Types

Define custom types with `@export()` to enforce consistent shapes across modules. This is especially useful for shared parameter structures like principal objects, IP allowlists, or configuration objects:

```bicep
// types/entra-principal.bicep
@description('Entra principal (user or group) with admin access')
@export()
type entraPrincipal = {
  @description('Display name of the principal')
  name: string
  @description('Object ID of the principal in Entra ID')
  objectId: string
  @description('Type of principal')
  type: 'User' | 'Group'
}
```

### Naming Convention Module Pattern

Centralizing all resource naming into a dedicated module is a key enterprise pattern. It ensures every resource across all templates follows the same naming standard. Version the module file (e.g., `naming.1.0.bicep`, `naming.1.1.bicep`) so that existing templates can pin to a known version while new features are added.

## External Configuration with loadJsonContent

Use `loadJsonContent()` to load structured configuration from JSON files. This keeps Bicep templates focused on resource definitions while externalizing environment-specific data, tag sets, or access control lists:

```bicep
// Load tags from a shared JSON file, keyed by environment
var tags = loadJsonContent('../../tags.json')['${environment}']

// Load admin access configuration
var adminAccess = loadJsonContent('../../admin-access.json')['${environment}']

resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: rgName
  location: location
  tags: tags
}
```

Use the pattern `tags: empty(tags) ? null : tags` when tags may be an empty object and the resource does not accept empty tag objects.

## Parameter Files (.bicepparam)

Use `.bicepparam` files for environment-specific parameter values. These are type-safe and support expressions, unlike legacy JSON parameter files:

```bicep
// main.dev.bicepparam
using './main.bicep'

param environment = 'DEV'
param location = 'westeurope'
param zoneRedundant = false
```

```bicep
// main.prod.bicepparam
using './main.bicep'

param environment = 'PROD'
param location = 'westeurope'
param zoneRedundant = true
```

Prefer `.bicepparam` over JSON parameter files for new projects. Name them to match the template: `main.dev.bicepparam`, `main.prod.bicepparam`.

## Module Versioning and Registry Publishing

For enterprise teams sharing modules across repositories, publish versioned Bicep modules to an Azure Container Registry (ACR):

- Name module files with semver: `naming.1.0.bicep`, `role-assignments/cosmos.1.0.bicep`
- Publish to ACR: `br:myregistry.azurecr.io/bicep/modules/naming:1.0`
- Consumers reference published modules:
  ```bicep
  module naming 'br:myregistry.azurecr.io/bicep/modules/naming:1.0' = {
    name: 'naming'
  }
  ```
- Bump the minor version for backwards-compatible changes, major for breaking changes
- Automate publishing in CI/CD pipelines

## Additional Decorators

### @batchSize

Use `@batchSize()` on resource or module loops to control parallelism. Set to `1` for serial deployment when resources have ordering dependencies that Bicep cannot infer (e.g., role assignments that must complete one at a time):

```bicep
@batchSize(1)
module roleAssignments 'modules/role-assignment.bicep' = [for principal in principals: {
  name: 'role-${principal.name}'
  params: {
    principalId: principal.objectId
    roleDefinitionId: readerRoleId
  }
}]
```

## Subscription-Scoped Deployments

For deployments that create resource groups and orchestrate cross-group resources, set `targetScope = 'subscription'` and create resource groups inline:

```bicep
targetScope = 'subscription'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName(environment)
  location: location
  tags: tags
}

module network 'network.bicep' = {
  name: 'network'
  scope: resourceGroup
  params: {
    location: location
    environment: environment
    tags: tags
  }
}
```

Use `scope: resourceGroup` to target modules at specific resource groups. This pattern enables a single main.bicep to orchestrate an entire environment with multiple resource groups and cross-group dependencies.

## Documentation

Include `//` comments to explain non-obvious decisions, workarounds, and the reasoning behind specific configurations. Comments are free -- they do not appear in the compiled ARM template.

```bicep
// Using a Premium SKU here because the workload requires zone redundancy
// and the Standard SKU does not support availability zones in this region.
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
  }
  properties: {
    zoneRedundant: true
  }
}
```

Use `@description()` on every parameter and output so that tooling (VS Code, `az deployment what-if`, documentation generators) can surface useful information without reading the template body.
