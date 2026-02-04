---
name: "table-columns"
description: "Building table columns with proper types, inline editing components, and pre-built cell renderers"
---

# Table Columns Skill

## Column Interface Quick Reference

```typescript
export interface IColumn<T extends object> {
  title: string;               // Header display
  field: keyof T;              // Model field name
  displayField?: keyof T;      // Use if display differs from field
  queryField: string | IField; // For sorting/filtering
  csvHeaderName?: string;      // CSV export header override
  render?: ColumnComponent<T>; // Custom render function
  noSort?: boolean;            // Disable sorting
  class?: string;              // Column className
  headerClass?: string;        // Header className
  total?: boolean;             // Show total at bottom
  totalFormat?: TotalFormat;   // Format for total
  hidden?: boolean;            // Hide by default
  format?: TextFormat;         // "dollars" | "percent" | "number" | "decimal" | "boolean"
  noExport?: boolean;          // Exclude from CSV
}
```

## Standard Read-Only Column

For data that shouldn't be edited inline (UUIDs, dates, joined data):

```typescript
{
  title: "First Name",
  field: "first_name",
  queryField: "first_name",
  format: "text" // or "number", "dollars", "percent", "decimal", "boolean"
}
```

## Inline Edit: Text Fields

```typescript
import { InlineEditCellText, InlineEditCellTextColumn } from "@/ui/common/components/table/cell/inline-edit/InlineEditCellText";

{
  title: "Description",
  field: "description",
  queryField: "description",
  type: "text", // or "number"
  render: (options: ColumnComponentOptions<AssetModel>) => {
    return (
      <InlineEditCellText
        record={options.record}
        column={options.column as InlineEditCellTextColumn<AssetModel>}
        index={options.index}
      />
    );
  },
} as InlineEditCellTextColumn<AssetModel>
```

## Inline Edit: Checkbox (Boolean Fields)

```typescript
import { InlineEditCellCheckbox, InlineEditCellCheckboxColumn } from "@/ui/common/components/table/cell/inline-edit/InlineEditCellCheckbox";

{
  title: "Is Required",
  field: "is_required",
  queryField: "is_required",
  render: (options: ColumnComponentOptions<AssetModel>) => {
    return (
      <InlineEditCellCheckbox
        record={options.record}
        column={options.column as InlineEditCellCheckboxColumn<AssetModel>}
        index={options.index}
      />
    );
  },
} as InlineEditCellCheckboxColumn<AssetModel>
```

## Inline Edit: Select (Constants)

```typescript
import { InlineEditCellSelect, InlineEditCellSelectColumn } from "@/ui/common/components/table/cell/inline-edit/InlineEditCellSelect";

{
  title: "Status",
  field: "status",
  queryField: "status",
  options: constants.asset.status,
  render: (options: ColumnComponentOptions<AssetModel>) => {
    return (
      <InlineEditCellSelect
        record={options.record}
        column={options.column as InlineEditCellSelectColumn<AssetModel>}
        index={options.index}
      />
    );
  },
} as InlineEditCellSelectColumn<AssetModel>
```

## Inline Edit: Model Select (Relationships)

```typescript
import { InlineEditCellModelSelect, InlineEditCellModelSelectColumn } from "@/ui/common/components/table/cell/inline-edit/InlineEditCellModelSelect";

{
  title: "Organization",
  field: "organization_id",
  displayField: "organization_name",
  queryField: "organization_id",
  modelName: "organization",
  modelSearchField: "q",
  modelDisplayField: "label",
  modelSearchFilters: { disabled: "0" },
  render: (options: ColumnComponentOptions<AssetModel>) => {
    return (
      <InlineEditCellModelSelect
        record={options.record}
        column={options.column as InlineEditCellModelSelectColumn<AssetModel>}
        index={options.index}
      />
    );
  },
} as InlineEditCellModelSelectColumn<AssetModel>
```

## Pre-Built Cell Components

| Component | Usage |
|-----------|-------|
| `BadgeCell` | Colored badges for status/types |
| `ImageCell` | Image preview |
| `JSONCell` | JSON preview with expandable view |
| `LinkCell` | Internal/external links |
| `MultiBadgeCell` | Multi-select fields as badges |
| `StatCell` | Stat with label/value (reporting) |

## Available Inline Edit Components

- `InlineEditCellText` - Text/number fields
- `InlineEditCellCheckbox` - Boolean yes/no
- `InlineEditCellSelect` - Single select from constants
- `InlineEditCellMultiSelect` - Multi-select from constants
- `InlineEditCellModelSelect` - Single model relationship (small lists)
- `InlineEditCellModelSearchSelect` - Single model relationship (large lists)
- `InlineEditCellModelMultiSelect` - Multi model relationship (small lists)
- `InlineEditCellModelSearchMultiSelect` - Multi model relationship (large lists)

## Badge Cell Example

```typescript
import { BadgeCell } from "@/ui/common/components/table/cell/BadgeCell";

{
  title: "Status",
  field: "status",
  queryField: "status",
  render: (options: ColumnComponentOptions<AssetModel>) => {
    return (
      <BadgeCell
        value={options.record.statusStr}
        color={options.record.statusConst.color}
      />
    );
  },
}
```

## Before Implementation

**IMPORTANT**: Before writing column code, list out ALL columns with descriptions of render types to get feedback.

Example planning format:
```
Columns to implement:
1. Name - InlineEditCellText (text field)
2. Description - InlineEditCellText (text field)
3. Status - BadgeCell (status with color)
4. Organization - Standard display (joined data, read-only)
5. Is Active - InlineEditCellCheckbox (boolean)
6. Created At - Standard display with date format
```

## Key Rules

1. Use `queryField` for the actual database field name
2. Use `displayField` when showing joined data but querying on ID
3. Add `format` for automatic formatting (dollars, percent, number, decimal, boolean)
4. Use appropriate inline edit component based on data type and list size
5. Always type-cast column `as InlineEditCell*Column<Model>` for inline editors
6. Keep `render` functions focused - extract complex logic to services
