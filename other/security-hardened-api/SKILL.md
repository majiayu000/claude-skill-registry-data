---
name: security-hardened-api
description: OWASP API Security Top 10 hardening, rate limiting, JWT validation, and input sanitization. Use when securing API endpoints, implementing authentication/authorization guards, preventing injection or broken object-level authorization (BOLA), or adding security headers.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: security-compliance-auth
---

# Security Hardened API

> **OWASP API Security Top 10, BOLA Defense, Rate Limiting & Zero-Trust Validation**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Prevent BOLA / IDOR (API1:2023)** | Never trust the client-supplied ID alone. Always verify that the authenticated user owns or has authorization to access the specific requested resource ID. |
| **Strict Request Validation** | Validate every parameter, query string, and body payload using strict schemas (Zod, class-validator) with strict stripping of unwhitelisted fields. |
| **Defensive Rate Limiting** | Apply multi-tier rate limiting (per-IP, per-user, and per-sensitive-endpoint like `/auth/login`) using token bucket algorithms. |
| **Safe Error Envelopes** | Never expose stack traces, database schema details, or raw SQL errors to API consumers. Return standardized sanitized error objects. |
| **HTTP Security Headers** | Enforce Helmet/CSP, HSTS, CORS with explicit origin whitelisting, and `no-cache` on sensitive endpoints. |

---

## 📋 Broken Object-Level Authorization (BOLA) Prevention Pattern

```typescript
// ❌ VULNERABLE: Direct object reference without ownership check
app.get('/api/documents/:id', async (req, res) => {
  const doc = await db.document.findUnique({ where: { id: req.params.id } });
  res.json(doc); // ANY user can view ANY document by ID!
});

// ✅ SECURE: Enforce tenant / user ownership boundary
app.get('/api/documents/:id', requireAuth, async (req, res) => {
  const doc = await db.document.findFirst({
    where: {
      id: req.params.id,
      tenantId: req.user.tenantId, // Scoped to authenticated tenant
      OR: [
        { ownerId: req.user.id },
        { permissions: { some: { userId: req.user.id, canRead: true } } }
      ]
    }
  });

  if (!doc) {
    return res.status(404).json({ error: 'Document not found' }); // Return 404 to avoid enumeration
  }
  res.json(doc);
});
```

---

## ❌ Anti-Patterns

- ❌ Storing JWTs in unencrypted `localStorage` (vulnerable to XSS). Use `HttpOnly`, `Secure`, `SameSite=Strict` cookies.
- ❌ Trusting headers like `X-Forwarded-For` without configuring trusted proxy hops.
- ❌ Using `cors({ origin: '*' })` on authenticated API endpoints.
