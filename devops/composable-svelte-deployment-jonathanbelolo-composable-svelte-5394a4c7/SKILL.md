---
name: composable-svelte-deployment
description: Production deployment patterns for Composable Svelte SSR applications. Use when deploying to Fly.io, Docker, or any cloud platform. Covers multi-stage Docker builds, Fly.io configuration, security hardening, performance optimization, and integration with Composable Rust backends.
---

# Composable Svelte Deployment

This skill covers production deployment of Composable Svelte SSR applications, with focus on Fly.io and Docker-based deployments.

---

## Architecture Overview

**Stack**: Fastify + Composable Svelte SSR (NOT SvelteKit)

```
┌─────────────────────────────────────────────────┐
│                    Fly.io                       │
├─────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐  │
│  │ Composable       │    │ Composable       │  │
│  │ Svelte SSR       │◄──►│ Rust Backend     │  │
│  │ (Fastify)        │    │ (Axum/Actix)     │  │
│  └──────────────────┘    └──────────────────┘  │
│   Docker Container        Docker Container      │
│   Internal Network: .internal (6PN)             │
└─────────────────────────────────────────────────┘
```

**Why NOT SvelteKit?**
- Incompatible with Composable Architecture patterns
- We use custom SSR from `@composable-svelte/core/ssr`
- Reducer-based state management on both client and server
- Effect system for async operations

---

## Docker Patterns

### Multi-Stage Build (REQUIRED)

**Goal**: <150MB final image, production-only dependencies

```dockerfile
# Stage 1: Dependencies (Production Only)
FROM node:20-alpine AS deps
WORKDIR /app
RUN npm install -g pnpm@9
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod

# Stage 2: Builder (Development Dependencies + Build)
FROM node:20-alpine AS builder
WORKDIR /app
RUN npm install -g pnpm@9
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build
RUN find dist -name "*.map" -type f -delete  # Remove source maps

# Stage 3: Production Runtime (Minimal)
FROM node:20-alpine AS runner
RUN apk add --no-cache dumb-init
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Copy ONLY production dependencies and built artifacts
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./package.json

USER nodejs
ENV NODE_ENV=production PORT=3000
EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server/index.js"]
```

**Key Patterns**:
- ✅ **3 stages**: deps (prod only) → builder (full build) → runner (minimal)
- ✅ **Non-root user**: `nodejs:nodejs` (UID 1001)
- ✅ **Alpine Linux**: Minimal attack surface (<50MB base)
- ✅ **dumb-init**: Proper signal handling (PID 1 problem)
- ✅ **Remove source maps**: `find dist -name "*.map" -delete`
- ✅ **Copy package.json**: Required for ES module resolution

**Common Mistakes**:
- ❌ Single-stage build → 500MB+ images
- ❌ Running as root → security vulnerability
- ❌ Including devDependencies → bloated images
- ❌ Missing package.json → import failures with "type": "module"

---

### Monorepo vs Standalone

**Monorepo** (like this repo):
```dockerfile
# Copy workspace structure
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/core/package.json ./packages/core/
COPY examples/ssr-server/package.json ./examples/ssr-server/

# Install workspace dependencies
RUN pnpm install --frozen-lockfile

# Build both packages
WORKDIR /app/packages/core
RUN pnpm run build
WORKDIR /app/examples/ssr-server
RUN pnpm run build

# Copy ALL workspace artifacts
COPY --from=builder /app/packages/core/dist ./packages/core/dist
COPY --from=builder /app/packages/core/package.json ./packages/core/package.json
COPY --from=builder /app/pnpm-workspace.yaml ./pnpm-workspace.yaml
```

**Standalone** (user's app):
```dockerfile
# Simple install
COPY package.json package-lock.json ./
RUN npm ci

# Simple build
COPY . .
RUN npm run build

# Simple copy
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
```

---

## Vite Configuration for SSR

**Required**: Vite must be configured for dual builds (client + server)

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],

  build: {
    // Client build (default)
    outDir: 'dist/client',
    rollupOptions: {
      input: 'src/client/index.ts'
    }
  },

  ssr: {
    // Don't externalize workspace packages
    noExternal: ['@composable-svelte/core']
  }
});
```

**package.json scripts**:
```json
{
  "scripts": {
    "build": "vite build && vite build --ssr",
    "build:client": "vite build",
    "build:server": "vite build --ssr src/server/index.ts --outDir dist/server",
    "start": "NODE_ENV=production node dist/server/index.js"
  }
}
```

**Why**: SSR requires TWO builds:
1. **Client bundle**: Runs in browser, hydrates SSR HTML
2. **Server bundle**: Runs in Node.js, renders initial HTML

---

## Fly.io Configuration

### fly.toml (Apps V2 Syntax)

```toml
app = "my-composable-app"
primary_region = "sjc"  # Choose region closest to users

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "3000"
  # Internal Fly network for backend communication
  COMPOSABLE_RUST_BACKEND_URL = "http://my-rust-backend.internal:8080"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero (change to 1+ for production)

  [http_service.concurrency]
    type = "connections"
    hard_limit = 250
    soft_limit = 200

[[vm]]
  memory = '512mb'  # Minimum for Node.js SSR
  cpu_kind = 'shared'
  cpus = 1

# Health checks (Apps V2 syntax)
[[http_service.checks]]
  interval = "30s"
  timeout = "5s"
  grace_period = "10s"
  method = "GET"
  path = "/health"
```

**Critical Patterns**:
- ✅ **Apps V2 syntax**: `[[http_service.checks]]` NOT `[[services.http_checks]]`
- ✅ **Internal networking**: `.internal` domain for Rust backend (no internet egress)
- ✅ **Health endpoint**: Must exist in your Fastify server
- ✅ **Secrets via CLI**: `fly secrets set KEY=value` (NOT in fly.toml)

**Common Mistakes**:
- ❌ Mixing Apps V1/V2 syntax → deployment fails
- ❌ Hardcoding secrets in fly.toml → security breach
- ❌ Missing health endpoint → app marked unhealthy
- ❌ Using public URL for backend → unnecessary egress costs

---

### Secrets Management

**NEVER commit secrets to fly.toml**:

```bash
# ✅ CORRECT: Use Fly secrets CLI
fly secrets set \
  SESSION_SECRET=$(openssl rand -hex 32) \
  JWT_SECRET=$(openssl rand -hex 32) \
  BACKEND_API_KEY=your-backend-api-key-here

# Verify secrets are set (values hidden)
fly secrets list

# ❌ WRONG: Environment variables in fly.toml
[env]
  SESSION_SECRET = "abc123"  # NEVER DO THIS
```

**Validate secrets at startup**:
```typescript
// src/server/index.ts
if (!process.env.SESSION_SECRET || process.env.SESSION_SECRET.length < 32) {
  throw new Error('SESSION_SECRET must be at least 32 characters');
}
```

---

## Security Hardening

### HTTP Security Headers

**Use built-in middleware**:
```typescript
import { fastifySecurityHeaders } from '@composable-svelte/core/ssr';

fastifySecurityHeaders(app, {
  contentSecurityPolicy: [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline'",  // Remove 'unsafe-inline' if possible
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "connect-src 'self' https://your-backend.fly.dev",
    "frame-ancestors 'none'",
    "base-uri 'self'"
  ].join('; '),
  frameOptions: 'DENY',
  referrerPolicy: 'strict-origin-when-cross-origin',
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
});
```

**Test headers**:
```bash
curl -I https://your-app.fly.dev
# Should see:
# Content-Security-Policy: default-src 'self'; ...
# X-Frame-Options: DENY
# Strict-Transport-Security: max-age=31536000
```

---

### Rate Limiting

**Per-IP rate limiting**:
```typescript
import { fastifyRateLimit } from '@composable-svelte/core/ssr';

fastifyRateLimit(app, {
  max: 100,        // 100 requests
  windowMs: 60000, // per minute
  message: 'Too many requests from this IP'
});
```

**Per-route rate limiting**:
```typescript
app.get('/api/expensive', {
  config: {
    rateLimit: {
      max: 10,       // 10 requests
      timeWindow: 60000  // per minute
    }
  }
}, async (request, reply) => {
  // Expensive operation
});
```

---

### CORS Configuration

**Strict CORS for Rust backend**:
```typescript
import cors from '@fastify/cors';

app.register(cors, {
  origin: [
    'https://your-app.fly.dev',
    process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : null
  ].filter(Boolean),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE']
});
```

---

### Docker Security

**Non-root user** (REQUIRED):
```dockerfile
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
USER nodejs
```

**Read-only filesystem** (optional):
```toml
# fly.toml
[[vm]]
  read_only = true

[[mounts]]
  source = "logs"
  destination = "/app/logs"  # Only writable directory
```

---

## Performance Optimization

### SSR Caching

**In-memory cache** (single instance):
```typescript
const cache = new Map<string, { html: string; timestamp: number }>();
const CACHE_TTL = 60000; // 1 minute

app.get('*', async (request, reply) => {
  const cacheKey = request.url;
  const cached = cache.get(cacheKey);

  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return reply.type('text/html').send(cached.html);
  }

  const html = await renderToHTML(/* ... */);
  cache.set(cacheKey, { html, timestamp: Date.now() });

  return reply.type('text/html').send(html);
});
```

**Redis cache** (multi-instance):
```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function getCachedHTML(key: string) {
  return await redis.get(key);
}

async function setCachedHTML(key: string, html: string, ttl: number) {
  await redis.setex(key, ttl, html);
}
```

---

### Compression

**Enable Brotli compression**:
```typescript
import compress from '@fastify/compress';

app.register(compress, {
  global: true,
  threshold: 1024, // Min size to compress (1KB)
  encodings: ['gzip', 'deflate', 'br'] // Brotli for best compression
});
```

---

### Bundle Optimization

**Code splitting** (automatic with Vite):
```typescript
// Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart.svelte'));

{#if showChart}
  <Suspense fallback={<Spinner />}>
    <HeavyChart data={chartData} />
  </Suspense>
{/if}
```

**Tree shaking** (use named imports):
```typescript
// ✅ GOOD: Named imports
import { createStore, Effect } from '@composable-svelte/core';

// ❌ BAD: Wildcard imports
import * as Core from '@composable-svelte/core';
```

---

## Deployment Workflow

### Local Testing

```bash
# 1. Build Docker image
docker build -t my-composable-app .

# 2. Check image size (should be <150MB)
docker images my-composable-app

# 3. Run locally
docker run -p 3000:3000 \
  -e COMPOSABLE_RUST_BACKEND_URL=http://localhost:8080 \
  my-composable-app

# 4. Test health check
curl http://localhost:3000/health
```

---

### Deploy to Fly.io

```bash
# 1. Login
fly auth login

# 2. Create app (first time)
fly launch

# 3. Set secrets
fly secrets set \
  SESSION_SECRET=$(openssl rand -hex 32) \
  JWT_SECRET=$(openssl rand -hex 32)

# 4. Deploy
fly deploy

# 5. Check status
fly status

# 6. Open in browser
fly open
```

---

### Scaling

**Horizontal scaling**:
```bash
# Scale to 2 instances
fly scale count 2

# Scale to multiple regions
fly scale count 2 --region sjc  # San Jose
fly scale count 1 --region lhr  # London
```

**Vertical scaling**:
```bash
# Increase memory
fly scale memory 1024

# Increase CPU
fly scale vm shared-cpu-2x
```

**Autoscaling** (paid):
```toml
[auto_scaling]
  min_instances = 1
  max_instances = 10

  [[auto_scaling.metrics]]
    type = "requests"
    target = 500  # Scale when avg requests > 500/sec
```

---

### Rollback

```bash
# List releases
fly releases

# Rollback to previous release
fly releases rollback

# Rollback to specific version
fly releases rollback v3
```

---

## Internal Networking (Fly.io 6PN)

**Key Pattern**: Use `.internal` domain for Composable Rust backend

```typescript
// fly.toml
[env]
  COMPOSABLE_RUST_BACKEND_URL = "http://my-rust-backend.internal:8080"

// Fastify server
export const backendAPI = createAPIClient({
  baseURL: process.env.COMPOSABLE_RUST_BACKEND_URL,
  timeout: 30000
});
```

**Benefits**:
- ✅ Private network (no internet routing)
- ✅ Faster (low latency)
- ✅ Free (no egress charges)
- ✅ Secure (not exposed to internet)

**CORS on Rust backend**:
```rust
let cors = CorsLayer::new()
    .allow_origin("https://my-composable-app.fly.dev".parse::<HeaderValue>().unwrap())
    .allow_methods([Method::GET, Method::POST])
    .allow_headers([AUTHORIZATION, CONTENT_TYPE]);
```

---

## Monitoring

### Health Check Endpoint

**Required for Fly.io**:
```typescript
app.get('/health', async () => {
  return {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  };
});
```

---

### Logs

```bash
# Stream logs
fly logs

# Filter errors only
fly logs | grep ERROR

# Tail last 100 lines
fly logs --tail 100
```

---

### SSH into Instance

```bash
# Open console in running instance
fly ssh console

# Check processes
ps aux

# Check memory
free -m

# Exit
exit
```

---

## Common Issues

### App Won't Start

```bash
# Check logs
fly logs

# Common issues:
# - Missing environment variables
# - Port mismatch (must use PORT env var)
# - Build failed (check Dockerfile)
```

---

### Health Check Failing

```bash
# Test locally first
docker run -p 3000:3000 my-composable-app
curl http://localhost:3000/health

# Check health check path in fly.toml matches your endpoint
```

---

### Backend Connection Issues

```bash
# Verify internal network
fly ssh console
wget http://my-rust-backend.internal:8080/health

# If fails, check:
# - Backend is running
# - Backend app name is correct (.internal must match)
# - Firewall rules (Fly apps can communicate by default)
```

---

### High Memory Usage

```bash
# Increase memory
fly scale memory 1024

# Or optimize Node.js
NODE_OPTIONS="--max-old-space-size=512"
```

---

## Checklist

### Pre-Deployment
- [ ] All secrets in `fly secrets` (not env vars)
- [ ] Security headers configured (CSP, HSTS)
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Dependencies audited (`pnpm audit`)
- [ ] Non-root user in Docker
- [ ] HTTPS enforced
- [ ] Health endpoint exists
- [ ] Vite configured for SSR builds

### Post-Deployment
- [ ] Security headers verified (`curl -I`)
- [ ] Rate limiting tested
- [ ] Error tracking configured
- [ ] Monitoring/alerts set up
- [ ] Backup/recovery tested
- [ ] Incident response plan documented

---

## Performance Targets

| Metric | Target | Excellent |
|--------|--------|-----------|
| Docker image size | <150MB | <100MB |
| Initial JS bundle | <100KB (gzipped) | <70KB |
| Time to First Byte (TTFB) | <200ms | <100ms |
| First Contentful Paint (FCP) | <1.8s | <1.0s |
| Largest Contentful Paint (LCP) | <2.5s | <1.5s |
| Time to Interactive (TTI) | <3.8s | <2.5s |
| Cumulative Layout Shift (CLS) | <0.1 | <0.05 |

---

## Reference

- Full deployment plan: `plans/production-deployment/`
- SSR implementation: `packages/core/src/lib/ssr/`
- Security guide: `plans/production-deployment/SECURITY.md`
- Optimization guide: `plans/production-deployment/OPTIMIZATION.md`
