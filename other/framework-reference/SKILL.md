---
name: framework-reference
description: Index of cloned framework repos for Maks's reference during builds.
---

# Framework Reference Repos

Cloned repositories available locally for searching API patterns, source code, and documentation.

---

## Repo Index

| Repo | Path | What It Contains | Primary Use |
|------|------|-----------------|-------------|
| **supabase-docs** | `repos/supabase-docs` | Official Supabase documentation (MDX), guides, API references, examples | Auth flows, RLS patterns, Edge Functions, Realtime, Storage, SSR |
| **next-auth** | `repos/next-auth` | Auth.js (NextAuth) v5 source code, providers, adapters, core logic | OAuth providers, session strategies, JWT callbacks, middleware |
| **tanstack-query** | `repos/tanstack-query` | TanStack Query source code and docs — React Query, Solid Query, etc. | useQuery, useMutation, useInfiniteQuery, prefetching, SSR |
| **stripe-sdk** | `repos/stripe-sdk` | Official Stripe Node.js/TypeScript SDK source | Checkout, subscriptions, webhooks, customer portal, types |
| **react-email** | `repos/react-email` | React Email component library source and examples | Email components (Html, Body, Button, etc.), rendering |
| **drizzle-orm** | `repos/drizzle-orm` | Drizzle ORM source code, drivers, and documentation | Schema definition, queries, relations, migrations, pg driver |

---

## How to Search

### Search All Repos for a Pattern

```bash
# Find any file mentioning "createServerClient"
grep -r "createServerClient" repos/ --include="*.ts" --include="*.tsx" --include="*.md" -l

# Find RLS policy examples in Supabase docs
grep -r "CREATE POLICY" repos/supabase-docs/ --include="*.mdx" --include="*.md" -l

# Search for a specific API in TanStack Query
grep -r "useInfiniteQuery" repos/tanstack-query/packages/ --include="*.ts" -l
```

### Search Specific Repos

```bash
# Supabase: auth SSR patterns
grep -r "getClaims\|getUser\|getSession" repos/supabase-docs/ --include="*.mdx" -l

# Supabase: edge function examples
grep -r "Deno.serve" repos/supabase-docs/ --include="*.mdx" --include="*.ts" -l

# Stripe: webhook handling
grep -r "constructEvent\|webhook" repos/stripe-sdk/src/ --include="*.ts" -l

# Stripe: checkout session types
grep -r "CheckoutSession\|checkout.sessions" repos/stripe-sdk/src/ --include="*.ts" -l

# TanStack Query: query options and hooks
grep -r "queryKey\|queryFn\|staleTime" repos/tanstack-query/packages/react-query/src/ --include="*.ts" -l

# Drizzle: schema helpers and column types
grep -r "pgTable\|uuid\|text\|timestamp" repos/drizzle-orm/drizzle-orm/src/pg-core/ --include="*.ts" -l

# Drizzle: migration tooling
grep -r "migrate\|generate\|push" repos/drizzle-orm/docs/ --include="*.md" -l

# NextAuth: provider configuration
grep -r "providers\|GitHub\|Google\|Credentials" repos/next-auth/packages/ --include="*.ts" -l

# React Email: component props
grep -r "interface.*Props" repos/react-email/packages/ --include="*.tsx" --include="*.ts" -l
```

### Find Source Files by Pattern

```bash
# List all TypeScript source files in a repo
find repos/stripe-sdk/src -name "*.ts" | head -30

# Find specific component files
find repos/react-email/packages -name "*.tsx" | grep -i button

# Find test files for a feature
find repos/tanstack-query/packages -name "*.test.*" | grep -i mutation
```

---

## Related Skills

For detailed usage patterns with code examples, see these companion skills:

| Skill | Description |
|-------|-------------|
| `supabase-deep` | Auth, RLS, Edge Functions, Realtime, Storage |
| `stripe-payments` | Checkout, subscriptions, webhooks, portal |
| `tanstack-query` | Data fetching, caching, mutations, SSR |
| `auth-patterns` | Supabase Auth + Auth.js patterns for Next.js |
| `drizzle-orm` | Schema, queries, relations, migrations |
| `react-email` | Email templates + Resend integration |

---

## Web Fallback URLs

When the local repos don't have what you need, fetch from these official sources:

| Framework | Documentation URL |
|-----------|------------------|
| Supabase | `https://supabase.com/docs` |
| Stripe | `https://docs.stripe.com` |
| TanStack Query | `https://tanstack.com/query/latest/docs` |
| Drizzle ORM | `https://orm.drizzle.team/docs/overview` |
| React Email | `https://react.email/docs` |
| Auth.js | `https://authjs.dev` |
| Next.js | `https://nextjs.org/docs` |

---

## Repo Maintenance

These repos are cloned snapshots. To update:

```bash
cd repos/supabase-docs && git pull origin main
cd repos/tanstack-query && git pull origin main
cd repos/stripe-sdk && git pull origin master
cd repos/drizzle-orm && git pull origin main
cd repos/react-email && git pull origin main
cd repos/next-auth && git pull origin main
```
