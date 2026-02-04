---
name: authhub
description: Use when implementing authentication, user management, organization/tenant management, team invitations, role-based access control (RBAC), or multi-tenant architecture in a Supabase project. Provides complete schema, API templates, and frontend components for AuthHub-style authentication.
allowed-tools: []
---

# AuthHub - Multi-Tenant Authentication System

A complete authentication and organization management system for Supabase projects. Use this skill when implementing:

- User signup/signin
- Organization (tenant) creation
- Multi-tenant data isolation
- Team invitations
- Role-based access control (RBAC)
- Organization switching
- Permission management

## Explicit Triggers

- `authhub`
- `authentication setup`
- `multi-tenant`
- `org switching`
- `team invitations`
- `RBAC`
- `tenant management`

## Quick Start

1. **Database Schema**: See [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) - Run migrations first
2. **Supabase Config**: See [SUPABASE_CONFIG.md](./SUPABASE_CONFIG.md) - Configure auth settings
3. **API Templates**: See [API_TEMPLATES.md](./API_TEMPLATES.md) - Copy and customize
4. **Frontend Setup**: See [FRONTEND_SETUP.md](./FRONTEND_SETUP.md) - React context and hooks
5. **Checklist**: See [IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md) - Track progress

---

## Deployment Modes

AuthHub supports two deployment modes. **Choose based on your use case:**

### Mode 1: Standalone App (Most Common)

**Use this if:** Building a single SaaS product with its own Supabase project.

```
┌─────────────────────────────────────────────────────────┐
│                  Your Supabase Project                   │
├─────────────────────────────────────────────────────────┤
│  AuthHub Tables (public schema)                         │
│  ├── products (your single product entry)               │
│  ├── user_profiles                                      │
│  ├── tenants (organizations)                            │
│  ├── user_tenants                                       │
│  ├── roles (for your product)                           │
│  └── user_role_assignments                              │
├─────────────────────────────────────────────────────────┤
│  Product Tables (public schema with RLS)                │
│  ├── customers (has organization_id + RLS)              │
│  ├── orders (has organization_id + RLS)                 │
│  └── ... all your product tables                        │
└─────────────────────────────────────────────────────────┘
```

**Characteristics:**
- Single Supabase project per product
- Still uses `products` table (for future central AuthHub integration)
- Product tables in `public` schema with `organization_id` column
- RLS policies filter data by organization
- Queries include `product_id` filter (your single product)

### Mode 2: Multi-Product Platform

**Use this if:** Multiple products share the same Supabase database (like DataSwim + Onboard).

```
┌─────────────────────────────────────────────────────────┐
│               Shared Supabase Project                    │
├─────────────────────────────────────────────────────────┤
│  AuthHub Tables (public schema)                         │
│  ├── products (DataSwim, Onboard, etc.)                 │
│  ├── user_profiles                                      │
│  ├── tenants                                            │
│  ├── user_tenants                                       │
│  ├── roles (per product)                                │
│  └── user_role_assignments (includes product_id)        │
├─────────────────────────────────────────────────────────┤
│  Product A Tables    │    Product B Tables              │
│  (public or schema)  │    (public or schema)            │
└─────────────────────────────────────────────────────────┘
```

**Characteristics:**
- Single Supabase project shared by multiple products
- Each product has unique `product_id`
- All queries MUST filter by `product_id`
- Enables cross-product features and central management

### Future: Central AuthHub Dashboard

By keeping the `products` table in all deployments, we enable future capabilities:
- Central dashboard to view all products across the ecosystem
- API integration to sync product/user data
- Cross-product analytics and management
- Single sign-on across products (future feature)

---

## Data Isolation Strategies

### Strategy 1: RLS with organization_id (RECOMMENDED)

**Best for:** Most SaaS applications with fixed schemas.

Every product table includes `organization_id` and RLS policies:

```sql
-- Example: customers table
CREATE TABLE public.customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES public.tenants(id),
  name TEXT NOT NULL,
  email TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their org's customers"
ON public.customers FOR SELECT
USING (
  organization_id IN (
    SELECT tenant_id FROM public.user_tenants
    WHERE user_id = auth.uid() AND is_active = true
  )
);
```

**Pros:**
- Simple to implement
- Standard PostgreSQL pattern
- Easy to query across organizations (for admin dashboards)
- Works with Supabase's built-in RLS

**Cons:**
- All tenants share table structure
- Large tables may need additional indexing

### Strategy 2: Schema-per-tenant (Advanced)

**Best for:** Applications where tenants define their own data structures (like DataSwim).

Each organization gets its own PostgreSQL schema:

```sql
-- Creates: tenant_abc123def456...
SELECT create_tenant_schema('abc123-def4-5678-...');
```

**Pros:**
- Complete data isolation
- Tenants can have different table structures
- Easier to export/delete tenant data

**Cons:**
- More complex to manage
- Can't easily query across tenants
- Schema migrations must run per-tenant

**When to use Schema-per-tenant:**
- Users create their own database tables (like DataSwim)
- Regulatory requirements demand physical data isolation
- Per-tenant backup/restore requirements

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Supabase Auth                         │
│              (auth.users - managed by Supabase)          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   public.user_profiles                   │
│         (extended user info, links to auth.users)        │
└─────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌─────────────────────┐     ┌─────────────────────────────┐
│  public.user_tenants │     │ public.user_role_assignments │
│  (user ↔ org link)   │     │ (user ↔ org ↔ product ↔ role)│
└─────────────────────┘     └─────────────────────────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    public.tenants                        │
│                    (organizations)                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│            Product Tables (with organization_id)         │
│     customers, orders, projects, etc. + RLS policies     │
└─────────────────────────────────────────────────────────┘
```

## Key Concepts

### 1. Product-Scoped Roles
Each product has its own roles tied to a `product_id`. Even in standalone mode, keep this structure for future compatibility.

### 2. Junction Tables
NEVER query `tenants` directly for user access. Always go through:
- `user_tenants` - for user-org membership
- `user_role_assignments` - for roles (always filter by product_id)

### 3. Soft Deletes
All tables use `is_active` boolean. Never hard delete - set `is_active = false`.

### 4. Organization ID in Product Tables
Every product table should have `organization_id` column with appropriate RLS policies.

### 5. Always Filter by Product ID
Even in standalone apps, include `product_id` in queries. This ensures:
- Consistent patterns across all AuthHub implementations
- Future compatibility with central management
- Clean separation if you add another product later

---

## Tech Stack Assumptions

This skill assumes:
- **Framework**: Next.js 14/15 with App Router
- **Language**: TypeScript
- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **Deployment**: Netlify, Vercel, or similar

---

## Files in This Skill

| File | Purpose |
|------|---------|
| [DATABASE_SCHEMA.md](./DATABASE_SCHEMA.md) | Complete SQL migrations |
| [SUPABASE_CONFIG.md](./SUPABASE_CONFIG.md) | Supabase dashboard settings |
| [API_TEMPLATES.md](./API_TEMPLATES.md) | Next.js API route templates |
| [FRONTEND_SETUP.md](./FRONTEND_SETUP.md) | React context and components |
| [IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md) | Step-by-step checklist |
