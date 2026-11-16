---
name: hex-test-restapi-auth
description: Use when testing a token verifier, or any other part of a REST service that authenticates its callers — the token-verifier adapter's unit test, the signing-key and token-minting fixtures, the `authenticated_client` factory, the DI override that makes minted tokens verify, the discovered probe that every operation not declared public refuses an anonymous or untrusted caller, and — where the app has them — the role and cross-tenant assertions on an endpoint. Not an endpoint's non-auth half — its success body and advertised error codes (`hex-test-restapi-endpoint`) — and not another capability adapter's test (`hex-test-capability-adapter`). - Adding the auth fixtures to an integration suite, writing a 401 or 403 endpoint test, minting a JWT inside a test, or asserting that a protected route rejects an anonymous caller.
---

# Hex Test — REST API Auth

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`,
the constitution wins.

Every test the auth machinery needs — the verifier's own unit test and the auth half of the integration
suite — and all of it exists **only for an app that declares auth**
(`hex-restapi-auth`). An auth-less app produces none of these files: no verifier to test, no
`tests/helpers/jwt.py`, no `tests/integration/api/conftest.py` — this skill creates it — no
`test_unauthenticated_returns_401.py`, and every endpoint test drives a plain ASGI client.

## When to use vs. neighbours

- Any other capability adapter's test — containerized, HTTP-gateway over a stub transport, or another pure-CPU one → `hex-test-capability-adapter`, which owns the three flavors; the verifier test in `UNIT.md` is its pure-CPU flavor bound to auth.
- The containers, the engine, the rollback `session_factory`, `container` and `real_app` itself →
  `hex-test-integration-setup` (one-shot; both are defined there and every integration file here consumes
  `real_app`).
- A per-endpoint test's non-auth half — success body, advertised error codes, per-resource fixtures →
  `hex-test-restapi-endpoint`.
- The other discovered invariants — OpenAPI error codes, CORS, request-size limit, the construct smoke →
  `hex-test-app-invariants`.
- The route-side dependencies, the verifier and the code sets under test → `hex-restapi-auth`.
- A handler-level authorization rule, tested without HTTP → `hex-test-application-handler`.
- The `Role` enum's own unit test → `hex-test-domain`.
- The testing constitution these rules defer to — fixture placement, the mocking prohibition, speed targets → `test-principles`.

## Template(s) — PyJWT, cryptography, httpx2 over ASGI, FastAPI, pytest

```
tests/
├── helpers/
│   └── jwt.py                                   # sign_token(...)
├── unit/
│   └── infrastructure/jwt/
│       └── test_pyjwt_token_verifier.py         # the verifier adapter, no IO, no fixtures
└── integration/
    └── api/
        ├── conftest.py                          # rsa_keypair, jwt_settings, authenticated_client
        ├── test_unauthenticated_returns_401.py  # the discovered probe
        └── <resource>/
            └── test_<verb>_<noun>.py            # the authenticated endpoint form
```

Two topic files carry the worked binding — **PyJWT, `cryptography`, httpx2 over ASGI, FastAPI and
pytest** — on either side of the unit/integration seam. **Read the one for the half you are writing
before writing it** — only this file is loaded automatically:

- **`UNIT.md`** — the verifier adapter's own test: module-scope keypair, real signatures, one case per
  check the verifier makes.
- **`INTEGRATION.md`** — the signer helper, the api conftest and its authenticated client, the DI
  substitution that makes a minted token verify against the real app, the discovered probe, and the
  authenticated endpoint form.

## Other bindings

- **Opaque token plus an introspection endpoint** (`hex-restapi-auth`, *Other bindings*). What changes:
  the verifier does IO, so rule 1 names the HTTP-gateway flavour of `hex-test-capability-adapter` in
  place of the pure-CPU one; there is no keypair and no signer, so the session-scoped fixture becomes a stub
  introspection server and the "mint a fresh token per call" rule becomes "register a fresh token with
  the stub per call". Rule 10's no-mocking line moves down a level — the verifier still runs for real;
  the *upstream* is the seam the test controls.
- **Gateway- or mTLS-authenticated** (no verifier in the app). The verifier unit test and `UNIT.md`
  disappear entirely; the authenticated client sets the trusted header instead of a bearer credential,
  and the probe asserts that a request arriving *without* it is rejected. That proves the header is
  required, not that only the gateway can send it; unreachability except through the gateway is the
  deployment's (`hex-restapi-auth`).
- **`dependency-injector` as the wiring mechanism.** Only the substitution in the api conftest changes,
  the way `hex-test-integration-setup`'s bullet describes; the fixtures, the probe and every assertion
  are untouched.

## Rules

Consult `test-principles` for the testing constitution.

### The verifier's unit test

1. **The verifier's unit test is `hex-test-capability-adapter`'s pure-CPU flavour** (its rules 2, 3, 14
   and 15) — real keys and real signatures, settings and keys at module scope, no fixtures, and the file
   under `tests/unit/infrastructure/<adapter>/`.
2. **One test per check the verifier makes** (`hex-test-capability-adapter` rule 15) — the signature and
   each claim it validates or requires.
3. **One signer for the whole suite.** The unit test and the integration fixtures mint tokens through
   the same helper, so a change to the claim shape cannot leave them disagreeing.

### The authenticated client

4. **One sanctioned authenticated client, and every test goes through it.** Building a client against
   the real app and attaching a credential header by hand is forbidden in any test file — a hand-rolled
   header is how the claim shape drifts between tests. A client without the fixture's credential is
   allowed only in the probe file — anonymous, or carrying the untrusted credential of rule 15 — and on a
   route with no auth dependency (`hex-test-restapi-endpoint`'s plain client). The client factory lives
   in `tests/integration/api/conftest.py`, never the root `tests/conftest.py`: a root-level app fixture
   makes every unit test pay the infrastructure import chain (`hex-test-integration-setup`).
5. **The client factory is entered as a context manager, never assigned** (`hex-test-restapi-endpoint`
   rule 6).
6. **Each call mints a fresh token — never cached: a reused token is how a test passes on the previous
   test's credential.** Tokens are not reused across tests, calls, or roles; a test that needs two roles
   in one body calls `authenticated_client(...)` twice.
7. **Mint only what the identity type declares; pass everything else via `extra_claims`.** The factory
   bakes in the subject, and the rank where the app has one, and nothing more (`hex-restapi-auth`).
   Anything further this app's identity carries (a tenant id, a display name, …) is the caller's to
   pass via `extra_claims`, pinned only when a test must share it with a fixture row (don't reuse such
   a value across unrelated tests). Never hardcode one app's identity
   model into the factory, and never name a claim key outside the binding files.
8. **The keypair and the verifier settings are session-scoped, the client factory function-scoped**
   (`test-principles`, *Fixture scope rules*): generating an RSA key is the one expensive step here.
9. **The credential the fixture mints is produced the way production's is verified**, off the same
   settings object the fixture built — same algorithm, same issuer, same audience. Substituting a
   cheaper algorithm "for speed" tests a path production does not run, and it is the substitution that
   hides an algorithm-confusion bug rather than catching it.
10. **No mocking of verification.** The verifier in `real_app` validates the token end-to-end against the
    public key these fixtures provided — that *is* the integration contract under test.
11. **`sign_token(...)` is a plain function under `tests/helpers/`** (`test-principles`, *Fixture vs.
    builder*): a test that needs an edge-case token — expired, wrong issuer — imports it directly, and no
    fixture wraps it.

### The discovered probe

12. **Protected is the default; public is declared.** Probe every operation the app serves — walked off
    its resolved routes rather than its published document, since a route left out of the document is
    still served, keyed on the path the document would publish (under FastAPI, `iter_route_contexts`
    filtered to `APIRoute`, keyed on `path_format`), and requested under the path a client must use —
    except those named in the probe file's public set. Never classify by whether the auth dependency is present: a route that forgot
    it looks exactly like a public one, and that classification drops it from the probe instead of
    failing it (`hex-restapi-auth` rule 9). Every input comes off the app and the declaration, so a new
    protected endpoint joins the probe with nothing to edit.
13. **The probe fills every braced segment by one pattern, with a value the router accepts.** A plain
    path parameter reaches the auth dependency whatever the segment holds, because dependencies run
    before path validation, but a typed converter such as `{n:int}` rejects a mismatched value at the
    router, before auth — the UUID-shaped dummy then answers 404, and that route fails the probe until
    its segment gets a value the converter accepts.
14. **An empty discovery is a failure, not a skip** (`test-principles`, *When to parametrize*). The companion
    net test asserts the walk found operations, and that every operation declared public is still one
    the app serves, so the declaration cannot drift from the routes.
15. **Every probed operation also refuses a credential the app does not trust.** The anonymous probe
    never reaches verification — the dependency refuses a missing credential first — and the verifier's
    unit test never reaches a route, so without this case a dependency that checks presence and never
    verifies passes the whole suite. Mint one with `sign_token(...)` under a key the app did not issue,
    send it to each probed operation from the probe file, and assert the 401 and its code. Per-check
    cases stay in the verifier's unit test; this is the one end-to-end case.
16. **Assert the code constant and the challenge scheme, never their literals.** The rejection body is
    asserted against the domain exception's own code attribute, so renaming the code moves both sides
    together; the challenge is asserted on its scheme only. The realm is app-specific and is never
    frozen in an assertion.

### Endpoint-level assertions

17. **A role-gated route is tested from below the bar as well as above it.** A happy path at the
    required rank, and a rejection at a lower one; a route whose gate is never exercised from below is
    a gate nothing proves.
18. **Where a resource is tenant-scoped, a test reads another tenant's row and asserts 404** —
    `hex-application` caller-derived rule 1; 403 would leak existence.

## Inlined typing / import rules

- The verifier unit test adds `cryptography.hazmat.*`, `myapp.domain.auth`, `myapp.domain.exceptions`
  and `myapp.infrastructure.jwt.*`; no `myapp.application.*` and no `myapp.restapi.*` — it drives the
  adapter directly.
- The api conftest adds `httpx2`, `jwt` (PyJWT), `cryptography.hazmat.*` and
  `myapp.infrastructure.jwt`, and `myapp.domain.auth` in a rank app; full annotations on the factory and its `_factory` closure.
- The probe adds `pytest`, `fastapi`, `fastapi.routing`, `httpx2`, `myapp.restapi.main`,
  `myapp.domain.exceptions` for the `UnauthorizedError.code` constant it asserts against, and
  `myapp.infrastructure.jwt` with `tests.helpers.jwt` for the untrusted credential. It never imports `myapp.containers`: `create_app()` builds the real
  composition root itself, and no factory runs at collection time.
- Full annotations on every fixture, helper and test — `-> None` on every test. `python-style` owns
  annotation policy and admits no test carve-out.
- No `from __future__ import annotations`.

## Hard stops

- The app has no auth (every endpoint anonymous) → stop, produce none of these files: the probe's
  module-level imports would fail collection and take `tests/integration/api/` down with it, and the
  `container` of an auth-less app substitutes no verifier settings (`hex-test-integration-setup`).
- Nothing up-tree builds the app on the test's own infrastructure bindings (`real_app` under this
  catalogue's binding) → stop, use `hex-test-integration-setup`; the suite cannot collect without it.
- Asked for a per-endpoint anonymous-caller test (e.g. "test that POST /foos returns 401 unauthenticated") →
  stop, write nothing; every operation not declared public is already probed. Making a route public
  adds it to the declaration.
- A per-resource row factory is added inside the api conftest → stop, use `hex-test-restapi-endpoint`;
  those live in `tests/integration/api/<resource>/conftest.py`.
