---
name: notepad-new-form-field
description: "Reference doc: New Form Field Checklist"
---

# New Form Field Checklist

Use this notepad when adding a form field to the simpler-grants-gov grant application system.

## The Three-Schema Architecture

Every form field in simpler-grants-gov is defined across three schemas:

| Schema | Purpose | Location |
|--------|---------|----------|
| **JSON Schema** | Data structure & types | `api/src/form_schema/` |
| **UI Schema** | Rendering & layout | `api/src/form_schema/` |
| **Rule Schema** | Validation & conditional logic | `api/src/form_schema/` |

## Step 1: JSON Schema (data definition)

Define the field's type, constraints, and metadata:

```json
{
  "properties": {
    "my_new_field": {
      "type": "string",
      "title": "My New Field",
      "maxLength": 500
    }
  },
  "required": ["my_new_field"]
}
```

Supported types: `string`, `number`, `integer`, `boolean`, `array`, `object`

## Step 2: UI Schema (rendering)

Control how the field appears in the form:

```json
{
  "my_new_field": {
    "ui:widget": "textarea",
    "ui:options": {
      "rows": 5
    },
    "ui:help": "Provide a detailed description."
  }
}
```

## Step 3: Rule Schema (validation & conditional logic)

Add cross-field validation or conditional display:

```json
{
  "rules": [
    {
      "conditions": {
        "my_other_field": { "const": "yes" }
      },
      "required": ["my_new_field"]
    }
  ]
}
```

## Custom Validator

The project uses `OUR_VALIDATOR`, a custom JSON Schema validator. Do NOT use the default `jsonschema` validator — it doesn't handle the project's extensions.

## XML Compatibility Warning

Grant application forms output XML that MUST match the legacy Grants.gov system's format. When adding fields:
- Element ordering matters (must match legacy schema)
- Namespace prefixes must be preserved
- Enum values must use legacy system values exactly

## Test Triad

Every form field needs three test cases:

```python
def test_form_minimal():
    """Form with only required fields"""
    pass

def test_form_full():
    """Form with all fields populated"""
    pass

def test_form_empty():
    """Form with no fields (validates required field errors)"""
    pass
```

## Don't Forget

- [ ] JSON Schema: field type, title, constraints
- [ ] UI Schema: widget, layout, help text
- [ ] Rule Schema: cross-field validation (if applicable)
- [ ] Test triad: minimal, full, empty
- [ ] XML compatibility verified (element order, namespaces)
- [ ] Uses `OUR_VALIDATOR` (not default jsonschema)
