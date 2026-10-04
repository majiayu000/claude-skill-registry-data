---
name: rule-api-error-handling
description: MANDATORY when editing files matching ["api/src/**/*.py"]. When handling errors anywhere in the API codebase
---

# API Error Handling Rules

## Core Error Mechanism

ALWAYS use `raise_flask_error(status_code, message, validation_issues=[...])` from `src.api.route_utils` for all error responses. NEVER raise raw exceptions or return error tuples from services.

Example from codebase:
```python
# From api/src/services/
if not org_user:
    raise_flask_error(404, message=f"Could not find User with ID {user_id}")

if not opportunity.is_draft:
    raise_flask_error(422, message="Only draft opportunities can be updated")

if user.user_id != user_id:
    raise_flask_error(403, "Forbidden")
```

## Validation Error Details

ALWAYS include `ValidationErrorDetail` objects in `validation_issues` when raising validation errors. Each detail MUST include a `type` from `ValidationErrorType` and a `message`. Optionally include `field` and `value`.

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

## Centralized Error Types

ALWAYS define error types in `ValidationErrorType(StrEnum)` in `api/src/validation/validation_constants.py`. NEVER define error type strings inline. ALWAYS use specific descriptive types. NEVER use generic types like `VALIDATION_ERROR`. Consolidate closely related types when the frontend treats them identically.

Example from codebase:
```python
class ValidationErrorType(StrEnum):
    NOT_IN_PROGRESS = "not_in_progress"
    MISSING_REQUIRED_FORM = "missing_required_form"
    APPLICATION_FORM_VALIDATION = "application_form_validation"
    COMPETITION_NOT_OPEN = "competition_not_open"
```

## Raise vs Return Pattern

ALWAYS use `raise_flask_error` for precondition checks that halt execution. ALWAYS return `list[ValidationErrorDetail]` for form validation where multiple errors coexist and must be aggregated.

Example from codebase:
```python
# Raise pattern for preconditions
def validate_competition_open(competition: Competition, action: ApplicationAction) -> None:
    if not competition.is_open:
        raise_flask_error(422, message, validation_issues=[...])

# Return pattern for aggregated form errors
def get_required_form_errors(application: Application) -> list[ValidationErrorDetail]:
    errors: list[ValidationErrorDetail] = []
    for required_form in required_forms:
        if required_form.form_id not in existing_form_ids:
            errors.append(ValidationErrorDetail(...))
    return errors
```

## Non-Blocking Saves

ALWAYS return validation issues as warnings during save/update operations. ONLY block (raise errors) during submission.

Example from codebase:
```python
# During save -- return warnings
warnings: list[ValidationErrorDetail] = validate_json_schema_for_form(
    application_response, form
)
return application_form, warnings

# During submission -- block
validate_forms(application, ApplicationAction.SUBMIT)  # raises 422
```

## HTTP Status Codes

ALWAYS use 403 for identity/authorization failures. ALWAYS use 404 for missing resources. ALWAYS use 422 for business rule violations. NEVER use 401 for authorization failures (401 = not authenticated). NEVER use 400 for business rule violations.

## Validation Order

ALWAYS follow this order in service functions: (1) request validation, (2) 404 checks, (3) authorization checks, (4) business logic validation. NEVER run business logic before auth -- it leaks information.

Example from codebase:
```python
# Correct order
opportunity = get_opportunity_for_grantors(db_session, user, opportunity_id)
verify_access(user, {Privilege.UPDATE_OPPORTUNITY}, opportunity.agency_record)
validate_opportunity_is_draft(opportunity)
```

## Logging Errors

ALWAYS use `logger.info()` for expected client errors (4xx). NEVER use `logger.warning()` for 4xx errors. ALWAYS use static log messages with dynamic data in `extra={}`.

Example from codebase:
```python
logger.info(
    "Cannot start application - competition is not open",
    extra={
        "opening_date": competition.opening_date,
        "closing_date": competition.closing_date,
        "application_action": action,
    },
)
```

## Validation Architecture

ALWAYS place validation logic in the service layer (e.g., `api/src/services/applications/application_validation.py`). NEVER put validation logic in route handlers. ALWAYS consolidate duplicate validation into shared modules.

## Context-Aware Error Messages

ALWAYS use `ApplicationAction(StrEnum)` to parameterize validation messages. NEVER hardcode action-specific text in shared validation functions.

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

## Two-Level Error Reporting

ALWAYS use two-level error reporting for form validation: top-level errors identify which forms have issues, `form_error_map` contains field-level errors.

Example from codebase:
```python
def get_application_form_errors(
    application: Application,
) -> tuple[list[ValidationErrorDetail], dict[str, list[ValidationErrorDetail]]]:
    form_error_map: dict[str, list[ValidationErrorDetail]] = {}
    form_errors: list[ValidationErrorDetail] = []
    for application_form in application.application_forms:
        validation_errors = validate_json_schema_for_form(
            application_form.application_response, application_form.form
        )
        if validation_errors:
            form_error_map[str(application_form.application_form_id)] = validation_errors
            form_errors.append(ValidationErrorDetail(
                type=ValidationErrorType.APPLICATION_FORM_VALIDATION,
                message="The application form has outstanding errors.",
                field="application_form_id",
                value=application_form.application_form_id,
            ))
    return form_errors, form_error_map
```

## Failed Submission Audits

ALWAYS record audit events for failed submissions in a separate transaction (main transaction was rolled back). ALWAYS wrap audit in try/except to prevent masking the original error.

Example from codebase:
```python
def _handle_submit_error(
    db_session: db.Session, error: HTTPError, application_id: UUID, user_id: UUID
) -> Never:
    if error.status_code != 422:
        raise error
    try:
        if db_session.is_active:
            db_session.rollback()
        with db_session.begin():
            add_audit_event_by_id(db_session, application_id=application_id,
                user_id=user_id,
                audit_event=ApplicationAuditEvent.APPLICATION_SUBMIT_REJECTED)
    except Exception:
        logger.exception("Failed to add audit event for failed submission")
    raise error
```

---

## Context Enrichment

When generating significant error handling code (new error patterns, new validation architecture, audit handling), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand error handling architectural principles
- Call `get_rule_detail("api-validation")` for validation error type conventions
- Call `get_rule_detail("api-routes")` for how errors surface through route handlers
- Consult **Compound Knowledge** for indexed documentation on error patterns and frontend error consumption

## Related Rules

When working on error handling, also consult these related rules:
- **`api-routes.mdc`** — error logging in route handlers, `response.ApiResponse` patterns
- **`api-services.mdc`** — `raise_flask_error()` usage in service functions, validation order
- **`api-validation.mdc`** — `ValidationErrorType` enum, raise vs return pattern, non-blocking saves
- **`frontend-services.mdc`** — how the frontend consumes API errors (`ApiRequestError`, `parseErrorStatus()`)
- **`cross-domain.mdc`** — structured logging for errors, `logger.info()` for 4xx

**Debugging:** Invoke the debugging agent (or use `/debug`) to trace error propagation through the error handling stack when debugging unexpected error responses.

## Specialist Validation

When generating or significantly modifying error handling code:

**For simple changes (adding a new error type, fixing a status code):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new error pattern, new validation function):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new error architecture, audit handling, cross-layer error flow):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate error contract consistency across API layers
- `security-sentinel` — validate no sensitive information leakage in error responses
- `kieran-python-reviewer` — Python-specific quality review

<!-- Hook enforcement: convention-checker validates raise_flask_error() usage, error-pattern-checker validates error handling contract -->
