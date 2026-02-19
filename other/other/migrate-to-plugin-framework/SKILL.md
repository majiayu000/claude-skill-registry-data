---
name: migrate-to-plugin-framework
description: >-
  This skill should be used when migrating Terraform provider data sources or
  resources from hashicorp/terraform-plugin-sdk/v2 to
  hashicorp/terraform-plugin-framework. Trigger phrases include "migrate to
  plugin framework", "SDK v2 to plugin framework", "convert to plugin framework",
  "migrate data source", "migrate resource", "plugin framework migration",
  "move to framework", or "upgrade from SDK v2". Provides step-by-step migration
  workflow, code patterns, schema mapping, and common gotchas.
---

# Terraform SDK v2 to Plugin Framework Migration

Migrate Terraform provider data sources and resources from `terraform-plugin-sdk/v2` to
`terraform-plugin-framework`, following patterns established by completed migrations in the
target codebase.

## Prerequisites

Before starting any migration, read the following to understand context:

1. The existing SDK v2 source file being migrated
2. Any existing migration notes or lessons-learned docs in the target repo (e.g. a `PLUGIN_FRAMEWORK_LESSONS_LEARNED.md` or similar)
3. The API client types used by the resource/data source

## Migration Workflow

### Phase 1: Analyse the SDK v2 Source

1. Read the existing SDK v2 file to understand:
   - Schema fields: types, Optional/Required/Computed, validation, defaults
   - CRUD operations: which API calls are made
   - Helper functions: filter logic, flatten functions, state waiting
   - CustomizeDiff: any custom validation logic
2. Identify the API client methods and response types used
3. Check for nested blocks (`TypeSet`/`TypeList` with `Elem: &schema.Resource{}`)
4. Note any `ForceNew`, `DiffSuppressFunc`, or `DefaultFunc` usage

### Phase 2: Create Package Structure

Create the target package directory. Follow the 3-file pattern:

**Data sources:**
```
internal/<package>/
├── datasource_<name>.go         # Schema, interfaces, Metadata, Configure
├── datasource_<name>_model.go   # Model struct with tfsdk tags
├── datasource_<name>_read.go    # Read implementation + helpers
└── helpers.go                   # Shared utilities (if needed)
```

**Resources:**
```
internal/<package>/
├── resource_<name>.go           # Schema, interfaces, Metadata, Configure, ModifyPlan
├── resource_<name>_model.go     # Model struct(s) with tfsdk tags
├── resource_<name>_crud.go      # Create, Read, Update, Delete implementations
└── helpers.go                   # Shared utilities (if needed)
```

> **Note:** Adapt the directory layout to match the target provider's existing conventions. Some providers use `internal/provider/`, others use `internal/<feature>/`, etc.

### Phase 3: Write the Model File

Create the model struct. Key rules:

- **`id` is always `types.String`** — even if SDK v2 used `TypeInt`
- Use `types.String`, `types.Bool`, `types.Int64`, `types.Float64` for scalars
- Use `types.Set`, `types.List`, `types.Map` for collections
- Every field needs a `tfsdk:"field_name"` tag matching the schema attribute name

Consult `references/schema-mapping.md` for the full type mapping table.

### Phase 4: Write the Schema File

Create the schema definition. Follow this structure:

1. **Interface checks** — compile-time verification of interface compliance
2. **Struct definition** — holds the provider's API client
3. **Constructor** — `NewXxxDataSource()` or `NewXxxResource()`
4. **Metadata** — sets `TypeName` to `req.ProviderTypeName + "_suffix"`
5. **Configure** — extracts the API client from `req.ProviderData`
6. **Schema** — defines all attributes and blocks

Critical rules for schema definition:
- **Protocol v5 constraint**: SDK v2 `TypeSet`/`TypeList` with `Elem: &schema.Resource{}` MUST become `SetNestedBlock`/`ListNestedBlock` in the `Blocks` map, NOT `SetNestedAttribute`/`ListNestedAttribute` in `Attributes`. See `references/lessons-learned.md` Lesson 1.
- **Explicit `id`**: Declare `id` as `schema.StringAttribute{Computed: true}` — the framework has no implicit `id`.
- **SDK v2 `ForceNew`** becomes `planmodifier.RequiresReplace()` in the framework.
- **SDK v2 `DefaultFunc`** becomes `Default` (e.g., `stringdefault.StaticString("value")`).
- **SDK v2 `DiffSuppressFunc`** becomes a custom `planmodifier`.
- **SDK v2 `CustomizeDiff`** becomes `ModifyPlan` (implement `ResourceWithModifyPlan` interface).

Consult `references/data-source-pattern.md` or `references/resource-pattern.md` for full code templates.

### Phase 5: Write the Read/CRUD File

Implement the operations. Key patterns:

1. **Defensive nil check** on `d.client` at the start of every operation
2. **Read config/state** via `req.Config.Get(ctx, &state)` (data sources) or `req.Plan.Get(ctx, &plan)` (resources)
3. **API pointer dereference** — if the API client returns pointer types (`*string`, `*int`), dereference safely with nil checks or helper functions
4. **Filter pattern** for data sources: list all items, apply filters, expect exactly 1 result
5. **Set state** via `resp.State.Set(ctx, &state)`
6. **Concurrency control** — if the provider uses mutexes for safe concurrent access, replicate that pattern
7. **State waiting** for resources: wait for the resource to reach a stable state after mutations

For nested objects, use `types.ObjectValueFrom(ctx, attrTypes, model)` — see `references/lessons-learned.md` Lesson 7.

### Phase 6: Register the New Implementation

Three changes required:

1. **Add to the framework provider**: Import the new package, add to `DataSources()` or `Resources()` return slice
2. **Remove from the SDK provider**: Delete the entry from `DataSourcesMap` or `ResourcesMap`
3. **Delete the old SDK v2 file**

> **Note:** The exact file names depend on the target provider's conventions. Look for how existing framework data sources/resources are registered.

### Phase 7: Update Tests

- If tests exist in the same package, they may continue to work without changes
- If migrating tests to the new package, update imports and use `protoV5ProviderFactories`
- Existing tests validate that the migration is behaviourally equivalent

### Phase 8: Update Documentation

Update the corresponding `docs/data-sources/` or `docs/resources/` markdown file if the schema changed (e.g., `id` type change from int to string).

## Migration Checklist

Use this as a tracking checklist for each migration:

- [ ] Read and understand SDK v2 source
- [ ] Create package directory
- [ ] Write model file (`_model.go`)
- [ ] Write schema file (`.go`)
- [ ] Write read/CRUD file (`_read.go` or `_crud.go`)
- [ ] Write helpers if needed (`helpers.go`)
- [ ] Add to framework provider
- [ ] Remove from SDK provider
- [ ] Delete old SDK v2 file
- [ ] Verify build: `go build ./...`
- [ ] Update tests if needed
- [ ] Update docs if needed
- [ ] Provide test command for user to run

## Common Gotchas

1. **`SetNestedAttribute` causes runtime panic** with muxed providers (protocol v5). Always use `SetNestedBlock`.
2. **Missing `id` attribute** causes cryptic test failures. Always declare it explicitly.
3. **API returns pointer types** (`*string`, `*int`). Dereference safely — never pass a nil pointer to `types.StringValue()`.
4. **Nil slice elements** in API responses. Always check `if item == nil { continue }` in loops.
5. **`d.SetId()` doesn't exist**. Assign directly to `state.ID = types.StringValue(...)`.

## Reference Files

For detailed patterns, code templates, and examples:

- **`references/lessons-learned.md`** — 9 lessons from completed migrations with full code examples
- **`references/data-source-pattern.md`** — Complete data source migration template
- **`references/resource-pattern.md`** — Complete resource migration template
- **`references/schema-mapping.md`** — SDK v2 to Plugin Framework type mapping table
