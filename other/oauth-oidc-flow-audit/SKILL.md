---
name: oauth-oidc-flow-audit
description: Review OAuth/OIDC login flows for redirect validation, state/nonce handling, PKCE, token storage, and session lifecycle.
---

# Oauth Oidc Flow Audit

## Goal

Identify authentication-flow weaknesses without collecting or exposing real user credentials or live tokens.

## Inputs to inspect

Identity-provider config, redirect URI allowlist, authorization-code flow, client type, session handling, and logout behavior.

## Workflow

1. Map the authorization flow from login initiation through callback, code exchange, token validation, session creation, refresh, and logout.
2. Verify state and nonce are unpredictable, bound to the initiating session, single-use where required, and checked before accepting a callback.
3. For public clients, confirm PKCE is applied and verifier/challenge handling follows the expected flow; validate redirect URIs by exact approved matching.
4. Inspect issuer, audience, signature, expiration, and nonce claims as applicable; distinguish ID tokens from access tokens and do not use them interchangeably.
5. Test replayed callbacks, missing/mismatched state, invalid redirect, expired tokens, clock skew, refresh failure, and logout/session revocation behavior.

## Validation checklist

- [ ] Redirect destinations are strictly allowlisted and cannot be chosen arbitrarily by request input.
- [ ] State/nonce and PKCE behavior are evidenced in the actual flow/configuration.
- [ ] Token validation checks the appropriate issuer/audience/expiry and expected token purpose.
- [ ] Tokens are not stored or logged in unsafe locations.
- [ ] Negative tests cover malformed and replayed callbacks without using real production credentials.

## Required output

Produce an auth-flow diagram, control checklist, confirmed gaps, test matrix, and prioritized remediation plan.

## Boundaries and failure handling

Do not paste real tokens into evidence; do not claim a provider configuration is secure from a screenshot alone.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
