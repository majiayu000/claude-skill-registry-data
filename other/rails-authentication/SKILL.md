---
name: rails-authentication
description: Use when designing, implementing, reviewing, testing, or debugging Rails authentication, credentials, sessions, password recovery, login abuse controls, authentication context propagation, or browser/API identity boundaries.
license: MIT
---

# Rails Authentication Engineering

## Purpose

Treat authentication as a stateful security boundary with explicit identity proof, credential handling, session/token lifecycle, recovery, revocation, abuse controls, observable failure semantics, and deterministic verification.

Authentication answers:

> Who is this requester, and what authenticated state does the application recognize for this request?

Authorization answers a different question:

> May that authenticated actor perform this action on this resource?

Keep those contracts separate.

Core flow:

~~~text
repository mechanism
-> identity/credential boundary
-> authentication attempt
-> authenticated state
-> session/token lifecycle
-> request context propagation
-> protected resource boundary
-> logout/revocation/recovery
-> abuse detection
-> audit/observability
-> deterministic verification
~~~

## Activate when

- adding sign-in, sign-out, or authentication middleware;
- introducing or changing Rails generated authentication;
- reviewing or customizing the Rails authentication system generator output;
- reviewing Devise or another authentication gem;
- changing password hashing or credential storage;
- changing session creation, renewal, rotation, expiry, or invalidation;
- implementing password reset or credential recovery;
- adding remember-me or persistent login behavior;
- adding API tokens, bearer credentials, signed credentials, or service identities;
- changing browser/session authentication versus API authentication;
- supporting multiple devices or active-session management;
- adding account lockout, throttling, or login-abuse controls;
- propagating authenticated identity into jobs, mailers, Action Cable, or service boundaries;
- debugging unexpected login/logout state;
- responding to session compromise or credential compromise;
- reviewing authentication security regressions.

Do not activate merely because an endpoint has an Authorization header if the task is only outbound HTTP authentication; use the relevant integration skill.

## Repository inspection

Before changing authentication, identify:

1. Ruby and Rails versions;
2. the actual authentication mechanism: Rails generator, Devise, custom code, OAuth/OIDC provider, API token layer, or a combination;
3. User/account/identity/session/credential models;
4. password hashing and credential storage;
5. authentication concern/module/middleware;
6. session store and cookie configuration;
7. token/session tables, digests, expiration fields, and indexes;
8. routes/controllers/concerns used for sign-in and sign-out;
9. password reset/recovery models, tokens, mailers, and jobs;
10. remember-me/persistent-login behavior;
11. current-user/request context implementation;
12. browser CSRF policy and same-site cookie settings;
13. API authentication scheme and endpoint classification;
14. login throttling, lockout, device/session limits, or bot controls;
15. authorization/policy layer and protected-resource lookup conventions;
16. background jobs, mailers, Action Cable connections, webhooks, and service boundaries that may need identity context;
17. logging, audit events, metrics, security alerts, and credential filtering;
18. test helpers, request tests, system tests, factories/fixtures, and security regression coverage.

Do not infer authentication behavior from routes alone. Find where identity is actually established and where it is invalidated.

## Decision rules

1. Identify the actual mechanism in use (Rails generator, Devise, custom concern, middleware, token store) before changing anything.
2. Classify the change: mechanism and credential storage, session lifecycle and revocation, recovery and abuse controls, browser versus API credentials and context propagation, or observability/performance/testing.
3. Load the matching reference below before changing behavior; a login, logout, or password change almost always also needs the sessions reference.
4. Hand permission decisions to rails-authorization; authentication establishes identity only.

## Critical invariants

- Authentication and authorization remain separate contracts even when they share request/session plumbing.
- A successful login must not preserve attacker-controlled pre-authentication session state.
- Treat credential material, password reset tokens, session cookies, and bearer tokens as secrets that never enter logs, jobs, events, or telemetry.
- Never serialize passwords, session cookies, bearer tokens, reset tokens, or live authentication objects into jobs/events.
- Reset tokens must not be logged or exposed through analytics, referrers, screenshots, or generic error reporting.
- Define current-session, per-device, and global session revocation semantics, including what a password change revokes.
- Password recovery is a bounded, one-time, expiring protocol with enumeration-safe responses.
- Do not disable CSRF protection broadly to make an API or integration work.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters the authentication mechanism, identity model, credential storage, or authentication states | [references/mechanism-and-credentials.md](references/mechanism-and-credentials.md) | Authentication mechanism boundary; Identity versus authorization; Credential storage; Authentication state machine | `authentication-mechanism-boundary`, `credential-storage-contract` |
| a change alters session establishment, rotation, expiry, revocation, cookies, remember-me, or multi-device sessions | [references/sessions.md](references/sessions.md) | Session lifecycle; Session fixation and rotation; Session revocation; Cookie and browser session contract; Remember-me and persistent login; Multi-device session management | `session-lifecycle-contract`, `session-fixation-rotation`, `session-revocation-contract`, `remember-me-contract` |
| a change alters password reset, login throttling or lockout, re-authentication for sensitive operations, or compromise handling | [references/recovery-and-abuse.md](references/recovery-and-abuse.md) | Password reset and recovery; Login abuse controls; Security-sensitive operations; Compromise response | `password-recovery-contract`, `login-abuse-controls`, `authentication-freshness-boundary` |
| a change adds API/token authentication, propagates the actor to jobs or services, adds authentication hooks, or changes failure responses | [references/browser-api-and-propagation.md](references/browser-api-and-propagation.md) | Browser authentication versus API authentication; Authentication context propagation; Authentication callbacks and hooks; Failure contracts | `browser-api-auth-boundary`, `authentication-context-propagation` |
| adding authentication audit/telemetry, reviewing capacity, or choosing and writing authentication tests | [references/operations-and-testing.md](references/operations-and-testing.md) | Observability and audit; Performance and capacity; Performance and reliability; Testing strategy | none |

## Anti-patterns / failure modes

- authentication treated as authorization;
- duplicate custom authentication beside an existing framework;
- plaintext passwords;
- credentials in logs;
- reset tokens in logs/analytics without controls;
- pre-authentication session reused after login;
- logout that only clears UI state;
- password reset that leaves compromised sessions active without an explicit rationale;
- bearer token with no revocation or expiry model;
- browser session reused as a generic service credential;
- client-supplied tenant used as authoritative identity context;
- account enumeration through inconsistent login/reset responses;
- permanent lockout as the only brute-force control;
- authentication callbacks relied on by bypassable persistence paths;
- live external provider dependencies in every CI authentication test;
- raw session IDs/tokens used as metric labels.

## Reference example

Session creation with the full fixation defense: reset_session on privilege change, constant responses, and status codes that match the outcome.

```ruby
class User < ApplicationRecord
  has_secure_password # password_digest + authenticate
end

class SessionsController < ApplicationController
  def create
    user = User.find_by(email: session_params[:email])

    if user&.authenticate(session_params[:password])
      reset_session                  # rotate the session identifier on login (fixation defense)
      session[:user_id] = user.id
      redirect_to root_url, notice: t(".signed_in")
    else
      flash.now[:alert] = t(".invalid") # identical message for unknown email and bad password
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    reset_session
    redirect_to root_url
  end

  private

  def session_params
    params.require(:session).permit(:email, :password)
  end
end
```

## Agent review checklist

- [ ] Ruby/Rails version resolved
- [ ] actual authentication mechanism identified
- [ ] identity boundary documented
- [ ] authentication/authorization distinction preserved
- [ ] credential hashing/storage inspected
- [ ] session lifecycle documented
- [ ] session fixation defense verified
- [ ] logout/revocation semantics explicit
- [ ] cookie attributes reviewed for browser auth
- [ ] password recovery lifecycle explicit
- [ ] account-enumeration behavior reviewed
- [ ] login/reset abuse controls reviewed
- [ ] remember-me semantics explicit if present
- [ ] browser/API authentication boundaries separated
- [ ] authentication context propagation explicit
- [ ] callback/bypass paths audited
- [ ] sensitive-operation freshness requirements reviewed
- [ ] safe authentication telemetry defined
- [ ] deterministic transition tests exist
- [ ] alternate auth paths/jobs/channels reviewed
- [ ] performance/capacity evidence collected when material
- [ ] compromise/revocation path exists

## Verification

For a new authentication capability:

~~~text
identify mechanism
-> model principal and state transitions
-> inspect credential/session storage
-> define login/logout/recovery contracts
-> define revocation
-> define browser/API boundary
-> add abuse/security controls
-> add transition-focused tests
-> run repository security tooling
-> run full validation
~~~

Do not claim authentication security merely because a framework helper exists. Verify the actual repository path.

## Rails 8 current framework considerations

- Rails 8 includes an authentication system generator that establishes a session-based, password-resettable starting point.
- Generated authentication is scaffolding, not a proof of repository-specific security correctness; reconcile it with the application's session, authorization, recovery, abuse-control, and observability contracts.

## Source foundation

Primary current Rails guidance:

- https://guides.rubyonrails.org/security.html
- https://guides.rubyonrails.org/8_0_release_notes.html
- https://api.rubyonrails.org/classes/ActiveModel/SecurePassword/ClassMethods.html
- https://api.rubyonrails.org/classes/ActionController/RequestForgeryProtection.html

The current Rails Security Guide documents the Rails 8+ authentication generator, password reset flow, has_secure_password, session storage, session fixation, session expiry, CSRF, brute-force/account-hijacking guidance, and secret rotation.

Repository composition:

- `rails-security` skill
- `rails-security-engineering` skill
- `rails-action-controller` skill
- `rails-api-integration` skill
- `rails-observability` skill
- `rails-incident-engineering` skill
- `rails-active-record` skill
- `rails-database-engineering` skill
- `rails-test-engineering` skill

Primary source: Ruby on Rails, Securing Rails Applications. The current guide documents the Rails authentication generator, password reset, has_secure_password, authenticate_by, sessions, session fixation, session expiry, CSRF, brute-force/account-hijacking concerns, credentials, and related security controls.

https://guides.rubyonrails.org/security.html

The repository's reusable authentication patterns operationalize the source material:

- authentication-mechanism-boundary
- credential-storage-contract
- session-lifecycle-contract
- session-fixation-rotation
- session-revocation-contract
- password-recovery-contract
- login-abuse-controls
- remember-me-contract
- browser-api-auth-boundary
- authentication-context-propagation
- authentication-freshness-boundary

Use patterns only when their problem shape exists; they are decision aids rather than mandatory abstractions.

## Rails authentication changes

For authentication changes:
- resolve the Ruby/Rails version and identify the actual mechanism in use before implementation;
- inspect generated Rails authentication, Devise, custom concerns, middleware, session stores, token stores, and alternate authentication paths;
- keep authentication and authorization separate and preserve the repository's authoritative policy boundary;
- authentication and authorization remain separate contracts even when they share request/session plumbing;
- treat credential material, password reset tokens, session cookies, and bearer tokens as secrets that must not enter logs, jobs, events, or telemetry;
- model authentication as explicit state transitions: credential verification, session/token establishment, request context, logout, expiry, and revocation;
- verify session fixation resistance and fresh session state after successful login;
- define current-session, per-device, global revocation, password-change, and compromise semantics where applicable;
- treat password recovery as a bounded one-time/expiring authentication protocol with enumeration-safe responses;
- separate browser session authentication from API/service credentials and verify CSRF semantics rather than disabling protection broadly;
- propagate actor/tenant attribution without serializing live authentication credentials and re-evaluate authorization at asynchronous boundaries;
- require fresh authentication for security-sensitive credential/privilege changes when the product/security contract requires it;
- add deterministic tests for success and rejection paths, expiry, revocation, fixation, recovery replay, and abuse controls;
- run bin/validate and security tooling, and report only observed verification evidence.

## Authentication and authorization boundary

authentication and authorization remain separate concerns: authentication establishes identity and session state; authorization decides permitted actions within that context.
