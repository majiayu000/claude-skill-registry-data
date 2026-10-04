---
name: bulk-widget-updates
description: "Discover and bulk-change widget properties across many pages with LIST WIDGETS and UPDATE WIDGETS. Use when the same widget setting has to change on many pages at once. Experimental — always DRY RUN first and back the project up."
---

# Bulk Widget Property Updates

> **EXPERIMENTAL**: These commands are an untested proof-of-concept.
> Always use `dry run` first and backup your project before applying changes.

Use `list widgets` and `update widgets` to discover and modify widget properties across pages and snippets in bulk.

**When to use which tool:**

| Scope | Tool |
|-------|------|
| One page, one or several related changes | `alter page` — see `alter-page` |
| Many pages matched by `WHERE` filter (across one or more modules) | `update widgets` (this skill) |

`alter page` is the right call for targeted, page-specific edits — it can combine `set`/`insert`/`drop`/`replace` in a single block. `update widgets` is for cross-page patterns like "set `Class` on every Container in `MyMod`" where naming each page explicitly would be tedious or error-prone.

## Prerequisites

Widget commands require a full catalog build:
```sql
refresh catalog full;
```

## LIST WIDGETS - Discover Widgets

### Basic Usage

```sql
-- Show all widgets
list widgets;

-- Filter by module
list widgets in MyModule;

-- Filter by widget type (case-insensitive LIKE)
list widgets where widgettype like '%combobox%';

-- Filter by name
list widgets where Name = 'myGrid';

-- Combine filters
list widgets where widgettype like '%DataGrid%' and Name like '%Overview%' in MyModule;
```

### Output Columns

| Column | Description |
|--------|-------------|
| NAME | Widget name (may be auto-generated) |
| WIDGET TYPE | Full widget type ID (e.g., `com.mendix.widget.web.combobox.Combobox`) |
| CONTAINER | Page or snippet qualified name |
| MODULE | Module name |

### Common Widget Type Patterns

| Pattern | Matches |
|---------|---------|
| `%combobox%` | ComboBox widgets |
| `%datagrid%` | DataGrid2 and related widgets |
| `%textbox%` | TextBox widgets |
| `%dropdown%` | DropDown widgets |
| `%gallery%` | Gallery widgets |

## UPDATE WIDGETS - Modify Properties

### Syntax

```sql
update widgets
  set 'propertyName' = value [, 'propertyName' = value ...]
  where condition [and condition ...]
  [in module]
  [dry run];
```

### Dry Run (Preview Changes)

Always preview changes first:

```sql
mdl 1;
-- See what would change without modifying
update widgets
  set 'showLabel' = false
  where widgettype like '%combobox%'
  dry run;
```

Output shows:
```
found 5 widget(s) in 3 container(s) matching the criteria

[dry run] The following changes would be made:
  Would set 'showLabel' = false on combobox1 (combobox) in MyModule.OrderForm
  Would set 'showLabel' = false on combobox2 (combobox) in MyModule.CustomerPage
  ...

[dry run] Would update 5 widget(s)

run without dry run to apply changes.
```

### Apply Changes

Remove `dry run` to apply:

```sql
mdl 1;
update widgets
  set 'showLabel' = false
  where widgettype like '%combobox%'
  in MyModule;
```

### Property Value Types

| Type | Examples |
|------|----------|
| String | `'contains'`, `'above'` |
| Number | `4`, `100`, `3.14` |
| Boolean | `true`, `false` |
| Null | `null` |

### Examples

```sql
mdl 1;
-- Hide labels on all comboboxes
update widgets
  set 'showLabel' = false
  where widgettype like '%combobox%';

-- Set multiple properties
update widgets
  set 'showLabel' = false, 'labelWidth' = 4
  where widgettype like '%textbox%'
  in MyModule;

-- Change filter mode on DataGrid filters
update widgets
  set 'filterMode' = 'contains'
  where widgettype like '%DatagridTextFilter%';
```

## Important Notes

### Known Limitations (Experimental)

**UPDATE WIDGETS functionality is not fully implemented.**
- The DRY RUN mode shows which widgets would be matched
- Actual property updates require additional implementation work
- Use LIST WIDGETS for discovery, then manually update properties in Studio Pro

### After Making Changes

1. Refresh the catalog to see updated data:
   ```sql
   refresh catalog full force;
   ```

2. Open the project in Studio Pro to verify changes

### Supported Properties

Only primitive properties (string, number, boolean) are supported:
- `showLabel`, `labelWidth`, `placeholder`
- `filterMode`, `defaultValue`
- Widget-specific configuration properties

NOT supported:
- DataSource properties
- Action properties (onClick, etc.)
- Nested object properties
- Expression properties

### Finding Property Names

To find the correct property names:
1. Create a widget in Studio Pro
2. Use `describe page Module.PageName` to see widget structure
3. Or check the Mendix widget documentation

## Workflow Example

```sql
mdl 1;
-- 1. Build catalog
refresh catalog full;

-- 2. Discover widgets
list widgets where widgettype like '%combobox%';

-- 3. Preview changes
update widgets set 'showLabel' = false where widgettype like '%combobox%' dry run;

-- 4. Apply changes
update widgets set 'showLabel' = false where widgettype like '%combobox%';

-- 5. Rebuild catalog
refresh catalog full force;

-- 6. Verify
list widgets where widgettype like '%combobox%';
```
