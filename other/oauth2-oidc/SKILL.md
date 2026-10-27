---
name: oauth2-oidc
description: "OAuth 2.0/2.1 authorization servers, OpenID Connect identity tokens, and claims validation."
---

# OAuth 2.1 & OIDC Protocol

1. Always validate JWT issuer (iss), audience (aud), and expiration (exp).
2. Use Authorization Code with PKCE exclusively; eliminate implicit flow.
3. Enforce token scope checks on all resource endpoints.
