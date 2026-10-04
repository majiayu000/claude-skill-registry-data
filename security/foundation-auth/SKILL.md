---
name: foundation-auth
description: Implement authentication and authorization for an AICP-domain backend (or sister fleet project) — user/identity model, credential storage, token/session machinery, middleware, RBAC, audit logging. Loads when an architecture calls for protected routes / multi-user identity / API authentication, or when the operator says "add auth", "implement login", "protect these endpoints".
argument-hint: [auth-type: token|session|oauth — default token (JWT)]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# foundation-auth

The foundation skill that authors authentication + authorization machinery. Foundation skills lay structural groundwork that feature skills then build on. AICP itself currently runs single-operator (no auth in `aicp/`); this skill is invoked mostly for sister projects (openfleet agent server, future Mission Control) that need real auth.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Architecture mandates auth**: a `docs/architecture.md` Security section names "JWT auth", "session cookies", "OAuth provider X", or any authenticated route — and no auth implementation exists yet.
- **Direct verb**: operator says "add auth", "implement login", "protect these endpoints", "set up authentication", "we need RBAC".
- **Multi-user transition**: a project moves from single-operator to multi-user — anything calling itself an API now needs callers identified.
- **Compliance trigger**: a security audit or `infra-security` scan flagged "no authentication on endpoint X".

Do NOT load when:

- AICP-internal CLI/MCP work — AICP's MCP server is intentionally local-only, no auth needed (per CLAUDE.md "User is in control" — single operator).
- The auth already exists and you're tuning it — load `infra-security` for an audit, or `feature-iterate` for refinement.
- The request is just "rotate the JWT secret" — load `config-secrets` instead; that's a secret-lifecycle operation, not an auth implementation.
- Adding API keys to call an external service (OpenRouter, Anthropic) — that's `config-secrets`, not auth.

## Operations

This skill has 4 named operations. Execute in order. Each has its own Quality bar.

### Operation 1: Read architecture and pick the auth shape

**Trigger**: skill loaded; operator confirmed auth is the actual ask (not config-secrets or infra-security).

**Process**:

1. Read [docs/architecture.md](../../../docs/architecture.md) Security section. Extract: who calls the system (humans, services, both), what's protected, threat model.
2. Pick the auth shape based on `$ARGUMENTS` and the architecture:
   - **token** (default — JWT): stateless, fits API + microservice patterns. Best for service-to-service and API clients.
   - **session**: server-side session store (cookies). Best for browser apps with same-origin clients.
   - **oauth**: delegate to an external IdP (Google, GitHub, etc.). Best when you don't want to own credential management.
3. State the shape choice + rationale to the operator and wait for "go". This is reversible cheaply; over-thinking blocks shipping.
4. List the components you'll author: user model, credential store, token issuer, validation middleware, RBAC layer (if needed), audit log hooks.

**Quality bar (Operation 1 done when)**:

- [ ] Architecture Security section read; threat model and protected-route list captured.
- [ ] Auth shape chosen with one-line rationale; operator approved.
- [ ] Component list named (user model / credential store / token issuer / middleware / RBAC / audit).
- [ ] No FORBIDDEN paths per the implement stage in [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml).

### Operation 2: Author the credential + identity layer

**Trigger**: Operation 1 shape approved.

**Process**:

1. Author the user/identity model. For Python+SQLAlchemy projects: a User table with id, email/username, password_hash, created_at, role(s). For document stores: equivalent shape.
2. Implement password hashing with **bcrypt or argon2** — never plaintext, never SHA-only, never MD5. Use a vetted library (`passlib`, `bcrypt`, `argon2-cffi`).
3. Author the registration + login handlers:
   - Registration: validate email format, hash password, store, return success without echoing the credential.
   - Login: lookup, constant-time compare hashed password, issue token/session, return.
4. Implement rate-limiting on registration + login (in-memory token bucket is fine for v1; Redis-backed for production).
5. Add audit-log calls at each auth event: registration, login success, login failure, token issuance, token refresh, logout.

**Quality bar (Operation 2 done when)**:

- [ ] User model has: stable id, identifier (email/username), `password_hash` (NOT `password`), timestamps, role field (even if "user" by default).
- [ ] Password hashing uses bcrypt or argon2 (verify import); cost factor is at least default-strong.
- [ ] Registration + login handlers exist, are wired to a route, and reject malformed input.
- [ ] Rate-limit middleware applies to registration + login (verifiable: 11th rapid call fails).
- [ ] Audit log emits an entry per auth event (verify in test by capturing logs).

### Operation 3: Author the token + middleware layer

**Trigger**: Operation 2 credential layer landed.

**Process**:

1. Implement the token issuer per the chosen shape:
   - **JWT**: HS256 with secret from env (NEVER hardcoded), `exp` claim ≤ 1 hour for access tokens, refresh token mechanism for longer sessions.
   - **session**: server-side store (Redis or DB), session ID in HttpOnly + Secure + SameSite=Lax cookie, configurable TTL.
   - **oauth**: delegate to provider library (authlib, oauthlib); store provider refresh tokens server-side.
2. Implement the validation middleware: extract token/session ID, validate, attach principal (user) to the request context. Reject with 401 on missing/invalid; 403 on insufficient role.
3. Implement RBAC if architecture calls for roles:
   - Roles in the user model.
   - Decorator/middleware function `requires_role("admin")` that checks principal.role ⊇ required.
   - Default-deny for routes without explicit role declaration.
4. Configuration via env vars (per AICP convention — `.env` gitignored): `<APP>_JWT_SECRET`, `<APP>_TOKEN_TTL_SECONDS`, `<APP>_ALLOWED_ORIGINS`. Document each in `.env.example`.

**Quality bar (Operation 3 done when)**:

- [ ] Token issuer reads its secret from env (verify by `grep -r "JWT_SECRET\|SESSION_SECRET" src/ tools/` — no literals).
- [ ] Token TTL is configurable + enforced (test: expired token rejected with 401).
- [ ] Middleware attaches principal to request and rejects 401/403 correctly (test for both).
- [ ] RBAC (if applicable): default-deny verified — a route without a `requires_role` decorator must NOT be accessible to unauthenticated requests.
- [ ] `.env.example` lists every auth-related env var with a comment.

### Operation 4: Test + document the auth flow

**Trigger**: Operations 2 + 3 landed.

**Process**:

1. Author tests covering each auth event:
   - Registration: success, duplicate email rejection, malformed input rejection, rate-limit kick.
   - Login: success, wrong password, unknown user, rate-limit kick.
   - Token validation: valid → pass, expired → 401, tampered → 401, missing → 401.
   - RBAC: correct role → 200, insufficient role → 403, no role declared on route → 401 (default-deny).
   - Audit log: each event produces an entry (snapshot test).
2. Run the project's standard test gate (for AICP-domain: `pytest tests/ -x --tb=short`); fix until green.
3. Document the auth flow:
   - Architecture: update `docs/architecture.md` Security section with the chosen shape and rationale.
   - README: a brief "Authentication" section pointing at how to register / log in / use a token.
   - For API projects: an OpenAPI security scheme entry.
4. Add the threat-model assumptions to a doc comment in the auth module — anyone reading the code understands what's protected and what isn't.

**Quality bar (Operation 4 done when)**:

- [ ] Tests cover: registration, login, token-validation (valid + expired + tampered + missing), RBAC (passing + failing + default-deny), audit log.
- [ ] `pytest -x` exits 0; no skipped auth tests without explicit reason.
- [ ] `docs/architecture.md` Security section updated.
- [ ] README has Authentication section with example flow.
- [ ] Threat model documented in code comments at the auth module's entry point.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Plaintext password leak via logs

Logging the request body or raw form data — passwords end up in server logs. Logs ship to monitoring; passwords leak.

**The rule**: configure the logging layer to redact `password`, `password_confirm`, `current_password`, `new_password` keys before any log call. Test it: post `password=secret123` and grep the log file for `secret123` — must not appear.

### Gotcha 2: JWT secret in source control

Hardcoded `JWT_SECRET = "changeme123"` or committed `.env` with the real secret. Once in git history, it's compromised forever — even after a rotation, anyone with old commits can mint valid tokens against the old secret.

**The rule**: secrets ONLY in `.env` (gitignored). Default for missing secret is FAIL CLOSED — refuse to start, don't fall back to a hardcoded value. Verify by `git log -p | grep "JWT_SECRET\s*=\s*['\"]"` returns nothing.

### Gotcha 3: Token expiry too generous

`exp: 30 days` on access tokens. A leaked token grants 30 days of access. Refresh-token mechanisms exist precisely so the access token can be short-lived.

**The rule**: access token TTL ≤ 1 hour. If you need longer-lived access without re-authentication, implement refresh tokens (longer TTL, revocable server-side). Don't extend the access TTL.

### Gotcha 4: RBAC default-allow

Routes that don't declare a required role are accessible to anyone authenticated (or worse, anyone). The convention "if not declared, anyone authenticated" looks safe but is the wrong default — any new route added without a `requires_role` becomes a backdoor.

**The rule**: default-deny. Routes without explicit `requires_role` should be inaccessible (or accessible only to a sentinel "no-role-required" decorator). Make the decision visible per-route.

### Gotcha 5: Forgetting timing attacks on credential lookup

Login that returns "user not found" in 5ms but "wrong password" in 50ms (because the latter ran the bcrypt verify). Attackers learn which usernames exist.

**The rule**: always run the password verify even when the user doesn't exist — against a stable dummy hash. Total response time is constant. Return the same generic "invalid credentials" message in both cases.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

## Domain context

This skill operates in the **backend-ai-platform-python** domain (or sibling fleet projects in the same domain). See [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml) for implement-stage gate commands (ruff + pytest -x), allowed paths, and integration requirements.

**AICP-specific scope note**: AICP itself has no auth in `aicp/` — it's single-operator local-only. This skill is invoked mostly for fleet agents (`aicp/agent/server.py` already uses HMAC `AICP_AGENT_SECRET` — that's the existing pattern), Mission Control (planned), or any external-facing API derived from AICP.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| config-secrets | Add/rotate the JWT secret or any cred | Secret lifecycle; foundation-auth IMPLEMENTS auth |
| infra-security | Audit existing auth posture | Reviews; foundation-auth authors |
| foundation-database | Set up the user table backing store | Database setup; foundation-auth uses it |
| foundation-config | Wire env vars for auth (token TTL, etc.) | Config plumbing; foundation-auth declares what to wire |
| feature-implement | Generic feature implementation | This skill is specifically auth — narrower scope |
