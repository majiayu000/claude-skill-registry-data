---
name: nextjs
title: Next.js
description: The React Framework for the Web - App Router, SSR, Security
icon: ▲
tags: [react, nextjs, ssr, framework, security]
---

Next.js - The React Framework for the Web

### Basics
- SSR vs SSG vs ISR concepts → See [basics](reference/basics.md)
- App Router vs Pages Router → See [basics](reference/basics.md)
- Directory structure → See [basics](reference/basics.md)
- Routing fundamentals → See [basics](reference/basics.md)

### App Router
- Layouts and nesting → See [app-router](reference/app-router.md)
- Pages and routing → See [app-router](reference/app-router.md)
- Loading and error states → See [app-router](reference/app-router.md)
- Server vs Client Components → See [app-router](reference/app-router.md)
- Route handlers (API) → See [app-router](reference/app-router.md)
- Middleware → See [app-router](reference/app-router.md)

### Data Fetching
- fetch API and caching → See [data-fetching](reference/data-fetching.md)
- Server Components data → See [data-fetching](reference/data-fetching.md)
- Server Actions → See [data-fetching](reference/data-fetching.md)
- Parallel and sequential fetching → See [data-fetching](reference/data-fetching.md)

### Rendering
- Server Components → See [rendering](reference/rendering.md)
- Client Components → See [rendering](reference/rendering.md)
- Streaming and Suspense → See [rendering](reference/rendering.md)
- Partial Prerendering → See [rendering](reference/rendering.md)

### Styling
- CSS Modules → See [styling](reference/styling.md)
- Tailwind CSS → See [styling](reference/styling.md)
- Global CSS → See [styling](reference/styling.md)

### API & Backend
- Route Handlers → See [api-backend](reference/api-backend.md)
- Headers and Cookies → See [api-backend](reference/api-backend.md)
- Server Actions → See [api-backend](reference/api-backend.md)

### Performance
- Image optimization → See [performance](reference/performance.md)
- Font optimization → See [performance](reference/performance.md)
- Code splitting → See [performance](reference/performance.md)
- Prefetching → See [performance](reference/performance.md)

### Deployment
- Vercel deployment → See [deployment](reference/deployment.md)
- Docker deployment → See [deployment](reference/deployment.md)
- Static export → See [deployment](reference/deployment.md)

### Security
- Authentication (NextAuth.js) → See [security](reference/security.md)
- Authorization and RBAC → See [security](reference/security.md)
- XSS prevention → See [security](reference/security.md)
- CSRF protection → See [security](reference/security.md)
- Server Actions security → See [security](reference/security.md)
- API route security → See [security](reference/security.md)

## Quick Start

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint
```

```bash
cd my-app
npm run dev
```

## Key Features

- **App Router**: New filesystem-based routing
- **Server Components**: Default rendering on server
- **Streaming**: Suspense for progressive loading
- **Data Cache**: Intelligent caching by default
- **Middleware**: Edge middleware for routing
- **TypeScript**: First-class TypeScript support

## Project Structure

```
app/
├── layout.tsx      # Root layout
├── page.tsx        # Home page
├── globals.css     # Global styles
├── (marketing)/    # Route group
│   └── about/
│       └── page.tsx
├── blog/
│   ├── page.tsx
│   └── [slug]/
│       └── page.tsx
└── api/
    └── route.ts   # API route
```
