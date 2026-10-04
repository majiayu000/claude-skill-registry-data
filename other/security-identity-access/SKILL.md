---
name: security-identity-access
description: Companion overlay used only with `security` when explicitly security-focused review, threat model, or implementation centers on authentication, sessions, recovery, MFA or passkey lifecycle, federation or account linking, identity-provider or recovery callbacks, invitations, or tenant authorization. Never use alone or for routine login, signup, user-model, RBAC, or backend work without a security objective.
---

# Security Identity Access

Use this companion only with `security`. If `security` is not applicable, do
not apply this overlay.

## Composition Contract

`security` remains primary and owns investigation authority, attacker and trust
boundary analysis, evidence outcomes, severity and confidence, remediation,
validation, and report shape.

This companion owns identity-specific state and transition modeling,
authentication and session invariants, recovery and federation risks, tenant
authorization, and routing to selectively needed identity detail. Matching
backend and language skills still own ordinary implementation mechanics.

## Model The Identity Boundary

Map the repository's actual objects and names. Do not invent states merely to
fit this model.

| Object | State or binding to establish |
|---|---|
| principal or account | lifecycle state and usable identifiers |
| authenticator or factor | pending, bound, active, replaced, lost, or revoked |
| transaction or capability | purpose, subject, initiating context, expiry, and unused or consumed state when one-time |
| session or token | principal, authentication event, issue time, expiry, rotation, and revocation |
| membership or grant | principal, tenant, role or capability, resource scope, and lifecycle state |
| external identity | trusted issuer or security domain plus its stable subject identifier |

For every security-relevant transition, establish as applicable:

- who or what may initiate it
- which authenticated, verified, or recent state it requires
- which principal, purpose, transaction, client, tenant, and destination it is
  bound to
- whether authorization is re-evaluated at use time
- whether consumption and state mutation are atomic
- which sessions, credentials, grants, caches, or notifications it affects

Use these compact invariants:

```text
accepted state-changing transition =
  valid actor or proof and authorized transition
  and required valid transaction, event, assertion, or capability bindings
  and atomic or otherwise replay-safe authoritative mutation

effective authority =
  principal, applicable grant or membership, and policy state
  are authoritative or sufficiently current for the accepted revocation window
  and target action/resource is within server-authorized scope
```

Client-selected identity, tenant, role, redirect, or resource values may select
a candidate context. They do not grant authority.

## Workflow

1. Confirm that `security` is primary and identify its active mode. Stop using
   this companion if the task is only routine auth implementation or generic
   access-control design.
2. Inspect the actual identity objects, entrypoints, storage, middleware,
   provider configuration, and deployment boundaries before forming findings.
3. Model the relevant states, bindings, transitions, and invalidation effects.
4. Read only the references that match the boundary under review:
   - [Sessions](references/sessions.md) for session, cookie, token, refresh,
     logout, or revocation behavior
   - [Recovery, invitations, and factor lifecycle](references/recovery-and-factors.md)
     for verification, recovery, enrollment, replacement, backup-code, or
     trusted-device flows
   - [Federation, account linking, and passkeys](references/federation-and-passkeys.md)
     for OAuth, OIDC, SAML, SSO, external identities, or WebAuthn
   - [Tenant authorization](references/tenant-authorization.md) for membership,
     role, organization switching, resource scope, or cross-tenant paths
5. Trace a concrete abuse path from an attacker-reachable or
   attacker-influenceable condition, or stale identity state, through an
   accepted transition or authorization decision to an impacted account,
   credential, privilege, or tenant asset.
6. Check framework, provider, and repository protections before reporting.
   Verify version- or protocol-dependent conclusions against current official
   specifications and the deployed implementation.
7. Fix or report through `security`. Add the violated identity invariant, state
   transition, relevant binding, and invalidation effect to its normal evidence
   and impact analysis.

## Critical Correctness Rules

- An absolute callback URL is only syntactically absolute; it is not thereby
  trusted. Require the applicable protocol's registered-target and
  transaction-binding rules, or trusted server-side construction for
  non-protocol callbacks.
- Protect authenticator material according to how verification uses it.
  One-way-verifiable backup codes, reversibly needed OTP seeds, passkey public
  credentials, and trusted-device tokens do not share one storage rule.
- Keep authentication, account linking, membership, and authorization as
  separate decisions. A valid external identity or session does not establish
  local tenant authority.
- Re-evaluate authorization for privilege changes, tenant switches,
  invitations, and sensitive resource access against authoritative or
  sufficiently current server-controlled state with an explicit acceptable
  revocation window.
- Treat enrollment, replacement, removal, recovery, and trusted-device changes
  as privileged identity transitions, not merely profile updates.

## False-Positive Guards

- Do not flag client-selected tenant context when a mandatory trusted server
  layer re-derives and enforces applicable authoritative or sufficiently
  current grants and resource scope on every sensitive path.
- Do not require every authorization check to appear in the endpoint when a
  demonstrably mandatory lower layer enforces the same invariant.
- Do not report persistent sessions, federated login, syncable passkeys, or
  redirects as vulnerabilities by category alone. Demonstrate a broken
  binding, transition, invalidation rule, or attacker-reachable trust failure.
- Do not import assurance levels, time limits, algorithms, or provider
  assumptions from a standard without showing that the deployment adopts that
  profile.
