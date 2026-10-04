---
name: rule-cross-domain
description: MANDATORY when editing files matching ["**/*"]. Cross-cutting conventions that apply to all code in the repository
---

# Cross-Domain Rules

## Structured Logging
ALWAYS use static log message strings. ALWAYS put dynamic values in `extra={}`. NEVER embed dynamic data in log message strings. NEVER log PII. ALWAYS use flat snake_case keys. NEVER use dotted/nested keys.

Example from codebase:
```python
# From api/src/auth/login.py
logger.info(
    "User login completed successfully",
    extra={"user_id": user.user_id, "auth_method": "jwt"},
)
```

## Log Level Discipline
NEVER use `logger.warning()` for expected client errors (4xx). ALWAYS use `logger.info()` for 4xx responses. Reserve `warning` for actual operational concerns that should trigger alerts.

Example from codebase:
```python
# From api/src/auth/auth_utils.py
logger.info(
    "Authentication failed: invalid token",
    extra={"auth_method": "jwt", "status_code": 401},
)
```

## Factory Pattern for Test Data
ALWAYS use factory `.build()` when no database/persistence is needed. Use `.create()` only when records must exist in the database. On the frontend, use centralized typed fixtures in `fixtures.ts`.

Example from codebase:
```python
# From api/tests/src/services/applications/test_update.py
app = ApplicationFactory.build()
app.application_attachments = attachments or []
app.application_forms = forms or []
```

## Structured Error Responses
ALWAYS use `raise_flask_error(status_code, message, validation_issues=[...])` for API error responses. Each `ValidationErrorDetail` MUST include a `type` from `ValidationErrorType` and a human-readable message. NEVER use raw Flask `abort()`.

Example from codebase:
```python
# From api/src/services/applications/validation.py
raise_flask_error(
    422, "Validation failed",
    validation_issues=[
        ValidationErrorDetail(
            type=ValidationErrorType.REQUIRED,
            message="'name' is a required property",
            field="$.name",
        )
    ],
)
```

## Thin Handlers / Service Layer Separation
ALWAYS keep route handlers thin. Business logic, validation, and DB queries MUST live in service functions under `src/services/<domain>/`. Route handlers contain only: logging, auth check, `db_session.begin()` block, and response return.

Example from codebase:
```python
# From api/src/api/routes/applications.py
@app.route("/v1/applications/<app_id>/forms/<form_id>", methods=["PUT"])
@login_required
def update_application_form(app_id, form_id):
    logger.info("PUT application form", extra={"application_id": app_id})
    with db_session.begin():
        result = update_application_form_service(db_session, app_id, form_id, request.json)
    return response.ApiResponse(result)
```

## Boolean Naming Convention
ALWAYS name boolean fields and parameters with question-form prefixes: `is_`, `has_`, `can_`, `was_`. NEVER use ambiguous names like `active` or `enabled`.

Example from codebase:
```python
# From api/src/db/models/agency.py
has_active_opportunity = Column(Boolean, default=False)
is_test_agency = Column(Boolean, default=False)
is_deleted = Column(Boolean, default=False)
```

## Accessibility Testing
ALWAYS include a `jest-axe` accessibility scan (`toHaveNoViolations()`) for every new frontend component. NEVER ship a component test suite without an accessibility test.

Example from codebase:
```tsx
// From frontend/tests/components/InviteLegacyUsersButton.test.tsx
import { axe } from "jest-axe";

it("should not have accessibility violations", async () => {
  const { container } = render(
    <InviteLegacyUsersButton organizationId="org-123" />,
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Feature Flags via Environment Variables / SSM
ALWAYS gate new capabilities behind feature flags. API flags use `ENABLE_{FEATURE}_ENDPOINTS` in Terraform. Frontend flags use `FEATURE_{NAME}_OFF` backed by SSM. Flags MUST be set in all environments before merge.

Example from codebase:
```hcl
# From infra/frontend/app-config/env-config/environment_variables.tf
FEATURE_USER_ADMIN_OFF = {
  manage_method     = "manual"
  secret_store_name = "/${var.app_name}/${var.environment}/feature-user-admin-off"
},
```

## No Wildcard Eager Loading
NEVER use `selectinload("*")`. ALWAYS specify exact relationships to load.

Example from codebase:
```python
# From api/src/services/opportunities/get_opportunity.py
query = select(Opportunity).options(
    selectinload(Opportunity.current_opportunity_summary),
    selectinload(Opportunity.agency),
)
```

## SSM Parameters Must Exist Before Merge
ALWAYS create SSM parameters in all environments (dev, staging, training, prod) before merging a PR that references them. Even placeholder values are acceptable. NEVER merge a PR that adds new secret references without confirming SSM parameters exist.

---

## Context Enrichment

When generating code that spans multiple domains or touches cross-cutting concerns, enrich your context:
- Call `get_conventions_summary()` from the `simpler-grants-context` MCP server for the full cross-cutting project standards
- Call `get_rules_for_file("[target file path]")` to load domain-specific rules in addition to this cross-domain rule
- Call `list_rules()` to see all available rules when working on cross-cutting changes
- Consult **Compound Knowledge** for indexed documentation on project-wide conventions, ADRs, and historical patterns

## Related Rules

This rule applies to ALL files. When it activates alongside a domain-specific rule, both sets of directives apply. The domain-specific rule takes precedence for domain-specific patterns; this rule governs cross-cutting concerns:
- **`api-routes.mdc`**, **`api-services.mdc`**, **`api-database.mdc`**, **`api-tasks.mdc`**, **`api-adapters.mdc`**, **`api-workflow.mdc`**, **`api-search.mdc`** — Python API domain rules
- **`frontend-components.mdc`**, **`frontend-hooks.mdc`**, **`frontend-services.mdc`**, **`frontend-app-pages.mdc`** — TypeScript frontend domain rules
- **`frontend-tests.mdc`**, **`frontend-e2e-tests.mdc`** — frontend testing rules
- **`accessibility.mdc`** — WCAG 2.1 AA / Section 508 compliance (legally mandated, activates on all frontend files)
- **`infra.mdc`**, **`ci-cd.mdc`** — infrastructure and CI/CD domain rules

**Debugging:** When tracing errors across domain boundaries, invoke the debugging agent (or use `/debug`) — it loads context from all relevant domains and traces the full error path.

**Refactoring:** When restructuring code across multiple domains or consolidating duplicated patterns, invoke the refactor agent (or use `/refactor`) — it maps the full blast radius, executes across all affected files, and validates against all applicable conventions.

## Specialist Validation

When working on cross-cutting changes that affect multiple domains:

**For simple changes (single-domain, < 20 lines):**
No specialist invocation needed — the domain-specific rule is sufficient.

**For moderate changes (touching 2+ domains, refactoring shared patterns):**
Invoke `codebase-conventions-reviewer` to validate against all applicable conventions.

**For complex changes (new cross-cutting convention, multi-domain refactor, feature flag rollout):**
Invoke the following specialists (run in parallel where possible):
- `architecture-strategist` — validate cross-cutting consistency and architectural alignment
- `pattern-recognition-specialist` — detect duplication and pattern violations across domains
- `codebase-conventions-reviewer` — validate against all applicable domain rules

<!-- Hook enforcement: convention-checker validates structured logging, no PII; import-validator validates import patterns -->
