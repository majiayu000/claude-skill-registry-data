---
name: nextjs-configuration
description: Next.js 15 configuration with App Router. Use when setting up or configuring Next.js projects.
---

# Next.js Configuration Skill

This skill covers Next.js 15 configuration with the App Router.

## When to Use

Use this skill when:
- Setting up new Next.js projects
- Configuring build and deployment
- Adding middleware and redirects
- Configuring image optimization

## Core Principle

**CONVENTIONS OVER CONFIGURATION** - Next.js has sensible defaults. Only configure when you need to deviate.

## Basic Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  reactStrictMode: true,
};

export default config;
```

## Full Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  // React strict mode (recommended)
  reactStrictMode: true,

  // NEVER ignore errors
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },

  // Experimental features
  experimental: {
    typedRoutes: true,
  },

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
    ],
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,
      },
    ];
  },

  // Rewrites
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ];
  },

  // Headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
        ],
      },
    ];
  },
};

export default config;
```

## App Router Structure

```
src/
├── app/
│   ├── layout.tsx       # Root layout
│   ├── page.tsx         # Home page (/)
│   ├── loading.tsx      # Loading UI
│   ├── error.tsx        # Error boundary
│   ├── not-found.tsx    # 404 page
│   ├── globals.css      # Global styles
│   ├── about/
│   │   └── page.tsx     # /about
│   ├── blog/
│   │   ├── page.tsx     # /blog
│   │   └── [slug]/
│   │       └── page.tsx # /blog/:slug
│   └── api/
│       └── health/
│           └── route.ts # /api/health
```

## Layout Configuration

```typescript
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App',
  },
  description: 'My application description',
  openGraph: {
    title: 'My App',
    description: 'My application description',
    url: 'https://myapp.com',
    siteName: 'My App',
    locale: 'en_US',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): React.ReactElement {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

## Image Configuration

```typescript
// next.config.ts
images: {
  // Remote image patterns
  remotePatterns: [
    {
      protocol: 'https',
      hostname: '**.example.com',
    },
    {
      protocol: 'https',
      hostname: 'cdn.example.com',
      pathname: '/images/**',
    },
  ],

  // Image formats
  formats: ['image/avif', 'image/webp'],

  // Device sizes for responsive images
  deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
  imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

  // Disable optimization for static export
  // unoptimized: true,
},
```

## Environment Variables

```bash
# .env.local (not committed)
DATABASE_URL=postgresql://...
API_SECRET=secret

# .env (committed)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_APP_NAME=My App
```

```typescript
// Usage
// Server-side only
const dbUrl = process.env.DATABASE_URL;

// Client-side (must have NEXT_PUBLIC_ prefix)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

## Middleware

```typescript
// middleware.ts (root level)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest): NextResponse {
  // Authentication check
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');

  return response;
}

// Configure which paths middleware runs on
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/:path*',
  ],
};
```

## Route Handlers (API Routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest): Promise<NextResponse> {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse> {
  const user = await db.user.findUnique({ where: { id: params.id } });
  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  return NextResponse.json(user);
}
```

## Static Export

```typescript
// next.config.ts
const config: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
  },
  trailingSlash: true,
};
```

## Standalone Build (Docker)

```typescript
// next.config.ts
const config: NextConfig = {
  output: 'standalone',
};
```

```dockerfile
FROM node:22-alpine AS runner
WORKDIR /app

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

ENV NODE_ENV=production
EXPOSE 3000
CMD ["node", "server.js"]
```

## Bundle Analyzer

```typescript
// next.config.ts
import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

const config: NextConfig = {
  // ...
};

export default withBundleAnalyzer(config);
```

```bash
ANALYZE=true npm run build
```

## Security Headers

```typescript
// next.config.ts
async headers() {
  return [
    {
      source: '/(.*)',
      headers: [
        {
          key: 'X-DNS-Prefetch-Control',
          value: 'on',
        },
        {
          key: 'Strict-Transport-Security',
          value: 'max-age=63072000; includeSubDomains; preload',
        },
        {
          key: 'X-Frame-Options',
          value: 'SAMEORIGIN',
        },
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
        {
          key: 'Referrer-Policy',
          value: 'origin-when-cross-origin',
        },
      ],
    },
  ];
},
```

## Commands

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

## Best Practices

1. **Use App Router** - Pages Router is legacy
2. **Server Components by default** - Use 'use client' only when needed
3. **Typed routes** - Enable experimental.typedRoutes
4. **Never ignore errors** - Keep ignoreBuildErrors: false
5. **Environment variables** - Use NEXT_PUBLIC_ for client-side
6. **Image optimization** - Use next/image component
7. **Middleware** - Use for auth, redirects, headers

## Notes

- App Router is the recommended approach for new projects
- Server Components reduce client-side JavaScript
- Middleware runs on the Edge Runtime
- Static export removes server-side features
