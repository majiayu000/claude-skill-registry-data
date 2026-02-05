---
name: converting-bicep-to-avm
description: Converts raw Bicep resource definitions to Azure Verified Modules (AVM). Use when user asks to convert to AVM, replace resources with modules, use verified modules, or modernize bicep templates.
---

# Converting Bicep to AVM Skill

## Before Converting

Call `Bicep:list_avm_metadata` MCP tool to get available Azure Verified Modules and their versions.

## Conversion Workflow

1. **Identify resources** — List all `resource` declarations in the template
2. **Find AVM matches** — Call `Bicep:list_avm_metadata`, match by resource type
3. **Map properties** — Translate resource properties to AVM parameters
4. **Generate module** — Create `module` declaration with registry reference
5. **Update references** — Replace `resource.property` with `module.outputs.property`
6. **Validate** — Lint the Bicep template and afterwards run `bicep build` to verify syntax
7. **Fix errors** — If build fails, review error, fix mapping, return to step 6

## AVM Module Reference Format

```bicep
module <symbolicName> 'br/public:avm/res/<provider>/<resource>:<version>' = {
  name: '<deploymentName>'
  params: {
    name: <resourceName>
    location: <location>
    // AVM-specific parameters
  }
}
```

## Common Resource Type Mappings

| Resource Type | AVM Module Path |
|---------------|-----------------|
| `Microsoft.KeyVault/vaults` | `avm/res/key-vault/vault` |
| `Microsoft.Storage/storageAccounts` | `avm/res/storage/storage-account` |
| `Microsoft.Web/sites` | `avm/res/web/site` |
| `Microsoft.Compute/virtualMachines` | `avm/res/compute/virtual-machine` |
| `Microsoft.Network/virtualNetworks` | `avm/res/network/virtual-network` |
| `Microsoft.ContainerRegistry/registries` | `avm/res/container-registry/registry` |
| `Microsoft.Sql/servers` | `avm/res/sql/server` |

⚠️ **Always call `Bicep:list_avm_metadata`** for current modules and versions. This table is for reference only and may be outdated.

## Property Mapping Guidelines

### Common Patterns

| Raw Resource | AVM Parameter |
|--------------|---------------|
| `properties.sku.name` | `skuName` |
| `properties.sku.tier` | Often bundled in `skuName` |
| `tags` | `tags` (same) |
| `location` | `location` (same) |
| `name` | `name` (same) |
| `properties.accessPolicies` | `accessPolicies` (flattened) |

### AVM Adds Common Features

AVM modules often include built-in support for:
- Diagnostic settings (`diagnosticSettings`)
- Role assignments (`roleAssignments`)
- Private endpoints (`privateEndpoints`)
- Locks (`lock`)
- Tags (`tags`)

## Handling No AVM Match

If no AVM module exists:

1. Keep the raw resource definition
2. Add comment: `// TODO: No AVM module available for <resourceType>`
3. Check for pattern modules (`avm/ptn/*`) as alternatives

## Output Transformation

**Before:**
```bicep
output keyVaultUri string = keyVault.properties.vaultUri
```

**After:**
```bicep
output keyVaultUri string = keyVaultModule.outputs.uri
```

Note: AVM output names differ from raw properties — check module documentation.

## Conversion Report Format

```markdown
## AVM Conversion: [filename]

### Converted
| Resource | AVM Module | Version |
|----------|------------|---------|
| keyVault | avm/res/key-vault/vault | 0.11.0 |

### Not Converted
| Resource | Reason |
|----------|--------|
| customResource | No AVM module available |

### Manual Review Required
- [ ] Verify parameter mappings
- [ ] Update output references
- [ ] Test deployment
```
