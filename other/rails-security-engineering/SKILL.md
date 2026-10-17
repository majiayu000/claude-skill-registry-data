---
name: rails-security-engineering
description: Use when security work requires architecture-level threat modeling, trust-boundary analysis, abuse-case prioritization, tenant isolation, secret governance, supply-chain review, or security regression strategy across a Rails system.
license: MIT
---

# Security Engineering & Threat Modeling

## Purpose

Treat security as a system property with explicit assets, trust boundaries, attacker capabilities, abuse cases, controls, verification, and residual risk.

Compose this skill with `rails-security`, `rails-authentication`, `rails-api-integration`, `rails-distributed-systems`, `rails-event-driven-messaging`, `rails-reliability-engineering`, `rails-database-engineering`, and `rails-test-engineering`.

Core flow:

identify assets
-> map trust boundaries
-> identify actors/capabilities
-> enumerate abuse cases
-> locate dangerous data/control flows
-> select preventive/detective/recovery controls
-> verify at the owning boundary
-> add adversarial regression coverage
-> verify tooling
-> document residual risk

## Activate when

- performing a threat model or security architecture review;
- introducing a new trust boundary, service, provider, admin surface, or tenant boundary;
- changing authorization across resources or roles;
- reviewing cross-tenant isolation;
- designing secrets/configuration governance;
- assessing SSRF or arbitrary outbound network behavior;
- reviewing file, command, browser, serialization, or deserialization boundaries;
- reviewing dependencies, plugins, build systems, or software supply chain;
- designing security abuse cases or regression suites;
- triaging security findings across multiple components;
- deciding where a security control should live;
- reviewing defense in depth for a security-sensitive workflow.

Do not activate merely because a security-sensitive line changed. Use `rails-security` for narrow Rails control implementation.

For direct secure-coding work on authentication, sessions, untrusted input, or scanner findings, `rails-security` is the lighter entry point; activate this skill for architecture-level security work.

## Repository inspection

Inspect:

1. application/domain assets and data sensitivity;
2. users, roles, service identities, and privileged actors;
3. routes/controllers/jobs/consumers/admin interfaces;
4. authentication/session/token mechanisms;
5. authorization policies and object-level access checks;
6. tenant scoping and database constraints;
7. outbound network/file/command/browser sinks;
8. webhooks and external integrations;
9. secret/configuration stores and deployment surfaces;
10. dependency manifests, lockfiles, CI/build scripts;
11. logging/error/reporting paths;
12. security headers/CORS/CSRF/host controls;
13. Brakeman, dependency-audit, secret-scanning, and CI configuration;
14. security tests and abuse-case coverage;
15. incident history and known accepted risks when available.

Never assume a control exists because the framework supports it. Verify where the repository actually applies it.

## Threat-model procedure

For every material boundary capture:

`asset -> actor -> trust boundary -> input -> transformation -> sink -> control -> verification -> residual risk`

Identify:

- assets: credentials, personal data, tenant data, money/value, privileged actions, operational secrets;
- actors: anonymous users, authenticated users, admins, service accounts, compromised dependencies, hostile providers;
- trust transitions: browser/server, user/service, service/service, tenant/tenant, application/database, application/provider, build/runtime;
- capabilities: read, create, modify, delete, execute, impersonate, publish, administer.

Prioritize by impact and exploitability rather than by number of findings.

Use the `threat-model` pattern.

## Trust boundaries

A trust boundary exists when the trust level, authority, ownership, or validation responsibility changes.

Common boundaries:

- browser -> Rails;
- API client -> Rails;
- tenant A -> tenant B;
- user -> admin operation;
- Rails -> database;
- Rails -> provider;
- webhook provider -> Rails;
- producer -> broker -> consumer;
- application -> filesystem/OS;
- source repository -> CI/build -> artifact/runtime.

Place validation, authentication, authorization, and encoding controls at the boundary that owns the security decision.

Do not rely on a downstream caller to repeat an authorization decision that only the resource owner can make.

Use the `trust-boundary` pattern.

## Authorization architecture

Authentication establishes identity. Authorization decides whether the actor may perform the specific action on the specific resource.

Do not treat authentication as authorization.

For material authorization domains define:

- actor/subject;
- resource;
- action;
- tenant/account scope;
- ownership/delegation;
- privileged roles;
- policy source;
- audit requirement.

Prefer a single authoritative policy boundary with database constraints for invariants that must survive concurrent writers.

Review alternate paths:

- controllers;
- JSON/API endpoints;
- background jobs;
- webhooks;
- admin actions;
- exports/downloads;
- service objects callable outside controllers.

Use the `authorization-matrix` pattern.

## Tenant isolation

Tenant isolation is a security invariant, not a convenience filter.

Define:

- tenant identity source;
- authoritative scope;
- object ownership;
- cross-tenant access rules;
- privileged cross-tenant operations;
- job/message propagation of tenant context;
- database enforcement;
- export/reporting boundaries;
- cache-key isolation.

Prefer database-level constraints/scoping invariants where practical and verify all alternate execution paths.

Never trust a client-supplied tenant ID when server-side identity already determines tenant scope.

Use the `tenant-isolation-review` pattern.

## Secrets and credentials

Classify secrets by:

- owner;
- storage;
- lifetime;
- rotation;
- access scope;
- exposure surfaces;
- revocation path.

Inspect:

- Rails credentials;
- environment/container/CI secrets;
- provider tokens;
- database credentials;
- signing keys;
- webhook secrets;
- logs/errors/telemetry;
- fixtures and development scripts.

Do not place secrets in source, durable message payloads, URL query parameters, or default logs.

Use the `secret-management-boundary` pattern.

## SSRF and arbitrary outbound access

For user-controlled or provider-derived URLs, model:

`input -> parser -> redirect -> DNS/IP -> connection -> response`

Verify:

- allowed scheme;
- host allowlist/denylist;
- DNS resolution behavior;
- private/link-local/loopback destinations;
- metadata-service addresses;
- redirect validation;
- connection/read timeouts;
- response size limits;
- credential forwarding rules;
- audit/logging.

A URL validator that checks only the original hostname is not necessarily sufficient when DNS rebinding or redirects are possible.

Use the `ssrf-outbound-boundary` pattern.

## Supply-chain security

Review:

- Gemfile.lock/package lockfiles where applicable;
- dependency source registries;
- native extensions;
- build scripts;
- CI workflows;
- release artifacts;
- dependency update automation;
- maintainer/publisher trust;
- transitive dependencies;
- checksum/signature controls when available.

Separate:

- known vulnerable dependency;
- malicious/compromised package risk;
- unsafe build/release configuration;
- unreviewed capability expansion.

Do not treat a clean vulnerability database as proof that the supply chain is safe.

Use the `dependency-supply-chain` pattern.

## Security regression engineering

Every important security finding should become an executable regression where feasible.

The regression should exercise the attacker-controlled boundary and prove the security property, such as:

- unauthorized access denied;
- cross-tenant record inaccessible;
- forged webhook rejected;
- malicious URL cannot reach forbidden network;
- dangerous query input remains parameterized;
- privileged action requires correct role;
- secret value does not appear in logs/errors;
- old vulnerable dependency/control path cannot reappear.

Use the narrowest security test that proves the contract, then run repository security tooling.

Use the `security-regression` pattern.

## Defense in depth

For high-impact assets, avoid relying on one fragile control.

Examples:

`tenant identity -> application authorization -> database constraint -> audit`

`provider signature -> event identity -> durable deduplication -> idempotent side effect`

`user URL -> scheme/host validation -> private-IP protection -> redirect controls -> timeout`

Defense in depth does not justify redundant controls without ownership. Each layer should cover a distinct failure mode.

## Detection and response

Security controls should create enough evidence to investigate abuse without exposing secrets.

Capture safe context:

- actor/service identity;
- resource/tenant identifier where permitted;
- action;
- policy decision;
- failure reason class;
- request/correlation ID;
- source/provider;
- security control triggered.

Do not log credentials, bearer tokens, signed bodies, or unnecessary sensitive payloads.

## Residual risk and exceptions

For every intentionally unmitigated risk state:

- asset affected;
- threat;
- reason control is absent;
- compensating controls;
- owner;
- expiry/review date;
- evidence supporting acceptance.

Do not encode accepted-risk decisions as permanent scanner ignores without ownership and review.

## Verification

Verify at four levels:

1. architecture: trust boundaries/assets/actors;
2. behavior: adversarial request/job/message tests;
3. tooling: static/dependency/secret scanners configured by repository;
4. operations: audit/detection/revocation/recovery path.

A passing scanner is evidence for the checks it performs, not a complete security assessment.

## Reference example

An abuse case as a regression test: cross-tenant reachability is probed through every known path, asserting 404 so existence is not leaked.

```ruby
class TenantIsolationAbuseTest < ActionDispatch::IntegrationTest
  test "tenant A cannot reach tenant B statements through any known path" do
    sign_in users(:tenant_a_admin)
    foreign = statements(:tenant_b)

    [
      "/billing/statements/#{foreign.id}",
      "/api/v1/statements/#{foreign.id}",
      "/billing/statements/#{foreign.id}.json"
    ].each do |path|
      get path
      assert_response :not_found, path  # 404: no existence oracle, no 403 tell
    end
  end
end

# Abuse cases are written from the attacker's goal, not from the happy path,
# and they run in CI so a new route cannot silently reopen the boundary.
```

## Agent review checklist

- [ ] assets identified
- [ ] actors/capabilities identified
- [ ] trust boundaries mapped
- [ ] authorization matrix explicit
- [ ] tenant isolation explicit where applicable
- [ ] dangerous sinks identified
- [ ] secrets/storage/rotation reviewed
- [ ] SSRF/outbound network boundary reviewed
- [ ] dependency/build supply chain reviewed
- [ ] defense-in-depth gaps identified
- [ ] abuse-case regression exists
- [ ] security tooling verified
- [ ] detection/audit context safe
- [ ] residual risk documented
- [ ] no broad scanner suppression introduced

## Anti-patterns

- treating authentication as authorization;
- controller-only tenant filtering;
- trusting client-supplied tenant scope;
- security validation duplicated in unrelated places with no owner;
- relying on UI visibility for authorization;
- URL allowlists that ignore redirects/DNS/private addresses;
- secrets in code, durable payloads, URLs, or logs;
- clean vulnerability scans treated as complete security assurance;
- broad scanner ignores hiding unknown findings;
- security tests asserting implementation instead of the security property;
- one control assumed to protect a high-impact asset from every path;
- accepted risks with no owner or review date.

## Source foundation

- Rails Security Guide: https://guides.rubyonrails.org/security.html
- Rails Guides: https://guides.rubyonrails.org/
- Brakeman: https://brakemanscanner.org/
- Bundler Audit: https://github.com/rubysec/bundler-audit
- Repository skills: rails-security, rails-authentication, rails-api-integration, rails-distributed-systems, rails-event-driven-messaging, rails-database-engineering, rails-test-engineering

## Security engineering and threat-model changes

For architecture-level security changes:
- identify protected assets, actors, attacker capabilities, and trust boundaries before selecting controls;
- distinguish authentication, authorization, tenant isolation, input validation, and output encoding responsibilities;
- map alternate execution paths including controllers, jobs, events, webhooks, admin actions, exports, and direct service entry points;
- treat client, provider, broker, file, URL, build, and dependency inputs as untrusted until the owning boundary verifies them;
- place authorization at the resource/action boundary and verify cross-tenant access cannot bypass it;
- govern secrets by owner, storage, scope, rotation, revocation, and exposure surface;
- constrain arbitrary outbound network access against SSRF, redirect, DNS, private-network, credential-forwarding, and resource-exhaustion risks;
- review dependency, CI, build, and release surfaces as security boundaries;
- turn concrete vulnerabilities into deterministic abuse-case regression tests;
- use repository-configured security scanners as evidence, not as the complete security assessment;
- record accepted residual risk with ownership and review criteria rather than permanent broad scanner suppressions.
