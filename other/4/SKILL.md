---
name: security-controls
description: Use this skill whenever writing authentication middleware, file upload handlers, API endpoints, secrets access, dependency management, input validation, or any code with a security surface in the Myelin platform. This is the authoritative security implementation contract aligned to OWASP ASVS. Do not implement security controls from intuition — load this skill first.
---

This skill defines the minimum security controls for the Myelin platform. It is aligned to OWASP ASVS Level 2. Every control listed here is required before production release. Security is not a phase — it is a constraint on every code path from day one.

---

## Transport Security

- TLS 1.2 minimum on all connections. TLS 1.3 preferred.
- HSTS header required: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- Redirect all HTTP to HTTPS at the load balancer layer — do not handle redirects in application code.
- No mixed content. All static assets, API calls, and media references must use HTTPS.
- Certificate pinning is not required for v1 web application but is required for any future native app.

---

## Encryption at Rest

- Database: encrypt at the storage layer (cloud provider managed encryption minimum).
- Object storage (evidence files, result PDFs): server-side encryption enabled on all buckets.
- Secrets (API keys, database credentials, signing keys): stored in a dedicated secrets manager (e.g. AWS Secrets Manager, HashiCorp Vault). Never in environment variables committed to source control, never in application config files.
- Password hashing: Argon2id with minimum parameters `m=65536, t=3, p=4`. Do not use bcrypt for new implementations (still acceptable for migration compatibility only). Never use MD5, SHA-1, or unsalted SHA-256.

---

## API Security

### Authentication on every endpoint

Every API route except `/auth/login`, `/auth/register`, `/auth/reset`, and `/demo/*` requires a valid session token. Unauthenticated requests return `401`. No endpoint silently degrades to anonymous access.

```javascript
function authMiddleware(req, res, next) {
  const token = extractBearerToken(req);
  if (!token) return res.status(401).json({ error: 'UNAUTHENTICATED' });

  try {
    const session = verifyAccessToken(token);
    req.session = session;
    next();
  } catch {
    return res.status(401).json({ error: 'INVALID_TOKEN' });
  }
}
```

### Input validation

All user-supplied input must be validated at the API layer before any processing. Use a schema validation library (e.g. Zod, Joi). Never trust client-supplied data.

```javascript
// Example: simulation step event ingestion
const stepEventSchema = z.object({
  sessionId:    z.string().uuid(),
  stepId:       z.string().regex(/^LOTO_STEP_0[1-7]$/),
  measuredValue: z.number().finite(),
  timestamp:    z.string().datetime()
});

function validateStepEvent(body) {
  return stepEventSchema.parse(body); // throws ZodError on invalid input
}
```

Validation failures return `400` with a structured error. Never return raw validation error stack traces to the client.

### Rate limiting

Apply rate limits at the API gateway layer:

| Endpoint category | Limit |
|---|---|
| Auth endpoints (`/auth/*`) | 10 requests / minute per IP |
| AI agent chat | 30 requests / minute per user |
| File upload | 5 uploads / minute per user |
| Simulation event ingestion | 120 events / minute per session |
| All other endpoints | 300 requests / minute per user |

Rate limit responses return `429` with a `Retry-After` header.

### SQL injection prevention

Use parameterised queries exclusively. Never concatenate user input into SQL strings.

```javascript
// Correct
db.query('SELECT * FROM users WHERE tenant_id = $1 AND email = $2', [tenantId, email]);

// Never do this
db.query(`SELECT * FROM users WHERE email = '${email}'`); // injection risk
```

### CORS

Configure CORS to allow only the platform's own origin domains. Do not use wildcard `*` origins on any authenticated endpoint.

```javascript
const corsOptions = {
  origin: [
    'https://app.myelin.io',
    'https://demo.myelin.io',
    process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : null
  ].filter(Boolean),
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};
```

---

## File Upload Security

File uploads (e-Portfolio evidence submissions) require all of these controls before a file is accepted:

```javascript
async function validateUpload(file, session) {
  // 1. Type check — inspect magic bytes, not file extension
  const detectedType = await detectMimeType(file.buffer);
  const allowed = ['video/mp4', 'video/webm'];
  if (!allowed.includes(detectedType)) {
    throw new ValidationError('FILE_TYPE_NOT_ALLOWED');
  }

  // 2. Size limit — 500 MB default, configurable per tenant
  const maxBytes = getTenantUploadLimit(session.tenantId) || 500 * 1024 * 1024;
  if (file.size > maxBytes) {
    throw new ValidationError('FILE_TOO_LARGE');
  }

  // 3. Malware scan — async, using ClamAV or cloud scanner
  const scanResult = await scanForMalware(file.buffer);
  if (scanResult.infected) {
    await logSecurityEvent('MALWARE_DETECTED', session, { filename: file.originalname });
    throw new ValidationError('FILE_QUARANTINED');
  }

  return true;
}
```

Files are stored in object storage using a system-generated key — never the original filename. Access to stored files is via short-lived signed URLs only (TTL: 15 minutes). Never expose permanent public URLs to evidence files.

```javascript
function generateSignedUrl(objectKey, tenantId, expirySeconds = 900) {
  // Verify tenant ownership of the object before signing
  verifyObjectBelongsToTenant(objectKey, tenantId);
  return storageClient.getSignedUrl('getObject', {
    Bucket: process.env.EVIDENCE_BUCKET,
    Key:    objectKey,
    Expires: expirySeconds
  });
}
```

---

## Secrets Management

```javascript
// Load secrets at startup from secrets manager — never from process.env for sensitive values
async function loadSecrets() {
  return {
    dbConnectionString: await secretsManager.get('myelin/db/connection'),
    jwtSigningKey:      await secretsManager.get('myelin/auth/jwt-signing-key'),
    aiApiKey:           await secretsManager.get('myelin/ai/api-key'),
    storageCredentials: await secretsManager.get('myelin/storage/credentials')
  };
}
```

Key rotation policy:
- JWT signing keys: rotate every 90 days. Support two active keys during rotation window (old key validates existing tokens; new key signs new ones).
- Database credentials: rotate every 180 days or immediately on suspected compromise.
- AI API keys: rotate every 90 days.
- On rotation: old key must remain valid for one full access token TTL (15 minutes) before being deactivated.

---

## Security Headers

Apply on every HTTP response:

```javascript
function applySecurityHeaders(res) {
  res.setHeader('X-Content-Type-Options',   'nosniff');
  res.setHeader('X-Frame-Options',          'DENY');
  res.setHeader('X-XSS-Protection',         '0');       // disabled — use CSP instead
  res.setHeader('Referrer-Policy',          'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy',       'camera=(), microphone=(self), geolocation=()');
  res.setHeader('Content-Security-Policy',  buildCSP());
}

function buildCSP() {
  return [
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",    // unsafe-inline needed for Three.js shader injection
    "img-src 'self' data: blob:",
    "media-src 'self' blob: https://content.myelin.io",
    "connect-src 'self' https://api.anthropic.com",
    "worker-src blob:",
    "frame-ancestors 'none'"
  ].join('; ');
}
```

`microphone=(self)` is the only hardware permission allowed — required for LIVE_CONVERSATIONAL agent mode when enabled.

---

## SAST, DAST, and Dependency Scanning

These are release gate requirements (see `release-gate-checklist` skill). Implementation requirements:

- SAST: run on every pull request. Block merge on HIGH or CRITICAL findings.
- Dependency scanning: run on every build. Block deployment on known CVEs with CVSS >= 7.0 in direct dependencies.
- DAST: run against staging before every production release. OWASP ZAP or equivalent.
- Secret scanning: run on every commit. Block push on detected secrets (API keys, credentials, private keys).

No production release without all four gates passing.

---

## Session Token Security

```javascript
function signAccessToken(session) {
  return jwt.sign(
    {
      sub:      session.userId,
      tid:      session.tenantId,
      role:     session.role,
      jti:      generateUUID()     // unique token ID — enables per-token revocation
    },
    secrets.jwtSigningKey,
    {
      algorithm: 'RS256',          // asymmetric — private key signs, public key verifies
      expiresIn: '15m'
    }
  );
}
```

Use RS256 (asymmetric). Do not use HS256 (symmetric) — a compromised verification service cannot forge tokens with RS256.

`jti` (JWT ID) must be stored server-side to support immediate token revocation. On revocation, add the `jti` to a revocation list checked on every token verification.

---

## AI Safety Controls

The AI agent pipeline has specific security requirements:

- **Prompt injection defence**: sanitise all user-supplied content before inclusion in system prompts. Strip any content that attempts to override the system prompt or claim to be Anthropic/system instructions.
- **Response moderation**: apply a content moderation check to agent responses before delivery. Flag and hold any response containing safety-critical procedural instructions that bypass policy.
- **Sensitive data filtering**: the agent must never reflect back PII from the session context in its response text. The `learnerId`, `tenantId`, and `sessionId` are in the context for routing — they must not appear verbatim in agent output.
- **Incident logging**: any agent response that triggers a `policyFlag` must also trigger a security incident log entry for operational review.

---

## What Not To Do

- Do not store secrets in environment variables committed to source control
- Do not use HS256 for JWT signing — use RS256
- Do not use MD5, SHA-1, or bcrypt for new password hashing — use Argon2id
- Do not use wildcard CORS origins on authenticated endpoints
- Do not accept file type from the file extension — inspect magic bytes
- Do not serve evidence files via permanent public URLs — use short-lived signed URLs
- Do not concatenate user input into SQL strings
- Do not deploy to production without SAST, DAST, dependency scanning, and secret scanning passing
- Do not allow the AI agent to reflect `learnerId`, `tenantId`, or `sessionId` in response text
