---
name: rails-security
description: Use when implementing, reviewing, testing, or debugging security-sensitive Ruby/Rails code involving authentication, authorization, sessions, CSRF, XSS, injection, redirects, file access, SSRF, secrets, headers, dependency vulnerabilities, multi-tenancy, webhooks, or security tooling.
license: MIT
---

# Rails Security

## Purpose
Treat security as an application-wide property across HTTP, authentication, authorization, input handling, persistence, rendering, files, secrets, dependencies, and deployment.

Primary source: the Rails Security Guide, which covers authentication, sessions, CSRF, redirects/files, user management, injection, unsafe query generation, security headers, admin security, credentials, and dependency CVEs.

## Activate when
- authentication or authorization changes
- sessions, cookies, passwords, tokens, or reset flows change
- untrusted input reaches SQL, HTML, shell, files, URLs, redirects, headers, or external calls
- uploads/downloads, webhooks, admin actions, or multi-tenant data change
- secrets/configuration or security dependencies change
- reviewing Brakeman/bundler-audit/security findings
- modifying CSP, CORS, HSTS, cookies, or host authorization

For security architecture work (threat modeling, trust-boundary design, cross-tenant isolation review, secrets governance, or abuse-case design), activate `rails-security-engineering` and treat this skill as supporting context.

## Repository inspection
Inspect runtime/version, auth/session strategy, authorization policies, privileged routes, controller input boundaries, views/helpers, raw SQL, command/file/network boundaries, webhooks, secrets, tenant scoping, dependency lockfile, security tooling, tests/CI, and relevant deployment configuration.

Never assume an endpoint is protected because a related controller is protected.

## Threat-model procedure
```text
asset -> trust boundary -> attacker-controlled input -> dangerous sink -> control -> verification -> abuse test -> security tooling -> residual risk
```
Record trusted/untrusted data and the control boundary.

## Authentication
Review password storage/verification, session creation/destruction, reset tokens, account enumeration, brute-force protection, session fixation/hijacking, expiry/revocation, secure cookie attributes, and MFA/token mechanisms where present.

Do not treat authentication as authorization.

Rails 8 includes an authentication generator, but application-specific signup and authorization policy still require application code.

## Authorization
Verify authorization at the resource/action boundary. Audit IDOR/BOLA, tenant scoping, privilege escalation, security-sensitive attribute assignment, admin routes, background jobs, and alternate endpoints.

Do not rely on hidden UI controls as authorization.

## Input and injection safety
Treat params, JSON, headers, cookies, path/query values, uploads, webhooks, and external responses as untrusted.

Prefer parameterized Active Record APIs. Audit raw where/find_by_sql/sanitize_sql, dynamic order clauses, raw SQL execution, command execution, shell interpolation, unsafe redirects, HTML marked safe, and dynamic file paths.

For dynamic identifiers/commands, map external values to fixed internal allowlists rather than interpolating unchecked input.

## XSS and HTML
Review html_safe/raw/safe_join, user-controlled content/attributes, JavaScript interpolation, Turbo Stream content, and JSON embedded into HTML/script contexts.

Do not mark input safe merely because validation passed.

## CSRF
For cookie-authenticated browser applications, verify CSRF protection at state-changing boundaries. Review auth/session endpoints, cookie-authenticated APIs, webhooks, and intentional exemptions.

Do not disable CSRF globally to accommodate an API integration.

## Redirects, files, and SSRF
Review dynamic redirects for open redirects. Review uploads/downloads for path traversal, executable content, size/content controls, authorization, signed URLs, and archive extraction.

Treat user-controlled URLs as SSRF risks; validate scheme, host/IP, redirects, private/link-local destinations, metadata-service access, and timeouts.

## Headers and browser security
Review Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, frame/clickjacking protection, Referrer-Policy, CORS, secure cookies, and host authorization. The Rails Security Guide documents these controls.

## Secrets
Never commit passwords, API keys, tokens, private keys, database credentials, or session secrets. Inspect Rails credentials, environment/CI/container secrets, logs, fixtures, exception payloads, and scripts. Never log credentials or bearer tokens.

## Webhooks and multi-tenancy
Verify webhook authenticity before side effects; review signatures, replay protection, raw-body handling, idempotency, event allowlists, and resource/tenant association.

For multi-tenancy, enforce tenant scope at server/persistence boundaries and audit controllers, jobs, admin actions, APIs, exports, callbacks, and direct model access.

## Dependency security
Treat dependency security as a separate verification dimension.

Brakeman is a static-analysis scanner for Rails security vulnerabilities. It supports confidence levels, multiple machine-readable report formats, configurable checks/ignores, and non-zero exits on warnings/errors by default.

bundler-audit performs patch-level verification of Bundler dependencies against the Ruby Advisory Database. Use the installed version and repository configuration as the compatibility authority.

## Scanner interpretation
For each finding:
1. identify the tool/check and confidence
2. trace data flow to the sink
3. confirm attacker control
4. verify the actual control
5. reproduce or add a focused security test when feasible
6. fix the root cause
7. rerun focused tooling
8. rerun broader security checks
9. document justified false positives/accepted risk

Scanner confidence is prioritization evidence, not proof of exploitability.

## Security tests
Add executable tests for unauthorized access, cross-tenant access, malicious input, unsafe redirects, injection payloads, path traversal, webhook signature failures/replays, privilege escalation, session invalidation, and security-sensitive authorization/serialization.

Prefer boundary tests over implementation-only assertions.

## Safe remediation procedure
```text
finding
-> trust boundary
-> root sink
-> framework-safe control
-> abuse-case regression
-> focused scanner
-> focused tests
-> broader security checks
-> final diff review
```
Do not weaken security tooling or broaden ignores merely to get a green build.

## Anti-patterns / failure modes
- authorization only in views
- authentication mistaken for authorization
- global CSRF disablement
- raw SQL interpolation
- shell interpolation of user input
- unchecked redirects
- unsafe html_safe/raw
- request-derived filesystem paths
- arbitrary outbound URLs
- unverified webhooks
- controller-only tenant scoping
- secrets in source control
- credentials in logs
- uninvestigated scanner suppression
- treating confidence as proof
- validation used as a substitute for an actual security control

## Reference example

A webhook ingress where the signature (timing-safe compare) replaces the CSRF token, and untrusted input never reaches params-style passthrough.

```ruby
class WebhooksController < ApplicationController
  skip_before_action :verify_authenticity_token, only: :create
  before_action :verify_signature, only: :create

  def create
    payload = JSON.parse(request.body.read)
    event = payload.slice("id", "type", "data").to_h  # explicit field allowlist

    IngestWebhookJob.perform_later(event)             # work leaves the request
    head :accepted
  rescue JSON::ParserError
    head :bad_request
  end

  private

  def verify_signature
    expected = Base64.strict_encode64(
      OpenSSL::HMAC.digest("SHA256", webhook_secret, request.raw_post)
    )
    head :unauthorized unless ActiveSupport::SecurityUtils.secure_compare(
      request.headers["X-Signature"].to_s, expected
    )
  end
end
```

## Agent review checklist
- [ ] runtime/version resolved
- [ ] authentication boundary identified
- [ ] authorization boundary identified
- [ ] attacker-controlled inputs identified
- [ ] dangerous sinks identified
- [ ] SQL/query safety reviewed
- [ ] HTML/XSS safety reviewed
- [ ] CSRF semantics reviewed
- [ ] redirects/files/network reviewed
- [ ] secrets reviewed
- [ ] tenant isolation reviewed when applicable
- [ ] headers/CORS/CSP reviewed when applicable
- [ ] webhook authenticity/idempotency reviewed when applicable
- [ ] security tooling checked
- [ ] abuse-case tests added or verified
- [ ] scanner findings investigated
- [ ] final diff reviewed

## Verification
Use repository-configured tooling first. When installed:
```bash
bundle exec brakeman
bundle exec bundler-audit check
```
For machine-readable reports where supported:
```bash
bundle exec brakeman -o tmp/brakeman.json
bundle exec brakeman -o tmp/brakeman.sarif
bundle exec bundler-audit check --format json
```
Never claim a clean security scan unless it actually ran.

## Source foundation
Ruby on Rails Security Guide. Brakeman and bundler-audit documentation/repositories.