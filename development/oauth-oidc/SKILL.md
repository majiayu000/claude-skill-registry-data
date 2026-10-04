---
name: oauth-oidc
description: Deep OAuth 2.0 / OpenID Connect workflow—choosing flows for client type, PKCE, tokens and validation, scopes and consent, rotation, and common misconfigurations. Use when implementing SSO, social login, or API access on behalf of users.
---

# OAuth 2.0 / OIDC (Deep Workflow)

OAuth solves **delegated authorization**; OIDC adds **identity** on top. Most production bugs are **wrong flow for client**, **token validation gaps**, and **confused redirect URIs**.

## When to Offer This Workflow

**Trigger conditions:**

- Web, mobile, or SPA login; **machine-to-machine** clients
- Debugging `invalid_grant`, **redirect_uri** mismatches, **token** **replay**
- Hardening **scopes**, **refresh** rotation, **logout**

**Initial offer:**

Use **six stages**: (1) actors & client type, (2) select flow & PKCE, (3) tokens & validation, (4) scopes & consent UX, (5) session & logout, (6) operational hardening). Confirm **IdP** (Auth0, Cognito, Keycloak, Google, etc.).

---

## Stage 1: Actors & Client Type

**Goal:** Classify **confidential** vs **public** clients and **who** holds secrets.

### Rules

- **Server-side web app** with secret: confidential; **SPA** and **native**: public → **PKCE** mandatory
- **M2M**: client credentials or JWT assertion—**no user** in loop

**Exit condition:** Architecture diagram: browser, backend, IdP, resource server.

---

## Stage 2: Select Flow & PKCE

**Goal:** Authorization Code (+ **PKCE** for public clients); avoid Implicit and ROPC for new apps.

### Practices

- **Exact** redirect URI allowlist—**no** wildcards that enable open redirects
- **State** and **nonce** for CSRF and token binding (OIDC)
- **Mobile**: **custom URL schemes** vs **universal links**—document trade-offs

**Exit condition:** Sequence diagram for login happy path and error paths.

---

## Stage 3: Tokens & Validation

**Goal:** **Access token** for APIs; **ID token** for identity claims—validate **issuer**, **audience**, **exp**, **signature** (JWKS rotation).

### Practices

- **Never** use ID token as API bearer unless your architecture explicitly defines that (usually wrong)
- **Refresh token**: rotation, reuse detection, secure storage (httpOnly cookie or secure OS storage on mobile)
- **Clock skew** tolerance when validating `exp`

**Exit condition:** Documented validation steps in code or API gateway config.

---

## Stage 4: Scopes & Consent

**Goal:** **Least privilege** scopes; **incremental** auth when possible.

### UX

- Clear consent copy; **minimize** scope creep at first login

---

## Stage 5: Session & Logout

**Goal:** **RP-initiated logout** vs **local** session clearing—know what breaks SSO across apps.

### Practices

- **Front-channel** / **back-channel** logout when enterprise IdP requires

---

## Stage 6: Operational Hardening

**Goal:** **Rotate** client secrets safely; **monitor** failed auth rates; **alert** on abnormal token issuance.

### Pitfalls

- **Mixing** dev and prod clients; **leaking** JWKS or introspection endpoints in client bundles

---

## Final Review Checklist

- [ ] Correct flow and PKCE for client class
- [ ] Redirect URIs strict; state/nonce used appropriately
- [ ] Token validation complete (sig, iss, aud, exp)
- [ ] Refresh handling and rotation policy
- [ ] Scopes minimal; logout behavior understood

## Tips for Effective Guidance

- Draw **Authorization Code + PKCE** as default for SPAs.
- Call out **BFF pattern** when SPA cannot hold secrets and APIs need cookies.
- Enterprise **SAML bridge** to OIDC adds quirks—defer to IdP docs when needed.

## Handling Deviations

- **First-party** only same-site: consider **session cookie** auth instead of full OAuth complexity if appropriate.
- **Legacy Implicit**: migration plan to Code+PKCE with downtime window.
