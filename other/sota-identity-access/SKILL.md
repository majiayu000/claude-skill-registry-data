---
name: sota-identity-access
description: >-
  State-of-the-art identity and access management engineering (2026) for
  BUILDING/configuring identity infrastructure AND AUDITING it — federation,
  IdPs, authorization models, the joiner-mover-leaver lifecycle,
  privileged/break-glass access, workload identity, MFA/passkeys, and
  assurance levels; audits cover orphaned accounts, over-privileged roles,
  weak MFA, long-lived tokens, and SAML misconfig. Owns identity
  INFRASTRUCTURE and access-management DESIGN, not app-level login/session/JWT
  mechanics (sota-code-security owns those). Trigger keywords: IAM, IdP, OIDC,
  OAuth 2.1, PKCE, DPoP, PAR, RAR, JAR, FAPI, SAML,
  SCIM, provisioning, deprovisioning, RBAC, ABAC, ReBAC, Zanzibar, OpenFGA,
  SpiceDB, OPA, Cedar, Kanidm, Keycloak, Authentik, Zitadel, Entra, Okta, SSO,
  single logout, MFA, passkey, FIDO2, WebAuthn, step-up, conditional access,
  CAEP, PAM, break-glass, just-in-time, SPIFFE, access review, NIST 800-63,
  IAL, AAL, FAL, Active Directory, Kerberos, Kerberoasting, ADCS, RBCD,
  gMSA, dMSA, LAPS, krbtgt.
---

# SOTA Identity & Access

## Purpose

Own the identity **infrastructure** and access-management **design** of a system:
the federation protocols themselves, the IdP that issues and validates tokens, the
authorization model that decides who may do what, the lifecycle that creates and
destroys access, privileged access, and machine identity. Two modes. In **BUILD**
mode you stand up or configure this infrastructure correctly by default. In **AUDIT**
mode you assess an existing identity estate against the same rules and report
severity-rated findings. The rules files are the single source of truth for both.

Boundary discipline — this skill does **not** re-teach what siblings own:
- **App-level authn ceremony** (password storage/argon2id, session cookie flags,
  WebAuthn ceremony, JWT *signature* validation mechanics at one RP): that is
  **sota-code-security** rules/02 (sessions and JWT: rules/17). This skill owns the protocol and the IdP side.
- **App-level object/function authz** (IDOR/BOLA in one service's handlers): that is
  **sota-code-security** rules/03. This skill owns the authorization *model* and the
  *policy engine* that the app calls.
- **Secret storage, OIDC-federation mechanics for workloads, JWT `kid` rotation as a
  credential operation**: **sota-secrets-management** rules/01 and rules/05.

Concurrent siblings to invoke alongside: **sota-network-security** (mTLS, ZTNA,
identity-aware proxy), **sota-kubernetes** (K8s RBAC, OIDC to the API server, SA
tokens), **sota-detection-engineering** (identity-based detections, impossible-travel,
auth anomaly), **sota-privacy-compliance** (consent, DSAR, audit evidence).

The hierarchy of preference, always: **(1)** no standing credential — short-lived,
federated, sender-constrained tokens; **(2)** standing identity with strong
phishing-resistant authentication and just-in-time elevation; **(3)** long-lived
secret-authenticated client with rotation and audit; **(4)** anything static and
broadly-scoped is a defect to be justified or removed.

## BUILD mode

Use when standing up or configuring any identity component.

1. **Pick the protocol, not the vibe.** Interactive user login → OIDC Authorization
   Code + PKCE (the only sanctioned interactive flow). Service-to-service → client
   credentials with `private_key_jwt`/mTLS, or workload identity federation. High
   assurance → FAPI 2.0. Legacy SAML only where a relying party requires it. Read
   `rules/01-federation-protocols.md` before configuring any client.
2. **Treat the IdP as a tier-0 asset.** HA, backups of the identity store, restricted
   admin plane, signing-key rotation, break-glass design. `rules/02-idp-operations.md`.
3. **Design the authorization model deliberately.** RBAC vs ABAC vs ReBAC is an
   architecture decision; model roles/relationships and write policy as code with a
   test matrix. `rules/03-authorization-models.md`.
4. **Wire the lifecycle before launch.** Joiner-mover-leaver, SCIM provisioning AND
   deprovisioning, access reviews. Deprovisioning is the #1 IAM failure — design it
   first. `rules/04-lifecycle-provisioning.md`.
5. **Separate and time-box privilege.** Admin-account separation, JIT elevation,
   logged-and-alerted break-glass, machine identity. `rules/05-privileged-workload.md`.
6. **Make authentication phishing-resistant and adaptive.** Passkeys/FIDO2 at the IdP,
   step-up, CAEP/SSF for continuous evaluation. `rules/06-mfa-federation-assurance.md`.
7. **Self-review against each file's Audit checklist** before declaring done.

## AUDIT mode

Use when assessing an existing identity estate.

### Sweep procedure

1. **Enumerate the IdP config**: clients/relying parties and their redirect URIs,
   client-auth methods, token lifetimes, grant types enabled, signing keys + rotation,
   session/SLO config, MFA policy, federation/brokering trusts. Pull from the IdP API
   or config export, not screenshots.
2. **Enumerate the population**: every human and service account, its
   authentication strength, last-login, group/role assignments, and owner. Cross
   against the HR/source-of-truth roster to find orphans.
3. **Sweep by rules file**: 01 (protocol/token misconfig), 02 (IdP hardening),
   03 (over-privilege/SoD), 04 (orphaned/dormant/no-reviews — usually the most
   findings), 05 (break-glass/standing admin/static workload creds), 06 (weak MFA).
4. **Verify, don't assume**: a wildcard redirect URI, an account that logged in 400
   days ago, a role granting `*` — confirm each against the live config/logs before
   reporting. Never authenticate as a discovered account or trigger break-glass
   without explicit permission.

### Severity conventions

| Severity | Definition | Examples |
|---|---|---|
| **Critical** | Identity-layer flaw enabling full account/tenant takeover or auth bypass for many principals | Wildcard/loose `redirect_uri` enabling token theft; IdP accepts unsigned SAML assertions or `alg:none`; standing super-admin with no MFA; signing key never rotated and leaked; OIDC issued to an open-redirect client |
| **High** | Compromise of a single privileged identity, or systemic over-grant | Orphaned admin account still active post-termination; break-glass account with a static shared password and no alerting; role granting estate-wide `*`; long-lived non-rotating refresh tokens; SSO with no Single Logout on credential change |
| **Medium** | Weak lifecycle/assurance on a contained scope | No access reviews/recertification; dormant non-priv accounts; phishable MFA (SMS/TOTP) where phishing-resistant is feasible; `client_secret_basic` where `private_key_jwt`/mTLS is supported; missing SoD on sensitive role pairs |
| **Low** | Hygiene and defense-in-depth gaps | No idle session timeout; consent screen not informative; no dormant-account detection job; PAR/DPoP available but unused for a low-risk client; missing `azp` validation on a single-audience token |
| **Info** | Observations and accepted risk | Legacy SAML RP documented and owner-acknowledged; planned migration off SMS MFA tracked |

### Finding format

Report every finding as one line, ordered Critical → Info:

```
file:line | rule | severity | effort (trivial/small/medium/large) | fix
```

Where `file:line` anchors to the offending config (e.g. `keycloak/realm.json:412`,
`policies/rbac.rego:88`, or `idp://clients/web-app#redirect_uris` for live config with
no file). `rule` is the rules-file section (e.g. `01 §redirect-uri`). Group repeated
instances of one weakness into a single finding listing all locations. End the audit
with: counts per severity, the orphaned/dormant account tally, and the top 3 systemic
fixes (almost always: deprovisioning automation, MFA hardening, least-privilege roles).

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-federation-protocols.md](rules/01-federation-protocols.md) | Configuring or auditing OIDC/OAuth flows, choosing a grant type, validating tokens at the RP, PKCE/PAR/RAR/JAR/DPoP, OAuth 2.1 & FAPI 2.0, SAML and its attack classes (XSW, comment injection, unsigned assertions), SAML signing/encryption certificates and metadata exchange, assertion minimisation, SCIM as a protocol, legacy protocols (WS-Fed, OpenID 2.0, non-MFA sign-in paths, protocol-translation gateways), redirect-URI matching, token-validation pitfalls |
| [rules/02-idp-operations.md](rules/02-idp-operations.md) | Running a self-hosted IdP (Kanidm/Keycloak/Authentik/Zitadel), client/RP registration discipline, client-auth ladder, token lifetimes + refresh rotation + reuse detection, signing-key (`kid`) rotation, revoking signed tokens (Token Status List, online checks, revoked-token reuse), session management + Single Logout + logout-token validation, consent, adopted SaaS tenants, multi-IdP brokering, IdP as tier-0 (HA/backup, trust-domain separation, hosted IdP/MFA as a supplier) |
| [rules/03-authorization-models.md](rules/03-authorization-models.md) | Choosing/designing RBAC vs ABAC vs ReBAC, role modeling and role explosion, the group→role mapping discipline, least privilege + segregation of duties, policy-as-code engines (OPA/Rego, Cedar, OpenFGA, SpiceDB), policy testing, birthright vs requested access |
| [rules/04-lifecycle-provisioning.md](rules/04-lifecycle-provisioning.md) | Designing or auditing joiner-mover-leaver, SCIM-driven provisioning/deprovisioning, the orphaned-account problem, access reviews/recertification, just-in-time provisioning, dormant-account detection, self-registration and service-account login, AI-agent inventory and non-human decommissioning |
| [rules/05-privileged-workload.md](rules/05-privileged-workload.md) | Admin-account separation, break-glass design (logged/time-bound/alerted, the Kanidm `recover-account` pattern), JIT/just-enough elevation, session recording, vaulting; machine/workload identity (SPIFFE/SPIRE, workload identity federation, mTLS identity, short-lived over static) |
| [rules/06-mfa-federation-assurance.md](rules/06-mfa-federation-assurance.md) | Phishing-resistant MFA (FIDO2/passkeys/WebAuthn at the IdP), step-up/adaptive/conditional access, CAEP/SSF continuous evaluation, push-bombing/MFA-fatigue defenses, B2B/B2C/social-login and account-linking risks, identity proofing and NIST 800-63-4 IAL/AAL/FAL, authenticator lifecycle (revocation, re-proofing, expiry, biometrics), SMS OTP as a restricted authenticator, client-certificate and edge/IoT device authentication |
| [rules/07-active-directory.md](rules/07-active-directory.md) | Hardening on-prem Active Directory / Kerberos / ADCS: Enterprise Access Model & tiering (ESAE/red-forest retired), delegation risks (unconstrained/constrained/RBCD), Kerberoasting/AS-REP + gMSA/dMSA & AES-only service accounts, SPN hygiene, machine-account quota, NTLM relay (SMB/LDAP signing + channel binding), ADCS ESC classes + template/enrollment-agent hardening + strong cert mapping (KB5014754), LAPS/Protected Users/Credential Guard/auth silos, krbtgt rotation, hybrid Entra sync boundary (PHS/PTA). Detection lives in sota-detection-engineering rules/07 |

## Top-10 non-negotiables

Violations are findings regardless of context; in BUILD mode they are never shortcuts.

1. **Authorization Code + PKCE is the only sanctioned interactive flow.** Implicit and
   ROPC/password grant are dead and disabled at the IdP. (rules/01)
2. **Exact redirect-URI matching, no wildcards, no scheme/host/path looseness.** A loose
   `redirect_uri` is a token-exfiltration primitive. (rules/01)
3. **At the RP, pin algorithms and validate `iss`, `aud`, `exp`, and `nonce`; reject
   unsigned tokens and `alg:none`.** SAML RPs reject unsigned assertions and validate
   the signature over the whole response with anti-XSW canonicalization. (rules/01)
4. **The IdP is a tier-0 asset**: HA, backed-up identity store, restricted admin plane,
   rotating signing keys with `kid` overlap, no standing super-admin without
   phishing-resistant MFA. (rules/02)
5. **Refresh tokens rotate with reuse detection, or are sender-constrained (DPoP/mTLS);
   access tokens are short-lived.** No non-expiring tokens. (rules/01, rules/02)
6. **Authorization is least-privilege by an explicit model with policy-as-code and a
   tested allow/deny matrix.** No role grants estate-wide `*`; segregation of duties
   enforced on sensitive pairs. (rules/03)
7. **Group→role mapping is explicit and default-deny**: a user with no matching mapping
   gets *no* access, never a silent default role. (rules/03)
8. **Deprovisioning is automated and prompt** — a leaver loses all access within the
   agreed SLA, source-of-truth driven via SCIM; access is recertified on a schedule.
   Deprovisioning is the #1 IAM failure. (rules/04)
9. **Privileged access is separated, just-in-time, and time-boxed; break-glass is
   logged, alerted, and expires.** No permanent quiet admin backdoor. (rules/05)
10. **Phishing-resistant MFA (FIDO2/passkeys) at the IdP for all privileged and,
    ideally, all users**; step-up for sensitive operations; SMS/voice OTP is not
    phishing-resistant. (rules/06)
