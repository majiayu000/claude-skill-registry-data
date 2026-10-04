---
name: rule-forms-vertical
description: MANDATORY when editing files matching ["api/src/form_schema/**/*", "frontend/src/**/form*/**/*"]. When working on grant application form features (API schemas, frontend forms, form tests)
---

# Forms Vertical Rules

## Three-Schema Form Definition
ALWAYS define every form with three co-located schemas: `FORM_JSON_SCHEMA` (validation), `FORM_UI_SCHEMA` (rendering), `FORM_RULE_SCHEMA` (business logic). ALWAYS bundle into a static `Form` instance registered in `get_active_forms()`. NEVER fetch forms from the database at runtime.

Example from codebase:
```python
# From api/src/form_schema/forms/__init__.py
def get_active_forms() -> list[Form]:
    return [
        SF424_v4_0,
        SF424a_v1_0,
        SF424b_v1_1,
        SFLLL_v2_0,
        ProjectAbstractSummary_v2_0,
        BudgetNarrativeAttachment_v1_2,
        ProjectNarrativeAttachment_v1_2,
    ]
```

## Custom JSON Schema Validator
ALWAYS use `OUR_VALIDATOR` (extends Draft2020-12 with correct required-field paths). ALWAYS enable format validation via `FORMAT_CHECKER`. NEVER use the stock `Draft202012Validator` directly.

Example from codebase:
```python
# From api/src/form_schema/jsonschema_validator.py
OUR_VALIDATOR = jsonschema.validators.extend(
    validator=jsonschema.Draft202012Validator,
    validators={"required": _required}
)
```

## Fail Loudly on Invalid Schemas
ALWAYS call `check_schema()` before using a JSON schema for validation. ALWAYS let `SchemaError` propagate as a 500. NEVER silently accept invalid schemas.

Example from codebase:
```python
# From api/src/form_schema/jsonschema_validator.py
try:
    OUR_VALIDATOR.check_schema(json_schema)
except jsonschema.exceptions.SchemaError:
    logger.exception("Invalid json schema found, cannot validate")
    raise
```

## Declarative XML Transform Rules
ALWAYS define XML generation as a declarative `FORM_XML_TRANSFORM_RULES` dict co-located with the form. ALWAYS include `_metadata` with namespace declarations. ALWAYS include `att`, `glob`, and `globLib` namespaces even if unused.

Example from codebase:
```python
# From api/src/form_schema/forms/sf424b.py
"_metadata": {
    "namespaces": {
        "default": "http://apply.grants.gov/forms/SF424B-V1.1",
        "SF424B": "http://apply.grants.gov/forms/SF424B-V1.1",
        "att": "http://apply.grants.gov/system/Attachments-V1.0",
        "globLib": "http://apply.grants.gov/system/GlobalLibrary-V2.0",
        "glob": "http://apply.grants.gov/system/Global-V1.0",
    },
}
```

## Static Values for Non-Input XML Fields
ALWAYS use `"static_value"` in XML transform config for XSD fields that are NOT user-input. NEVER add non-input fields to the JSON schema.

Example from codebase:
```python
# From api/src/form_schema/forms/sf424b.py
"form_version_identifier": {
    "xml_transform": {
        "target": "FormVersionIdentifier",
        "namespace": "glob",
        "static_value": "1.1",
    }
}
```

## Legacy XML Fidelity
ALWAYS verify generated XML matches legacy Grants.gov output: `FormVersionIdentifier` as first child, all namespaces present, element order matching XSD sequence. ALWAYS include legacy XML comparison tests.

Example from codebase:
```python
# From api/tests/src/form_schema/test_xml_transform.py
first_child = next(iter(root))
assert first_child.tag == (
    "{http://apply.grants.gov/system/Global-V1.0}"
    "FormVersionIdentifier"
), "FormVersionIdentifier must be first child per XSD"
```

## Non-Blocking Validation with Warnings
ALWAYS return validation issues as `warnings` in PUT responses. NEVER block saves on validation errors. Only block at submission time.

Example from codebase:
```python
# From api/src/services/applications/update_application_form.py
warnings: list[ValidationErrorDetail] = validate_json_schema_for_form(
    application_response, form
)
# Save proceeds regardless of warnings
```

## Minimal/Full/Empty Validation Test Triad
ALWAYS write three core tests per form: `test_*_minimal_valid_json`, `test_*_full_valid_json`, `test_*_empty_json`. ALWAYS use the shared `validate_required()` helper from `conftest.py`.

Example from codebase:
```python
# From api/tests/src/form_schema/forms/conftest.py
def validate_required(data, expected_required_fields, form):
    validation_issues = validate_json_schema_for_form(data, form)
    assert len(validation_issues) == len(expected_required_fields)
    for issue in validation_issues:
        assert issue.type == "required"
        assert issue.field in expected_required_fields
```

## Page Object Model for E2E Form Tests
ALWAYS use Page Object Model for complex form E2E tests. ALWAYS separate test data into fixtures, form metadata into page objects, and form-filling logic into shared utilities.

Example from codebase:
```typescript
// From frontend/tests/e2e/page-objects/sflll-form.page.ts
export function getSflllFillFields(data: SflllEntityData): FillFieldDefinition[] {
  return [
    { selector: "#federal_action_type", value: data.federalAction.type,
      type: "dropdown", section: "Section 1" },
    { testId: "material_change_year", value: data.materialChange.year,
      type: "text", section: "Section 3" },
  ];
}
```

## Single Path, No Fallbacks
NEVER add placeholder values or silent error handling for malformed form data. ALWAYS let errors propagate. NEVER mask bugs with fallback paths.

## Set Relationships, Not Foreign Keys
ALWAYS set SQLAlchemy relationships (e.g., `application.submitted_by_user = user`). NEVER directly set foreign keys. NEVER set both.

## UI Section Labels Match PDF
ALWAYS number and label UI schema sections to match the official PDF form. When PDF and legacy instructions conflict, ALWAYS use the PDF.

---

## Context Enrichment

When generating significant forms code (new form definition, XML transforms, E2E form tests), enrich your context:
- Call `get_architecture_section("forms")` from the `simpler-grants-context` MCP server to understand the three-schema architecture
- Call `get_rule_detail("api-form-schema")` for detailed form schema conventions
- Call `get_rule_detail("api-validation")` for validation patterns that forms integrate with
- Call `get_rule_detail("api-database")` for model conventions for form-related tables
- Consult **Compound Knowledge** for indexed documentation on form patterns, XML compatibility, legacy Grants.gov requirements, and ADRs related to forms architecture

## Related Rules

When working on forms, also consult these related rules:
- **`api-form-schema.mdc`** — JSON Schema standard, non-blocking validation, XML transforms, rule processing
- **`api-database.mdc`** — model conventions for form-related tables, relationship patterns
- **`api-validation.mdc`** — `ValidationErrorType`, `ValidationErrorDetail`, non-blocking saves
- **`api-tests.mdc`** — three-test triad (minimal, full, empty), factory patterns
- **`frontend-tests.mdc`** — Page Object Model for E2E form tests, Playwright conventions
- **`frontend-components.mdc`** — form component patterns, `useActionState` for submissions
- **`cross-domain.mdc`** — structured logging, boolean naming, feature flags

## Specialist Validation

When generating or significantly modifying forms code:

**For simple changes (adding a field to existing form schema):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new XML transform rules, new validation logic):**
Invoke `schema-drift-detector` to validate three-schema consistency (JSON, UI, Rule).

**For complex changes (new form definition, new rule processing handler, legacy XML compatibility):**
Invoke the following specialists (run in parallel where possible):
- `schema-drift-detector` — validate three-schema consistency (JSON, UI, Rule)
- `data-integrity-guardian` — validate form data handling and transform safety
- `pattern-recognition-specialist` — detect duplication across form definitions
- `kieran-python-reviewer` — Python-specific quality review for form schema patterns
