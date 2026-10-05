---
name: nick-fullstack
description: Enterprise-grade fullstack build standards for all projects. Covers code quality, Supabase patterns, error handling, security, SEO, accessibility, performance, and QA. Injected into every Claude Code build spec alongside the design system.
metadata:
  openclaw:
    requires: {}
---

# Fullstack Build Standards

## When to Use
Referenced by `app-builder` on every build. These standards are injected into every Claude Code prompt alongside the design system. Also use standalone when reviewing or improving existing projects.

---

## Project Structure (Next.js App Router)

```
project-root/
├── app/
│   ├── layout.tsx          # Root layout (fonts, metadata, providers)
│   ├── page.tsx            # Homepage
│   ├── globals.css         # Global styles + Tailwind
│   ├── (marketing)/        # Public pages group
│   │   ├── about/
│   │   ├── pricing/
│   │   └── contact/
│   ├── (app)/              # Authenticated app pages group
│   │   ├── layout.tsx      # App layout (sidebar, auth guard)
│   │   ├── dashboard/
│   │   └── settings/
│   ├── api/                # API routes
│   │   └── webhooks/
│   └── auth/               # Auth pages (login, signup, callback)
├── components/
│   ├── ui/                 # Reusable primitives (Button, Card, Input, etc.)
│   ├── layout/             # Nav, Footer, Sidebar, MobileMenu
│   ├── sections/           # Page sections (Hero, Features, CTA, etc.)
│   └── forms/              # Form components
├── lib/
│   ├── supabase/
│   │   ├── client.ts       # Browser client
│   │   ├── server.ts       # Server client
│   │   └── admin.ts        # Service role client (server only)
│   ├── utils.ts            # Shared utilities
│   └── constants.ts        # App constants
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript types/interfaces
├── public/                 # Static assets
├── .env.local              # Environment variables (never commit)
└── middleware.ts            # Auth middleware for protected routes
```

---

## Supabase Patterns

### Client Setup
```typescript
// lib/supabase/client.ts — Browser client (anon key only)
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts — Server client (for Server Components, Route Handlers)
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch { /* Server Component read-only */ }
        },
      },
    }
  )
}

// lib/supabase/admin.ts — Service role (NEVER import in client code)
import { createClient } from '@supabase/supabase-js'

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)
```

### Database Conventions
- Table names: snake_case, plural (e.g., `user_profiles`, `project_tasks`)
- Column names: snake_case (e.g., `created_at`, `user_id`)
- Always include: `id` (uuid, primary key, default gen_random_uuid()), `created_at` (timestamptz, default now()), `updated_at` (timestamptz)
- Foreign keys: `<table_singular>_id` (e.g., `user_id`, `project_id`)
- Always enable RLS on every table. No exceptions.
- Write RLS policies for every operation (SELECT, INSERT, UPDATE, DELETE)
- Use `auth.uid()` in policies for user-scoped data

### Auth Flow
- Use Supabase Auth with `@supabase/ssr` package
- Auth callback at `/auth/callback` (Route Handler)
- Middleware protects `/app/*` routes
- Login/signup pages at `/auth/login`, `/auth/signup`
- Always handle auth errors gracefully with user-friendly messages

---

## Error Handling

### API Routes
```typescript
try {
  // operation
  return NextResponse.json({ data }, { status: 200 })
} catch (error) {
  console.error('[API_ROUTE_NAME]', error)
  return NextResponse.json(
    { error: 'Something went wrong' },
    { status: 500 }
  )
}
```
- Never expose internal error details to the client
- Always log errors server-side with context (route name, operation)
- Use appropriate HTTP status codes (400, 401, 403, 404, 500)

### Client-Side
- Wrap data fetching in try/catch
- Show user-friendly error messages (toast or inline)
- Loading states for all async operations (skeleton loaders, not spinners when possible)
- Empty states for lists with no data (never show a blank page)

### Form Validation
- Client-side validation with clear error messages per field
- Server-side validation always (never trust client-only validation)
- Use Zod for schema validation when forms are complex

---

## Security Checklist

- [ ] All API keys / secrets in `.env.local` only
- [ ] `SUPABASE_SERVICE_ROLE_KEY` never in client-side code or `NEXT_PUBLIC_` vars
- [ ] RLS enabled on every Supabase table
- [ ] RLS policies written for every operation
- [ ] Auth middleware protecting private routes
- [ ] Input sanitization on all user inputs
- [ ] CSRF protection (Next.js handles this by default with Server Actions)
- [ ] Rate limiting on sensitive endpoints (login, signup, API)
- [ ] No sensitive data in URL params
- [ ] Secure headers configured (Content-Security-Policy if applicable)

---

## Performance

- Use Next.js Image component for all images (automatic optimization)
- Lazy load below-fold content and images
- Use `next/font` for font loading (no layout shift)
- Server Components by default — only use `'use client'` when needed
- Dynamic imports for heavy components (`next/dynamic`)
- Database queries: always select only needed columns, use indexes on filtered columns
- Target: Lighthouse score 90+ on all categories

---

## SEO

### Every Page Must Have
```typescript
export const metadata: Metadata = {
  title: 'Page Title | Brand Name',
  description: 'Compelling 150-160 char description',
  openGraph: {
    title: 'Page Title | Brand Name',
    description: 'Description for social shares',
    url: 'https://domain.com/page',
    siteName: 'Brand Name',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Page Title | Brand Name',
    description: 'Description for Twitter',
    images: ['/og-image.png'],
  },
}
```

### Structure
- One `<h1>` per page
- Heading hierarchy: h1 → h2 → h3 (never skip levels)
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Alt text on all images
- Canonical URLs on all pages

---

## Accessibility

- Semantic HTML elements (not divs for everything)
- ARIA labels on interactive elements without visible text
- Keyboard navigation works for all interactive elements
- Focus states visible on all focusable elements (use brand color ring)
- Color contrast minimum 4.5:1 for text
- Skip-to-content link
- Form inputs linked to labels with `htmlFor`
- Error messages associated with fields via `aria-describedby`

---

## Code Quality

### TypeScript
- Strict mode enabled
- Explicit types on function params and returns (no `any` unless absolutely necessary)
- Interfaces for data shapes, types for unions/utilities
- Export types from `types/` directory

### Component Patterns
- Server Components by default
- Client Components only for: interactivity, hooks, browser APIs, event handlers
- Extract reusable logic into custom hooks (`hooks/`)
- Keep components focused — one primary responsibility
- Props interfaces defined and exported

### Tailwind CSS
- Use Tailwind utility classes directly (not @apply in most cases)
- Extract repeated patterns to components, not utility classes
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes
- Custom design tokens in `tailwind.config.ts` matching the design system

### Environment Variables
```
# .env.local
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
NEXT_PUBLIC_APP_URL=
```
- `NEXT_PUBLIC_` prefix ONLY for values safe to expose to the browser
- Service role key, API secrets, webhook secrets: NO `NEXT_PUBLIC_` prefix

---

## Pre-Deploy Checklist

- [ ] All pages render without errors
- [ ] Auth flow works (signup → login → protected page → logout)
- [ ] Forms validate and submit correctly
- [ ] Responsive at all breakpoints (375, 768, 1024, 1280, 1920)
- [ ] No console errors or warnings
- [ ] Environment variables set in Vercel project settings
- [ ] Loading states on all async operations
- [ ] Error states handled gracefully
- [ ] SEO metadata on every page
- [ ] Images optimized and using Next/Image
- [ ] Design system compliance (run through nick-design-system checklist)

---

## Self-Check Before Reporting Done (MANDATORY)

After Claude Code finishes building, before reporting complete, it must verify these 5 checks by reviewing its own output:

1. **No default shadcn borders** — check that cards, inputs, and panels don't have the default gray-200 border with no visual personality. Every bordered element must use intentional color, opacity, or shadow.

2. **Loading states exist on every async operation** — every button that fires an API call must show a spinner or disabled state. Every data fetch must show a skeleton, not a blank space.

3. **Empty states are useful** — every list, table, or data view must have a designed empty state with an icon, message, and call-to-action. Never a blank white area.

4. **Error states are recoverable** — every form must show inline validation errors per field. API errors must show a toast or inline message. Never fail silently.

5. **Responsive tested** — mentally check that the layout works at 375px mobile. If any section uses a multi-column grid that would break on mobile, verify Tailwind responsive classes (`md:grid-cols-3 grid-cols-1`) are applied.

If any of these 5 checks fail, fix them before deploying. Do not hand off a build that fails any of these.
