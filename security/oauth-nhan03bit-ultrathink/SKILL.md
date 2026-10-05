---
name: oauth
description: OAuth 2.0 authorization code flow, PKCE, token refresh, OpenID Connect, social login providers, and security considerations
layer: domain
category: security
triggers:
  - "oauth"
  - "oauth2"
  - "authorization code"
  - "PKCE"
  - "openid connect"
  - "oidc"
  - "social login"
  - "google login"
  - "github login"
  - "token refresh"
  - "oauth flow"
  - "access token"
  - "refresh token"
inputs:
  - Application type (SPA, server-side, mobile, CLI)
  - Identity providers needed (Google, GitHub, Apple, custom)
  - Scopes required (profile, email, custom API)
  - Token storage strategy
  - Session management approach
outputs:
  - OAuth flow implementation
  - PKCE challenge generation
  - Token refresh logic
  - Provider configuration
  - Security checklist
linksTo:
  - authentication
  - better-auth
  - api-designer
  - encryption
  - owasp
linkedFrom:
  - nextjs
  - react
  - nodejs
preferredNextSkills:
  - authentication
  - better-auth
fallbackSkills:
  - api-designer
  - encryption
riskLevel: high
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - May add OAuth client libraries
  - May create OAuth callback routes
  - May store tokens in database or cookies
---

# OAuth Domain Skill

## Purpose

OAuth 2.0 is the industry standard for delegated authorization. Most "Login with Google/GitHub" flows use OAuth + OpenID Connect. This skill covers implementing OAuth correctly and securely -- the protocol has many subtle pitfalls that create real security vulnerabilities when done wrong.

## When to Use What

| Flow | Use Case | PKCE? | Client Secret? |
|------|----------|-------|----------------|
| **Authorization Code + PKCE** | SPAs, mobile apps, any public client | Yes | No |
| **Authorization Code** | Server-side apps with secret storage | Optional | Yes |
| **Client Credentials** | Machine-to-machine, no user involved | No | Yes |
| **Device Code** | CLI tools, smart TVs, no browser | No | Yes |

**Always use PKCE** -- even for server-side apps, PKCE adds defense-in-depth at zero cost.

**Never use**: Implicit flow (deprecated), Resource Owner Password (deprecated).

## Key Concepts

### OAuth 2.0 vs OpenID Connect

```
OAuth 2.0:
  - Authorization protocol (what can you access?)
  - Returns access_token (opaque or JWT)
  - For accessing APIs on behalf of user

OpenID Connect (OIDC):
  - Authentication layer ON TOP of OAuth 2.0 (who are you?)
  - Returns id_token (always JWT) + access_token
  - For identifying the user (name, email, picture)
  - Adds standardized scopes: openid, profile, email
  - Adds userinfo endpoint
  - Adds discovery document (.well-known/openid-configuration)

TL;DR: Use OIDC when you need to know WHO the user is.
       Use plain OAuth when you just need API access.
```

### The Authorization Code Flow (with PKCE)

```
1. Client generates code_verifier (random 43-128 chars)
2. Client computes code_challenge = SHA256(code_verifier), base64url-encoded
3. Client redirects user to authorization server:
   GET /authorize?
     response_type=code&
     client_id=xxx&
     redirect_uri=https://app.com/callback&
     scope=openid profile email&
     state=random_csrf_token&
     code_challenge=abc123&
     code_challenge_method=S256

4. User authenticates and consents
5. Authorization server redirects back:
   GET /callback?code=AUTH_CODE&state=random_csrf_token

6. Client verifies state matches (CSRF protection)
7. Client exchanges code for tokens:
   POST /token
     grant_type=authorization_code&
     code=AUTH_CODE&
     redirect_uri=https://app.com/callback&
     client_id=xxx&
     code_verifier=original_verifier

8. Authorization server verifies:
   SHA256(code_verifier) === stored code_challenge
   Returns: { access_token, refresh_token, id_token, expires_in }
```

## Patterns

### 1. PKCE Challenge Generation

```typescript
// src/lib/oauth/pkce.ts
import { randomBytes, createHash } from 'crypto';

export function generatePKCE() {
  // code_verifier: 43-128 characters, [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
  const verifier = randomBytes(32)
    .toString('base64url')
    .slice(0, 64);

  // code_challenge: SHA256 hash of verifier, base64url-encoded
  const challenge = createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return { verifier, challenge };
}

// Browser-compatible version (Web Crypto API)
export async function generatePKCEBrowser() {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  const verifier = btoa(String.fromCharCode(...array))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '')
    .slice(0, 64);

  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest('SHA-256', data);
  const challenge = btoa(String.fromCharCode(...new Uint8Array(hash)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  return { verifier, challenge };
}
```

### 2. Server-Side OAuth (Next.js Route Handlers)

```typescript
// src/lib/oauth/providers.ts
interface OAuthProvider {
  name: string;
  authorizationUrl: string;
  tokenUrl: string;
  userInfoUrl: string;
  clientId: string;
  clientSecret: string;
  scopes: string[];
}

export const providers: Record<string, OAuthProvider> = {
  google: {
    name: 'Google',
    authorizationUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenUrl: 'https://oauth2.googleapis.com/token',
    userInfoUrl: 'https://www.googleapis.com/oauth2/v3/userinfo',
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    scopes: ['openid', 'profile', 'email'],
  },
  github: {
    name: 'GitHub',
    authorizationUrl: 'https://github.com/login/oauth/authorize',
    tokenUrl: 'https://github.com/login/oauth/access_token',
    userInfoUrl: 'https://api.github.com/user',
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    scopes: ['read:user', 'user:email'],
  },
};
```

```typescript
// src/app/api/auth/[provider]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { generatePKCE } from '@/lib/oauth/pkce';
import { providers } from '@/lib/oauth/providers';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ provider: string }> }
) {
  const { provider: providerName } = await params;
  const provider = providers[providerName];
  if (!provider) {
    return NextResponse.json({ error: 'Unknown provider' }, { status: 400 });
  }

  const { verifier, challenge } = generatePKCE();

  // Generate CSRF state token
  const state = crypto.randomUUID();

  // Store verifier and state in httpOnly cookies (short-lived)
  const cookieStore = await cookies();
  cookieStore.set('oauth_verifier', verifier, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 600, // 10 minutes
    path: '/',
  });
  cookieStore.set('oauth_state', state, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 600,
    path: '/',
  });

  const redirectUri = `${process.env.NEXT_PUBLIC_APP_URL}/api/auth/${providerName}/callback`;

  const authUrl = new URL(provider.authorizationUrl);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', provider.clientId);
  authUrl.searchParams.set('redirect_uri', redirectUri);
  authUrl.searchParams.set('scope', provider.scopes.join(' '));
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('code_challenge', challenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');
  // Google-specific: force account selection
  if (providerName === 'google') {
    authUrl.searchParams.set('prompt', 'select_account');
  }

  return NextResponse.redirect(authUrl.toString());
}
```

```typescript
// src/app/api/auth/[provider]/callback/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { providers } from '@/lib/oauth/providers';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ provider: string }> }
) {
  const { provider: providerName } = await params;
  const provider = providers[providerName];
  if (!provider) {
    return NextResponse.redirect(`${process.env.NEXT_PUBLIC_APP_URL}/login?error=unknown_provider`);
  }

  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  const error = searchParams.get('error');

  if (error) {
    return NextResponse.redirect(
      `${process.env.NEXT_PUBLIC_APP_URL}/login?error=${error}`
    );
  }

  const cookieStore = await cookies();
  const storedState = cookieStore.get('oauth_state')?.value;
  const verifier = cookieStore.get('oauth_verifier')?.value;

  // CRITICAL: Verify state to prevent CSRF
  if (!state || !storedState || state !== storedState) {
    return NextResponse.redirect(
      `${process.env.NEXT_PUBLIC_APP_URL}/login?error=state_mismatch`
    );
  }

  if (!code || !verifier) {
    return NextResponse.redirect(
      `${process.env.NEXT_PUBLIC_APP_URL}/login?error=missing_params`
    );
  }

  // Clean up OAuth cookies
  cookieStore.delete('oauth_state');
  cookieStore.delete('oauth_verifier');

  // Exchange code for tokens
  const redirectUri = `${process.env.NEXT_PUBLIC_APP_URL}/api/auth/${providerName}/callback`;

  const tokenResponse = await fetch(provider.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Accept: 'application/json',
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: provider.clientId,
      client_secret: provider.clientSecret,
      code_verifier: verifier,
    }),
  });

  if (!tokenResponse.ok) {
    console.error('Token exchange failed:', await tokenResponse.text());
    return NextResponse.redirect(
      `${process.env.NEXT_PUBLIC_APP_URL}/login?error=token_exchange_failed`
    );
  }

  const tokens = await tokenResponse.json();

  // Fetch user info
  const userResponse = await fetch(provider.userInfoUrl, {
    headers: { Authorization: `Bearer ${tokens.access_token}` },
  });
  const userInfo = await userResponse.json();

  // Normalize user data across providers
  const normalizedUser = normalizeUser(providerName, userInfo);

  // Create or link account in your database
  const { user, session } = await findOrCreateUser(normalizedUser, {
    provider: providerName,
    providerAccountId: normalizedUser.providerId,
    accessToken: tokens.access_token,
    refreshToken: tokens.refresh_token,
    expiresAt: tokens.expires_in
      ? Math.floor(Date.now() / 1000) + tokens.expires_in
      : undefined,
  });

  // Set session cookie
  cookieStore.set('session_token', session.token, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 30, // 30 days
    path: '/',
  });

  return NextResponse.redirect(`${process.env.NEXT_PUBLIC_APP_URL}/dashboard`);
}

function normalizeUser(provider: string, raw: Record<string, unknown>) {
  switch (provider) {
    case 'google':
      return {
        providerId: raw.sub as string,
        email: raw.email as string,
        name: raw.name as string,
        avatarUrl: raw.picture as string,
        emailVerified: raw.email_verified as boolean,
      };
    case 'github':
      return {
        providerId: String(raw.id),
        email: raw.email as string,
        name: (raw.name ?? raw.login) as string,
        avatarUrl: raw.avatar_url as string,
        emailVerified: true, // GitHub emails are verified
      };
    default:
      throw new Error(`Unknown provider: ${provider}`);
  }
}
```

### 3. Token Refresh

```typescript
// src/lib/oauth/token-refresh.ts

interface StoredTokens {
  accessToken: string;
  refreshToken: string | null;
  expiresAt: number; // Unix timestamp in seconds
  provider: string;
}

export async function getValidAccessToken(
  accountId: string
): Promise<string> {
  const account = await db.query.oauthAccounts.findFirst({
    where: eq(oauthAccounts.id, accountId),
  });

  if (!account) throw new Error('Account not found');

  // Check if token is still valid (with 5-minute buffer)
  const now = Math.floor(Date.now() / 1000);
  if (account.expiresAt && account.expiresAt > now + 300) {
    return account.accessToken;
  }

  // Token expired -- refresh it
  if (!account.refreshToken) {
    throw new Error('Token expired and no refresh token available');
  }

  const provider = providers[account.provider];
  const response = await fetch(provider.tokenUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Accept: 'application/json',
    },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: account.refreshToken,
      client_id: provider.clientId,
      client_secret: provider.clientSecret,
    }),
  });

  if (!response.ok) {
    // Refresh token may be revoked -- user needs to re-authenticate
    await db.update(oauthAccounts)
      .set({ refreshToken: null })
      .where(eq(oauthAccounts.id, accountId));
    throw new Error('Token refresh failed -- re-authentication required');
  }

  const tokens = await response.json();

  // Update stored tokens
  await db.update(oauthAccounts)
    .set({
      accessToken: tokens.access_token,
      // Some providers rotate refresh tokens
      refreshToken: tokens.refresh_token ?? account.refreshToken,
      expiresAt: tokens.expires_in
        ? Math.floor(Date.now() / 1000) + tokens.expires_in
        : null,
    })
    .where(eq(oauthAccounts.id, accountId));

  return tokens.access_token;
}
```

### 4. Device Authorization Flow (CLI Tools)

```typescript
// For CLI tools that cannot open a browser redirect

async function deviceCodeLogin(provider: OAuthProvider) {
  // Step 1: Request device code
  const deviceResponse = await fetch(provider.deviceAuthorizationUrl!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: provider.clientId,
      scope: provider.scopes.join(' '),
    }),
  });

  const {
    device_code,
    user_code,
    verification_uri,
    verification_uri_complete,
    expires_in,
    interval,
  } = await deviceResponse.json();

  // Step 2: Display code to user
  console.log(`\nOpen this URL: ${verification_uri}`);
  console.log(`Enter code: ${user_code}\n`);
  // Or open browser automatically:
  // await open(verification_uri_complete);

  // Step 3: Poll for token
  const deadline = Date.now() + expires_in * 1000;
  const pollInterval = (interval ?? 5) * 1000;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, pollInterval));

    const tokenResponse = await fetch(provider.tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
        device_code,
        client_id: provider.clientId,
      }),
    });

    const body = await tokenResponse.json();

    if (body.error === 'authorization_pending') continue;
    if (body.error === 'slow_down') {
      await new Promise((r) => setTimeout(r, 5000)); // Extra delay
      continue;
    }
    if (body.error) throw new Error(`OAuth error: ${body.error}`);

    return body; // { access_token, refresh_token, ... }
  }

  throw new Error('Device code expired');
}
```

### 5. OIDC Discovery

```typescript
// Auto-configure from provider's discovery document
async function discoverOIDCProvider(issuer: string) {
  const discoveryUrl = `${issuer}/.well-known/openid-configuration`;
  const response = await fetch(discoveryUrl);
  const config = await response.json();

  return {
    authorizationEndpoint: config.authorization_endpoint,
    tokenEndpoint: config.token_endpoint,
    userInfoEndpoint: config.userinfo_endpoint,
    jwksUri: config.jwks_uri,
    issuer: config.issuer,
    supportedScopes: config.scopes_supported,
    supportedResponseTypes: config.response_types_supported,
    supportedGrantTypes: config.grant_types_supported,
  };
}

// Example usage:
// const google = await discoverOIDCProvider('https://accounts.google.com');
// const auth0 = await discoverOIDCProvider('https://your-tenant.auth0.com');
```

### 6. ID Token Validation

```typescript
// CRITICAL: Always validate ID tokens server-side
import { createRemoteJWKSet, jwtVerify } from 'jose';

const JWKS = createRemoteJWKSet(
  new URL('https://www.googleapis.com/oauth2/v3/certs')
);

async function validateIdToken(idToken: string, expectedNonce?: string) {
  const { payload } = await jwtVerify(idToken, JWKS, {
    issuer: 'https://accounts.google.com',
    audience: process.env.GOOGLE_CLIENT_ID,
  });

  // Verify nonce if provided (prevents replay attacks)
  if (expectedNonce && payload.nonce !== expectedNonce) {
    throw new Error('Invalid nonce');
  }

  // Verify token is not expired (jose does this, but be explicit)
  if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
    throw new Error('ID token expired');
  }

  return {
    sub: payload.sub!,
    email: payload.email as string,
    name: payload.name as string,
    picture: payload.picture as string,
    emailVerified: payload.email_verified as boolean,
  };
}
```

## Security Checklist

```
[x] Use Authorization Code flow with PKCE (never Implicit)
[x] Validate state parameter on callback (CSRF protection)
[x] Use code_challenge_method=S256 (never plain)
[x] Store tokens server-side (never in localStorage)
[x] Set cookies: httpOnly, secure, sameSite=lax
[x] Validate id_token signature and claims (issuer, audience, expiry)
[x] Use nonce for replay protection in OIDC flows
[x] Validate redirect_uri exactly matches registered URI
[x] Store client_secret server-side only (never in client code)
[x] Implement token refresh with rotation detection
[x] Handle revoked refresh tokens gracefully (re-auth flow)
[x] Use short-lived access tokens (< 1 hour)
[x] Log all authentication events for audit trail
[x] Rate-limit token exchange endpoint
```

## Best Practices

1. **Always use PKCE** -- it is required for public clients and recommended for all clients
2. **Validate state on every callback** -- this is your CSRF protection
3. **Store tokens in httpOnly cookies** -- never localStorage (XSS vulnerable)
4. **Use the `jose` library** for JWT operations -- well-maintained, standards-compliant
5. **Fetch user info from the userinfo endpoint** -- do not solely trust the id_token for mutable data
6. **Support account linking** -- let users connect multiple OAuth providers to one account
7. **Handle provider downtime** -- show clear error messages, offer alternative login methods
8. **Request minimal scopes** -- ask only for what you need; users abandon consent screens with many scopes
9. **Use OIDC discovery** -- auto-configure endpoints from `.well-known/openid-configuration`
10. **Rotate refresh tokens** -- detect token reuse (indicates theft) and revoke all tokens for that grant

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Not validating `state` param | CSRF attacks -- attacker can link their account to victim | Always verify state matches stored value |
| Storing tokens in localStorage | XSS can steal all tokens | Use httpOnly secure cookies |
| Using Implicit flow | Tokens in URL fragment, no refresh | Use Authorization Code + PKCE |
| Not checking `iss` and `aud` in ID token | Token confusion attacks | Validate issuer and audience on every ID token |
| Hardcoding redirect URIs | Breaks in different environments | Use environment variables, validate against allow-list |
| Not handling refresh token rotation | Stale refresh tokens cause logout | Store new refresh token when provider rotates |
| Missing `prompt=consent` for scope changes | Users denied new permissions silently | Force consent when requesting additional scopes |
| No CSRF on login initiation | Login CSRF -- attacker forces victim to log into attacker's account | Use state parameter + validate on callback |
