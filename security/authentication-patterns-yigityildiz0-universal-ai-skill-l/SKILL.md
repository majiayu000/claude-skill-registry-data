---
name: authentication-patterns
description: Authentication and authorization patterns including OAuth 2.0, OIDC, JWT, session management, MFA, and passkeys. Use when implementing login flows, securing.
---

# Authentication Patterns

Comprehensive guidance for implementing secure authentication and authorization systems. Covers OAuth 2.0 flows, OpenID Connect, JWT lifecycle management, session security, password hashing, multi-factor authentication, passkeys/WebAuthn, role-based and attribute-based access control, API key management, and common vulnerability prevention.

## When to Use This Skill

Use this skill for:

- Implementing OAuth 2.0 authorization code flow with PKCE
- Integrating OpenID Connect for SSO (Single Sign-On)
- Designing JWT issuance, validation, and refresh token rotation
- Building secure session management with cookies or tokens
- Implementing password hashing with bcrypt or Argon2
- Adding MFA (TOTP, WebAuthn/passkeys) to an application
- Designing RBAC or ABAC authorization models
- Managing API keys for service-to-service communication
- Configuring security headers (CSP, CORS, HSTS)
- Reviewing auth architecture for common vulnerabilities

**Trigger phrases**: "authentication", "authorization", "OAuth", "OIDC", "JWT", "session management", "login flow", "MFA", "passkeys", "WebAuthn", "RBAC", "ABAC", "API key", "CORS", "CSRF", "password hashing", "refresh token"

## What This Skill Does

Provides production-grade authentication patterns including:

- **OAuth 2.0**: Authorization code + PKCE, client credentials, device flow
- **OpenID Connect**: ID tokens, userinfo endpoint, discovery
- **JWT**: Structure, signing algorithms, validation, refresh rotation
- **Sessions**: Cookie security, token storage, session fixation prevention
- **Passwords**: Hashing (bcrypt, Argon2), salting, migration strategies
- **MFA**: TOTP setup, WebAuthn/passkeys registration and assertion
- **Access Control**: RBAC middleware, ABAC policies, permission models
- **API Security**: API key management, rate limiting, scope enforcement
- **Headers**: CSP, CORS, HSTS, X-Frame-Options configuration

## Instructions

### Step 1: Understand OAuth 2.0 Flows

**Flow Selection Guide**:

| Flow | Use Case | Client Type |
|------|----------|-------------|
| Authorization Code + PKCE | Web apps, SPAs, mobile | Public clients |
| Client Credentials | Machine-to-machine | Confidential clients |
| Device Authorization | Smart TVs, CLI tools | Input-constrained devices |
| Refresh Token | Extend sessions without re-auth | Any client with refresh grant |

**Authorization Code Flow with PKCE** (recommended for all user-facing apps):

```
┌──────┐     1. Auth Request + code_verifier     ┌──────────────┐
│      │────────────────────────────────────────▶│              │
│      │                                         │ Authorization│
│ App  │◀────────────────────────────────────────│   Server     │
│      │     2. Authorization Code               │              │
│      │                                         └──────┬───────┘
│      │     3. Token Request + code_verifier            │
│      │────────────────────────────────────────▶        │
│      │                                                 │
│      │◀────────────────────────────────────────        │
│      │     4. Access Token + Refresh Token             │
└──────┘                                         ┌──────┴───────┐
   │                                             │   Resource   │
   │         5. API Request + Access Token       │   Server     │
   │────────────────────────────────────────────▶│              │
   │                                             └──────────────┘
```

**PKCE Implementation (Node.js)**:

```typescript
import crypto from 'crypto';

// Step 1: Generate PKCE code verifier and challenge
function generatePKCE(): { verifier: string; challenge: string } {
  // Code verifier: 43-128 character random string
  const verifier = crypto.randomBytes(32).toString('base64url');

  // Code challenge: SHA-256 hash of verifier, base64url encoded
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');

  return { verifier, challenge };
}

// Step 2: Build authorization URL
function buildAuthUrl(clientId: string, redirectUri: string, challenge: string): string {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: clientId,
    redirect_uri: redirectUri,
    scope: 'openid profile email',
    state: crypto.randomBytes(16).toString('hex'),  // CSRF protection
    code_challenge: challenge,
    code_challenge_method: 'S256',
  });
  return `https://auth.example.com/authorize?${params}`;
}

// Step 3: Exchange authorization code for tokens
async function exchangeCode(
  code: string,
  verifier: string,
  clientId: string,
  redirectUri: string
): Promise<TokenResponse> {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirectUri,
      client_id: clientId,
      code_verifier: verifier,  // Prove we initiated the request
    }),
  });

  if (!response.ok) {
    throw new Error(`Token exchange failed: ${response.status}`);
  }

  return response.json();
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  id_token: string;     // Present with OIDC
  token_type: 'Bearer';
  expires_in: number;
}
```

**Client Credentials Flow** (service-to-service):

```typescript
async function getServiceToken(clientId: string, clientSecret: string): Promise<string> {
  const response = await fetch('https://auth.example.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString('base64')}`,
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      scope: 'orders:read orders:write',
    }),
  });

  const data = await response.json();
  return data.access_token;
}
```

### Step 2: Implement JWT Lifecycle

**JWT Structure**:

```
Header.Payload.Signature

Header:  { "alg": "RS256", "typ": "JWT", "kid": "key-2026-03" }
Payload: { "sub": "user-123", "iss": "https://auth.example.com",
           "aud": "https://api.example.com", "exp": 1709500800,
           "iat": 1709497200, "scope": "read write" }
Signature: RS256(base64url(header) + "." + base64url(payload), privateKey)
```

**JWT Signing and Validation (Node.js)**:

```typescript
import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';

// ── Token Creation (auth server side) ─────────────────────────────

const PRIVATE_KEY = process.env.JWT_PRIVATE_KEY!;

function createAccessToken(userId: string, scopes: string[]): string {
  return jwt.sign(
    {
      sub: userId,
      scope: scopes.join(' '),
    },
    PRIVATE_KEY,
    {
      algorithm: 'RS256',
      issuer: 'https://auth.example.com',
      audience: 'https://api.example.com',
      expiresIn: '15m',   // Short-lived access tokens
      keyid: 'key-2026-03',
    }
  );
}

function createRefreshToken(userId: string, tokenFamily: string): string {
  return jwt.sign(
    {
      sub: userId,
      family: tokenFamily,  // For rotation detection
    },
    PRIVATE_KEY,
    {
      algorithm: 'RS256',
      issuer: 'https://auth.example.com',
      expiresIn: '7d',
      jwtid: crypto.randomUUID(),  // Unique token ID for revocation
    }
  );
}

// ── Token Validation (resource server side) ───────────────────────

const client = jwksClient({
  jwksUri: 'https://auth.example.com/.well-known/jwks.json',
  cache: true,
  rateLimit: true,
  jwksRequestsPerMinute: 5,
});

function getSigningKey(header: jwt.JwtHeader, callback: jwt.SigningKeyCallback): void {
  client.getSigningKey(header.kid, (err, key) => {
    if (err) return callback(err);
    callback(null, key?.getPublicKey());
  });
}

function validateAccessToken(token: string): Promise<jwt.JwtPayload> {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getSigningKey,
      {
        algorithms: ['RS256'],
        issuer: 'https://auth.example.com',
        audience: 'https://api.example.com',
        clockTolerance: 30,  // 30-second clock skew tolerance
      },
      (err, decoded) => {
        if (err) return reject(err);
        resolve(decoded as jwt.JwtPayload);
      }
    );
  });
}
```

**Refresh Token Rotation** (prevents token theft):

```typescript
async function refreshTokens(refreshToken: string): Promise<TokenResponse> {
  // 1. Validate the refresh token
  const decoded = await validateRefreshToken(refreshToken);

  // 2. Check if token has been revoked (detect reuse attacks)
  const isRevoked = await tokenStore.isRevoked(decoded.jti);
  if (isRevoked) {
    // Token reuse detected: revoke the entire token family
    await tokenStore.revokeFamily(decoded.family);
    throw new Error('Refresh token reuse detected. All sessions revoked.');
  }

  // 3. Revoke the old refresh token
  await tokenStore.revoke(decoded.jti);

  // 4. Issue new token pair
  const newAccessToken = createAccessToken(decoded.sub, decoded.scope);
  const newRefreshToken = createRefreshToken(decoded.sub, decoded.family);

  return {
    access_token: newAccessToken,
    refresh_token: newRefreshToken,
    token_type: 'Bearer',
    expires_in: 900,
  };
}
```

### Step 3: Secure Session Management

**Cookie-Based Sessions (Express.js)**:

```typescript
import express from 'express';
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

const app = express();

app.use(session({
  store: new RedisStore({ client: redisClient }),
  name: '__Host-session',           // __Host- prefix enforces Secure + no Domain
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  rolling: true,                    // Reset expiry on each request
  cookie: {
    secure: true,                   // HTTPS only
    httpOnly: true,                 // Not accessible via JavaScript
    sameSite: 'lax',                // CSRF protection
    maxAge: 30 * 60 * 1000,        // 30 minutes
    path: '/',
  },
}));

// Session fixation prevention: regenerate session ID after login
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body.email, req.body.password);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  // Regenerate session to prevent fixation attacks
  req.session.regenerate((err) => {
    if (err) return res.status(500).json({ error: 'Session error' });
    req.session.userId = user.id;
    req.session.role = user.role;
    res.json({ message: 'Logged in' });
  });
});

// Logout: destroy session and clear cookie
app.post('/logout', (req, res) => {
  req.session.destroy(() => {
    res.clearCookie('__Host-session');
    res.json({ message: 'Logged out' });
  });
});
```

**Token Storage in SPAs** (security comparison):

| Storage | XSS Risk | CSRF Risk | Recommendation |
|---------|----------|-----------|----------------|
| localStorage | High (JS accessible) | None | Avoid for tokens |
| sessionStorage | High (JS accessible) | None | Avoid for tokens |
| HttpOnly cookie | None (not JS accessible) | Medium | Preferred with SameSite |
| In-memory variable | Low (lost on refresh) | None | Good for access tokens |

### Step 4: Implement Password Hashing

```typescript
import bcrypt from 'bcrypt';
import argon2 from 'argon2';

// ── bcrypt (widely supported, proven) ─────────────────────────────

const BCRYPT_ROUNDS = 12;  // Aim for ~250ms hash time

async function hashPasswordBcrypt(password: string): Promise<string> {
  return bcrypt.hash(password, BCRYPT_ROUNDS);
}

async function verifyPasswordBcrypt(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ── Argon2id (recommended for new projects, OWASP preferred) ──────

async function hashPasswordArgon2(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,    // Hybrid: resistant to side-channel + GPU attacks
    memoryCost: 65536,        // 64 MB
    timeCost: 3,              // 3 iterations
    parallelism: 4,           // 4 threads
  });
}

async function verifyPasswordArgon2(password: string, hash: string): Promise<boolean> {
  return argon2.verify(hash, password);
}

// ── Password policy enforcement ───────────────────────────────────

function validatePasswordPolicy(password: string): string[] {
  const errors: string[] = [];
  if (password.length < 12) errors.push('Minimum 12 characters');
  if (password.length > 128) errors.push('Maximum 128 characters');
  // Check against common breached passwords (use a bloom filter or k-anonymity API)
  // Do NOT enforce complex character rules (NIST SP 800-63B guidance)
  return errors;
}
```

### Step 5: Add Multi-Factor Authentication

**TOTP Implementation (Google Authenticator compatible)**:

```typescript
import { authenticator } from 'otplib';
import QRCode from 'qrcode';

// ── TOTP Setup ────────────────────────────────────────────────────

async function enableTOTP(userId: string, email: string) {
  // Generate a secret for this user
  const secret = authenticator.generateSecret(20);  // 160-bit secret

  // Store secret (encrypted) in database, marked as unverified
  await db.users.update(userId, {
    totp_secret: encrypt(secret),
    totp_verified: false,
  });

  // Generate QR code for authenticator app
  const otpauthUrl = authenticator.keyuri(email, 'MyApp', secret);
  const qrCodeDataUrl = await QRCode.toDataURL(otpauthUrl);

  return {
    secret,        // Show to user as backup
    qrCode: qrCodeDataUrl,
  };
}

// ── TOTP Verification ─────────────────────────────────────────────

async function verifyTOTP(userId: string, token: string): Promise<boolean> {
  const user = await db.users.findById(userId);
  const secret = decrypt(user.totp_secret);

  // Validate with a 1-step window (allows 30s clock drift)
  const isValid = authenticator.check(token, secret);

  if (isValid && !user.totp_verified) {
    await db.users.update(userId, { totp_verified: true });
  }

  return isValid;
}
```

**WebAuthn/Passkeys Registration (using SimpleWebAuthn)**:

```typescript
import {
  generateRegistrationOptions,
  verifyRegistrationResponse,
  generateAuthenticationOptions,
  verifyAuthenticationResponse,
} from '@simplewebauthn/server';

const RP_NAME = 'MyApp';
const RP_ID = 'example.com';
const ORIGIN = 'https://example.com';

// ── Passkey Registration ──────────────────────────────────────────

async function startPasskeyRegistration(userId: string, email: string) {
  const existingCredentials = await db.credentials.findByUser(userId);

  const options = await generateRegistrationOptions({
    rpName: RP_NAME,
    rpID: RP_ID,
    userName: email,
    userDisplayName: email,
    attestationType: 'none',       // Skip attestation for simpler flow
    excludeCredentials: existingCredentials.map(cred => ({
      id: cred.credentialId,
      type: 'public-key',
    })),
    authenticatorSelection: {
      residentKey: 'preferred',    // Enable discoverable credentials (passkeys)
      userVerification: 'preferred',
    },
  });

  // Store challenge in session for verification
  await sessionStore.set(userId, { challenge: options.challenge });

  return options;
}

async function finishPasskeyRegistration(userId: string, response: any) {
  const session = await sessionStore.get(userId);

  const verification = await verifyRegistrationResponse({
    response,
    expectedChallenge: session.challenge,
    expectedOrigin: ORIGIN,
    expectedRPID: RP_ID,
  });

  if (verification.verified && verification.registrationInfo) {
    await db.credentials.create({
      userId,
      credentialId: verification.registrationInfo.credentialID,
      publicKey: verification.registrationInfo.credentialPublicKey,
      counter: verification.registrationInfo.counter,
    });
  }

  return verification.verified;
}
```

### Step 6: Implement Role-Based Access Control (RBAC)

**RBAC Middleware (Express.js)**:

```typescript
// ── Permission Model ──────────────────────────────────────────────

interface Role {
  name: string;
  permissions: string[];
}

const ROLES: Record<string, Role> = {
  admin: {
    name: 'admin',
    permissions: ['users:read', 'users:write', 'users:delete',
                  'orders:read', 'orders:write', 'orders:delete',
                  'reports:read', 'settings:write'],
  },
  manager: {
    name: 'manager',
    permissions: ['users:read', 'orders:read', 'orders:write', 'reports:read'],
  },
  viewer: {
    name: 'viewer',
    permissions: ['orders:read', 'reports:read'],
  },
};

// ── Authorization Middleware ──────────────────────────────────────

function requirePermission(...requiredPermissions: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userRole = req.session?.role;

    if (!userRole) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    const role = ROLES[userRole];
    if (!role) {
      return res.status(403).json({ error: 'Unknown role' });
    }

    const hasPermission = requiredPermissions.every(
      perm => role.permissions.includes(perm)
    );

    if (!hasPermission) {
      return res.status(403).json({
        error: 'Insufficient permissions',
        required: requiredPermissions,
      });
    }

    next();
  };
}

// ── Route Usage ───────────────────────────────────────────────────

app.get('/api/orders', requirePermission('orders:read'), getOrders);
app.post('/api/orders', requirePermission('orders:write'), createOrder);
app.delete('/api/orders/:id', requirePermission('orders:delete'), deleteOrder);
app.get('/api/reports', requirePermission('reports:read'), getReports);
app.delete('/api/users/:id', requirePermission('users:delete'), deleteUser);
```

**Attribute-Based Access Control (ABAC) Example**:

```typescript
interface PolicyContext {
  user: { id: string; role: string; department: string };
  resource: { ownerId: string; type: string; classification: string };
  action: string;
  environment: { time: Date; ipAddress: string };
}

function evaluatePolicy(ctx: PolicyContext): boolean {
  const policies = [
    // Admins can do anything
    (c: PolicyContext) => c.user.role === 'admin',

    // Users can read their own resources
    (c: PolicyContext) =>
      c.action === 'read' && c.resource.ownerId === c.user.id,

    // Managers can write resources in their department
    (c: PolicyContext) =>
      c.user.role === 'manager' &&
      c.action === 'write' &&
      c.resource.classification !== 'confidential',

    // No access to confidential resources outside business hours
    (c: PolicyContext) => {
      if (c.resource.classification === 'confidential') {
        const hour = c.environment.time.getHours();
        return hour >= 8 && hour <= 18;
      }
      return true;
    },
  ];

  return policies.some(policy => policy(ctx));
}
```

### Step 7: Configure Security Headers

```typescript
import helmet from 'helmet';

app.use(helmet({
  // Content Security Policy: prevent XSS and data injection
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'strict-dynamic'"],
      styleSrc: ["'self'", "'unsafe-inline'"],  // Consider nonces for stricter CSP
      imgSrc: ["'self'", "data:", "https://cdn.example.com"],
      connectSrc: ["'self'", "https://api.example.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],          // Prevent clickjacking
      baseUri: ["'self'"],
      formAction: ["'self'"],
      upgradeInsecureRequests: [],
    },
  },

  // HSTS: force HTTPS for 1 year including subdomains
  strictTransportSecurity: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },

  // Prevent MIME type sniffing
  xContentTypeOptions: true,   // X-Content-Type-Options: nosniff

  // Referrer policy
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },

  // Permissions policy
  permittedCrossDomainPolicies: { permittedPolicies: 'none' },
}));

// ── CORS Configuration ────────────────────────────────────────────

import cors from 'cors';

app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,             // Allow cookies in cross-origin requests
  maxAge: 86400,                 // Cache preflight for 24 hours
}));
```

### Step 8: Prevent Common Vulnerabilities

**CSRF Protection**:

```typescript
import csrf from 'csurf';

// For cookie-based sessions, use double-submit cookie pattern
app.use(csrf({
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
  },
}));

// Include CSRF token in responses for forms/SPAs
app.get('/api/csrf-token', (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});
```

**Session Fixation Prevention**:

```typescript
// Always regenerate session ID after authentication state changes
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  // Destroy old session and create new one
  const oldSession = { ...req.session };
  req.session.regenerate((err) => {
    if (err) return res.status(500).json({ error: 'Session error' });
    // Copy non-sensitive data from old session if needed
    req.session.userId = user.id;
    req.session.role = user.role;
    res.json({ message: 'Authenticated' });
  });
});
```

**Token Theft Mitigation**:

```typescript
// Bind tokens to client fingerprint
function createBoundToken(userId: string, clientFingerprint: string): string {
  return jwt.sign(
    {
      sub: userId,
      fpt: crypto.createHash('sha256').update(clientFingerprint).digest('hex'),
    },
    PRIVATE_KEY,
    { algorithm: 'RS256', expiresIn: '15m' }
  );
}

// Validate fingerprint on each request
function validateBoundToken(token: string, clientFingerprint: string): boolean {
  const decoded = jwt.verify(token, PUBLIC_KEY) as any;
  const expectedFpt = crypto.createHash('sha256').update(clientFingerprint).digest('hex');
  return decoded.fpt === expectedFpt;
}
```

## Best Practices

- **Use PKCE for all OAuth flows**: Even confidential clients benefit from PKCE as defense-in-depth
- **Short-lived access tokens**: 5-15 minutes; use refresh tokens for longer sessions
- **Rotate refresh tokens**: Issue a new refresh token on every use; detect reuse attacks
- **Store tokens in HttpOnly cookies**: Not localStorage or sessionStorage
- **Use Argon2id for passwords**: OWASP-recommended; bcrypt is acceptable but Argon2id is stronger
- **Never store plaintext passwords**: This rule has no exceptions
- **Regenerate session IDs**: After login, logout, privilege escalation, and periodically
- **Implement rate limiting on auth endpoints**: Prevent brute-force attacks
- **Log all authentication events**: Successful logins, failures, MFA challenges, token refreshes
- **Use SameSite cookies**: Set to `Lax` or `Strict` to prevent CSRF
- **Validate JWT claims thoroughly**: Always check `iss`, `aud`, `exp`, and `nbf`
- **Use asymmetric signing (RS256)**: Allows resource servers to validate without the signing key

## Common Patterns

### Pattern 1: API Key with Rate Limiting

```typescript
// API key middleware with per-key rate limiting
const rateLimiter = new Map<string, { count: number; resetAt: number }>();

function apiKeyAuth(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'] as string;
  if (!apiKey) return res.status(401).json({ error: 'API key required' });

  // Validate key and get associated client
  const client = await db.apiKeys.findByKey(hashApiKey(apiKey));
  if (!client) return res.status(401).json({ error: 'Invalid API key' });

  // Rate limiting per key
  const now = Date.now();
  const limit = rateLimiter.get(client.id) || { count: 0, resetAt: now + 60000 };
  if (now > limit.resetAt) {
    limit.count = 0;
    limit.resetAt = now + 60000;
  }
  limit.count++;
  rateLimiter.set(client.id, limit);

  if (limit.count > client.rateLimit) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }

  req.client = client;
  next();
}
```

### Pattern 2: Scope-Based Authorization for APIs

```typescript
function requireScope(...requiredScopes: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'Token required' });

    try {
      const decoded = await validateAccessToken(token);
      const tokenScopes = (decoded.scope || '').split(' ');

      const hasScope = requiredScopes.every(s => tokenScopes.includes(s));
      if (!hasScope) {
        return res.status(403).json({
          error: 'insufficient_scope',
          required: requiredScopes,
          provided: tokenScopes,
        });
      }

      req.user = decoded;
      next();
    } catch (err) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  };
}

// Usage
app.get('/api/orders', requireScope('orders:read'), getOrders);
app.post('/api/orders', requireScope('orders:write'), createOrder);
```

## Quality Checklist

- [ ] OAuth 2.0 flow uses PKCE (even for confidential clients)
- [ ] Access tokens are short-lived (5-15 minutes)
- [ ] Refresh token rotation implemented with reuse detection
- [ ] Passwords hashed with Argon2id or bcrypt (cost factor >= 12)
- [ ] Session IDs regenerated after authentication state changes
- [ ] Cookies use Secure, HttpOnly, SameSite attributes
- [ ] CSRF protection implemented for cookie-based auth
- [ ] JWT validation checks iss, aud, exp, and algorithm
- [ ] MFA available for all user accounts
- [ ] Security headers configured (CSP, HSTS, CORS)
- [ ] Rate limiting applied to login and token endpoints
- [ ] Authentication events logged for audit trail
- [ ] API keys are hashed before storage (never stored in plaintext)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We can skip PKCE because our client is confidential" | Authorization code interception attacks (via open redirects or referrer headers) are possible even with confidential clients; PKCE prevents code replay at zero implementation cost. |
| "JWTs are stateless so we don't need refresh token rotation" | Without rotation, a stolen refresh token grants indefinite access until expiry; rotation with reuse detection (family-based revocation) limits the window to a single use, as demonstrated by the approach recommended after the Auth0 token reuse incidents. |
| "bcrypt with cost 10 is fine for new projects" | Cost 10 was calibrated for ~2012 hardware; modern GPUs can test billions of candidates per second — cost 12 or Argon2id is the current OWASP minimum. |
| "We store access tokens in localStorage because it's simpler" | XSS in any third-party script on the page (analytics, chat widgets) can exfiltrate localStorage tokens silently; HttpOnly cookies are immune to JavaScript access. |
| "Session ID regeneration after login is optional" | Session fixation allows an attacker to pre-set a known session ID, then hijack it after the victim authenticates — a P0 vulnerability with trivial exploitation. |
| "We check authorization at the route level, which is sufficient" | Route-level checks prevent accessing the wrong endpoint; IDOR exploits occur at the data layer when a user passes a valid endpoint but with another user's resource ID, bypassing route guards entirely. |

## Verification

- [ ] OAuth 2.0 flows use PKCE (`code_challenge_method: S256`) confirmed in code or config
- [ ] Refresh token rotation is implemented and reuse detection revokes the token family on replay
- [ ] Password hashing uses Argon2id or bcrypt with cost >= 12 (verified in source, not just docs)
- [ ] All session cookies have `Secure`, `HttpOnly`, and `SameSite` attributes set in code
- [ ] JWT validation explicitly checks `iss`, `aud`, `exp`, and `alg` — no `none` algorithm accepted
- [ ] Rate limiting is applied to the login endpoint (verified by attempting >10 requests/minute)

## Related Skills

- `security-review` - Application security assessment including auth review
- `pre-commit-checklist` - Security checks before committing auth code
- `dependency-security-audit` - Auditing auth library vulnerabilities
- `cicd-architect` - Securing CI/CD pipelines with service accounts and tokens

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
