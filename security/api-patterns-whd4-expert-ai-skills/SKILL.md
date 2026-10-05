---
name: api-patterns
description: API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# API Patterns

> API design principles and decision-making for 2025.
> **Learn to THINK, not copy fixed patterns.**

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

---

## 📑 Content Map

| File | Description | When to Read |
|------|-------------|--------------|
| `api-style.md` | REST vs GraphQL vs tRPC decision tree | Choosing API type |
| `rest.md` | Resource naming, HTTP methods, status codes | Designing REST API |
| `response.md` | Envelope pattern, error format, pagination | Response structure |
| `graphql.md` | Schema design, when to use, security | Considering GraphQL |
| `trpc.md` | TypeScript monorepo, type safety | TS fullstack projects |
| `versioning.md` | URI/Header/Query versioning | API evolution planning |
| `auth.md` | JWT, OAuth, Passkey, API Keys | Auth pattern selection |
| `rate-limiting.md` | Token bucket, sliding window | API protection |
| `documentation.md` | OpenAPI/Swagger best practices | Documentation |
| `security-testing.md` | OWASP API Top 10, auth/authz testing | Security audits |

## 🧠 Decision Matrix (Expert)

| Style | Best For | Pros | Cons |
|-------|----------|------|------|
| **REST** | Public APIs, Simple CRUD | Caching, Universal support | Over-fetching, multiple round-trips |
| **GraphQL** | Complex Frontends, Mobile Apps | Single request, Flexible data | Complexity, N+1 queries, Harder caching |
| **tRPC** | TypeScript Monorepos (Next.js) | End-to-end type safety, Speed | Tight coupling (Frontend+Backend) |
| **gRPC** | Microservices (Internal) | High performance (Protobuf), Streaming | Browser support is weak (requires proxy) |

## 🛡️ Robustness Patterns

### Idempotency

**Problem:** User clicks "Pay" twice. You charge them twice.
**Solution:** Client sends `Idempotency-Key: <uuid>`.

1. Server checks Redis: `GET idempotency:<uuid>`.
2. If exists: Return cached 200 OK immediately.
3. If new: Process charge, save result to Redis, return 200 OK.

### Rate Limiting (Algorithms)

| Algorithm | How it works | Pros | Cons |
|-----------|--------------|------|------|
| **Fixed Window** | "100 reqs per hour" (resets at :00) | Simple | Stampede at window reset |
| **Sliding Window** | Smoothed over time | Fairer | More Redis memory needed |
| **Token Bucket** | "Bucket of coins", refill at rate X | Allows bursts (good for users) | Complex implementation |

---

## 🔗 Related Skills

| Need | Skill |
|------|-------|
| API implementation | `@[skills/backend-development]` |
| Data structure | `@[skills/database-design]` |
| Security details | `@[skills/security-hardening]` |

---

## ✅ Decision Checklist

Before designing an API:

- [ ] **Asked user about API consumers?**
- [ ] **Chosen API style for THIS context?** (REST/GraphQL/tRPC)
- [ ] **Defined consistent response format?**
- [ ] **Planned versioning strategy?**
- [ ] **Considered authentication needs?**
- [ ] **Planned rate limiting?**
- [ ] **Documentation approach defined?**

---

## ❌ Anti-Patterns

**DON'T:**

- Default to REST for everything
- Use verbs in REST endpoints (/getUsers)
- Return inconsistent response formats
- Expose internal errors to clients
- Skip rate limiting

**DO:**

- Choose API style based on context
- Ask about client requirements
- Document thoroughly
- Use appropriate status codes

---

## Script

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/api_validator.py` | API endpoint validation | `python scripts/api_validator.py <project_path>` |
