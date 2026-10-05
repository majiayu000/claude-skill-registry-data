---
name: nextjs-expert
description: Deep Next.js expertise for App Router, Server Components, data fetching, middleware, and deployment. Use when building Next.js applications, migrating to.
---

# Next.js Expert

Specialized expertise in Next.js development, providing deep guidance on the App Router architecture, Server and Client Components, data fetching with caching and revalidation, middleware, route handlers, authentication, image and font optimization, streaming, and production deployment strategies.

## When to Use This Skill

Use this skill for:

- Scaffolding new Next.js applications with App Router
- Migrating from Pages Router to App Router
- Designing layouts, loading states, and error handling
- Implementing Server Components and Client Components correctly
- Building data fetching pipelines with caching and revalidation
- Writing server actions for form mutations
- Creating middleware for auth, redirects, and request modification
- Configuring ISR, streaming, and parallel/intercepting routes
- Deploying to Vercel, self-hosted Node.js, or Docker
- Optimizing images, fonts, metadata, and Core Web Vitals

**Trigger phrases**: "nextjs", "next.js", "app router", "server component", "server action", "next middleware", "next deployment", "next.js routing", "pages to app router", "next.js caching", "ISR", "next image"

## What This Skill Does

Provides Next.js expertise including:

- **App Router**: File-based routing, layouts, loading/error UI, parallel and intercepting routes
- **Server Components**: Data fetching, streaming, composition with Client Components
- **Data Fetching**: fetch caching, server actions, revalidatePath, revalidateTag
- **Middleware**: Request/response modification, authentication, redirects
- **Route Handlers**: API routes in the App Router, streaming responses
- **Performance**: Image optimization, font optimization, metadata, Core Web Vitals
- **Authentication**: Auth patterns with middleware, session management
- **Deployment**: Vercel, standalone Node.js output, Docker, static export

## Instructions

### Step 1: Structure the App Router

**Standard App Router file structure**:

```
app/
  layout.tsx              # Root layout (required)
  page.tsx                # Home page (/)
  loading.tsx             # Root loading UI
  error.tsx               # Root error UI
  not-found.tsx           # 404 page
  global-error.tsx        # Global error boundary (wraps root layout)
  dashboard/
    layout.tsx            # Dashboard layout (nested)
    page.tsx              # /dashboard
    loading.tsx           # Dashboard loading state
    settings/
      page.tsx            # /dashboard/settings
  blog/
    page.tsx              # /blog (list)
    [slug]/
      page.tsx            # /blog/:slug (dynamic segment)
      opengraph-image.tsx # Dynamic OG image generation
  api/
    route.ts              # /api (route handler)
    users/
      route.ts            # /api/users
      [id]/
        route.ts          # /api/users/:id
  (marketing)/            # Route group (no URL segment)
    about/
      page.tsx            # /about
    contact/
      page.tsx            # /contact
```

**Root layout with metadata**:

```tsx
// app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  title: {
    default: "My App",
    template: "%s | My App",     // Child pages: "About | My App"
  },
  description: "Production Next.js application",
  metadataBase: new URL("https://example.com"),
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "My App",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <header>
          <nav>{/* Navigation */}</nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

**Loading and error boundaries**:

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded mb-4" />
      <div className="h-64 bg-gray-200 rounded" />
    </div>
  );
}

// app/dashboard/error.tsx
"use client";   // Error boundaries must be Client Components

import { useEffect } from "react";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error reporting service
    console.error("Dashboard error:", error);
  }, [error]);

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Step 2: Server Components vs Client Components

**Decision rule**: Components are Server Components by default. Add `"use client"` only when you need browser APIs, event handlers, useState, or useEffect.

```tsx
// app/dashboard/page.tsx  (Server Component - no directive needed)
import { Suspense } from "react";
import { RevenueChart } from "./revenue-chart";      // Client Component
import { LatestInvoices } from "./latest-invoices";   // Server Component

// Data fetching happens directly in the Server Component
async function getStats() {
  const res = await fetch("https://api.example.com/stats", {
    next: { revalidate: 60 },   // ISR: revalidate every 60 seconds
  });
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json() as Promise<Stats>;
}

export default async function DashboardPage() {
  const stats = await getStats();

  return (
    <div>
      <h1>Dashboard</h1>
      <StatsCards stats={stats} />
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />
      </Suspense>
      <Suspense fallback={<InvoiceSkeleton />}>
        <LatestInvoices />
      </Suspense>
    </div>
  );
}
```

```tsx
// app/dashboard/revenue-chart.tsx  (Client Component)
"use client";

import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis } from "recharts";

export function RevenueChart() {
  const [period, setPeriod] = useState<"week" | "month">("month");

  return (
    <div>
      <select value={period} onChange={(e) => setPeriod(e.target.value as any)}>
        <option value="week">Weekly</option>
        <option value="month">Monthly</option>
      </select>
      <BarChart width={600} height={300} data={[]}>
        <XAxis dataKey="name" />
        <YAxis />
        <Bar dataKey="revenue" fill="#4f46e5" />
      </BarChart>
    </div>
  );
}
```

**Composition boundary**: pass Server Component output as children to Client Components.

```tsx
// Client Component that wraps server-rendered content
"use client";
import { useState } from "react";

export function Collapsible({ title, children }: {
  title: string;
  children: React.ReactNode;   // Server-rendered content passed as children
}) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen(!open)}>{title}</button>
      {open && <div>{children}</div>}
    </div>
  );
}

// Server Component usage
import { Collapsible } from "./collapsible";

export default async function Page() {
  const data = await fetchData();     // Runs on server
  return (
    <Collapsible title="Details">
      {/* This content is server-rendered, then hydrated inside the client wrapper */}
      <DataTable rows={data} />
    </Collapsible>
  );
}
```

### Step 3: Data Fetching and Caching

**fetch with caching strategies**:

```tsx
// Cache indefinitely (static data)
const staticData = await fetch("https://api.example.com/config", {
  cache: "force-cache",
});

// Revalidate on a time interval (ISR)
const revalidatedData = await fetch("https://api.example.com/products", {
  next: { revalidate: 3600 },    // Revalidate every hour
});

// No caching (always fresh)
const freshData = await fetch("https://api.example.com/stock", {
  cache: "no-store",
});

// Tag-based revalidation
const taggedData = await fetch("https://api.example.com/posts", {
  next: { tags: ["posts"] },     // Revalidate with revalidateTag("posts")
});
```

**Server Actions for mutations**:

```tsx
// app/actions.ts
"use server";

import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";
import { z } from "zod";

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  // Validate
  const parsed = CreatePostSchema.safeParse({
    title: formData.get("title"),
    content: formData.get("content"),
  });

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors };
  }

  // Persist
  const post = await db.post.create({ data: parsed.data });

  // Revalidate cached data
  revalidateTag("posts");
  revalidatePath("/blog");

  // Redirect to the new post
  redirect(`/blog/${post.slug}`);
}

// app/blog/new/page.tsx
import { createPost } from "../actions";

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <label htmlFor="title">Title</label>
      <input id="title" name="title" required />

      <label htmlFor="content">Content</label>
      <textarea id="content" name="content" required />

      <button type="submit">Publish</button>
    </form>
  );
}
```

### Step 4: Middleware

```tsx
// middleware.ts (project root)
import { NextResponse, type NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // 1. Authentication check
  const token = request.cookies.get("session")?.value;
  const protectedPaths = ["/dashboard", "/settings", "/admin"];
  const isProtected = protectedPaths.some((p) => pathname.startsWith(p));

  if (isProtected && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // 2. Role-based access control
  if (pathname.startsWith("/admin")) {
    const role = request.cookies.get("role")?.value;
    if (role !== "admin") {
      return NextResponse.redirect(new URL("/unauthorized", request.url));
    }
  }

  // 3. Add custom headers
  const response = NextResponse.next();
  response.headers.set("x-request-id", crypto.randomUUID());

  // 4. Geolocation-based redirect (Vercel Edge)
  const country = request.geo?.country;
  if (pathname === "/" && country === "DE") {
    return NextResponse.redirect(new URL("/de", request.url));
  }

  return response;
}

export const config = {
  // Run middleware on all routes except static files and API
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/).*)"],
};
```

### Step 5: Route Handlers

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get("page") ?? "1", 10);
  const limit = parseInt(searchParams.get("limit") ?? "20", 10);

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({ data: users, page, limit });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const user = await db.user.create({ data: body });
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to create user" },
      { status: 400 }
    );
  }
}

// Streaming response
export async function GET(request: NextRequest) {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify({ i })}\n\n`));
        await new Promise((r) => setTimeout(r, 500));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
```

### Step 6: Parallel and Intercepting Routes

**Parallel routes** (render multiple pages in the same layout simultaneously):

```
app/
  dashboard/
    layout.tsx
    page.tsx
    @analytics/
      page.tsx            # Rendered in parallel
      loading.tsx
    @notifications/
      page.tsx            # Rendered in parallel
      loading.tsx
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  notifications,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-12 gap-4">
      <main className="col-span-8">{children}</main>
      <aside className="col-span-4">
        {analytics}
        {notifications}
      </aside>
    </div>
  );
}
```

**Intercepting routes** (show a modal on soft navigation, full page on hard navigation):

```
app/
  feed/
    page.tsx              # Feed with photo links
    (.)photo/[id]/
      page.tsx            # Intercepted: shows modal
  photo/[id]/
    page.tsx              # Direct URL: shows full page
```

```tsx
// app/feed/(.)photo/[id]/page.tsx
import { Modal } from "@/components/modal";
import { PhotoDetail } from "@/components/photo-detail";

export default async function InterceptedPhoto({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <Modal>
      <PhotoDetail id={id} />
    </Modal>
  );
}
```

### Step 7: Image and Font Optimization

```tsx
import Image from "next/image";
import { Inter, Roboto_Mono } from "next/font/google";
import localFont from "next/font/local";

// Google fonts (automatic subsetting, self-hosting, zero layout shift)
const inter = Inter({ subsets: ["latin"], display: "swap" });
const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-mono",
});

// Local font
const customFont = localFont({
  src: "./fonts/CustomFont.woff2",
  display: "swap",
  variable: "--font-custom",
});

// Optimized image usage
function HeroImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero banner showing product overview"
      width={1200}
      height={600}
      priority                    // Preload for LCP images
      sizes="(max-width: 768px) 100vw, 1200px"
      className="rounded-lg"
    />
  );
}

// Remote images require domain allowlist in next.config
function Avatar({ user }: { user: { name: string; avatar: string } }) {
  return (
    <Image
      src={user.avatar}
      alt={`${user.name}'s avatar`}
      width={48}
      height={48}
      className="rounded-full"
    />
  );
}
```

### Step 8: Deployment Configurations

**Vercel (recommended)**:

```json
// vercel.json (optional overrides)
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "crons": [
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 3 * * *"
    }
  ]
}
```

**Docker (self-hosted)**:

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

```ts
// next.config.ts (enable standalone output for Docker)
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "cdn.example.com" },
    ],
  },
  experimental: {
    typedRoutes: true,    // Type-safe Link hrefs
  },
};

export default nextConfig;
```

### Step 9: Authentication Pattern

```tsx
// lib/auth.ts
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { jwtVerify, type JWTPayload } from "jose";

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET!);

export interface SessionPayload extends JWTPayload {
  userId: string;
  role: "user" | "admin";
}

export async function getSession(): Promise<SessionPayload | null> {
  const cookieStore = await cookies();
  const token = cookieStore.get("session")?.value;
  if (!token) return null;

  try {
    const { payload } = await jwtVerify(token, JWT_SECRET);
    return payload as SessionPayload;
  } catch {
    return null;
  }
}

export async function requireAuth(): Promise<SessionPayload> {
  const session = await getSession();
  if (!session) redirect("/login");
  return session;
}

export async function requireAdmin(): Promise<SessionPayload> {
  const session = await requireAuth();
  if (session.role !== "admin") redirect("/unauthorized");
  return session;
}

// Usage in a Server Component
export default async function AdminPage() {
  const session = await requireAdmin();
  return <h1>Welcome, admin {session.userId}</h1>;
}
```

## Best Practices

- **Default to Server Components**: only add `"use client"` when you genuinely need browser APIs or React state/effects
- **Colocate data fetching with the component that uses it**: avoid lifting fetches to the layout unless the data is shared
- **Use Suspense boundaries strategically**: wrap slow data fetches so the rest of the page streams immediately
- **Prefer server actions over API routes for form mutations**: they integrate with revalidation and provide progressive enhancement
- **Set revalidation times based on data freshness requirements**: static config rarely changes, product prices change hourly, stock levels need no-store
- **Use route groups for layout organization**: `(marketing)`, `(dashboard)` keep URLs clean while sharing layouts
- **Always provide image dimensions or use `fill`**: prevents cumulative layout shift
- **Use `loading.tsx` at every route segment**: gives instant loading feedback via streaming

## Common Patterns

### Pattern 1: Optimistic Mutation with Server Action

```tsx
"use client";

import { useOptimistic, useRef } from "react";
import { addComment } from "./actions";

export function CommentForm({ comments }: { comments: Comment[] }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [optimisticComments, addOptimistic] = useOptimistic(
    comments,
    (current, newComment: string) => [
      ...current,
      { id: "temp", text: newComment, pending: true },
    ]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get("text") as string;
    addOptimistic(text);
    formRef.current?.reset();
    await addComment(formData);
  }

  return (
    <>
      <ul>
        {optimisticComments.map((c) => (
          <li key={c.id} style={{ opacity: c.pending ? 0.5 : 1 }}>
            {c.text}
          </li>
        ))}
      </ul>
      <form ref={formRef} action={handleSubmit}>
        <input name="text" required />
        <button type="submit">Add Comment</button>
      </form>
    </>
  );
}
```

### Pattern 2: Streaming with Suspense Boundaries

```tsx
// app/products/page.tsx
import { Suspense } from "react";

export default function ProductsPage() {
  return (
    <div>
      <h1>Products</h1>
      {/* Featured loads fast */}
      <Suspense fallback={<FeaturedSkeleton />}>
        <FeaturedProducts />
      </Suspense>
      {/* Reviews are slower, streamed in later */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <RecentReviews />
      </Suspense>
    </div>
  );
}

async function FeaturedProducts() {
  const products = await fetch("https://api.example.com/featured", {
    next: { revalidate: 300 },
  }).then((r) => r.json());

  return (
    <ul>
      {products.map((p: Product) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}

async function RecentReviews() {
  // This fetch is slow, but the page renders immediately
  // and streams this section when ready
  const reviews = await fetch("https://api.example.com/reviews", {
    cache: "no-store",
  }).then((r) => r.json());

  return (
    <ul>
      {reviews.map((r: Review) => (
        <li key={r.id}>{r.text} - {r.rating}/5</li>
      ))}
    </ul>
  );
}
```

## Quality Checklist

- [ ] Root layout defines `<html>` and `<body>` with lang attribute
- [ ] Every route segment with slow data has a `loading.tsx`
- [ ] Error boundaries exist at critical layout levels
- [ ] Server Components do not import client-only modules
- [ ] Client Components have `"use client"` directive at the top
- [ ] fetch calls specify explicit caching strategy
- [ ] Server actions validate input (Zod or similar)
- [ ] Middleware matcher excludes static assets and images
- [ ] Images use `priority` for above-the-fold LCP images
- [ ] Fonts use `display: "swap"` and subsetting
- [ ] `next.config.ts` has `output: "standalone"` for Docker deployments
- [ ] Metadata is defined in layouts and pages for SEO
- [ ] Dynamic routes use `generateStaticParams` where appropriate

## Related Skills

- `react-expert` - React component architecture, hooks, and testing patterns
- `javascript-cleanup` - JavaScript code quality and refactoring
- `performance-review` - Performance analysis methodology
- `kubernetes-expert` - Container orchestration for self-hosted deployments
- `cicd-architect` - CI/CD pipeline design for Next.js builds

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
