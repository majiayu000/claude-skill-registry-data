---
name: litestar-security
description: "Auto-activate for litestar_security, SecurityPlugin, SecurityConfig, SecureController, CurrentUser, Principal, SecurityContext, or requires_role/scope/tenant/capability/assurance. Not for basic Litestar Guards."
---

# Litestar Security

`litestar-security` 0.6.0 is a declarative authentication and authorization framework for Litestar. It provides credential slots and mechanisms, unified session management, local accounts, MFA, WebAuthn passkeys, OAuth/OIDC, API keys, workload JWTs, and browser hardening.

Two separate axes, wired through two separate Litestar keywords:

- **Authentication** — *who is calling* — is a policy on `auth=` (or `opt={"auth": ...}`).
- **Authorization** — *what they may do* — is a predicate in Litestar's native `guards=[...]`.

Do not conflate them: the policy helpers (`public`, `required`, `any_of`, `all_of`, `at_least`, `optional`, `exclude`, `mechanism`) take **mechanism names**, while the guard combinators (`requires_any_of`, `requires_all_of`, `requires_at_least`, `requires_one_of`) take **predicates**.

## Code Style Rules

- **Declare authentication with `SecureController`, `PublicController`, or `auth=`.** Subclass `SecureController` (`auth: ClassVar[AuthenticationPolicy] = required(...)`) or `PublicController` for controllers, pass `auth=` on individual routes, and use `opt={"auth": ...}` on routers or third-party controllers. The nearest native owner wins.
- **Keep authorization in `guards=[...]`.** Litestar's `security=` parameter is reserved for the OpenAPI requirements projected from `auth`.
- **Inject the user with `CurrentUser[T]`.** Annotate `current_user: CurrentUser[UserType]` (already a `NamedDependency[UserType]` alias); it rejects anonymous and userless service principals. `principal` and `security_context` stay typed on public routes too via `NamedDependency`.
- **Authorize from the snapshot.** Guards read the `AuthorizationSnapshot` produced by the configured `authorization_resolver`. Never query the database inside a guard.
- **Compose predicates with `requires_*`.** Use `requires_any_of`, `requires_all_of`, `requires_at_least`, `requires_one_of` for predicate composition.
- **Exclude other plugins' routes by path.** Static assets and dashboards carry no `auth` and compile to implicit `required()`, so they answer `401` until listed in `SecurityConfig(exclude=[...])`. Inspect routes with `litestar security routes`.
- **Secure WebSockets with connect tokens.** Browsers cannot set handshake headers; mint a short-lived token over authenticated HTTP via `WebSocketConnectTokenService` or `WebSocketConnectTokenIssuer`.
- **Load protector keys from a secret store.** MFA and OAuth protectors need application-owned 32-byte AES-256-GCM keys, never source literals.

## Quick Reference

### Plugin Registration

```python
from litestar import Litestar, get
from litestar.di import NamedDependency

from litestar_security import (
    SecurityConfig,
    SecurityContext,
    SecurityPlugin,
    public,
)


@get("/", auth=public(), sync_to_thread=False)
def index(security_context: NamedDependency[SecurityContext]) -> dict[str, bool]:
    return {"authenticated": bool(security_context.evidence)}


app = Litestar(
    route_handlers=[index],
    plugins=[SecurityPlugin(SecurityConfig())],
)
```

With mechanisms configured and no inherited policy, routes default to implicit `required()`. With no mechanisms at all they are public.

### Authentication Policy

```python
from typing import ClassVar

from litestar import get
from litestar_security import (
    AuthenticationPolicy,
    PublicController,
    SecureController,
    all_of,
    any_of,
    at_least,
    public,
    required,
)

policy_default = required()
policy_session = required("session")
policy_either = any_of("session", "api-key")
policy_both = all_of("api-key", "service-jwt")
policy_threshold = at_least(2, "session", "api-key", "service-jwt")
policy_public = public()
```

Apply policy on controllers via `SecureController` / `PublicController` and on routes via `auth=`:

```python
class HealthController(PublicController):
    path = "/health"

    @get("/")
    async def check(self) -> dict[str, str]:
        return {"status": "ok"}


class AccountController(SecureController):
    path = "/accounts"
    auth: ClassVar[AuthenticationPolicy] = required("session")
```

Use `opt={"auth": ...}` only on `Router`, `Litestar`, or third-party controllers that cannot subclass `SecureController`.

### Authorization Guards

```python
from typing import ClassVar

from litestar import get
from litestar_security import (
    AuthenticationPolicy,
    SecureController,
    required,
    requires_any_of,
    requires_role,
    requires_scope,
)


class ReportsController(SecureController):
    path = "/reports"
    auth: ClassVar[AuthenticationPolicy] = required("session")
    guards = [requires_role("analyst")]

    @get("/", guards=[requires_any_of(requires_scope("read:all"), requires_scope("read:reports"))])
    async def list_reports(self) -> list[dict[str, str]]:
        return []
```

### Reserved Dependency Names

The plugin registers these; do not shadow them.

| Key | Type | Use |
| --- | --- | --- |
| `principal` | `NamedDependency[Principal[User]]` | Stable envelope identity plus the active user model |
| `security_context` | `NamedDependency[SecurityContext]` | Active session, evidence, snapshot, and restrictions |
| `current_user` | `CurrentUser[User]` | Narrowing shortcut (`NamedDependency[User]`); rejects anonymous and service principals |
| `csp_nonce` | `NamedDependency[str]` | Per-request CSP nonce when `SecurityHeadersConfig.use_csp_nonce=True` |
| `websocket_connect_tokens` | `NamedDependency[WebSocketConnectTokenIssuer]` | Route-aware WebSocket connect-token issuer |

### Status Code Contract

| Outcome | Status |
| --- | --- |
| Authentication failure | `401` |
| Guard denial | `403` |
| Verification unavailable (fails closed) | `503` |

<workflow>

## Workflow

### Step 1: Install the capabilities in use

Core install covers JWT/JWKS validation, API keys, IAP, and OIDC token verification. Use `[argon2,mfa]` for `LocalAuth`; add `[passkeys]` or `[oauth]` only when needed, or use `[all]`.

### Step 2: Choose providers

Pick where identity is established — local accounts, OAuth/OIDC, Google IAP, API keys, or workload JWTs. Adding a provider makes its mechanism available; route policy decides where it is accepted. See [Providers](references/providers.md).

### Step 3: Implement the authorization resolver

Implement an async `resolve(principal)` method that returns an `AuthorizationSnapshot` of granted roles, scopes, capabilities, tenant roles, and tenant IDs. Return `InvalidCredentials` or `VerificationUnavailable` for expected denial or dependency failure. It runs once per request, so guards must not perform I/O.

```python
from litestar_security import AuthorizationSnapshot, Principal


class AppAuthorizationResolver:
    async def resolve(self, principal: Principal[User]) -> AuthorizationSnapshot:
        if not principal.is_authenticated:
            return AuthorizationSnapshot()
        user = principal.require_user()
        return AuthorizationSnapshot(
            roles=frozenset(user.roles),
            scopes=frozenset(user.scopes),
        )
```

### Step 4: Register the plugin and set default policy

Scope an application-wide `opt={"auth": ...}` default to the router that owns the application's own routes, so policy-less third-party routes keep the implicit default rather than counting as declared.

### Step 5: Exclude routes the application did not write

Add `SecurityConfig(exclude=[...])` patterns for static files, queue dashboards, and schema browsers. See [Composition](references/composition.md).

### Step 6: Harden the deployment

Apply `SecurityHeadersConfig.hardened()`, supply every CSP directive explicitly, and move protector keys and peppers into secret management. See [Hardening](references/hardening.md).

</workflow>

<guardrails>

## Guardrails

- **Do not pass predicates to `any_of` / `all_of` / `at_least`.** Those compose authentication mechanisms. Use `requires_any_of`, `requires_all_of`, `requires_at_least`, or `requires_one_of` for predicates.
- **Do not shadow reserved dependencies.** Avoid naming providers `principal`, `security_context`, `current_user`, `csp_nonce`, or `websocket_connect_tokens`.
- **Do not perform I/O in predicates.** Guards evaluate synchronously against the snapshot; put database checks in the `authorization_resolver`.
- **Do not use `guards=` for authentication or `auth=` for authorization.** They compile to different things — runtime admission plus OpenAPI projection versus permission checks.
- **Do not put a layer-level policy above excluded routes.** A route that both declares `auth` and matches an exclusion pattern is rejected at startup.
- **Do not put bearer credentials in WebSocket query strings.** Use a connect token or an HttpOnly cookie.
- **Do not enable `MFAConfig(require_at_login=True)` before enrolling factors.** Unenrolled accounts lock themselves out; use `require_at_login="enrolled"` to enforce login MFA only for accounts that have enrolled a factor.
- **Do not hard-code protector keys.** Load exact 32-byte material from a KMS or secret store, and retain the previous key through rotation.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] `SecurityPlugin` is registered in application `plugins`.
- [ ] Every route's authentication policy is declared via `auth=` or inherited `opt={"auth": ...}`.
- [ ] Authorization uses `guards=[...]` with predicates, never the mechanism combinators.
- [ ] A custom `authorization_resolver` implements async `resolve()` and returns an `AuthorizationSnapshot`, `InvalidCredentials`, or `VerificationUnavailable`.
- [ ] No handler or guard queries the database to perform authorization checks.
- [ ] Handler injection uses `current_user: CurrentUser[UserType]` (or `NamedDependency[Principal[UserType]]` / `NamedDependency[SecurityContext]`).
- [ ] Routes registered by other plugins are excluded by anchored path pattern or given an explicit policy.
- [ ] WebSockets use connect tokens verified against the registered handler name and exact Origin.
- [ ] Exception handlers cover `401`, `403`, and `503` outcomes.
- [ ] Protector keys, peppers, and session secrets come from secret management.

</validation>

<example>

## Example

```python
from dataclasses import dataclass, field
from typing import ClassVar

from litestar import Litestar, get
from litestar_security import (
    AuthenticationPolicy,
    AuthorizationSnapshot,
    CurrentUser,
    Principal,
    PublicController,
    SecureController,
    SecurityConfig,
    SecurityHeadersConfig,
    SecurityPlugin,
    required,
    requires_any_of,
    requires_role,
    requires_scope,
)


@dataclass
class User:
    id: str
    username: str
    roles: list[str] = field(default_factory=list)
    scopes: list[str] = field(default_factory=list)


class AppAuthorizationResolver:
    async def resolve(self, principal: Principal[User]) -> AuthorizationSnapshot:
        if not principal.is_authenticated:
            return AuthorizationSnapshot()
        user = principal.require_user()
        return AuthorizationSnapshot(
            roles=frozenset(user.roles),
            scopes=frozenset(user.scopes),
        )


class SystemController(PublicController):
    path = "/health"

    @get("/")
    async def health(self) -> dict[str, str]:
        return {"status": "ok"}


class OrdersController(SecureController):
    path = "/api/orders"
    auth: ClassVar[AuthenticationPolicy] = required("session")

    @get(
        "/",
        guards=[requires_any_of(requires_scope("read:all"), requires_scope("read:orders"))],
    )
    async def list_orders(self, current_user: CurrentUser[User]) -> dict[str, str]:
        return {"owner": current_user.username}

    @get("/admin", guards=[requires_role("admin")])
    async def admin_orders(self) -> list[dict[str, str]]:
        return []


security_config = SecurityConfig[User](
    authorization_resolver=AppAuthorizationResolver(),
    headers=SecurityHeadersConfig.hardened(),
    exclude=["^/static"],
)

app = Litestar(
    route_handlers=[SystemController, OrdersController],
    plugins=[SecurityPlugin(config=security_config)],
)
```

</example>

## References Index

- **[Authentication](references/authentication.md)** — policy helpers, ownership layers, controller base classes, CSRF interaction.
- **[Authorization](references/authorization.md)** — snapshots, resolvers, predicates, combinators, tenant checks, assurance.
- **[Providers](references/providers.md)** — local accounts, OAuth/OIDC, IAP, API keys, workload JWTs, transaction protectors.
- **[Composition](references/composition.md)** — excluding routes other plugins register, and the patterns per plugin.
- **[Hardening](references/hardening.md)** — CSP, security headers, secrets, key rotation, MFA operational rules.
- **[WebSockets](references/websockets.md)** — connect tokens, close codes, snapshot refresh, revocation.

## Cross-References

- **[litestar](../litestar/SKILL.md)** — Litestar app setup and plugin list.
- **[Litestar auth & guards](../litestar/references/auth-and-guards.md)** — native guards and low-level ASGI connection context.
- **[Litestar exceptions](../litestar/references/exceptions.md)** — mapping `401` / `403` / `503` to Problem Details responses.

## Official References

- <https://github.com/cofin/litestar-security>
- <https://github.com/cofin/litestar-security/tree/v0.6.0/docs>
- <https://github.com/cofin/litestar-security/tree/v0.6.0/examples>

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
