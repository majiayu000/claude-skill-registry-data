---
name: web-oauth
description: >
  Attack OAuth 2.0 / OIDC / SSO flows for account takeover. Load on "Login with Google/GitHub",
  /authorize, /callback, redirect_uri, state, code/token params, SAML/OIDC SSO. Signals: OAuth
  endpoints, redirect_uri handling, missing state, implicit flow, pre-account-linking.
domain: web
type: technique
stability: learning
modes: [bugbounty]
severity: critical
owasp: [A07:2021-Auth-Failures]
cwe: [CWE-287, CWE-601]
tools: [burp]
schema_version: 1
---

# OAuth / OIDC / SSO abuse

## When it applies
The app delegates auth via OAuth/OIDC (social login, enterprise SSO). Flaws here are frequently
full account takeover.

## Why it works
OAuth security depends on strict validation of `redirect_uri`, `state`, `code` binding, and how
identities are linked. Implementations relax one of these — and the token/code that proves
identity leaks to the attacker or an account gets linked to the wrong user.

## Method
1. **redirect_uri validation**: try appended paths, `//evil`, `@`, subdomain/suffix tricks,
   open-redirect on an allowed host (→ `web-open-redirect`) to exfiltrate the `code`/`token`.
2. **state / CSRF**: missing or unvalidated `state` → login CSRF / force-link the victim to your account.
3. **Account linking / pre-takeover**: sign up with the victim's email pre-verification, or link
   a social account to an existing local account by email without proof → ATO.
4. **Token/flow issues**: implicit-flow token in URL/referrer leak; `code` reuse/no PKCE; ID-token
   `email_verified` trust; audience/issuer not checked; mixing providers.
5. **Steal & replay**: capture leaked `code`/`token`, complete the flow as the victim.

## Gotchas
- Most impact rides on a `redirect_uri` weakness or open redirect on an allowlisted host — chase that first.
- "email_verified: false" trusted by the app is a classic pre-account-takeover.
- Keep it your own test accounts; prove ATO against an account you control on both sides.

## Verify success
You authenticate as (or link/hijack) a victim account — e.g. captured code completes login as
the victim, demonstrated with two accounts you own.

## References
PortSwigger OAuth labs; RFC 6749/6819; "OAuth security" (Salt/PortSwigger write-ups).
