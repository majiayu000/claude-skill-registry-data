---
name: rule-api-routes
description: MANDATORY when editing files matching ["api/src/api/**/*.py"]. When working on API route handlers in api/src/api/
---

# API Routes Rules

## Route Definition

ALWAYS organize each API domain under `api/src/api/<domain>/` with three files: `<domain>_blueprint.py`, `<domain>_routes.py`, `<domain>_schemas.py`. NEVER mix schemas into route files.

Example from codebase:
```python
# From api/src/api/agencies_v1/
agency_blueprint.py
agency_routes.py
agency_schema.py
```

## Decorator Stack Order

ALWAYS apply decorators in this exact top-to-bottom order: (1) `@blueprint.METHOD("/path")`, (2) `@blueprint.input(...)`, (3) `@blueprint.output(...)`, (4) `@blueprint.doc(...)`, (5) auth decorator, (6) `@flask_db.with_db_session()`.

Example from codebase:
```python
# From api/src/api/users/user_routes.py
@user_blueprint.post("/<uuid:user_id>/saved-opportunities/notifications")
@user_blueprint.input(SetUserSavedOpportunityNotificationRequestSchema)
@user_blueprint.output(SetUserSavedOpportunityNotificationResponseSchema)
@user_blueprint.doc(
    responses=[200, 401, 403, 404, 422], security=jwt_or_api_user_key_security_schemes
)
@jwt_or_api_user_key_multi_auth.login_required
@flask_db.with_db_session()
def user_saved_opportunities_notifications(
    db_session: db.Session, user_id: UUID, json_data: dict
) -> response.ApiResponse:
```

## Thin Route Handlers

ALWAYS keep route handlers thin. NEVER put business logic in route handlers. MUST delegate to service functions under `src/services/<domain>/`. Route handlers contain only: logging setup, auth verification, a `db_session.begin()` block calling the service, and returning `response.ApiResponse`.

Example from codebase:
```python
# From api/src/api/users/user_routes.py
def user_get_saved_opportunity_notifications(
    db_session: db.Session, user_id: UUID
) -> response.ApiResponse:
    logger.info("GET /v1/users/:user_id/saved-opportunities/notifications")
    user = jwt_or_api_user_key_multi_auth.get_user()
    if user.user_id != user_id:
        raise_flask_error(403, "Forbidden")
    with db_session.begin():
        db_session.add(user)
        result = get_saved_opportunity_notification_preferences(db_session, user)
    return response.ApiResponse(message="Success", data=result)
```

## Authentication

ALWAYS use `jwt_or_api_user_key_multi_auth` for new user-facing endpoints. ALWAYS pair `@blueprint.doc(security=jwt_or_api_user_key_security_schemes)` with `@jwt_or_api_user_key_multi_auth.login_required`. NEVER combine `@blueprint.auth_required(...)` with `@multi_auth.login_required` on the same handler.

ALWAYS call `.get_user()` on the same multi-auth object that decorates the endpoint. NEVER use `api_jwt_auth.current_user` or `api_jwt_auth.get_user_token_session()` on a multi-auth endpoint.

Example from codebase:
```python
from src.auth.multi_auth import jwt_or_api_user_key_multi_auth, jwt_or_api_user_key_security_schemes

user = jwt_or_api_user_key_multi_auth.get_user()
```

## User Identity Verification

ALWAYS verify the authenticated user matches the URL `user_id` on user-scoped endpoints. MUST use 403, NEVER 401, for identity mismatch.

Example from codebase:
```python
user = jwt_or_api_user_key_multi_auth.get_user()
if user.user_id != user_id:
    raise_flask_error(403, "Forbidden")
```

## Transaction Management

ALWAYS wrap database operations inside `with db_session.begin():`. ALWAYS call `db_session.add(user)` inside the transaction block after retrieving the user from auth. MUST return `response.ApiResponse` outside the `with` block.

Example from codebase:
```python
user = jwt_or_api_user_key_multi_auth.get_user()
if user.user_id != user_id:
    raise_flask_error(403, "Forbidden")
with db_session.begin():
    db_session.add(user)
    set_saved_opportunity_notification_settings(db_session, user, json_data)
return response.ApiResponse(message="Success")
```

## Response Handling

ALWAYS return `response.ApiResponse(message="Success", data=..., pagination_info=..., warnings=...)`. NEVER manually build response dicts -- let Marshmallow serialize domain objects.

Example from codebase:
```python
return response.ApiResponse(
    message="Success",
    data=agencies,
    pagination_info=pagination_info,
)
```

## Error Handling

ALWAYS use `raise_flask_error(status_code, message, validation_issues=[...])` for errors. ALWAYS log 4xx errors at `logger.info()` level. NEVER use `logger.warning()` for client errors.

Example from codebase:
```python
logger.info(
    "Application cannot be submitted, not currently in progress",
    extra={"application_status": application.application_status},
)
raise_flask_error(403, message, validation_issues=[
    ValidationErrorDetail(
        type=ValidationErrorType.NOT_IN_PROGRESS,
        message="Application cannot be submitted, not currently in progress",
    )
])
```

## Structured Logging

ALWAYS use `add_extra_data_to_current_request_logs({"entity_id": value})` with flat snake_case field names. NEVER use nested/dotted field names. NEVER call `str()` on UUIDs in log extra data. NEVER put variable data in log message strings -- use `extra={}`.

Example from codebase:
```python
add_extra_data_to_current_request_logs({"application_id": application_id, "form_id": form_id})

logger.info(
    "Modified saved opportunity notification setting",
    extra={"organization_id": org_id, "email_enabled": requested_setting.email_enabled},
)
```

## Schema Conventions

ALWAYS define schemas in a separate `*_schemas.py` file. Response schemas MUST extend `AbstractResponseSchema`. ALWAYS mark mandatory fields as `required=True`. NEVER use string booleans (e.g., `"False"`) as example values. ALWAYS name boolean fields with `is_`, `has_`, `can_`, `was_` prefixes. Schema names for `generate_pagination_schema()` MUST be globally unique.

Example from codebase:
```python
class SetUserSavedOpportunityNotificationRequestSchema(Schema):
    organization_id = fields.UUID(
        required=True, allow_none=True,
        metadata={"description": "The ID of the organization"},
    )
    email_enabled = fields.Boolean(
        required=True, metadata={"description": "Whether email notifications are enabled"}
    )
```

## Cross-Field Schema Validation

ALWAYS use `@validates_schema` for validation rules depending on multiple fields. MUST raise `ValidationError` with `MarshmallowErrorContainer` instances.

Example from codebase:
```python
@validates_schema
def validate_category_explanation(self, data: dict, **kwargs: dict) -> None:
    if data.get("category") == OpportunityCategory.OTHER:
        explanation = data.get("category_explanation", "")
        if explanation.strip() == "":
            raise ValidationError([
                MarshmallowErrorContainer(
                    ValidationErrorType.REQUIRED,
                    "Explanation of the category is required when category is 'other'.",
                )
            ])
```

## Soft Delete

ALWAYS implement user-facing deletions as soft deletes (`is_deleted = True`). NEVER use `db_session.delete()` for user-facing operations. ALWAYS filter with `.where(Model.is_deleted.isnot(True))`.

Example from codebase:
```python
saved_opp = db_session.execute(
    select(UserSavedOpportunity).where(
        UserSavedOpportunity.user_id == user_id,
        UserSavedOpportunity.opportunity_id == opportunity_id,
    )
).scalar_one_or_none()
if not saved_opp:
    raise_flask_error(404, "Saved opportunity not found")
saved_opp.is_deleted = True
```

---

## Context Enrichment

When generating significant route code (new endpoint, new blueprint, major refactor), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to ground output in architectural principles
- Call `get_rule_detail("api-services")` for service layer conventions that route handlers delegate to
- Call `get_rule_detail("api-error-handling")` for error response patterns
- Consult **Compound Knowledge** for indexed documentation on route patterns and decorator conventions

## Related Rules

When working on API routes, also consult these related rules:
- **`api-services.mdc`** — service function signatures, `db_session` first param, business logic placement
- **`api-error-handling.mdc`** — `raise_flask_error()`, `ValidationErrorDetail`, status code conventions
- **`api-auth.mdc`** — multi-auth decorator patterns, user retrieval, security scheme registration
- **`api-validation.mdc`** — `ValidationErrorType` enum, schema validation patterns
- **`cross-domain.mdc`** — structured logging, boolean naming, feature flags

## Specialist Validation

When generating or significantly modifying route code:

**For simple changes (< 20 lines, single decorator fix):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new route handler, refactoring auth):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new blueprint, new endpoint with auth, multi-route changes):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate route/service layering and boundary integrity
- `security-sentinel` — validate auth patterns, token handling, identity verification
- `kieran-python-reviewer` — Python-specific quality review
