---
name: authentication-review
description: Review a repository or local codebase with a focus on how authentication and identities are established, verified, propagated, refreshed, and revoked. Use when Codex needs to inspect login flows, session or token handling, identity providers, service-to-service authentication, account provisioning, secret-backed auth, or authentication-related trust boundaries and risks.
---

# Authentication Review

## Overview

Use this skill to build a focused, evidence-based review of authentication and identity handling in a codebase. Trace how principals are identified, how credentials or assertions are verified, how identity is propagated, and where authentication state can be bypassed, confused, or leaked.

Prefer one concrete auth path over a broad but shallow survey. Make uncertainty explicit and label inferred edges clearly.

## Workflow

### 1. Establish the review scope

Choose the smallest meaningful authentication slice before reading everything.

Start with:

- the README and architecture docs
- dependency manifests and framework config
- auth-related entrypoints such as login routes, callback handlers, middleware, guards, passport or oauth setup, JWT/session utilities, API gateways, and service clients

If the codebase is large, choose one of these scopes and say which one you chose:

- one interactive login flow
- one API authentication path
- one service-to-service authentication flow
- one identity provider or auth subsystem

### 2. Discover identity boundaries

Identify the key trust boundaries and identity artifacts:

- inbound credentials: passwords, API keys, bearer tokens, cookies, client certificates, SAML assertions, OIDC codes, OAuth tokens
- identity systems: local user store, SSO provider, IAM service, LDAP, Active Directory, cloud identity, custom auth service
- state carriers: sessions, cookies, JWTs, opaque tokens, headers, mTLS identities, cached auth context
- sensitive dependencies: secret stores, signing keys, token issuers, session stores, MFA providers

Prefer code search over assumptions. Follow concrete routing, middleware registration, callback wiring, and verifier implementations.

### 3. Trace the primary authentication path

Trace data from the first auth input to the established identity and its downstream use. Look for:

- credential receipt and parsing
- validation and canonicalization
- verifier calls and signature or secret checks
- user lookup, account linking, or subject mapping
- token or session creation
- identity propagation to handlers, jobs, or downstream services
- refresh, rotation, logout, revocation, timeout, or re-auth behavior

Capture authn/authz handoff points when they materially affect trust in the flow.

### 4. Review the key functions

For every important function in the chosen flow, review the function instead of only naming it. Capture:

- file path
- function or method name
- role in the auth flow
- direct callers and important callees, if visible
- expected inputs
- produced outputs or identity context
- validation or normalization performed
- state changes or side effects
- failure modes, fallback behavior, and security assumptions

Prioritize functions that:

- accept credentials or bearer material
- verify signatures, hashes, or secrets
- map claims to local identities or roles
- mint, persist, refresh, or revoke sessions or tokens
- skip checks in test, debug, internal, or legacy paths

### 5. Surface authentication findings

Call out issues that materially change how much the auth design can be trusted, especially:

- missing or weak validation at auth boundaries
- insecure password handling or credential storage
- disabled TLS or weak trust of upstream identity assertions
- missing signature, audience, issuer, nonce, state, expiry, or replay checks
- long-lived or unrevocable sessions and tokens
- identity confusion across tenants, providers, or account-linking paths
- auth bypasses in middleware order, default routes, background jobs, or internal APIs
- excessive trust in headers from proxies or upstream services
- hidden privileged paths, bootstrap accounts, or fallback identities
- secret exposure in logs, exceptions, config, or client-visible tokens

Separate confirmed findings from open questions.

### 6. Deliver a concise report

Default to this structure:

1. Scope reviewed
2. High-level authentication flow
3. Step-by-step function review
4. Findings and open questions

## Search Strategy

Use fast repository discovery first:

- `rg --files` for project shape
- `rg` for auth signals such as `login`, `signin`, `callback`, `session`, `cookie`, `jwt`, `passport`, `oauth`, `oidc`, `saml`, `auth`, `guard`, `middleware`, `claims`, `token`, `refresh`, `logout`, `revoke`, `apikey`, `mfa`, `totp`
- framework-specific files such as `routes`, `middleware`, `guards`, `strategies`, `providers`, `security`, `auth`, `sessions`, `filters`, `interceptors`

Prioritize these signals:

- files where external credentials first enter the system
- functions that validate, decode, verify, or exchange identity artifacts
- functions that translate external identity into local user or service context
- code that persists auth state or forwards identity downstream

## Output Rules

Be explicit about evidence quality:

- say `confirmed` when the code directly shows the path
- say `inferred` when the path is likely but not fully wired in the inspected files
- say `not verified` when a dependency, proxy, IdP, or generated layer is missing

Do not present authorization findings as authentication findings unless the handoff is relevant to identity trust.

When presenting the flow, prefer real functions and files over generic labels like "auth layer".

## Example Requests

- Review this repo and explain how users authenticate from login request to established session.
- Inspect this codebase and map how JWT identities are verified and propagated to handlers.
- Review this service with a focus on OAuth or OIDC callback handling and token storage.
- Trace service-to-service authentication in this folder and call out identity or trust-boundary risks.
