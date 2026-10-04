---
name: rule-api-services
description: MANDATORY when editing files matching ["api/src/services/**/*.py"]. When working on API service layer functions in api/src/services/
---

# API Services Rules

## File Organization

ALWAYS place each primary service function in its own file within `api/src/services/{domain}/`. NEVER cram multiple service functions into one file.

Example from codebase:
```python
# From api/src/services/opportunities_grantor_v1/opportunity_update.py
import logging
import src.adapters.db as db
from src.auth.endpoint_access_util import verify_access

logger = logging.getLogger(__name__)

def update_opportunity(
    db_session: db.Session, user: User, opportunity_id: uuid.UUID, opportunity_data: dict
) -> Opportunity:
    ...
```

## Shared Logic Extraction

ALWAYS extract shared logic to `_utils.py` or `service_utils.py` when two or more services need the same code. NEVER duplicate service logic across files.

Example from codebase:
```python
# From api/src/services/organizations_v1/organization_user_utils.py
def validate_organization_user_exists(
    db_session: db.Session, user_id: UUID, organization: Organization
) -> OrganizationUser:
    org_user = db_session.execute(
        select(OrganizationUser)
        .where(OrganizationUser.organization_id == organization.organization_id)
        .where(OrganizationUser.user_id == user_id)
    ).scalar_one_or_none()
    if not org_user:
        raise_flask_error(404, message=f"Could not find User with ID {user_id}")
    return org_user
```

## Function Signatures

ALWAYS pass `db_session: db.Session` as the first parameter. ALWAYS return SQLAlchemy model instances (or tuples of model + warnings). NEVER return raw dicts.

Example from codebase:
```python
def update_opportunity(
    db_session: db.Session, user: User, opportunity_id: uuid.UUID, opportunity_data: dict
) -> Opportunity:
    ...
    return opportunity
```

## Transaction Management

NEVER commit or call `begin()` inside service functions. Route layer MUST manage transaction boundaries. NEVER call `db_session.flush()` followed by a re-query -- objects are already tracked by the session.

Example from codebase:
```python
# Correct: simply return the already-tracked object
def update_opportunity(db_session, user, opportunity_id, data):
    opportunity = get_opportunity_for_grantors(db_session, user, opportunity_id)
    for field, value in data.items():
        setattr(opportunity, field, value)
    return opportunity  # already tracked by the session
```

## Logging

ALWAYS begin every service module with `logger = logging.getLogger(__name__)`. NEVER use custom logger names. NEVER interpolate variable data into log message strings -- ALWAYS use `extra={}`. NEVER log PII (emails, names).

Example from codebase:
```python
import logging
logger = logging.getLogger(__name__)

logger.info(
    "Updated opportunity",
    extra={"opportunity_id": opportunity_id},
)
```

## Error Handling

ALWAYS use `raise_flask_error(status_code, message)` from `src.api.route_utils`. NEVER raise raw exceptions or return error tuples.

Example from codebase:
```python
if not org_user:
    raise_flask_error(404, message=f"Could not find User with ID {user_id}")

if not opportunity.is_draft:
    raise_flask_error(422, message="Only draft opportunities can be updated")
```

## Database Query Patterns

ALWAYS use `select(Model).where(...)` with `.scalar_one_or_none()` for single record lookups. ALWAYS follow with a `raise_flask_error(404, ...)` guard. NEVER use `.first()` which silently ignores duplicates. NEVER use `selectinload("*")` -- ALWAYS specify individual relationships.

Example from codebase:
```python
org_user = db_session.execute(
    select(OrganizationUser)
    .where(OrganizationUser.organization_id == organization.organization_id)
    .where(OrganizationUser.user_id == user_id)
).scalar_one_or_none()
if not org_user:
    raise_flask_error(404, message=f"Could not find User with ID {user_id}")
```

## Authorization

ALWAYS use `can_access()` / `verify_access()` from `src.auth.endpoint_access_util`. NEVER write custom membership validation queries. ALWAYS check authorization after 404 checks, before business logic.

Example from codebase:
```python
# Correct order: fetch -> auth -> business logic
opportunity = get_opportunity_for_grantors(db_session, user, opportunity_id)
verify_access(user, {Privilege.UPDATE_OPPORTUNITY}, opportunity.agency_record)
validate_opportunity_is_draft(opportunity)
```

## Input Validation

ALWAYS define a Pydantic `BaseModel` to validate service input data. ALWAYS use `model_validate()` to parse incoming dicts.

Example from codebase:
```python
class OpportunityCreateRequest(BaseModel):
    opportunity_title: str
    category: OpportunityCategory
    category_explanation: str | None = None

def create_opportunity(db_session: db.Session, user: User, opportunity_data: dict) -> Opportunity:
    request = OpportunityCreateRequest.model_validate(opportunity_data)
```

## PUT Semantics

ALWAYS update all fields on a PUT endpoint. For nullable optional fields, use `load_default=None` so omitted fields clear existing values.

Example from codebase:
```python
for field, value in opportunity_data.items():
    setattr(opportunity, field, value)
```

## API Security

NEVER expose internal URLs (S3, internal services) in API response schemas. NEVER modify shared utility function behavior for a single endpoint -- add checks after calling it or create a separate function.

## Naming Conventions

ALWAYS name boolean fields with `is_`, `has_`, `can_`, `was_` prefixes. ALWAYS match schema field names to DB model field names. NEVER import private (`_`-prefixed) functions from other modules.

Example from codebase:
```python
has_active_opportunity = fields.Nested(
    BoolSearchSchemaBuilder("HasActiveOpportunityFilterV1Schema")
    .with_one_of(example=True)
    .build()
)
```

## Style

NEVER use the walrus operator (`:=`). ALWAYS use explicit variable assignment.

Example from codebase:
```python
config = ACTION_RULE_CONFIG_MAP.get(action, None)
if config is None:
    raise Exception(...)
return config
```

## Validation Warnings

ALWAYS return form validation issues as warnings during save/update. ONLY block (raise errors) during submission.

Example from codebase:
```python
warnings: list[ValidationErrorDetail] = validate_json_schema_for_form(
    application_response, form
)
return application_form, warnings
```

## Testing

ALWAYS use Factory `.build()` for unit tests, `.create()` for integration tests. NEVER use custom test helpers instead of factories.

Example from codebase:
```python
att = ApplicationAttachmentFactory.build()
form = ApplicationFormFactory.build(application_response={"att1": uid})
app = ApplicationFactory.build()
```

---

## Context Enrichment

When generating significant service code (new service function, complex business logic, authorization), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand service layer architectural principles
- Call `get_rule_detail("api-database")` for database query conventions that services use
- Call `get_rule_detail("api-error-handling")` for error patterns in service functions
- Consult **Compound Knowledge** for indexed documentation on service patterns and authorization flows

## Related Rules

When working on API services, also consult these related rules:
- **`api-database.mdc`** — query patterns (`select().where()`), `scalar_one_or_none()`, relationship loading
- **`api-error-handling.mdc`** — `raise_flask_error()`, validation order, error logging
- **`api-auth.mdc`** — `can_access()`/`verify_access()` authorization patterns
- **`api-validation.mdc`** — `ValidationErrorType`, raise vs return pattern for validation
- **`api-tasks.mdc`** — background task patterns that services may trigger
- **`api-workflow.mdc`** — workflow orchestration that services participate in
- **`cross-domain.mdc`** — structured logging, boolean naming, factory patterns
- **Refactor agent** (`.cursor/agents/refactor.md`) — invoke with `/refactor` for service layer restructuring (extract, split, move, consolidate service functions)

## Specialist Validation

When generating or significantly modifying service code:

**For simple changes (< 20 lines, single function modification):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new service function, new authorization logic):**
Invoke `codebase-conventions-reviewer` to validate against project conventions.

**For complex changes (new service module, cross-service logic, complex business rules):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate service boundaries and separation of concerns
- `code-simplicity-reviewer` — check for unnecessary complexity in business logic
- `kieran-python-reviewer` — Python-specific quality review

<!-- Hook enforcement: convention-checker validates no business logic in routes, no db_session in handlers -->
