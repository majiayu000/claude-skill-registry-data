---
description: Add, update, or remove UI Kit to Nimbus migration mappings in the MCP migration data
argument-hint: add|update|remove UiKitComponentName [NimbusEquivalent]
---

# Update UI Kit Migration Mapping

You are a migration data specialist. This skill helps maintain the UI Kit to
Nimbus component migration mappings used by the `migrate_from_uikit` MCP tool.

## Data Location

All migration data lives in a single file:

```
packages/nimbus-mcp/src/data/uikit-migration.ts
```

This file contains:

- `UiKitMappingType` — the type of migration (`direct`, `variant`, `compound`,
  `pattern`, `removed`)
- `UiKitMigrationEntry` — the interface for each mapping entry
- `MIGRATION_DATA` — the array of all migration entries
- Lookup helpers (`getUiKitMigration`, `getUiKitCompoundMigrations`,
  `getAllUiKitMigrations`)

## Mode Detection

Parse the request to determine the operation:

- **add** — Add a new mapping entry for a UI Kit component
- **update** — Modify an existing mapping (fix notes, breaking changes, mapping
  type, etc.)
- **remove** — Remove a mapping entry that is incorrect or no longer needed

If no mode is specified, ask the user what they want to do.

## Step 1: Read Current State

Always read the migration data file first:

```
packages/nimbus-mcp/src/data/uikit-migration.ts
```

For **add** mode, verify the component doesn't already have a mapping. For
**update** and **remove** modes, find the existing entry.

## Step 2: Research (for add and update)

When adding or updating a mapping, gather information to write accurate data:

1. **Check the Nimbus component** — Read the component's types, recipe, and main
   file to understand its API:

   ```
   packages/nimbus/src/components/<component-name>/
   ```

2. **Check UI Kit documentation** if the user provides context about the UI Kit
   component's API, use that. Otherwise, ask the user for:
   - The UI Kit component name and package
   - Key props and their types
   - How the component is typically used

3. **Determine the mapping type**:
   - `direct` — 1:1 replacement with same or very similar API
   - `variant` — Becomes a prop/variant value on a Nimbus component (e.g.
     `PrimaryButton` → `<Button variant="solid">`)
   - `compound` — Replaced by composing multiple Nimbus components
   - `pattern` — Replaced by design tokens or layout patterns
   - `removed` — No Nimbus equivalent exists

4. **Check for slot-prop collapse** — If UIKit props (e.g. `label`, `icon`)
   become `children` in Nimbus, add a `propMigrations` array:

   ```typescript
   propMigrations: [
     { from: "label", to: "children" },
     { from: "icon", to: "children", position: "before" },
   ],
   ```

5. **Check for code-deletion patterns** — If the Nimbus component has built-in
   functionality that replaces custom consumer code (e.g. selection columns),
   add a `codeReduction` object:

   ```typescript
   codeReduction: {
     type: "selection-model-collapse",
     deletableFiles: ["**/*-selection-column-cell.tsx"],
     rationale: "Nimbus DataTable provides built-in selection via selectionMode='multiple'.",
   },
   ```

## Step 3: Apply Changes

### Add Mode

Insert a new entry into the `MIGRATION_DATA` array. Place it in the appropriate
section (entries are grouped by category with comment headers). Follow this
template:

```typescript
{
  uiKitName: "ComponentName",
  nimbusEquivalent: "NimbusComponent",
  importPath: "@commercetools/nimbus",
  mappingType: "direct",
  notes:
    "Description of how to migrate. Include key prop changes and usage differences.",
  breakingChanges: [
    "Specific breaking change 1",
    "Specific breaking change 2",
  ],
  // For layout-related entries only:
  layoutGuidance: LAYOUT_NESTING_GUIDANCE,
},
```

For layout-related components (`Constraints.*`, `Spacings.*`), set the
`layoutGuidance` field to the shared `LAYOUT_NESTING_GUIDANCE` constant. This
tells the consuming LLM to migrate nested layout primitives as a group. Non-layout
entries should omit this field.

For compound components (dotted names like `Spacings.Stack`), place the entry
near its siblings. The `COMPOUND_ROOT_MAP` at the bottom of the file is built
automatically from entries with dots in `uiKitName`.

If the component has no Nimbus equivalent:

```typescript
{
  uiKitName: "DeprecatedComponent",
  nimbusEquivalent: null,
  importPath: null,
  mappingType: "removed",
  notes: "This component has no Nimbus equivalent. Suggested alternative: ...",
  breakingChanges: ["Remove usage entirely"],
},
```

### Update Mode

Edit the existing entry in place. Only change the fields that need updating.
Common updates:

- Fix incorrect `nimbusEquivalent` or `importPath`
- Improve `notes` with more specific migration guidance
- Add missing `breakingChanges`
- Change `mappingType` if the original categorization was wrong

### Remove Mode

Delete the entry from the `MIGRATION_DATA` array. Confirm with the user before
removing.

## Step 4: Verify

After making changes:

1. **Build** to catch any syntax errors:

   ```bash
   pnpm --filter @commercetools/nimbus-mcp build
   ```

2. **Run tests** to ensure nothing broke:

   ```bash
   pnpm vitest run --config packages/nimbus-mcp/vitest.config.ts
   ```

3. **Spot-check** the mapping with the MCP tool (if the server is running):
   - For a new/updated entry: verify
     `migrate_from_uikit(componentName: "TheComponent")` returns the expected
     data
   - For compound components: verify
     `migrate_from_uikit(componentName: "RootName")` includes the sub-component

## Guidelines

- **Notes should be actionable** — Tell the developer exactly what to change,
  not just that something changed. Include the specific Nimbus prop/variant to
  use.
- **Breaking changes should be specific** — Each entry should describe one
  concrete change (e.g. "label prop replaced by children", not "API changed").
- **Keep entries grouped** — The file uses comment section headers. Place new
  entries in the right section or create a new section if needed.
- **importPath is almost always `@commercetools/nimbus`** — Exceptions are
  `@commercetools/nimbus-icons` for icon-related mappings and
  `@commercetools/nimbus-tokens` for token-only patterns.
