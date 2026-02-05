---
name: converting-to-strong-types
description: Converts loosely typed Bicep parameters using object or array to strongly typed alternatives like string[], user-defined types, or resource-derived types. Use when user mentions type safety, weak typing, object parameters, array parameters, resourceInput, resourceOutput, or asks to improve parameter definitions.
---

# Converting to Strong Types

Replaces loose `object` and `array` parameter types with strong alternatives for compile-time validation and autocompletion.

## Conversion Workflow

Copy and track progress:

```
Conversion Progress:
- [ ] Step 1: Identify loose types
- [ ] Step 2: Analyze parameter usage
- [ ] Step 3: Choose conversion strategy
- [ ] Step 4: Define types and update parameters
- [ ] Step 5: Validate with bicep build
```

**Step 1: Identify loose types**

Search for `param <name> object` and `param <name> array` declarations.

**Step 2: Analyze parameter usage**

Examine how the parameter is used in the template to determine expected structure.

**Step 3: Choose conversion strategy**

| Pattern | Strategy |
|---------|----------|
| Array of primitives | `string[]`, `int[]`, `bool[]` |
| Array with constrained values | `('value1' \| 'value2')[]` |
| Object matching resource property | `resourceInput<'Type@Version'>.properties.X` |
| Custom object structure | User-defined type with `type` keyword |
| Array of objects | User-defined type with `[]` suffix |

**Step 4: Define types and update parameters**

Place type definitions above parameters. Add `@description()` decorators.

**Step 5: Validate**

Run `bicep build <file>` to verify syntax and type correctness.

## Quick Reference

### Simple Arrays

```bicep
// Before
param addresses array

// After
param addresses string[]
```

### Union Types (Constrained Values)

```bicep
param environments ('dev' | 'staging' | 'prod')[]
param skuName 'Standard_LRS' | 'Premium_LRS'
```

### User-Defined Types

```bicep
type subnetType = {
  name: string
  addressPrefix: string
  nsgId: string?  // Optional property
}

param subnets subnetType[]
```

### Resource-Derived Types

```bicep
// Derive from Azure schema (Bicep 0.34.1+)
type accountKind = resourceInput<'Microsoft.Storage/storageAccounts@2024-01-01'>.kind
param storageProps resourceInput<'Microsoft.Storage/storageAccounts@2024-01-01'>.properties
```

**For full resource-derived type details**: See [RESOURCE-DERIVED.md](RESOURCE-DERIVED.md)

## Type Best Practices

- Use `?` for optional properties: `description: string?`
- Use `@sealed()` to prevent extra properties at deployment
- Use `@description()` on types and properties
- Use constraints: `@minLength()`, `@maxLength()`, `@minValue()`, `@maxValue()`
- Compose complex types from simpler types

## Common Patterns

**For ready-to-use type definitions**: See [PATTERNS.md](PATTERNS.md)

Includes: tags, access policies, subnets, diagnostic settings, role assignments, private endpoints.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `Bicep:get_bicep_best_practices` | Current best practices |
| `Bicep:get_az_resource_type_schema` | Schema for resource-derived types |
| `Bicep:list_az_resource_types_for_provider` | Available types and API versions |

## Edge Cases

**Dynamic objects** (unknown keys): Use wildcard `{ *: string }`

**Mixed-type arrays**: Use union `(string | int | bool)[]`

**Backward compatibility**: Use optional types `?` for new properties
