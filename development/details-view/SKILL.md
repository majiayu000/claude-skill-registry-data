---
name: "details-view"
description: "Building view/details pages with DetailField components, model relationships, and JSONB handling"
---

# Details View Skill

## Core Principles

- **MobX state management** - NO state hooks or other libraries
- **Group related fields** using `DetailFieldContainer`
- **Ask first** if unclear about field importance

## Available Components

Located in: `ui/src/common/components/form/details/`

### Container

- `DetailFieldContainer` - Groups related fields, wraps grid safely

### Basic Fields

- `DetailFieldText` - Short text fields
- `DetailFieldTextArea` - Long text fields
- `DetailFieldCheckbox` - Boolean 0/1 fields
- `DetailFieldReadOnly` - Display-only fields
- `DetailFieldDate` - Date picker
- `DetailFieldColor` - Color picker
- `DetailFieldCodeEdit` - Code editor

### Single Select (Constants)

```typescript
import { constants } from "@/models/constants";

<DetailFieldSelect
  record={props.asset}
  field="status"
  label="Status"
  options={constants.asset.status}
  displayField="statusStr"
/>
```

### Multi Select (Constants)

```typescript
<DetailFieldMultiSelect
  record={props.account}
  field="permissions"
  label="Permissions"
  options={constants.account.permissions}
/>
```

### Model Relationships

**Small lists** (< 50 options):

```typescript
<DetailFieldModelSelect<AssetModel, OrganizationModel>
  record={props.asset}
  field="organization_id"
  displayField="organization_name"
  label="Organization"
  placeholder="Select Organization"
  modelName="organization"
  modelSearchField="q"
  modelDisplayField="label"
  modelSearchFilters={{ disabled: "0" }}
  reloadOnSave={true}
/>
```

**Large lists** (use search):

```typescript
<DetailFieldModelSearchSelect<AssetModel, OrganizationModel>
  record={props.asset}
  field="organization_id"
  displayField="organization_name"
  label="Organization"
  placeholder="Search Organization"
  modelName="organization"
  modelSearchField="q"
  modelDisplayField="label"
  modelSearchFilters={{ disabled: "0" }}
  reloadOnSave={true}
/>
```

**Multi-select (small lists)**:

```typescript
<DetailFieldModelMultiSelect<AssetModel, TagModel>
  record={props.asset}
  field="tag_ids"
  label="Tags"
  placeholder="Select Tags"
  modelName="tag"
  modelSearchField="q"
  modelDisplayField="label"
/>
```

**Multi-select (large lists with search)**:

```typescript
<DetailFieldModelSearchMultiSelect<AssetModel, TagModel>
  record={props.asset}
  field="tag_ids"
  label="Tags"
  placeholder="Search Tags"
  modelName="tag"
  modelSearchField="q"
  modelDisplayField="label"
/>
```

## Model Relationship Best Practices

- **Always try to use `label` as modelDisplayField**
- **Always try to use `q` as modelSearchField**
- If model doesn't have a good label, modify it in `XXModel.ts`
- Assume all models exist - don't create new ones
- Use `reloadOnSave={true}` if related data needs refresh

## JSONB Fields Pattern

For nested JSONB objects, use `SafeBaseModel` helper and `parentRecord`:

```typescript
import { SafeBaseModel } from "@/models/types";

// JSONB class must extend ValidationClass
<DetailFieldTextArea
  record={props.organization.properties as SafeBaseModel<Properties>}
  parentRecord={props.organization}
  field="pricing_text"
  label="Pricing Text"
  placeholder="Enter pricing text..."
  helpText="Default text if no pricing info in plan"
/>
```

## Grouping Fields with Container

```typescript
<DetailFieldContainer label="Basic Information">
  <DetailFieldText
    record={props.asset}
    field="name"
    label="Name"
    placeholder="Asset Name"
  />
  <DetailFieldTextArea
    record={props.asset}
    field="description"
    label="Description"
    placeholder="Description..."
  />
</DetailFieldContainer>

<DetailFieldContainer label="Organization Details">
  <DetailFieldModelSearchSelect<AssetModel, OrganizationModel>
    record={props.asset}
    field="organization_id"
    displayField="organization_name"
    label="Organization"
    modelName="organization"
    modelSearchField="q"
    modelDisplayField="label"
  />
  <DetailFieldSelect
    record={props.asset}
    field="status"
    label="Status"
    options={constants.asset.status}
    displayField="statusStr"
  />
</DetailFieldContainer>
```

## Complete Example

```typescript
import { observer } from "mobx-react-lite";
import { AssetModel } from "@/models/asset";
import { OrganizationModel } from "@/models/organization";
import { constants } from "@/models/constants";
import {
  DetailFieldContainer,
  DetailFieldText,
  DetailFieldTextArea,
  DetailFieldSelect,
  DetailFieldModelSearchSelect,
  DetailFieldCheckbox,
  DetailFieldDate,
} from "@/ui/common/components/form/details";

interface AssetDetailsProps {
  asset: AssetModel;
}

export const AssetDetails = observer((props: AssetDetailsProps) => {
  return (
    <div className="space-y-6">
      <DetailFieldContainer label="Basic Information">
        <DetailFieldText
          record={props.asset}
          field="name"
          label="Name"
          placeholder="Asset Name"
        />
        <DetailFieldTextArea
          record={props.asset}
          field="description"
          label="Description"
          placeholder="Asset description..."
        />
        <DetailFieldCheckbox
          record={props.asset}
          field="is_active"
          label="Is Active"
        />
      </DetailFieldContainer>

      <DetailFieldContainer label="Organization & Status">
        <DetailFieldModelSearchSelect<AssetModel, OrganizationModel>
          record={props.asset}
          field="organization_id"
          displayField="organization_name"
          label="Organization"
          modelName="organization"
          modelSearchField="q"
          modelDisplayField="label"
          modelSearchFilters={{ disabled: "0" }}
          reloadOnSave={true}
        />
        <DetailFieldSelect
          record={props.asset}
          field="status"
          label="Status"
          options={constants.asset.status}
          displayField="statusStr"
        />
        <DetailFieldDate
          record={props.asset}
          field="effective_date"
          label="Effective Date"
        />
      </DetailFieldContainer>
    </div>
  );
});
```

## Key Rules

1. Always generate component with `#ui_code_tools`
2. Group related fields logically with `DetailFieldContainer`
3. Use search variants for large option lists (>50 items)
4. Use `displayField` for computed string versions of IDs
5. Pass `parentRecord` when editing JSONB nested objects
6. Constants are model-specific: `constants.{model}.{field}`
7. Ask before implementing if field importance is unclear
