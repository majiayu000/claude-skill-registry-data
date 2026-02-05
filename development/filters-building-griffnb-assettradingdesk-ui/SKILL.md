---
name: "filters-building"
description: "Building table filters with query parameters, model search, and supported query patterns"
---

# Filters Building Skill

## Filter Types Quick Reference

```typescript
type FilterType =
  | "simple-select"              // Constants (single)
  | "multi-select"               // Constants (multiple)
  | "model-select"               // Model relationship (small lists)
  | "model-multi-select"         // Model relationships (small lists)
  | "model-search-select"        // Model relationship (large lists)
  | "model-search-multi-select"  // Model relationships (large lists)
  | "text"                       // Text input
  | "email"                      // Email input
  | "number"                     // Number input
  | "checkbox"                   // Boolean 0/1
  | "date-range"                 // Date range picker
  | "gap";                       // Visual spacing
```

## Field Definition

Field can be string OR object:

```typescript
// Simple string - used for all three
field: "organization_id"

// Complex object for custom queries
field: {
  queryParam: "organization_type_id",       // URL query param
  postgresColumn: "organizations.type",     // Postgres column
  elasticsearchColumn: "organization_type_id" // ES column
}
```

## Supported Query Patterns

| Query Parameter | SQL Result | Description |
|-----------------|------------|-------------|
| `?name=john` | `WHERE account.name = 'john'` | Exact match |
| `?name[]=john&name[]=jane` | `WHERE account.name IN('john','jane')` | Multiple values |
| `?not:name=john` | `WHERE account.name != 'john'` | Not equal |
| `?q:name=john` | `WHERE LOWER(account.name) ILIKE '%john%'` | Like search |
| `?gt:age=25` | `WHERE account.age > 25` | Greater than |
| `?lt:age=65` | `WHERE account.age < 65` | Less than |
| `?between:age=25\|65` | `WHERE account.age >= 25 AND account.age <= 65` | Range |

## Gap (Section Separator)

```typescript
{
  type: "gap",
  placeholder: "",
  label: "Organization Filters",
  field: "",
}
```

## Text Filter

```typescript
{
  placeholder: "Search Name",
  type: "text",
  field: "name", // Uses q:name for ILIKE search
}
```

## Checkbox Filter

```typescript
{
  placeholder: "Is Active",
  type: "checkbox",
  field: "is_active",
  checkedValue: "1",
  uncheckedValue: "",
}
```

## Simple Select (Constants)

```typescript
import { constants } from "@/models/constants";

{
  placeholder: "Status",
  type: "simple-select",
  field: "status",
  options: constants.asset.status,
}
```

## Multi Select (Constants)

```typescript
{
  placeholder: "Organization Type",
  type: "multi-select",
  field: {
    queryParam: "organization_type_id",
    postgresColumn: "organizations.type",
    elasticsearchColumn: "organization_type_id",
  },
  options: constants.organization.type,
}
```

## Model Select (Small Lists)

For < 50 options:

```typescript
{
  placeholder: "Organization",
  type: "model-select",
  field: "organization_id",
  modelName: "organization",
  modelDisplayField: "label",
  modelSearchFilters: { disabled: "0" },
}
```

## Model Multi Select (Small Lists)

```typescript
{
  placeholder: "Tags",
  type: "model-multi-select",
  field: "tag_ids",
  modelName: "tag",
  modelDisplayField: "label",
  modelSearchFilters: { disabled: "0" },
}
```

## Model Search Select (Large Lists)

For > 50 options:

```typescript
{
  placeholder: "Organization",
  type: "model-search-select",
  field: "organization_id",
  modelName: "organization",
  modelDisplayField: "label",
  modelSearchParam: "q",
  modelSearchFilters: { disabled: "0" },
}
```

## Model Search Multi Select (Large Lists)

```typescript
{
  placeholder: "Organizations",
  type: "model-search-multi-select",
  field: "organization_id",
  modelName: "organization",
  modelDisplayField: "label",
  modelSearchParam: "q",
  modelSearchFilters: { disabled: "0" },
}
```

## Date Range Filter

```typescript
{
  placeholder: "Created Date",
  type: "date-range",
  field: "created_at",
}
```

## Complete Example

```typescript
import { IFilterField } from "@/ui/common/components/types/filters";
import { constants } from "@/models/constants";

export const assetFilters: IFilterField[] = [
  // Section 1: Basic Filters
  {
    placeholder: "Search Name",
    type: "text",
    field: "name",
  },
  {
    placeholder: "Status",
    type: "multi-select",
    field: "status",
    options: constants.asset.status,
  },
  {
    placeholder: "Is Active",
    type: "checkbox",
    field: "is_active",
    checkedValue: "1",
    uncheckedValue: "",
  },

  // Gap for visual separation
  {
    type: "gap",
    placeholder: "",
    label: "Organization Filters",
    field: "",
  },

  // Section 2: Relationships
  {
    placeholder: "Organization",
    type: "model-search-multi-select",
    field: "organization_id",
    modelName: "organization",
    modelDisplayField: "label",
    modelSearchParam: "q",
    modelSearchFilters: { disabled: "0" },
  },
  {
    placeholder: "Organization Type",
    type: "multi-select",
    field: {
      queryParam: "organization_type_id",
      postgresColumn: "organizations.type",
      elasticsearchColumn: "organization_type_id",
    },
    options: constants.organization.type,
  },

  // Gap for dates section
  {
    type: "gap",
    placeholder: "",
    label: "Date Filters",
    field: "",
  },

  // Section 3: Dates
  {
    placeholder: "Created Date",
    type: "date-range",
    field: "created_at",
  },
];
```

## Best Practices

1. **Group related filters** with `gap` separators
2. **Use search variants** for lists > 50 items
3. **Always use `label` as modelDisplayField** (modify model if needed)
4. **Always use `q` as modelSearchParam** for consistency
5. **Add modelSearchFilters** to exclude disabled/archived records
6. **Use field objects** only when postgres/ES columns differ from query param
7. **Constants are model-specific**: `constants.{model}.{field}`

## Filter Selection Guide

| Data Type | Count | Filter Type |
|-----------|-------|-------------|
| Text field | N/A | `text` |
| Email field | N/A | `email` |
| Number field | N/A | `number` |
| Boolean | N/A | `checkbox` |
| Date | N/A | `date-range` |
| Constants | 1 | `simple-select` |
| Constants | Many | `multi-select` |
| Model | < 50 | `model-select` or `model-multi-select` |
| Model | > 50 | `model-search-select` or `model-search-multi-select` |

## Key Rules

1. Use gaps to separate logical filter sections
2. Model filters should always filter out disabled records
3. Use search variants for better UX with large datasets
4. Field objects allow custom query building (see Go controller docs)
5. Keep placeholder text concise and descriptive
