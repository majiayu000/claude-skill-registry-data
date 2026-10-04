---
name: nextjs-app-router-patterns
description: Complete Next.js App Router patterns — file conventions, metadata, loading/error states, route groups, server actions, image optimization, and advanced routing. Use when structuring any Next.js 14+ project.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Next.js App Router Patterns

## Purpose
Complete reference for Next.js App Router project structure and conventions. Every pattern is production-tested. After reading this skill, you can structure any Next.js project correctly without consulting external documentation.

## When to Use This Skill
Use when:
- Starting a new Next.js project
- Structuring routes, layouts, and loading states
- Implementing SEO metadata
- Setting up server actions and data fetching
- Configuring images and fonts
- Advanced routing (parallel routes, intercepting routes, middleware)

Do NOT use when:
- Structuring vanilla HTML/JS projects or non-Next.js apps.

## Phase 1: Next.js Architecture Strategy

## 1. File Conventions

```
app/
├── layout.tsx          # Root layout (persists across all routes)
├── template.tsx        # Root template (remounts on navigation — use for page transitions)
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI while page.tsx loads
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── global-error.tsx    # Root error boundary (catches layout errors)
│
├── (marketing)/        # Route group — no URL impact, separate layout
│   ├── layout.tsx      # Marketing-specific layout
│   ├── page.tsx        # Still serves /
│   ├── about/
│   │   └── page.tsx    # /about
│   └── pricing/
│       └── page.tsx    # /pricing
│
├── (app)/              # Route group — app shell with sidebar
│   ├── layout.tsx      # App layout with sidebar
│   ├── dashboard/
│   │   ├── page.tsx    # /dashboard
│   │   └── loading.tsx # Dashboard loading skeleton
│   └── settings/
│       └── page.tsx    # /settings
│
├── blog/
│   ├── page.tsx        # /blog (list)
│   └── [slug]/
│       └── page.tsx    # /blog/:slug (dynamic)
│
└── api/
    └── webhook/
        └── route.ts    # API route handler
```

### layout.tsx vs template.tsx

| Feature | `layout.tsx` | `template.tsx` |
|---------|-------------|---------------|
| Persists across navigation | ✅ Yes | ❌ No (remounts) |
| State preserved | ✅ Yes | ❌ No (reset) |
| Use for | Shared chrome (nav, footer) | Page transitions, analytics |
| Effect cleanup | No cleanup on navigate | `useEffect` cleanup fires |

**RULE**: Page transition animations belong in `template.tsx`, NOT `layout.tsx`. Layouts never unmount, so `exit` animations never fire.

---

## 2. Metadata & SEO

> See [`seo-metadata-patterns`](../seo-metadata-patterns/SKILL.md) for complete metadata implementation including static/dynamic metadata, OG images, JSON-LD structured data, sitemap, and robots.txt.

Key rule: Root `layout.tsx` must set `metadataBase` and a title template. Every page exports its own `metadata` or `generateMetadata`.

---

## 3. Loading & Error States

### loading.tsx — Streaming Skeleton
```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="space-y-6 p-6">
      {/* Deterministic dimensions — MUST match actual page layout */}
      <div className="h-8 w-48 bg-zinc-800 rounded animate-pulse" />
      <div className="grid grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-32 bg-zinc-800 rounded-xl animate-pulse" />
        ))}
      </div>
      <div className="h-64 bg-zinc-800 rounded-xl animate-pulse" />
    </div>
  );
}
```

**RULE**: Skeleton dimensions MUST match the actual page layout. A skeleton that doesn't match causes layout shift when content loads (CLS penalty).

### error.tsx — Error Boundary with Retry
```tsx
// app/dashboard/error.tsx
"use client"; // Error boundaries must be Client Components

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
      <h2 className="text-xl font-semibold text-zinc-100">Something went wrong</h2>
      <p className="text-zinc-400 text-sm max-w-md text-center">
        {error.message || "An unexpected error occurred."}
      </p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-100 rounded-lg transition-colors"
      >
        Try again
      </button>
    </div>
  );
}
```

### not-found.tsx — Custom 404
```tsx
// app/not-found.tsx
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-4">
      <h1 className="text-6xl font-bold text-zinc-100">404</h1>
      <p className="text-zinc-400">This page doesn't exist.</p>
      <Link
        href="/"
        className="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-100 rounded-lg transition-colors"
      >
        Go home
      </Link>
    </div>
  );
}
```

---

## 4. Server Components vs Client Components

### Decision Tree
```
Does this component use:
  ├── useState, useEffect, useRef?  →  "use client"
  ├── onClick, onChange, onSubmit?   →  "use client"
  ├── Browser APIs (window, document, localStorage)?  →  "use client"
  ├── Framer Motion, GSAP, Three.js?  →  "use client"
  └── None of the above?  →  Server Component (default, no directive needed)
```

### Data Fetching (Server Component)
```tsx
// app/blog/page.tsx — Server Component (default)
// No "use client" directive — this runs on the server

async function getPosts() {
  const res = await fetch("https://api.example.com/posts", {
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  });
  return res.json();
}

export default async function BlogPage() {
  const posts = await getPosts();

  return (
    <main>
      {posts.map((post: any) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
        </article>
      ))}
    </main>
  );
}
```

### Static Generation
```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

// Pages are pre-rendered at build time for each slug
```

---

## 5. Server Actions

```tsx
// app/contact/page.tsx
import { submitContact } from "./actions";

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

```tsx
// app/contact/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function submitContact(formData: FormData) {
  const email = formData.get("email") as string;
  const message = formData.get("message") as string;

  // Validate
  if (!email || !message) {
    throw new Error("All fields required");
  }

  // Process (save to DB, send email, etc.)
  await saveContact({ email, message });

  // Revalidate the page
  revalidatePath("/contact");
}
```

---

## 6. Images & Fonts

### next/image
```tsx
import Image from "next/image";

// Responsive image with blur placeholder
<Image
  src="/hero.webp"
  alt="Hero image description"
  width={1200}
  height={630}
  priority                    // Above-the-fold images: preload
  placeholder="blur"
  blurDataURL="data:image/..."  // Base64 blur placeholder
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="rounded-xl object-cover"
/>

// Fill container (for background images)
<div className="relative h-96">
  <Image
    src="/bg.webp"
    alt=""
    fill
    sizes="100vw"
    className="object-cover"
    priority={false}          // Below-fold images: lazy load (default)
  />
</div>
```

**RULE**: Always provide `sizes` prop. Without it, Next.js assumes 100vw and serves oversized images.

### next/font
```tsx
// app/layout.tsx
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`}>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}

// tailwind.config.ts
// fontFamily: {
//   sans: ["var(--font-geist-sans)", ...defaultTheme.fontFamily.sans],
//   mono: ["var(--font-geist-mono)", ...defaultTheme.fontFamily.mono],
// }
```

---

## 7. Advanced Routing

### Parallel Routes (Modals)
```
app/
├── layout.tsx
├── page.tsx
├── @modal/
│   ├── default.tsx        # Fallback when no modal is active
│   └── (.)photo/[id]/
│       └── page.tsx       # Intercepted route — renders as modal
└── photo/[id]/
    └── page.tsx           # Full page — direct navigation
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <>
      {children}
      {modal}
    </>
  );
}

// app/@modal/default.tsx
export default function Default() {
  return null; // No modal by default
}
```

### Middleware
```tsx
// middleware.ts (root of project)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Redirect example
  if (request.nextUrl.pathname === "/old-page") {
    return NextResponse.redirect(new URL("/new-page", request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set("x-custom-header", "value");
  return response;
}

export const config = {
  matcher: [
    // Match all routes except static files and API routes
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
```

---

## 8. Verification Checklist

- [ ] Every file with `useState`/`useEffect`/event handlers has `"use client"` directive
- [ ] Root `layout.tsx` has `<html lang="en">` and proper metadata
- [ ] `loading.tsx` skeletons match actual page dimensions
- [ ] `error.tsx` exists with retry button for data-fetching routes
- [ ] `not-found.tsx` provides navigation back to home
- [ ] Images use `next/image` with `sizes` prop
- [ ] Fonts use `next/font` with CSS variable pattern
- [ ] Above-fold images have `priority` prop
- [ ] `template.tsx` used for page transitions (not `layout.tsx`)
- [ ] Server Actions use `"use server"` directive
- [ ] Dynamic routes have `generateStaticParams` for SSG where applicable
- [ ] Metadata includes title, description, OG image, and Twitter card

## Output Format / Delivery
- High-fidelity Next.js App Router folders, page structures, server actions, and middleware configuration.

## Behavior Rules
- Put page transitions in template.tsx, never layout.tsx.
- Always use Next.js Image/Font optimization components.

## Maintenance Notes
- Updated to match structural guidelines in June 2026.
