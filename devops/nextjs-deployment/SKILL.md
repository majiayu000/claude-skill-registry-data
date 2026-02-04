---
name: nextjs-deployment
description: Next.js deployment strategies and platform configurations. Use when deploying Next.js applications.
---

# Next.js Deployment Skill

This skill covers deploying Next.js applications to various hosting platforms.

## When to Use

Use this skill when:
- Deploying Next.js applications
- Configuring Server Components deployment
- Setting up edge functions
- Optimizing for production hosting

## Core Principle

**CHOOSE THE RIGHT PLATFORM** - Next.js features (SSR, ISR, Edge) require different hosting capabilities. Choose based on your needs.

## Build Configuration

### Production Build

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'standalone', // For Docker/self-hosted
  // output: 'export',  // For static export only

  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
    ],
  },

  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

export default nextConfig;
```

### Environment Configuration

```env
# .env.production
NEXT_PUBLIC_API_URL=https://api.production.com
DATABASE_URL=postgresql://...
NEXTAUTH_SECRET=your-secret
```

## Vercel Deployment (Recommended)

### Configuration

```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "regions": ["iad1"],
  "functions": {
    "app/api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "crons": [
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### Deploy Script

```bash
# Install Vercel CLI
npm install -g vercel

# Link project
vercel link

# Deploy preview
vercel

# Deploy production
vercel --prod
```

### GitHub Actions

```yaml
# .github/workflows/deploy-vercel.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel@latest

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Netlify Deployment

### Configuration

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NEXT_TELEMETRY_DISABLED = "1"

[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Install Netlify Plugin

```bash
npm install -D @netlify/plugin-nextjs
```

### GitHub Actions

```yaml
# .github/workflows/deploy-netlify.yml
name: Deploy to Netlify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: '.next'
          production-branch: main
          github-token: ${{ secrets.GITHUB_TOKEN }}
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## Cloudflare Pages

### Configuration

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  experimental: {
    runtime: 'edge',
  },
};
```

### Install Adapter

```bash
npm install -D @cloudflare/next-on-pages
```

### Build Script

```json
// package.json
{
  "scripts": {
    "build:cloudflare": "npx @cloudflare/next-on-pages"
  }
}
```

### GitHub Actions

```yaml
# .github/workflows/deploy-cloudflare.yml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npx @cloudflare/next-on-pages

      - name: Deploy
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: my-nextjs-app
          directory: .vercel/output/static
```

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM node:22-alpine AS base

# Install dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Production
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

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=http://localhost:3000
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Build and Run

```bash
# Build image
docker build -t my-nextjs-app .

# Run container
docker run -p 3000:3000 my-nextjs-app

# With docker-compose
docker-compose up -d
```

## AWS Amplify

### Configuration

```yaml
# amplify.yml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

## Static Export

### Configuration

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};
```

### Limitations

- No Server Components with dynamic rendering
- No API routes
- No ISR/revalidation
- No middleware
- No image optimization (unless external service)

## Edge Functions

### Edge API Route

```typescript
// app/api/edge/route.ts
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name');

  return new Response(JSON.stringify({ message: `Hello ${name}` }), {
    headers: { 'Content-Type': 'application/json' },
  });
}
```

### Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add custom header
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'value');
  return response;
}

export const config = {
  matcher: '/api/:path*',
};
```

## ISR Configuration

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { NextRequest } from 'next/server';
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request: NextRequest) {
  const { path, tag, secret } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return new Response('Invalid secret', { status: 401 });
  }

  if (path) {
    revalidatePath(path);
  }

  if (tag) {
    revalidateTag(tag);
  }

  return new Response('Revalidated', { status: 200 });
}
```

### Time-Based Revalidation

```typescript
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }, // Revalidate every hour
  });
  return res.json();
}
```

## Health Checks

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Check database connection
    // await db.query('SELECT 1');

    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
    });
  } catch {
    return NextResponse.json(
      { status: 'unhealthy' },
      { status: 503 }
    );
  }
}
```

## Monitoring

### Vercel Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## Commands

```bash
# Build for production
npm run build

# Start production server
npm run start

# Deploy to Vercel
vercel --prod

# Build Docker image
docker build -t my-app .

# Export static site
npm run build && npx next export
```

## Platform Comparison

| Feature | Vercel | Netlify | Cloudflare | AWS | Docker |
|---------|--------|---------|------------|-----|--------|
| Server Components | Full | Full | Edge only | Full | Full |
| ISR | Full | Limited | No | Full | Full |
| Edge Functions | Yes | Yes | Yes | Yes | No |
| Image Optimization | Built-in | Plugin | No | Custom | Custom |
| Serverless | Yes | Yes | Yes | Yes | No |

## Best Practices

1. **Use standalone output** - For Docker deployments
2. **Enable ISR** - For dynamic content with caching
3. **Configure health checks** - For load balancers
4. **Set up monitoring** - Analytics and error tracking
5. **Use edge when possible** - For lower latency
6. **Cache static assets** - Long cache times with hashing

## Notes

- Vercel has best Next.js support (same team)
- Docker requires standalone output mode
- Static export loses many Next.js features
- Edge runtime has Node.js API limitations
