---
name: rule-api-auth
description: MANDATORY when editing files matching ["api/src/auth/**/*.py"]. When working on authentication and authorization in api/src/auth/
---

# API Auth Rules

## Module Organization

ALWAYS place each auth mechanism in its own file under `api/src/auth/`. ALWAYS register new auth schemes in `get_app_security_scheme()` in `auth_utils.py`. ALWAYS create a matching test file at `api/tests/src/auth/test_{module_name}.py`.

Example from codebase:
```python
# From api/src/auth/internal_jwt_auth.py
internal_jwt_auth = JwtUserHttpTokenAuth(
    "ApiKey", header="X-SGG-Internal-Token", security_scheme_name="InternalApiJwtAuth"
)
```

## Security Scheme Registration

ALWAYS register every auth scheme in `get_app_security_scheme()` with header name and OpenAPI scheme name.

Example from codebase:
```python
def get_app_security_scheme() -> dict[str, Any]:
    return {
        "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-Auth"},
        "ApiJwtAuth": {"type": "apiKey", "in": "header", "name": "X-SGG-Token"},
        "InternalApiJwtAuth": {"type": "apiKey", "in": "header", "name": "X-SGG-Internal-Token"},
    }
```

## Multi-Auth Composition

ALWAYS define multi-auth compositions as module-level constants in `multi_auth.py` using `MultiHttpTokenAuth`. ALWAYS create a paired `_security_schemes` constant. NEVER create multi-auth objects inside route handlers.

Example from codebase:
```python
jwt_or_key_multi_auth = MultiHttpTokenAuth(api_jwt_auth, api_key_auth)
jwt_or_key_security_schemes = [
    api_jwt_auth.security_scheme_name, api_key_auth.security_scheme_name
]
```

## Multi-Auth Decorators

ALWAYS use `@multi_auth.login_required` and `@blueprint.doc(security=...)` for multi-auth endpoints. NEVER use `@blueprint.auth_required()` with multi-auth -- APIFlask does not support it.

Example from codebase:
```python
@application_blueprint.doc(
    responses=[200, 401, 404], security=jwt_key_or_internal_security_schemes,
)
@jwt_key_or_internal_multi_auth.login_required
@flask_db.with_db_session()
def application_form_get(db_session: db.Session, application_id: UUID, app_form_id: UUID):
```

## User Retrieval

ALWAYS call `.get_user()` on the same multi-auth object that decorates the endpoint. NEVER use `api_jwt_auth.current_user` or `api_jwt_auth.get_user_token_session()` on a multi-auth endpoint.

Example from codebase:
```python
user = jwt_or_api_user_key_multi_auth.get_user()
```

## User Type Discrimination

ALWAYS use `isinstance()` checks on `MultiAuthUser.user` to determine auth type.

Example from codebase:
```python
multi_auth_user = jwt_key_or_internal_multi_auth.get_user()
if isinstance(multi_auth_user.user, UserTokenSession):
    user = multi_auth_user.user.user
else:
    user = None  # Internal token, skip access checks
```

## JWT Token Management

ALWAYS expose `create_jwt_for_{purpose}` and `parse_jwt_for_{purpose}` function pairs. Create functions MUST generate a UUID token_id, build claims, store a DB session record, and return `(token_string, session_record)`.

Example from codebase:
```python
def create_jwt_for_internal_token(
    expires_at: datetime, db_session: db.Session, config: ApiJwtConfig | None = None,
) -> Tuple[str, ShortLivedInternalToken]:
    token_id = uuid.uuid4()
    short_lived_token = ShortLivedInternalToken(
        short_lived_internal_token_id=token_id, expires_at=expires_at, is_valid=True,
    )
    db_session.add(short_lived_token)
    payload = {"sub": str(token_id), "iat": current_time, "aud": config.audience}
    return jwt.encode(payload, config.private_key, algorithm="RS256"), short_lived_token
```

## Query Performance

NEVER use `selectinload("*")` in auth queries. ALWAYS specify exact relationships. NEVER use `noload` -- use `lazyload` instead.

Example from codebase:
```python
.options(selectinload(UserTokenSession.user))
```

## Endpoint Security

NEVER add generic API key auth to endpoints that handle user-specific data. MUST use user JWT or internal JWT only for sensitive endpoints.

Example from codebase:
```python
# Sensitive endpoint excludes generic api_key_auth
jwt_key_or_internal_multi_auth = MultiHttpTokenAuth(api_jwt_auth, internal_jwt_auth)
```

## Multi-Auth Default

ALWAYS default new user-facing endpoints to `jwt_or_api_user_key_multi_auth` unless there is a documented reason not to.

## Logging

ALWAYS use flat snake_case keys in `extra={}` log parameters. Auth-specific fields may use the `auth.` prefix. ALWAYS use `logger.info()` for expected auth failures (401, 403). NEVER use `logger.warning()` for auth failures.

Example from codebase:
```python
logger.info(
    "Internal JWT Authentication Failed for provided token",
    extra={"auth.issue": e.message},
)
```

## Naming Conventions

NEVER name a dataclass `User` in auth modules -- use qualified names like `ApiKeyUser`. NEVER reference infrastructure providers (AWS, Login.gov) in auth class names visible to API consumers.

Example from codebase:
```python
@dataclass
class ApiKeyUser:
    username: str
```

## Auth Testing

ALWAYS use an isolated Flask mini-app fixture with dummy endpoints for auth tests. ALWAYS define reusable auth token fixtures in `api/tests/conftest.py`.

Example from codebase:
```python
@pytest.fixture(scope="module")
def mini_app(monkeypatch_module):
    def stub(app):
        pass
    monkeypatch_module.setattr(app_entry, "register_blueprints", stub)
    monkeypatch_module.setattr(app_entry, "setup_logging", stub)
    mini_app = app_entry.create_app()
    with src.logging.init(__package__):
        yield mini_app
```

---

## Context Enrichment

When generating significant auth code (new auth mechanism, new multi-auth composition, JWT changes), enrich your context:
- Call `get_architecture_section("api")` from the `simpler-grants-context` MCP server to understand auth architectural principles
- Call `get_rule_detail("api-routes")` for how auth decorators integrate into the route decorator stack
- Consult **Compound Knowledge** for indexed documentation on auth patterns, security ADRs, and compliance requirements

## Related Rules

When working on authentication and authorization, also consult these related rules:
- **`api-routes.mdc`** — decorator stack order (auth is position 5), `@blueprint.doc(security=...)` pairing
- **`api-services.mdc`** — `can_access()`/`verify_access()` authorization in service layer
- **`api-error-handling.mdc`** — 401/403 status code conventions, auth failure logging
- **`cross-domain.mdc`** — structured logging with `auth.` prefix, boolean naming

## Specialist Validation

When generating or significantly modifying auth code:

**For simple changes (< 20 lines, adding auth to an existing endpoint):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new multi-auth composition, new JWT function pair):**
Invoke `security-sentinel` to validate auth correctness — improper token handling, missing permission checks, auth bypass risks.

**For complex changes (new auth mechanism, security scheme registration, token management):**
Invoke the following specialists (run in parallel where possible):
- `security-sentinel` — auth correctness, token handling, permission model integrity
- `architecture-strategist` — auth layering, separation between auth and business logic
- `kieran-python-reviewer` — Python-specific quality review for security patterns
