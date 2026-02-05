---
name: "model-building"
description: "Building MobX models with proper architecture, BaseModel patterns, Store usage, and validation"
---

# Model Building Skill

## Quick Reference

**ALWAYS use `#ui_code_tools` to scaffold new models - never create manually**

## Architecture Essentials

- Every model extends `BaseModel` → `StoreModel` (lifecycle metadata + MobX)
- Always create records via Store: `Store.asset.create()` - NEVER `new Model()`
- Each model has an `APIStore` registered in `Store.ts` for caching and hydration

## File Structure

```
packages/models/src/models/<entity>/
  ├── _constants/       # Enums and status values
  ├── model/
  │   ├── <Entity>BaseModel.ts   # Pure API fields with @attr
  │   └── <Entity>Model.ts       # Computed logic and helpers
  ├── services/         # Complex workflows
  └── constants.ts      # Re-export constants
```

## BaseModel Rules

- **Only** `@attr` decorated fields that mirror the backend API
- Separate editable fields from `{readOnly: true}` joined data
- Use narrowest type: `string`, `number`, `decimal`, `uuid`, `json`
- Mark joins as `readOnly` so serialization skips them

```typescript
// BaseModel - Pure API data only
export class AssetBaseModel extends BaseModel {
  @attr("string") name: string = "";
  @attr("uuid") organization_id: string = "";
  @attr("number") status: number = 1;
  @attr("json", { readOnly: true }) organization?: Organization;
}
```

## Derived Model Pattern

- Add computed getters, validation, navigation helpers
- Call `this.addObserve(this)` in constructor for MobX tracking
- For nested JSON: create class extending `ValidationClass`, use `addObserve(child, this, "field")`

```typescript
export class AssetModel extends AssetBaseModel {
  constructor() {
    super();
    this.addObserve(this);
  }

  get statusConst(): IConstant {
    return findConstant(constants.asset.status, this.status);
  }

  get statusStr(): string {
    return this.statusConst.label;
  }

  get validationRules() {
    return assetValidationRules;
  }
}
```

## Loading Data

```typescript
// Lists
Store.asset.query({ organization_id: "123" });

// Single record
Store.asset.get("asset-id");

// Custom routes
Store.asset.queryRecord("/custom-endpoint");

// Force fresh data
Store.asset.get("id", { skipCache: true });
```

## Mutations

```typescript
// Update directly - MobX tracks changes
model.name = "Updated";

// Save (auto POST/PUT based on isNew)
await model.save();

// Discard changes
model.rollback();
```

## Constants Pattern

Always create helper getters for constants:

```typescript
get asset_typeConst(): IConstant {
  return findConstant(constants.asset.asset_type, this.asset_type);
}

get asset_typeStr(): string {
  return this.asset_typeConst.label;
}
```

## Validation

- Define rules in `<entity>/validation_rules.ts` using `ValidationRulesType<Model>`
- Expose via `get validationRules()` in derived model
- Nested JSON classes can maintain their own rules
- Ask before implementing more detailed validations

## Key Principles

1. **Never** call `new Model()` directly - use Store methods
2. **Never** mutate `_loaded_attributes` or `_dirtyAttributes` manually
3. Keep BaseModels pure - no computed logic
4. Wire observers on nested JSON immediately after instantiation
5. Keep getters cheap and side-effect free - HTTP belongs in services/stores
