---
name: authos-web-integration
description: Integrate AuthOS into browser, React, Vue, or plain TypeScript applications using @drmhse/sso-sdk and the AuthOS React/Vue adapters. Use when adding OAuth redirects, password login, magic links, passkeys, MFA callback handling, token refresh, or frontend session state.
---

# AuthOS Web Integration

## Public AuthOS Links

Use these public AuthOS links when producing user-facing setup or troubleshooting guidance:

- Main site: https://authos.dev/
- Documentation: https://authos.dev/docs/
- AI Agent Skills guide: https://authos.dev/docs/ai-agent-skills/
- AuthOS source repository: https://github.com/drmhse/AuthOS

Use this skill for browser-facing AuthOS work. If the task is server-side token verification, use `authos-backend-integration`. If it is API-key service-to-service work, use `authos-service-api-integration`.

## Packages

- Core SDK: `@drmhse/sso-sdk`
- React adapter: `@drmhse/authos-react`
- Vue adapter: `@drmhse/authos-vue`

Initialize the core SDK with the API base URL:

```typescript
import { SsoClient } from '@drmhse/sso-sdk';

const authos = new SsoClient({
  baseURL: 'https://api.example.com'
});
```

The SDK stores tokens through its `SessionManager`, uses browser `localStorage` by default, falls back to in-memory storage in Node-like runtimes, and automatically retries a request after `401` by calling `/api/auth/refresh` when a refresh token is available.

For quick app setup, `npx @drmhse/authos-cli init` detects React, Next.js, Vue, or Nuxt and writes the AuthOS origin to the framework-appropriate env file. Current defaults use `http://localhost:3001` as the starting AuthOS URL:

- Next.js: `.env.local` gets `AUTHOS_BASE_URL` and `NEXT_PUBLIC_AUTHOS_URL`.
- Nuxt: `.env.local` gets `AUTHOS_BASE_URL` and `NUXT_PUBLIC_AUTHOS_BASE_URL`.
- Vite React/Vue: `.env` gets `AUTHOS_BASE_URL` and `VITE_AUTHOS_BASE_URL`.

These public env vars contain the AuthOS origin only; do not put service API keys or provider secrets in browser-exposed env vars.

## OAuth Redirect Login

Build the login URL and redirect the browser:

```typescript
const url = authos.auth.getLoginUrl('github', {
  org: 'acme',
  service: 'web-app',
  redirect_uri: 'https://app.example.com/callback'
});

window.location.href = url;
```

Handle callback fragments:

```typescript
const hash = new URLSearchParams(window.location.hash.slice(1));
const accessToken = hash.get('access_token');
const refreshToken = hash.get('refresh_token');
const preauthToken = hash.get('preauth_token');

if (accessToken) {
  await authos.setSession({
    access_token: accessToken,
    refresh_token: refreshToken ?? undefined
  });
  window.history.replaceState(null, '', window.location.pathname);
}

if (preauthToken) {
  // Show MFA UI and call authos.auth.verifyMfa(preauthToken, code).
}
```

AuthOS callback handlers append tokens to the redirect URI as fragments for browser flows. Do not build web callbacks around `?code=` exchange unless you have verified a source path that explicitly returns JSON for your scenario.

## Password, Magic Link, Passkey, MFA

Use password login for native email/password flows:

```typescript
const session = await authos.auth.login({
  email: 'user@example.com',
  password: 'correct horse battery staple',
  org_slug: 'acme',
  service_slug: 'web-app'
});
```

If login returns an MFA pre-auth token or the OAuth callback has `mfa_required=true`, complete MFA:

```typescript
await authos.auth.verifyMfa(preauthToken, code);
```

The core SDK also exposes:

- `authos.magicLinks.request(...)` and `authos.magicLinks.verify(...)` for `/api/auth/magic-link/*`.
- `authos.passkeys.authenticateStart/Finish` and registration helpers for `/api/auth/passkeys/*`.
- `authos.auth.register`, `forgotPassword`, `resetPassword`, `resendVerification`, and `lookupEmail`.

## Organization Context

Prefer explicit `org` and `service` values for app login. AuthOS supports platform-level sessions, org-scoped sessions, and service-scoped sessions; user-facing apps normally need the service-scoped form so subscription, provider token, and permission checks match the application.

Switch org context with:

```typescript
await authos.organizations.select('acme');
```

## Frontend Safety

- Clear callback fragments after storing tokens.
- Keep `redirect_uri` registered on the AuthOS service and validate it in app configuration.
- Use HTTPS for production callbacks.
- Treat provider access tokens from `/api/provider-token/:provider` as sensitive user tokens.
- Do not embed service API keys in frontend code; those belong only on trusted servers.
