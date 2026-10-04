---
name: rule-api-form-schema
description: MANDATORY when editing files matching ["api/src/form_schema/**/*.py"]. When working on form schema definitions in api/src/form_schema/
---

# API Form Schema Rules

## Three-Schema Architecture

ALWAYS define every form with three co-located schemas: `FORM_JSON_SCHEMA` (validation), `FORM_UI_SCHEMA` (rendering), `FORM_RULE_SCHEMA` (pre/post population and custom validation). ALWAYS bundle into a static `Form` instance and register in `get_active_forms()`. NEVER fetch forms from the database at runtime.

Example from codebase:
```python
# From api/src/form_schema/forms/__init__.py
def get_active_forms() -> list[Form]:
    return [
        SF424_v4_0, SF424a_v1_0, SF424b_v1_1, SFLLL_v2_0,
        ProjectAbstractSummary_v2_0, BudgetNarrativeAttachment_v1_2,
    ]
```

## JSON Schema Standard

ALWAYS use JSON Schema Draft 2020-12. ALWAYS enable format validation via `FORMAT_CHECKER`. ALWAYS use `OUR_VALIDATOR` (custom required-field path fix) instead of the stock validator. ALWAYS call `check_schema()` before validation. NEVER silently accept invalid schemas.

Example from codebase:
```python
# From api/src/form_schema/jsonschema_validator.py
OUR_VALIDATOR = jsonschema.validators.extend(
    validator=jsonschema.Draft202012Validator, validators={"required": _required}
)

try:
    OUR_VALIDATOR.check_schema(json_schema)
except jsonschema.exceptions.SchemaError:
    logger.exception("Invalid json schema found, cannot validate")
    raise
```

## Non-Blocking Validation

ALWAYS return validation issues as `warnings` in the PUT response. NEVER block saves on validation errors. ONLY block at submission time.

Example from codebase:
```python
warnings: list[ValidationErrorDetail] = validate_json_schema_for_form(
    application_response, form
)
```

## UI Schema Labels

ALWAYS number and label UI schema sections to match the official PDF form. When PDF and legacy instructions conflict, use the PDF as source of truth.

Example from codebase:
```python
{"type": "section", "label": "1. Type of Federal Action", ...}
{"type": "section", "label": "2. Status of Federal Action", ...}
```

## XML Transform Rules

ALWAYS define XML generation as declarative `FORM_XML_TRANSFORM_RULES` co-located with the form. ALWAYS include `_metadata` with namespace declarations. ALWAYS include `att`, `glob`, and `globLib` namespaces even if unused.

Example from codebase:
```python
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

ALWAYS use `"static_value"` for XSD fields that are NOT user-input. NEVER add non-input fields to the JSON schema.

Example from codebase:
```python
"form_version_identifier": {
    "xml_transform": {
        "target": "FormVersionIdentifier",
        "namespace": "glob",
        "static_value": "1.1",
    }
}
```

## Legacy XML Matching

ALWAYS verify generated XML matches legacy Grants.gov output: `FormVersionIdentifier` as first child, all namespaces present, element order matching XSD, attribute values matching legacy format. ALWAYS write legacy XML comparison tests.

Example from codebase:
```python
def test_generate_sf424b_xml_matches_legacy_format(self):
    first_child = next(iter(root))
    assert first_child.tag == "{http://apply.grants.gov/system/Global-V1.0}FormVersionIdentifier"
    child_tags = [child.tag for child in list(root)]
    assert child_tags == expected_order
```

## Rule Schema Processing

ALWAYS structure rule schemas to mirror the JSON response shape. ALWAYS use the `handlers` dict for dispatch. ALWAYS use `JsonRuleContext` with deep-copied `json_data` to avoid partial mutations on error.

Example from codebase:
```python
# From api/src/form_schema/rule_processing/json_rule_processor.py
handlers: dict[str, Callable[...]] = {
    "gg_pre_population": handle_pre_population,
    "gg_post_population": handle_post_population,
    "gg_validation": handle_validation,
}

def _process_rule_schema(context: JsonRuleContext, rule_schema: dict, path: list[str]) -> None:
    for k, v in rule_schema.items():
        if k in handlers:
            handlers[k](context, v, path)
        elif isinstance(v, dict):
            _process_rule_schema(context=context, rule_schema=v, path=path + [k])
```

## Shared Schemas

ALWAYS reference shared fields via `"$ref": shared_schema.field_ref("field_name")`. ALWAYS resolve all `$ref` references before storing or validating (using `jsonref.replace_refs` with `lazy_load=False`, `proxies=False`). NEVER require network calls for resolution.

## Enum Format

ALWAYS format enum values for states/countries as `"XX: Full Name"` (e.g., `"NY: New York"`). ALWAYS source from `shared_form_constants.py`.

## Conditional Address Validation

ALWAYS use JSON Schema `allOf` with `if/then` to conditionally require `state` and `zip_code` when country is `"USA: UNITED STATES"`.

Example from codebase:
```python
"allOf": [{
    "if": {
        "properties": {"country": {"const": "USA: UNITED STATES"}},
        "required": ["country"],
    },
    "then": {"required": ["state", "zip_code"]},
}]
```

## ORM Conventions

ALWAYS set SQLAlchemy relationships (e.g., `application.submitted_by_user = user`). NEVER directly set foreign keys.

## Builder Pattern

NEVER put domain-specific logic in `JsonSchemaBuilder`. ALWAYS keep detection and mapping logic in the calling layer. NEVER add fallback values for malformed data -- let errors propagate.

## Attachment Handling

ALWAYS use `str(UUID)` as mapping keys for attachment lookups. ALWAYS store attachment fields as UUID strings referencing `application_attachment` records.

Example from codebase:
```python
application_attachment_ids = [
    str(att.application_attachment_id)
    for att in context.application_form.application.application_attachments
]
```

## Testing

ALWAYS write three core tests per form: `test_*_minimal_valid_json`, `test_*_full_valid_json`, `test_*_empty_json`. ALWAYS use `validate_required()` helper and session-scoped resolved-form fixtures from `conftest.py`. ALWAYS use factory classes for test data setup.

Example from codebase:
```python
def test_budget_narrative_v1_2_empty_json(budget_narrative_attachment_v1_2):
    validate_required({}, ["$.attachments"], budget_narrative_attachment_v1_2)

def test_budget_narrative_v1_2_minimal_valid_json(
    minimal_valid_budget_narrative_v1_2, budget_narrative_attachment_v1_2
):
    issues = validate_json_schema_for_form(
        minimal_valid_budget_narrative_v1_2, budget_narrative_attachment_v1_2
    )
    assert len(issues) == 0
```

---

## Context Enrichment

When generating significant form schema code (new form, XML transforms, rule processing), enrich your context:
- Call `get_architecture_section("forms")` from the `simpler-grants-context` MCP server to understand the three-schema architecture
- Call `get_rule_detail("forms-vertical")` for the cross-cutting forms conventions
- Call `get_rule_detail("api-validation")` for validation patterns that form schemas integrate with
- Consult **Compound Knowledge** for indexed documentation on form schema patterns, XML transform conventions, and legacy Grants.gov compatibility

## Related Rules

When working on form schemas, also consult these related rules:
- **`forms-vertical.mdc`** — three-schema definition, custom validator, non-blocking validation, XML transform rules
- **`api-database.mdc`** — model conventions for form-related tables
- **`api-validation.mdc`** — `ValidationErrorType`, `ValidationErrorDetail` for form validation errors
- **`api-error-handling.mdc`** — non-blocking saves with warnings pattern
- **`api-tests.mdc`** — three-test triad (minimal, full, empty) for form validation tests
- **`cross-domain.mdc`** — structured logging, boolean naming

## Specialist Validation

When generating or significantly modifying form schema code:

**For simple changes (adding a field to an existing schema):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new XML transform rules, new validation logic):**
Invoke `schema-drift-detector` to validate schema consistency across JSON/UI/Rule schemas.

**For complex changes (new form definition, new rule processing handler, XML namespace changes):**
Invoke the following specialists (run in parallel where possible):
- `schema-drift-detector` — validate three-schema consistency (JSON, UI, Rule)
- `data-integrity-guardian` — validate data transforms and form data handling
- `kieran-python-reviewer` — Python-specific quality review for schema patterns
