---
name: api-security
description: Apply the OWASP API Security Top 10 to REST and GraphQL endpoints. Covers broken object-level authorization (BOLA), mass assignment, excessive data exposure, unrestricted resource consumption, SSRF, broken function-level authorization, and GraphQL depth and complexity limits. Invoke when designing a new API, reviewing one before scaling, or after API abuse (scraping, account takeover).
---

# API Security

Web-app and API security overlap but are not the same. APIs ship with different defaults (CORS-permissive, no CSRF tokens, often no rate-limiting), different consumers (mobile apps, integrations, scripts — not just browsers), and a different attack surface (object IDs in URLs, JSON bodies, scoped tokens). The **OWASP API Security Top 10 (2023 edition)** is the canonical reference; this skill walks each item with concrete detection and fix patterns.

## When to invoke

- Designing a new REST or GraphQL API
- Reviewing an existing API before scaling user count
- After abuse — scraping, account takeover, suspicious 4xx/5xx patterns
- Adding a public-facing endpoint to a previously internal service
- An API is feeding a mobile or single-page app where the client cannot be trusted
- Periodic API audit (quarterly is reasonable)

## API01:2023 — Broken Object Level Authorization (BOLA)

**The #1 API vulnerability and not even close.** Every endpoint that takes an ID and returns the corresponding resource must check the caller is allowed to see *that specific* object.

```ts
// Bad — any authenticated user reads any invoice
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await db.invoices.findUnique({ where: { id: req.params.id }});
  res.json(invoice);
});

// Good — scoped to the requester's ownership
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await db.invoices.findFirst({
    where: { id: req.params.id, userId: req.user.id }
  });
  if (!invoice) return res.status(404).json({ error: 'not found' });
  res.json(invoice);
});
```

Detection in a codebase:

```bash
# Every parameterized route is a BOLA candidate. Walk them.
grep -rEn ":id|:slug|:uuid" src/routes src/api app 2>/dev/null

# Routes that fetch by primary key alone — high-suspicion pattern
grep -rEn 'findUnique\\(\\{\\s*where:\\s*\\{\\s*id:' --include='*.{ts,js}' . | head
```

Patterns that make BOLA harder to introduce:

- **Always include `userId` or `tenantId` in the `where` clause**, not just the resource ID
- **Use database row-level security (RLS)** as a backstop — Postgres RLS plus per-request `SET LOCAL app.current_user`. See [`postgres-hardening`](../postgres-hardening/SKILL.md).
- **Use opaque IDs** (UUIDs or hashids), not sequential integers. Doesn't fix BOLA but slows enumeration if it slips through.

## API02:2023 — Broken Authentication

Auth on APIs has its own failure modes beyond web-app auth.

- **Token validation skipped on health/info/debug endpoints** that grew to leak data
- **JWTs validated for signature but not for `iss`, `aud`, `exp`** — pin all three
- **No revocation path** for issued tokens — long-lived JWTs are session cookies you cannot recall
- **API keys with no expiry, no rotation, no scope** — issued once, lives forever, total power
- **Bearer tokens in URLs** (showing up in access logs, referer headers) — always in `Authorization` header

For password-based API auth specifically:

- Same patterns as web auth — see [`auth-hardening`](../auth-hardening/SKILL.md)
- Per-IP and per-account rate-limiting on `/api/auth/login`
- MFA flow that works over API (TOTP code as a field; WebAuthn via session)
- Generic error on auth failure — never "user not found"

## API03:2023 — Broken Object Property Authorization

Two flavors:

### Mass assignment

```ts
// Bad — user can set their own role to admin
app.patch('/api/users/me', requireAuth, async (req, res) => {
  const updated = await db.users.update({
    where: { id: req.user.id },
    data: req.body,                    // ☠️ accepts arbitrary keys including 'role'
  });
  res.json(updated);
});

// Good — explicit allowlist of editable fields
const PROFILE_FIELDS = ['displayName', 'avatarUrl', 'timezone'];

app.patch('/api/users/me', requireAuth, async (req, res) => {
  const data = Object.fromEntries(
    Object.entries(req.body).filter(([k]) => PROFILE_FIELDS.includes(k))
  );
  const updated = await db.users.update({ where: { id: req.user.id }, data });
  res.json(updated);
});
```

Better: validate with a schema library (Zod, Valibot, class-validator) and let it reject unknown keys.

### Excessive data exposure

API returns the whole DB row when the consumer needs three fields. Browser-facing this leaks PII; mobile-app-facing the same leak is in production traffic forever.

```ts
// Bad
const user = await db.users.findUnique({ where: { id }});
return user;   // includes password_hash, email_verified_at, internal_notes, ...

// Good — explicit projection
const user = await db.users.findUnique({
  where: { id },
  select: { id: true, displayName: true, avatarUrl: true },
});
```

For GraphQL: the schema *is* the contract. Treat every field on every type as "is this safe to expose to this kind of caller?"

## API04:2023 — Unrestricted Resource Consumption

DoS via expensive operations. APIs are easier to DoS than web apps because each request can deliberately ask for more work.

Defenses, all of which you need:

- **Rate limiting** — per IP, per user, per endpoint. Cheap to add, eliminates the easy attacks.

  ```ts
  // Express + express-rate-limit
  import rateLimit from 'express-rate-limit';
  app.use('/api/', rateLimit({
    windowMs: 60_000, max: 100,
    standardHeaders: 'draft-7', legacyHeaders: false,
  }));
  app.use('/api/auth/login', rateLimit({ windowMs: 60_000, max: 5, skipSuccessfulRequests: true }));
  ```

- **Body size limits** — `app.use(express.json({ limit: '100kb' }))`. The default of 1MB is too generous for most APIs.
- **Request timeout** — 10–30s max for any endpoint. Long-running work goes to a queue.
- **Pagination caps** — `limit=10000` is not pagination, it is "give me everything." Cap server-side at 100 or so.
- **Query complexity for GraphQL** — `graphql-depth-limit` + `graphql-query-complexity`. Without these, `{ user { friends { friends { friends { ... } } } } }` brings the DB down.
- **Cost-aware operations** — anything that touches an external paid API (email send, SMS, AI) needs its own budget cap per user per time window.

## API05:2023 — Broken Function Level Authorization

Admin / privileged endpoints reachable by non-admins. Common when:

- Admin routes are nested under `/api/admin/` but the auth check is at middleware level only — and a route was added later that bypasses middleware
- Mobile-app endpoints hide admin features client-side; the API still serves them to anyone with a token

Detection:

```bash
grep -rE '/api/admin' src 2>/dev/null
grep -rE 'role.*admin|isAdmin|requireAdmin' src 2>/dev/null
# Every admin route should have the role check in the handler, not just middleware
```

Same rule as elsewhere in this repo: **never rely on middleware alone**. Each privileged handler does its own check.

## API06:2023 — Unrestricted Access to Sensitive Business Flows

A specific subclass of resource consumption: even with rate limits, an attacker can scrape your "show me product X price" endpoint at 1 RPS for weeks. The data eventually leaves your system.

Examples in the wild:

- Booking sites scraped for hotel inventory
- E-commerce APIs scraped for product catalogs
- Review/ratings APIs scraped for user data
- "Refer a friend" flows automated for promo abuse

Mitigations require business-context decisions:

- **CAPTCHAs / proof of work** for high-value flows after first hit
- **Behavioral signals** (user-agent diversity, mouse movement patterns, ASN reputation) — Cloudflare Bot Fight / Turnstile is a free starting point
- **Account-level rate limiting** beyond IP — one user creating 1000 referrals per hour is suspicious even if from 1000 IPs
- **Pricing / catalog data** served via signed, time-limited URLs after auth, not as free GET endpoints

## API07:2023 — Server-Side Request Forgery (SSRF)

```ts
// Bad — fetches whatever the user says, including internal services
app.get('/api/preview', async (req, res) => {
  const url = req.query.url as string;
  const r = await fetch(url);
  res.send(await r.text());
});
```

Attacker submits `http://169.254.169.254/latest/meta-data/` (AWS metadata) or `http://localhost:6379/` (your Redis) and your server happily proxies.

Fix:

- **Allowlist destination hostnames** — only `https://known-customer-domains.example.com/*`
- **Resolve and validate the IP** before fetching — reject private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`, `::1`, `fc00::/7`)
- **Disable redirects** or revalidate at each hop — an allowed domain can 302 to a bad one
- **Run the fetcher in a network-isolated process** without access to internal services

For URL-fetching features, consider routing through a dedicated proxy service (e.g. Cloudflare Workers) that enforces the rules outside the app's trust boundary.

## API08:2023 — Security Misconfiguration

A grab bag, but the high-frequency ones:

- **CORS too permissive** — `Access-Control-Allow-Origin: *` on endpoints that return user data, or echoing back the `Origin` header unchanged
- **Verbose errors in production** — stack traces, DB errors, internal paths in 500 responses
- **`OPTIONS` / `TRACE` enabled** when not needed
- **Missing security headers** — `Strict-Transport-Security`, `X-Content-Type-Options`, etc. See [`site-server-audit`](../site-server-audit/SKILL.md).
- **Default credentials** somewhere in the stack (admin tools, DB admin UI, etc.)
- **Debug endpoints accessible** in production (`/debug`, `/__profile__`, `/_admin/inspect`)

Detection:

```bash
grep -rEn 'cors.*\\*|Access-Control-Allow-Origin.*\\*' --include='*.{js,ts,py}' .
grep -rEn 'NODE_ENV.*development|DEBUG.*True|app\\.debug' --include='*.{js,ts,py}' .
curl -sI https://api.example.com | grep -iE 'strict-transport|x-content-type|x-frame'
```

## API09:2023 — Improper Inventory Management

The API you forgot about is the one that gets exploited:

- **Old `/v1/*` endpoints** still live after the app moved to `/v2/*`
- **Staging environments** with prod-like data accessible from the internet
- **Mobile-app endpoints** still serving older app versions long after they're deprecated, with weaker auth
- **Internal endpoints** that became externally reachable when networking changed

Mitigations:

- **Inventory all hosts and endpoints** quarterly. `dig`, `subfinder`, your DNS records, your reverse-proxy config
- **Sunset old API versions** with concrete dates communicated to consumers
- **Stage-prod separation** at the network layer, not just hope
- **Robots/sitemap discipline** — your sitemap should not list `/api/*`

## API10:2023 — Unsafe Consumption of APIs

Your API calls third-party APIs (Stripe, SendGrid, OpenAI, weather, etc.). Treat third-party responses as untrusted input.

- **Validate the response** — schema-check, range-check, length-check. Do not blindly pipe into your DB.
- **TLS verification on** — never `rejectUnauthorized: false` in production
- **Timeouts** — third-party slowness becomes your outage if you wait forever
- **Circuit breakers** for repeatedly-failing third parties — fail fast, fall back gracefully
- **Secret hygiene** — third-party API keys are secrets, treat them as such ([`secret-hygiene`](../secret-hygiene/SKILL.md))

## GraphQL-specific patterns

GraphQL adds attack surface even when REST patterns are addressed:

- **Introspection on in production** — turn off unless you need the playground for a reason
- **Field-level authorization** is the explicit responsibility of resolvers — `@auth` directives are good
- **N+1 query patterns** become DoS — `DataLoader` is essentially mandatory
- **Query depth limit** — most schemas should cap at 8–10 levels
- **Query complexity limit** — assign cost per field; total cap per request
- **Aliasing for amplification** — one query can request the same expensive field 100 times with aliases; limit alias count too

```ts
import depthLimit from 'graphql-depth-limit';
import { createComplexityRule } from 'graphql-query-complexity';

const server = new ApolloServer({
  schema,
  validationRules: [
    depthLimit(10),
    createComplexityRule({ maximumComplexity: 1000, /* ... */ }),
  ],
  introspection: process.env.NODE_ENV !== 'production',
});
```

## API design patterns that prevent classes of issues

- **Resource scoping in URLs** — `/users/me/invoices/:id` instead of `/invoices/:id`. Forces the design to think about who owns the resource.
- **Standard pagination** — cursor-based, server-controlled page size, with documented limits
- **Consistent error format** — `{ error: { code, message } }` with sanitized messages, codes mapped to client behavior
- **Versioning explicit in the URL** — `/api/v1/`, `/api/v2/`. Forces deprecation discipline.
- **OpenAPI / GraphQL schema as contract** — every endpoint is documented; what isn't documented isn't supposed to be reachable.
- **`Content-Type: application/json` enforced** on POST/PUT/PATCH — rejects naive form-encoded probes

## Quick audit checklist

Walk every endpoint against:

- [ ] Auth required? Owner/role check in the handler (not just middleware)?
- [ ] Input validated against a schema?
- [ ] Output projection explicit — no leaking internal fields?
- [ ] Rate limit applied at per-endpoint or per-user level?
- [ ] Body size capped?
- [ ] Timeouts set?
- [ ] No SSRF: user-supplied URLs allowlisted before fetching?
- [ ] CORS scoped to known origins, not `*`?
- [ ] Errors are generic in production?
- [ ] If GraphQL: depth + complexity limits, introspection off in prod?
- [ ] Versioned and dated for sunset?
- [ ] Documented in your API catalog?

Anything you cannot answer → finding.

## What this skill will not do

- Help test or exploit APIs you do not own
- Recommend disabling auth, CORS, or rate-limiting "for the dev environment that's also publicly reachable"
- Endorse trusting the client (browser, mobile app) for security-relevant checks
