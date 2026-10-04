---
name: rule-api-validation
description: MANDATORY when editing files matching ["api/src/validation/**/*.py"]. When working on validation logic in api/src/validation/
---

# API Validation Rules

## Error Type Definitions

ALWAYS define new validation error types in `ValidationErrorType(StrEnum)` in `api/src/validation/validation_constants.py`. NEVER define error type strings inline. ALWAYS use specific, descriptive types the frontend can map to localized messages. NEVER use generic types like `FORM_ERROR`.

Example from codebase:
```python
# From api/src/validation/validation_constants.py
class ValidationErrorType(StrEnum):
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    NOT_IN_PROGRESS = "not_in_progress"
    MISSING_REQUIRED_FORM = "missing_required_form"
    APPLICATION_FORM_VALIDATION = "application_form_validation"
    COMPETITION_NOT_OPEN = "competition_not_open"
```

## Error Raising

ALWAYS use `raise_flask_error(status_code, message, validation_issues=[ValidationErrorDetail(...)])`. Each `ValidationErrorDetail` MUST include `type` from `ValidationErrorType` and a `message`. NEVER raise without structured validation details.

Example from codebase:
```python
raise_flask_error(
    422,
    "Cannot start application - competition is not yet open",
    validation_issues=[
        ValidationErrorDetail(
            type=ValidationErrorType.COMPETITION_NOT_YET_OPEN,
            message="Competition is not yet open for applications",
            field="opening_date",
        )
    ],
)
```

## Raise vs Return Pattern

ALWAYS use `raise_flask_error` for precondition checks that halt execution. ALWAYS return `list[ValidationErrorDetail]` for form validation where multiple errors coexist.

Example from codebase:
```python
# Raise pattern for preconditions
def validate_competition_open(competition: Competition, action: ApplicationAction) -> None:
    if not competition.is_open:
        raise_flask_error(422, message, validation_issues=[...])

# Return pattern for aggregated errors
def get_required_form_errors(application: Application) -> list[ValidationErrorDetail]:
    errors: list[ValidationErrorDetail] = []
    for required_form in required_forms:
        if required_form.form_id not in existing_form_ids:
            errors.append(ValidationErrorDetail(
                message=f"Form {required_form.form_name} is required",
                type=ValidationErrorType.MISSING_REQUIRED_FORM,
                field="form_id",
                value=required_form.form_id,
            ))
    return errors
```

## Validation Architecture

ALWAYS place validation functions in `api/src/services/applications/` (e.g., `application_validation.py`). NEVER put validation logic in route handlers.

## Consolidation

ALWAYS consolidate duplicate validation into `application_validation.py`. NEVER duplicate the same validation check in separate service files.

Example from codebase:
```python
# Single function, imported everywhere
from src.services.applications.application_validation import (
    ApplicationAction, validate_competition_open,
)
validate_competition_open(competition, ApplicationAction.START)
validate_competition_open(application.competition, ApplicationAction.SUBMIT)
```

## ApplicationAction Enum

ALWAYS use `ApplicationAction(StrEnum)` to parameterize validation error messages. NEVER hardcode action-specific text.

Example from codebase:
```python
class ApplicationAction(StrEnum):
    START = "start"
    SUBMIT = "submit"
    MODIFY = "modify"

def validate_application_in_progress(application: Application, action: ApplicationAction):
    if application.application_status != ApplicationStatus.IN_PROGRESS:
        message = f"Cannot {action} application. Status: {application.application_status}"
        raise_flask_error(403, message, validation_issues=[...])
```

## Model-Level Business Rules

ALWAYS define reusable business rule computations as `@property` on the DB model when logic depends only on the model's own fields.

Example from codebase:
```python
@property
def is_open(self) -> bool:
    current_date = get_now_us_eastern_date()
    if self.opening_date is not None and current_date < self.opening_date:
        return False
    if self.closing_date is not None:
        grace_period = self.grace_period or 0
        if current_date > self.closing_date + timedelta(days=grace_period):
            return False
    return True
```

## Shared Schemas

ALWAYS extract API schemas used across multiple domains into `api/src/api/schemas/shared_schema.py`. NEVER duplicate schema definitions.

## JSON Schema Validation

ALWAYS validate form responses against JSON Schema via the `jsonschema` library. ALWAYS map JSON Schema errors to `ValidationErrorDetail` objects.

## Non-Blocking Saves

ALWAYS return validation issues as `warnings` during save/update. NEVER block saves on validation errors. ONLY block at submission time.

## Rule Processing

ALWAYS use the rule processing system (`api/src/form_schema/rule_processing/`) for validation beyond standard JSON Schema. Rules MUST be defined as JSON matching the form response shape.

## Logging

NEVER use `logger.warning()` for expected client validation errors (4xx). ALWAYS use `logger.info()` with `extra={}`. NEVER embed dynamic values in log message strings.

Example from codebase:
```python
logger.info(
    "User attempted to access an application they are not associated with",
    extra={"user_id": user.user_id, "application_id": application.application_id},
)
```

## Consolidate Error Types

NEVER create separate error types for closely related scenarios when the frontend treats them identically. NEVER include dynamic IDs in error message strings.

## Testing

ALWAYS use `@freeze_time(TEST_DATE)` for date-dependent validation tests. ALWAYS use parametrized tests for boundary conditions. ALWAYS use Factory `.build()` for unit tests, `.create()` for integration tests.

Example from codebase:
```python
@pytest.mark.parametrize("opening_date,closing_date,grace_period,expected_is_open", [
    (None, None, None, True),
    (date(2025, 1, 1), date(2025, 12, 31), 10, True),
    (date(2025, 1, 16), date(2025, 1, 31), 0, False),
])
@freeze_time("2025-01-15 12:00:00", tz_offset=0)
def test_competition_get_200_is_open(...):
```

---

## Context Enrichment

When generating significant validation code (new error types, validation functions, schema validation), enrich your context:
- Call `get_rule_detail("api-error-handling")` from the `simpler-grants-context` MCP server for error handling patterns that validation integrates with
- Call `get_rule_detail("api-routes")` for how validation errors surface through route handlers
- Consult **Compound Knowledge** for indexed documentation on validation patterns and error type conventions

## Related Rules

When working on validation logic, also consult these related rules:
- **`api-routes.mdc`** — how validation errors propagate through route handlers
- **`api-error-handling.mdc`** — `raise_flask_error()`, `ValidationErrorDetail`, raise vs return pattern
- **`api-form-schema.mdc`** — JSON Schema validation, non-blocking saves, form validation patterns
- **`cross-domain.mdc`** — structured logging for validation failures, boolean naming

## Specialist Validation

When generating or significantly modifying validation code:

**For simple changes (adding a new `ValidationErrorType` value):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new validation function, new error patterns):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new validation architecture, cross-field validation, rule processing):**
Invoke the following specialists (run in parallel where possible):
- `security-sentinel` — validate input validation completeness, no bypass risks
- `code-simplicity-reviewer` — check validation logic complexity and maintainability
- `kieran-python-reviewer` — Python-specific quality review
