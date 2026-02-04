---
name: doctype-patterns
description: Frappe DocType creation patterns, field types, controller hooks, and data modeling best practices. Use when creating DocTypes, designing data models, adding fields, or setting up document relationships in Frappe/ERPNext.
---

# Frappe DocType Patterns

Comprehensive guide to creating and configuring DocTypes in Frappe Framework, the core building block for all Frappe applications.

## When to Use This Skill

- Creating new DocTypes
- Adding or modifying fields on DocTypes
- Designing data models and relationships
- Setting up naming patterns and autoname
- Configuring permissions and workflows
- Creating child tables
- Working with Virtual or Single DocTypes

## DocType Directory Structure

When you create a DocType named "My Custom DocType" in module "My Module":

```
my_app/
└── my_module/
    └── doctype/
        └── my_custom_doctype/
            ├── my_custom_doctype.json      # DocType definition
            ├── my_custom_doctype.py        # Python controller
            ├── my_custom_doctype.js        # Client script
            ├── test_my_custom_doctype.py   # Test file
            └── __init__.py
```

## DocType JSON Structure

```json
{
  "name": "My Custom DocType",
  "module": "My Module",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": ["field1", "field2"],
  "fields": [
    {
      "fieldname": "field1",
      "fieldtype": "Data",
      "label": "Field 1",
      "reqd": 1
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1
    }
  ],
  "autoname": "naming_series:",
  "naming_rule": "By \"Naming Series\" field",
  "is_submittable": 0,
  "istable": 0,
  "issingle": 0,
  "track_changes": 1,
  "sort_field": "modified",
  "sort_order": "DESC"
}
```

## Field Types Reference

### Text Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Data` | Single line text (140 chars) | Names, codes, short text |
| `Small Text` | Multi-line text | Short descriptions |
| `Text` | Multi-line text (unlimited) | Long descriptions |
| `Text Editor` | Rich text with formatting | Content, notes |
| `Code` | Syntax-highlighted code | Python, JS, JSON |
| `HTML Editor` | WYSIWYG HTML | Email templates |
| `Markdown Editor` | Markdown input | Documentation |
| `Password` | Masked input | Secrets (stored encrypted) |

### Numeric Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Int` | Integer | Counts, quantities |
| `Float` | Decimal number | Measurements |
| `Currency` | Money with precision | Prices, amounts |
| `Percent` | 0-100 percentage | Discounts, rates |
| `Rating` | Star rating (0-1) | Reviews, scores |

### Date/Time Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Date` | Date only | Birth dates, due dates |
| `Datetime` | Date and time | Timestamps |
| `Time` | Time only | Schedules |
| `Duration` | Time duration | Task duration |

### Selection Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Select` | Dropdown options | Status, type |
| `Check` | Boolean checkbox | Flags, toggles |
| `Autocomplete` | Text with suggestions | Tags |

### Link Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Link` | Reference to another DocType | Foreign key relationship |
| `Dynamic Link` | Reference based on another field | Polymorphic links |
| `Table` | Child table (1-to-many) | Line items, details |
| `Table MultiSelect` | Many-to-many via link | Multiple selections |

### Special Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Attach` | Single file attachment | Documents |
| `Attach Image` | Image with preview | Photos, logos |
| `Image` | Display image from URL field | Gallery |
| `Signature` | Signature pad | Approvals |
| `Geolocation` | Map coordinates | Locations |
| `Barcode` | Barcode/QR display | Inventory |
| `JSON` | JSON data | Configuration |

### Layout Fields
| Type | Description | Use Case |
|------|-------------|----------|
| `Section Break` | Horizontal section divider | Form organization |
| `Column Break` | Vertical column divider | Multi-column layout |
| `Tab Break` | Tab navigation | Large forms |
| `HTML` | Static HTML content | Instructions, headers |
| `Heading` | Section heading | Visual separation |
| `Button` | Clickable button | Actions |

## Field Options

### Common Field Properties
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "label": "Customer",
  "options": "Customer",
  "reqd": 1,
  "unique": 0,
  "in_list_view": 1,
  "in_standard_filter": 1,
  "in_global_search": 1,
  "bold": 1,
  "read_only": 0,
  "hidden": 0,
  "print_hide": 0,
  "no_copy": 0,
  "allow_in_quick_entry": 1,
  "translatable": 0,
  "default": "",
  "description": "Select the customer",
  "depends_on": "eval:doc.is_customer",
  "mandatory_depends_on": "eval:doc.status=='Active'",
  "read_only_depends_on": "eval:doc.docstatus==1"
}
```

### Link Field Options
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "options": "Customer",
  "filters": {
    "disabled": 0,
    "customer_type": "Company"
  },
  "ignore_user_permissions": 0
}
```

### Select Field Options
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "options": "\nDraft\nPending\nApproved\nRejected",
  "default": "Draft"
}
```

### Dynamic Link
```json
{
  "fieldname": "party_type",
  "fieldtype": "Link",
  "options": "DocType"
},
{
  "fieldname": "party",
  "fieldtype": "Dynamic Link",
  "options": "party_type"
}
```

## Naming Patterns (autoname)

### Naming Series
```json
{
  "autoname": "naming_series:",
  "naming_rule": "By \"Naming Series\" field"
}
```
Add a naming_series field:
```json
{
  "fieldname": "naming_series",
  "fieldtype": "Select",
  "options": "INV-.YYYY.-\nINV-.MM.-.YYYY.-",
  "default": "INV-.YYYY.-"
}
```

### Field-Based Naming
```json
{
  "autoname": "field:customer_code",
  "naming_rule": "By fieldname"
}
```

### Expression-Based
```json
{
  "autoname": "format:{customer_type}-{###}",
  "naming_rule": "Expression"
}
```

### Hash/Random
```json
{
  "autoname": "hash",
  "naming_rule": "Random"
}
```

### Prompt (Manual)
```json
{
  "autoname": "Prompt",
  "naming_rule": "Set by user"
}
```

## Controller Lifecycle Hooks

```python
# my_doctype.py
import frappe
from frappe.model.document import Document

class MyDocType(Document):
    # ===== BEFORE DATABASE OPERATIONS =====

    def autoname(self):
        """Set the document name before saving"""
        self.name = f"{self.prefix}-{frappe.generate_hash()[:8]}"

    def before_naming(self):
        """Called before autoname, can modify naming logic"""
        pass

    def validate(self):
        """Validate data before save (called on insert and update)"""
        self.validate_dates()
        self.calculate_totals()

    def before_validate(self):
        """Called before validate"""
        pass

    def before_save(self):
        """Called before document is saved to database"""
        self.modified_by_script = True

    def before_insert(self):
        """Called before new document is inserted"""
        self.set_defaults()

    # ===== AFTER DATABASE OPERATIONS =====

    def after_insert(self):
        """Called after new document is inserted"""
        self.notify_users()

    def on_update(self):
        """Called after document is saved (insert or update)"""
        self.update_related_docs()

    def after_save(self):
        """Called after on_update, always runs"""
        pass

    def on_change(self):
        """Called when document changes in database"""
        pass

    # ===== SUBMISSION WORKFLOW =====

    def before_submit(self):
        """Called before document is submitted"""
        self.validate_for_submit()

    def on_submit(self):
        """Called after document is submitted"""
        self.create_gl_entries()

    def before_cancel(self):
        """Called before document is cancelled"""
        self.validate_cancellation()

    def on_cancel(self):
        """Called after document is cancelled"""
        self.reverse_gl_entries()

    def on_update_after_submit(self):
        """Called when submitted doc is updated (limited fields)"""
        pass

    # ===== DELETION =====

    def before_delete(self):
        """Called before document is deleted"""
        self.check_dependencies()

    def after_delete(self):
        """Called after document is deleted"""
        self.cleanup_attachments()

    def on_trash(self):
        """Called when document is trashed"""
        pass

    def after_restore(self):
        """Called after document is restored from trash"""
        pass

    # ===== CUSTOM METHODS =====

    def validate_dates(self):
        if self.end_date and self.start_date > self.end_date:
            frappe.throw("End date cannot be before start date")

    def calculate_totals(self):
        self.total = sum(d.amount for d in self.items)
```

## Child Table (Table Field)

### Parent DocType
```json
{
  "fieldname": "items",
  "fieldtype": "Table",
  "label": "Items",
  "options": "My DocType Item",
  "reqd": 1
}
```

### Child DocType JSON
```json
{
  "name": "My DocType Item",
  "module": "My Module",
  "doctype": "DocType",
  "istable": 1,
  "editable_grid": 1,
  "fields": [
    {
      "fieldname": "item",
      "fieldtype": "Link",
      "options": "Item",
      "in_list_view": 1,
      "reqd": 1
    },
    {
      "fieldname": "qty",
      "fieldtype": "Float",
      "in_list_view": 1
    },
    {
      "fieldname": "rate",
      "fieldtype": "Currency",
      "in_list_view": 1
    },
    {
      "fieldname": "amount",
      "fieldtype": "Currency",
      "in_list_view": 1,
      "read_only": 1
    }
  ]
}
```

## Single DocType (Settings)

For application settings that have only one record:

```json
{
  "name": "My App Settings",
  "module": "My Module",
  "doctype": "DocType",
  "issingle": 1,
  "fields": [
    {
      "fieldname": "enable_feature",
      "fieldtype": "Check",
      "label": "Enable Feature"
    },
    {
      "fieldname": "api_key",
      "fieldtype": "Password",
      "label": "API Key"
    }
  ]
}
```

Access in code:
```python
settings = frappe.get_single("My App Settings")
if settings.enable_feature:
    do_something()
```

## Virtual DocType

DocType without database table, computed on-the-fly:

```json
{
  "name": "My Virtual DocType",
  "module": "My Module",
  "doctype": "DocType",
  "is_virtual": 1
}
```

Controller:
```python
class MyVirtualDocType(Document):
    @staticmethod
    def get_list(args):
        # Return list of virtual documents
        return [{"name": "doc1", "value": 100}]

    @staticmethod
    def get_count(args):
        return len(MyVirtualDocType.get_list(args))

    @staticmethod
    def get_stats(args):
        return {}
```

## Permissions

```json
{
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1,
      "submit": 1,
      "cancel": 1,
      "amend": 1,
      "report": 1,
      "export": 1,
      "import": 1,
      "share": 1,
      "print": 1,
      "email": 1
    },
    {
      "role": "Sales User",
      "read": 1,
      "write": 1,
      "create": 1,
      "if_owner": 1
    }
  ]
}
```

## Best Practices

### Naming Conventions
- Use singular names: "Customer" not "Customers"
- Use Title Case with spaces: "Sales Invoice"
- Fieldnames use snake_case: `customer_name`

### Field Design
- Put most important fields first
- Use Section Breaks to organize
- Use Tab Breaks for complex forms
- Set `in_list_view` for key fields
- Set `in_standard_filter` for filterable fields

### Performance
- Index frequently queried fields with `search_index: 1`
- Use `read_only` to prevent unnecessary validation
- Limit child table rows with `max_attachments`

### Data Integrity
- Use `unique: 1` for unique constraints
- Set appropriate `reqd` (required) flags
- Use `depends_on` for conditional visibility
- Use `mandatory_depends_on` for conditional requirements

## Common Patterns

### Status Field Pattern
```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "options": "\nDraft\nPending Approval\nApproved\nRejected",
  "default": "Draft",
  "in_list_view": 1,
  "in_standard_filter": 1,
  "read_only": 1,
  "allow_on_submit": 1
}
```

### Amount Calculation Pattern
```json
[
  {"fieldname": "qty", "fieldtype": "Float"},
  {"fieldname": "rate", "fieldtype": "Currency"},
  {"fieldname": "amount", "fieldtype": "Currency", "read_only": 1}
]
```
With controller:
```python
def validate(self):
    for item in self.items:
        item.amount = flt(item.qty) * flt(item.rate)
    self.total = sum(item.amount for item in self.items)
```

### Linked Document Pattern
```json
{
  "fieldname": "customer",
  "fieldtype": "Link",
  "options": "Customer",
  "reqd": 1
},
{
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "fetch_from": "customer.customer_name",
  "read_only": 1
}
```
