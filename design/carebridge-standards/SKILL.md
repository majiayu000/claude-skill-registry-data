---
name: carebridge-standards
description: Comprehensive coding standards and architectural patterns for the CareBridge eldercare management application. Includes critical patterns for case context management, Stripe integration, Next.js 15 requirements, component creation rules, and database operations. This skill should be used whenever working on the CareBridge codebase to ensure consistency and prevent common mistakes.
---

# CareBridge Development Standards

This skill provides comprehensive coding standards, architectural patterns, and best practices for developing the CareBridge application - a multi-case eldercare management SaaS platform.

## Overview

CareBridge has specific architectural patterns that MUST be followed to ensure:
- **Case context preservation** across all navigation
- **Consistent Stripe integration** for SaaS subscriptions and concierge packages
- **Next.js 15 compliance** with async request APIs
- **UI consistency** using shadcn/ui components only
- **Database security** with proper RLS policies and migrations

Breaking these patterns causes critical bugs, build errors, and scalability issues.

## When to Use This Skill

**ALWAYS use this skill when:**
- Adding new features to CareBridge
- Fixing bugs in the CareBridge codebase
- Creating new pages or components
- Implementing navigation or routing
- Working with Stripe payments
- Creating database migrations
- Reviewing or refactoring code

**Critical scenarios that require this skill:**
- Any page that displays case-specific data
- Any navigation component or link
- Any Stripe checkout or webhook code
- Any new UI component creation
- Any database schema changes

## Core Standards

### 🚨 Rule #1: NEVER Break Case Context

**Every navigation link, redirect, or router.push MUST preserve the `caseId` query parameter.**

Bad example:
```typescript
<Link href="/dashboard">Dashboard</Link>
```

Good example:
```typescript
const caseId = searchParams.get('caseId')
<Link href={caseId ? `/dashboard?caseId=${caseId}` : '/dashboard'}>Dashboard</Link>
```

See `references/case-context.md` for complete patterns.

### 🚨 Rule #2: NEVER Create Custom Components

**Always use shadcn/ui. Never create custom UI components.**

Bad example:
```typescript
export function CustomButton({ children }) {
  return <button className="custom-btn">{children}</button>
}
```

Good example:
```typescript
import { Button } from '@/components/ui/button'
<Button variant="default">{children}</Button>
```

Add components with: `npx shadcn@latest add button`

See `references/component-standards.md` for the complete list of available components.

### 🚨 Rule #3: ALWAYS Await Params in Next.js 15

**Next.js 15 requires awaiting params and searchParams.**

Bad example:
```typescript
export default function Page({ params }: { params: { id: string } }) {
  const { id } = params // ERROR!
}
```

Good example:
```typescript
type Props = { params: Promise<{ id: string }> }

export default async function Page({ params }: Props) {
  const { id } = await params
}
```

See `references/nextjs-15-patterns.md` for all Next.js 15 changes.

### 🚨 Rule #4: ALWAYS Use Metadata in Stripe Checkouts

**Stripe webhooks route based on metadata.package_type.**

Bad example:
```typescript
const session = await stripe.checkout.sessions.create({
  line_items: [...],
  mode: 'subscription',
})
```

Good example:
```typescript
const session = await stripe.checkout.sessions.create({
  line_items: [...],
  mode: 'subscription',
  metadata: {
    clerk_user_id: userId,
    package_type: 'concierge_plus',
    payment_type: 'subscription',
  },
})
```

See `references/stripe-integration.md` for the complete integration guide.

### 🚨 Rule #5: ALWAYS Use Supabase CLI for Migrations

**Never create tables via SQL in application code.**

Bad example:
```typescript
await supabase.sql`CREATE TABLE ...` // Don't do this!
```

Good example:
```bash
npx supabase migration new create_table
# Edit the generated .sql file
npx supabase db push
```

See `references/database-patterns.md` for migration workflows.

## Implementation Workflow

When implementing any feature in CareBridge, follow this workflow:

### Step 1: Identify the Domain

Before writing any code, identify which domain(s) you're working in:

- **Navigation/Routing** → Read `references/case-context.md`
- **Payments/Subscriptions** → Read `references/stripe-integration.md`
- **Pages/API Routes** → Read `references/nextjs-15-patterns.md`
- **UI Components** → Read `references/component-standards.md`
- **Database Operations** → Read `references/database-patterns.md`

### Step 2: Follow the Patterns

Each reference document contains:
- ✅ **CORRECT** patterns to follow
- ❌ **WRONG** anti-patterns to avoid
- Executable code examples
- Common mistakes section
- Checklists

### Step 3: Validate Against Standards

Before completing any task, verify:

**Case Context Checklist:**
- [ ] All navigation links preserve `caseId` query parameter
- [ ] Page components await params in Next.js 15
- [ ] Client components use `useEffect` for `caseId` to prevent hydration mismatch
- [ ] Empty states shown when `caseId` is missing

**Stripe Integration Checklist:**
- [ ] Pricing uses `src/lib/config/concierge-pricing.ts` as single source of truth
- [ ] Checkout sessions include proper metadata for webhook routing
- [ ] Webhook handlers check `metadata.package_type` for routing
- [ ] Price validation happens before checkout creation

**Next.js 15 Checklist:**
- [ ] All `params` are typed as `Promise<{ ... }>` and awaited
- [ ] All `searchParams` are typed as `Promise<{ ... }>` and awaited
- [ ] 'use client' only added when needed (hooks, interactivity, browser APIs)
- [ ] Server components used for data fetching by default

**Component Standards Checklist:**
- [ ] Using shadcn/ui components (added via `npx shadcn@latest add`)
- [ ] NO custom UI components created
- [ ] NO custom CSS variables defined
- [ ] Using Tailwind classes instead of inline styles
- [ ] Proper TypeScript types defined

**Database Patterns Checklist:**
- [ ] Migrations created via `npx supabase migration new`
- [ ] RLS enabled on all tables
- [ ] RLS policies created for SELECT, INSERT, UPDATE, DELETE
- [ ] Indexes added for frequently queried columns
- [ ] Using `createServerClient()` in server components
- [ ] Using `createBrowserClient()` in client components

## Common Mistakes to Avoid

Based on real bugs encountered during development:

1. **Losing case context** - Navigation without preserving caseId
2. **Not awaiting params** - Using Next.js 14 patterns in Next.js 15
3. **Creating custom components** - Instead of using shadcn/ui
4. **Defining custom CSS variables** - Instead of using existing ones
5. **Forgetting RLS policies** - Creating tables without Row-Level Security
6. **Skipping migrations** - Creating tables in application code
7. **Missing webhook metadata** - Webhooks unable to route correctly
8. **Using client Supabase in server** - Wrong client type for component

## Project Context

**Application**: CareBridge - Multi-case eldercare management platform

**Tech Stack**:
- Next.js 15.5.4 with App Router
- React 19.1.0
- TypeScript 5.x
- Supabase (PostgreSQL with RLS)
- Clerk (Authentication)
- Stripe (Payments)
- shadcn/ui (Components)
- Tailwind CSS (Styling)

**Architecture**:
- Multi-tenant: Users can manage multiple care cases
- Case-centric: All data scoped to caseId
- SaaS subscription: $19.99/month platform access
- Concierge packages: 4 service tiers (one-time, project-based, subscription)

## Resources

This skill includes comprehensive reference documentation in the `references/` directory:

### references/

1. **`case-context.md`**
   - How caseId preservation works
   - Reading case context in server/client components
   - Navigation patterns
   - Common mistakes and fixes

2. **`stripe-integration.md`**
   - Pricing configuration (single source of truth)
   - Creating checkout sessions
   - Webhook handling and metadata routing
   - Database structure
   - Testing checklist

3. **`nextjs-15-patterns.md`**
   - Async params and searchParams
   - Server vs client components
   - Data fetching patterns
   - Metadata API
   - Common migration errors

4. **`component-standards.md`**
   - Using shadcn/ui components
   - CSS variables (read-only)
   - Form patterns with React Hook Form + Zod
   - Dialog/modal patterns
   - Loading and empty states

5. **`database-patterns.md`**
   - Supabase client patterns
   - Migration creation and structure
   - RLS policies and patterns
   - Query patterns (CRUD, joins, filtering)
   - Transaction patterns with RPC
   - Error handling

## Getting Help

When stuck, refer to the reference documents for:
- Copy-paste ready code examples
- Step-by-step checklists
- Anti-patterns to avoid
- Testing procedures

Remember: These patterns exist because they've been proven through real development. Breaking them leads to bugs, build errors, and technical debt.
