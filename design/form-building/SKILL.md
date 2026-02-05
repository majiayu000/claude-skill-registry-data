---
name: "form-building"
description: "Building create/edit forms with FormField components, validation integration, and save patterns"
---

# Form Building Skill

## Core Principles

- **MobX state management** - NO state hooks or other libraries unless specified
- **Group related fields** using `DetailFieldContainer`
- **Ask first** if unclear about field importance
- Forms are for CREATE and EDIT operations

## Available Components

Located in: `ui/src/common/components/form/fields/`

### Basic Fields

- `FormFieldText` - Short text fields
- `FormFieldTextArea` - Long text fields
- `FormFieldCheckbox` - Boolean 0/1 fields
- `FormFieldReadOnly` - Display-only fields
- `FormFieldDate` - Date picker
- `FormFieldColor` - Color picker
- `FormFieldCodeEdit` - Code editor

### Single Select (Constants)

```typescript
import { constants } from "@/models/constants";

<FormFieldSelect
  record={props.asset}
  field="status"
  label="Status"
  options={constants.asset.status}
/>
```

### Multi Select (Constants)

```typescript
<FormFieldMultiSelect
  record={props.account}
  field="permissions"
  label="Permissions"
  options={constants.account.permissions}
/>
```

### Model Relationships

**Small lists** (< 50 options):

```typescript
<FormFieldModelSelect<AssetModel, OrganizationModel>
  record={props.asset}
  field="organization_id"
  label="Organization"
  placeholder="Select Organization"
  modelName="organization"
  modelSearchField="q"
  modelDisplayField="label"
  modelSearchFilters={{ disabled: "0" }}
/>
```

**Large lists** (use search):

```typescript
<FormFieldModelSearchSelect<AssetModel, OrganizationModel>
  record={props.asset}
  field="organization_id"
  label="Organization"
  placeholder="Search Organization"
  modelName="organization"
  modelSearchField="q"
  modelDisplayField="label"
  modelSearchFilters={{ disabled: "0" }}
/>
```

**Multi-select (small lists)**:

```typescript
<FormFieldModelMultiSelect<AssetModel, TagModel>
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
<FormFieldModelSearchMultiSelect<AssetModel, TagModel>
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

## JSONB Fields Pattern

For nested JSONB objects:

```typescript
// JSONB class must extend ValidationClass
<FormFieldTextArea
  record={props.organization.properties}
  field="pricing_text"
  label="Pricing Text"
  placeholder="Enter pricing text..."
  helpText="Default text if no pricing info in plan"
/>
```

**Note**: Unlike DetailFields, FormFields don't need `parentRecord` or `SafeBaseModel` wrapper

## Grouping Fields with Container

```typescript
<DetailFieldContainer label="Basic Information">
  <FormFieldText
    record={props.asset}
    field="name"
    label="Name"
    placeholder="Asset Name"
  />
  <FormFieldTextArea
    record={props.asset}
    field="description"
    label="Description"
    placeholder="Description..."
  />
</DetailFieldContainer>

<DetailFieldContainer label="Organization Details">
  <FormFieldModelSearchSelect<AssetModel, OrganizationModel>
    record={props.asset}
    field="organization_id"
    label="Organization"
    modelName="organization"
    modelSearchField="q"
    modelDisplayField="label"
  />
  <FormFieldSelect
    record={props.asset}
    field="status"
    label="Status"
    options={constants.asset.status}
  />
</DetailFieldContainer>
```

## Complete Form Example

```typescript
import { observer } from "mobx-react-lite";
import { AssetModel } from "@/models/asset";
import { OrganizationModel } from "@/models/organization";
import { constants } from "@/models/constants";
import {
  DetailFieldContainer,
  FormFieldText,
  FormFieldTextArea,
  FormFieldSelect,
  FormFieldModelSearchSelect,
  FormFieldCheckbox,
  FormFieldDate,
} from "@/ui/common/components/form/fields";
import { Button } from "@/ui/shadcn/ui/button";

interface AssetFormProps {
  asset: AssetModel;
  onSave: () => void;
  onCancel: () => void;
}

export const AssetForm = observer((props: AssetFormProps) => {
  const handleSave = async () => {
    await props.asset.save();
    props.onSave();
  };

  return (
    <div className="space-y-6">
      <DetailFieldContainer label="Basic Information">
        <FormFieldText
          record={props.asset}
          field="name"
          label="Name"
          placeholder="Asset Name"
        />
        <FormFieldTextArea
          record={props.asset}
          field="description"
          label="Description"
          placeholder="Asset description..."
        />
        <FormFieldCheckbox
          record={props.asset}
          field="is_active"
          label="Is Active"
        />
      </DetailFieldContainer>

      <DetailFieldContainer label="Organization & Status">
        <FormFieldModelSearchSelect<AssetModel, OrganizationModel>
          record={props.asset}
          field="organization_id"
          label="Organization"
          modelName="organization"
          modelSearchField="q"
          modelDisplayField="label"
          modelSearchFilters={{ disabled: "0" }}
        />
        <FormFieldSelect
          record={props.asset}
          field="status"
          label="Status"
          options={constants.asset.status}
        />
        <FormFieldDate
          record={props.asset}
          field="effective_date"
          label="Effective Date"
        />
      </DetailFieldContainer>

      <div className="flex justify-end gap-2">
        <Button variant="outline" onClick={props.onCancel}>
          Cancel
        </Button>
        <Button onClick={handleSave}>
          Save
        </Button>
      </div>
    </div>
  );
});
```

## Validation Integration

Forms automatically connect to model validation rules:

```typescript
// Model already has validation rules defined
get validationRules() {
  return assetValidationRules;
}

// Form fields automatically show errors
<FormFieldText
  record={props.asset}
  field="name"
  label="Name"
  // Validation errors show automatically
/>
```

## Save Pattern

```typescript
const handleSave = async () => {
  try {
    await props.asset.save();
    // Success - redirect or close modal
    props.onSave();
  } catch (error) {
    // Error handling - validation errors show on fields automatically
    console.error("Save failed:", error);
  }
};
```

## Key Differences from Details View

| Feature      | Form Fields   | Detail Fields        |
| ------------ | ------------- | -------------------- |
| Use case     | Create/Edit   | View/Edit            |
| JSONB        | Direct record | Needs `parentRecord` |
| Type casting | Not needed    | `SafeBaseModel<T>`   |
| Save button  | Required      | Optional             |
| Validation   | Built-in      | Built-in             |

## Key Rules

1. Always create components with `#ui_code_tools`
2. Use search variants for large option lists (>50 items)
3. Constants are model-specific: `constants.{model}.{field}`
4. Forms handle validation automatically via model rules
5. Call `model.save()` to persist changes
6. Ask before implementing if field importance is unclear
7. JSONB fields don't need `parentRecord` in forms
