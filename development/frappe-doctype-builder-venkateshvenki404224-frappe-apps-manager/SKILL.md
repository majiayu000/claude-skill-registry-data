---
name: frappe-doctype-builder
description: Build Frappe DocTypes with fields, permissions, and naming configurations. Use this skill when creating or modifying DocType structures.
---

# Frappe DocType Builder Skill

Build complete DocType definitions with proper field types, permissions, and configurations.

## When to Use This Skill

Claude should invoke this skill when:
- User wants to create a new DocType
- User needs to add fields to an existing DocType
- User asks about DocType structure or design
- User wants to modify DocType properties
- User needs help with DocType JSON schema

## Capabilities

### 1. DocType JSON Generation
Create complete DocType JSON files with:
- Metadata (name, module, naming, permissions)
- Fields with proper types and options
- Permissions for different roles
- Form layout and sections
- Naming series configuration

### 2. Field Type Expertise
Support all Frappe field types:
- **Data**: Short text fields
- **Text**: Long text with editor options
- **Int**: Integer numbers
- **Float**: Decimal numbers
- **Currency**: Money values
- **Date**: Date picker
- **Datetime**: Date and time
- **Time**: Time picker
- **Link**: Reference to another DocType
- **Select**: Dropdown with options
- **Check**: Boolean checkbox
- **Table**: Child table
- **Attach**: File upload
- **Attach Image**: Image upload with preview
- **Signature**: Signature capture
- **HTML**: Custom HTML content
- **Markdown Editor**: Markdown content
- **Code**: Code editor with syntax highlighting
- **Dynamic Link**: Polymorphic references
- **Rating**: Star rating
- **Color**: Color picker
- **Geolocation**: GPS coordinates

### 3. DocType Patterns

**Master DocType:**
```json
{
  "name": "Customer",
  "module": "CRM",
  "autoname": "naming_series:",
  "naming_rule": "By naming series",
  "track_changes": 1,
  "is_submittable": 0
}
```

**Transaction DocType:**
```json
{
  "name": "Sales Order",
  "module": "Selling",
  "is_submittable": 1,
  "autoname": "naming_series:",
  "track_changes": 1
}
```

**Child Table:**
```json
{
  "name": "Sales Order Item",
  "module": "Selling",
  "istable": 1,
  "editable_grid": 1
}
```

**Settings DocType:**
```json
{
  "name": "System Settings",
  "module": "Core",
  "issingle": 1
}
```

### 4. Common Field Patterns

**Naming Series:**
```json
{
  "fieldname": "naming_series",
  "fieldtype": "Select",
  "label": "Naming Series",
  "options": "CUST-.YYYY.-\nCUST-",
  "reqd": 1
}
```

**Status Field:**
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Draft\nSubmitted\nCancelled",
  "default": "Draft"
}
```

**Link Field:**
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1
}
```

**Child Table:**
```json
{
  "fieldname": "items",
  "fieldtype": "Table",
  "label": "Items",
  "options": "Sales Order Item",
  "reqd": 1
}
```

**Computed Field:**
```json
{
  "fieldname": "total",
  "fieldtype": "Currency",
  "label": "Total Amount",
  "read_only": 1
}
```

### 5. Permission Configuration

```json
{
  "permissions": [
    {
      "role": "Sales User",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 0,
      "submit": 0,
      "cancel": 0
    },
    {
      "role": "Sales Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1,
      "submit": 1,
      "cancel": 1
    }
  ]
}
```

### 6. Advanced Features

**Dependent Fields:**
```json
{
  "fieldname": "customer_group",
  "fieldtype": "Link",
  "options": "Customer Group",
  "depends_on": "eval:doc.customer"
}
```

**Mandatory Depends On:**
```json
{
  "fieldname": "tax_id",
  "fieldtype": "Data",
  "label": "Tax ID",
  "mandatory_depends_on": "eval:doc.country=='United States'"
}
```

**Read Only Depends On:**
```json
{
  "fieldname": "posted_date",
  "fieldtype": "Date",
  "read_only_depends_on": "eval:doc.docstatus==1"
}
```

## Output Format

When building a DocType, provide:
1. Complete JSON structure
2. Explanation of key fields
3. Permission rationale
4. Controller method suggestions (if needed)
5. Migration instructions

## Best Practices

1. **Naming**: Use clear, descriptive field names in snake_case
2. **Required Fields**: Mark essential fields as required
3. **Defaults**: Provide sensible default values
4. **Permissions**: Start restrictive, expand as needed
5. **Indexing**: Add database indexes for frequently queried fields
6. **Validation**: Use field properties for basic validation
7. **Organization**: Group related fields with sections and column breaks

## Integration with Controllers

After creating DocType JSON, suggest controller methods:
- `validate()` - Pre-save validation
- `before_save()` - Modify values before saving
- `on_submit()` - Actions when document is submitted
- `on_cancel()` - Actions when document is cancelled
- `on_trash()` - Actions before deletion

## Example Usage Flow

1. **User asks**: "Create a Customer DocType with name, email, and phone"
2. **Skill generates**:
   - Complete DocType JSON
   - Appropriate field types
   - Basic permissions
   - Naming configuration
3. **Output includes**:
   - JSON file content
   - Where to save it (`apps/<app>/doctype/customer/customer.json`)
   - Migration command (`bench --site <site> migrate`)
   - Next steps for customization

## File Structure

Generated files should follow:
```
apps/
└── <app_name>/
    └── <module_name>/
        └── doctype/
            └── <doctype_name>/
                ├── __init__.py
                ├── <doctype_name>.json
                ├── <doctype_name>.py
                └── <doctype_name>.js
```

Remember: This skill is model-invoked. Claude will use it autonomously when detecting DocType-related tasks.
