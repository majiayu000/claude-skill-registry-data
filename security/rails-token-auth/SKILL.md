---
name: rails-token-auth
description: Build secure DB-backed token session auth in Rails — one mechanism for web, Action Cable, and Hotwire Native, with Current attributes and secure-by-default controller concerns. Use when adding login/sessions to a Rails app, when web and native clients need to share authentication, when you need revocable server-side sessions (logout/kick a device) instead of stateless JWTs, or when auditing existing auth for user-enumeration, plaintext tokens, readable cookies, or opt-in-auth mistakes. Provides templates and a security audit.
---

# Rails token-backed session auth

A revocable, DB-backed session model (`AppSession`) that authenticates web **and**
native clients with one mechanism — plus `Current` attributes and secure-by-default
controller concerns. Built without a gem (plain `has_secure_password` +
`authenticate_by`). Full design + rationale: [`references/token-auth-guide.md`](references/token-auth-guide.md).

## When to use

- Adding login/logout to a Rails app and you want it done securely from the start.
- Web + Hotwire Native (and Action Cable) need to share one auth.
- You need **revocable** sessions (real logout, kick a device) — not stateless JWTs.
- Auditing existing auth for the expensive mistakes.

## The shape

| File | Role |
|---|---|
| `AppSession` (`app/models/app_session.rb`) | one row per login; token stored as a **digest** (`has_secure_password :token`) |
| `User::Authentication` (`app/models/user/authentication.rb`) | `has_secure_password`; `authenticate_by` login; mint/verify sessions |
| `Current` (`app/models/current.rb`) | request-scoped `user` / `app_session` / `organization` |
| `Authenticate` (`app/controllers/concerns/authenticate.rb`) | **secure-by-default** `before_action`; `skip_authentication` / `allow_unauthenticated`; `log_in`/`log_out` |
| `SessionsController` | `create_app_session` → `log_in`; `destroy` → `log_out` |

Copy the templates from `templates/` (they're generic, ready to adapt). Add the
migration (`app_sessions`: `user` ref + `token_digest`), the routes
(`login`/`logout`), and `include User::Authentication` + `include Authenticate` in
`ApplicationController`.

## The non-negotiables (why this design)

- **`authenticate_by`**, not `find_by(email:)&.authenticate` — timing-safe, no
  account enumeration.
- **Token hashed at rest** (`has_secure_password :token`) — plaintext token lives
  only in the **encrypted** cookie. A DB leak yields no usable sessions.
- **`cookies.encrypted`** for the session payload — confidential + tamper-proof.
- **Secure-by-default**: global `before_action :authenticate`; public actions opt
  **out** explicitly. A forgotten controller stays locked.
- **Real logout** destroys the `AppSession` row — server-side revocation.

## Audit an app

```bash
scripts/audit_token_auth.sh path/to/rails-app
```

Checks all six properties above and flags: `find_by(email:)+authenticate` (enumeration),
plaintext token storage, token/session in a **plain** cookie, opt-in auth (no global
`before_action`), cookie-only logout, missing `has_secure_password` / password length.
Heuristic grep scan — it names its ceiling; a clean run is not a formal proof, so still
review custom logic. Verified: passes the secure Piazza app, flags a synthetic
insecure one on every check.

## Testing the concerns

The `Authenticate` concern is tested in isolation with a `TestController` +
`draw_test_routes` harness. That harness has a Rails 8 `LazyRouteSet` flake — use the
fixed helper and the detector from the **`rails-8-upgrade`** skill.
