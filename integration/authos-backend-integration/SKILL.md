---
name: authos-backend-integration
description: Secure backend APIs with AuthOS-issued JWTs and the AuthOS Node server adapter. Use when building an API that must verify AuthOS bearer tokens, enforce JWT claims, add Express middleware, validate JWKS keys, or create a backend-owned session after a browser OAuth callback.
---

# AuthOS Backend Integration

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill when protecting an application backend with AuthOS. Keep frontend login, service API keys, and webhook receiver work in their own skills unless the user explicitly asks for an end-to-end integration.

## Source-Verified Contract

- AuthOS publishes OIDC metadata at `GET /.well-known/openid-configuration`.
- AuthOS publishes RSA signing keys at `GET /.well-known/jwks.json`.
- AuthOS JWTs are signed with RS256 and include a `kid` header that must match a JWKS key.
- The Node package is `@drmhse/authos-node`.
- The SDK package is `@drmhse/sso-sdk`; do not invent an `@authos/*` package name.
- Browser OAuth callbacks normally return `access_token` and `refresh_token` in the URL fragment. The callback handlers also support `format=json` for JSON token responses in source, but the browser-facing SDK flow expects fragment handling.

## Backend Pattern

1. Let the frontend complete login with AuthOS.
2. Read `access_token` from the callback fragment, or receive it from the frontend over HTTPS.
3. Verify the token with JWKS before trusting any claim.
4. Map `sub`, `email`, `org_slug`, `service_slug`, `permissions`, and `is_platform_owner` claims to local authorization decisions only after verification.
5. If the app uses backend-owned sessions, exchange the verified token for an app session, then clear the fragment from browser history.

## Node Verification

Install the server adapter:

```bash
npm install @drmhse/authos-node
```

Verify a token directly:

```typescript
import { createTokenVerifier } from '@drmhse/authos-node';

const verifier = createTokenVerifier({
  baseURL: process.env.AUTHOS_BASE_URL!
});

const verified = await verifier.verifyToken(accessToken, {
  issuer: process.env.AUTHOS_BASE_URL,
  clockTolerance: 30
});

const userId = verified.claims.sub;
```

For Express, import middleware from the package subpath:

```typescript
import { createAuthMiddleware } from '@drmhse/authos-node/express';

const { requireAuth, requirePlatformOwner, requireAnyPermission } =
  createAuthMiddleware({ baseURL: process.env.AUTHOS_BASE_URL! });

app.get('/api/me', requireAuth(), (req, res) => {
  res.json({ user: req.auth!.claims.sub });
});

app.get(
  '/api/admin',
  requireAuth(),
  requirePlatformOwner(),
  (_req, res) => res.json({ ok: true })
);

app.post(
  '/api/billing',
  requireAuth(),
  requireAnyPermission(['billing.manage']),
  (_req, res) => res.json({ ok: true })
);
```

## Manual Verification

For non-Node backends:

1. Extract `Authorization: Bearer <jwt>`.
2. Decode the JWT header without trusting claims yet.
3. Require `alg = RS256` and a present `kid`.
4. Fetch and cache `/.well-known/jwks.json`.
5. Select the RSA JWK by `kid`.
6. Verify the signature, `exp`, optional `iss`, optional `aud`, and then enforce app authorization.

Do not verify AuthOS access tokens with a shared secret. Do not use the private signing key in applications. Do not accept unsigned or HS256 tokens.

## Common Pitfalls

- Do not send callback fragments to the backend by expecting `?access_token=...`; fragments are client-side only.
- Do not assume all tokens are org-scoped. Platform-owner and platform-level sessions may lack `org_slug` or `service_slug`.
- Do not use service API keys as user JWTs. API keys belong to `X-Api-Key` service API routes.
- If the backend relies on roles, fetch explicit permissions when needed instead of assuming legacy strings like `org:manage` cover every capability.
