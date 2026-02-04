---
name: fly-deployment
description: Use when deploying to Fly.io - covers single volume limitation, monorepo deployment, Dockerfile patterns for Next.js/Python, and common troubleshooting
---

# Fly.io Deployment Knowledge

## Overview

Comprehensive guide for deploying applications to Fly.io, covering configuration, Dockerfiles, volumes, and common pitfalls. Based on official documentation and real deployment experience.

## Sources

- [Fly.io Configuration Reference](https://fly.io/docs/reference/configuration/)
- [Fly Volumes Overview](https://fly.io/docs/volumes/overview/)
- [Fly.io Monorepo Deployments](https://fly.io/docs/launch/monorepo/)
- [Vercel's Official Next.js Dockerfile](https://github.com/vercel/next.js/tree/canary/examples/with-docker)

---

## Critical Limitations

### Volumes

**A Machine can only mount ONE volume.** This is the most common gotcha.

```toml
# WRONG - Will fail with "only 1 volume supported"
[[mounts]]
  source = "data"
  destination = "/data"

[[mounts]]
  source = "repos"
  destination = "/repos"

# CORRECT - Single volume with subdirectories
[[mounts]]
  source = "app_data"
  destination = "/data"

# Then use /data/repos, /data/db, etc. in your app
```

Other volume constraints:
- Volumes are pinned to specific physical hosts
- Cannot shrink volumes, only extend
- Not available during Docker build or release_command
- One-to-one mapping: 1 volume = 1 machine

### Build Context

When using `fly deploy --config path/to/fly.toml`:
- The **dockerfile path** is relative to where fly.toml is located
- The **build context** is the current working directory

For monorepos, place fly.toml files in the **project root** with dockerfile paths like `apps/api/Dockerfile`.

---

## fly.toml Configuration

### Minimal Working Example

```toml
app = "my-app"
primary_region = "dfw"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
```

### With Volume (for stateful apps)

```toml
app = "my-api"
primary_region = "dfw"

[build]
  dockerfile = "apps/api/Dockerfile"

[env]
  DB_PATH = "/data/app.db"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false  # Keep running for API
  auto_start_machines = true
  min_machines_running = 1

[[mounts]]
  source = "app_data"
  destination = "/data"

[[vm]]
  memory = "1gb"
  cpu_kind = "shared"
  cpus = 1
```

### With Build Args (for Next.js NEXT_PUBLIC_* vars)

```toml
[build]
  dockerfile = "apps/web/Dockerfile"
  [build.args]
    NEXT_PUBLIC_API_URL = "https://my-api.fly.dev"

[env]
  PORT = "3000"
  NODE_ENV = "production"
  NEXT_PUBLIC_API_URL = "https://my-api.fly.dev"
```

---

## Dockerfile Patterns

### Next.js Standalone (Official Pattern)

```dockerfile
FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# Runner
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

**Requirements:**
- `next.config.js` must have `output: 'standalone'`
- Install `sharp` if using Next.js Image optimization

### FastAPI/Python

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# IMPORTANT: Use exec form and --proxy-headers for Fly's TLS proxy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
```

### Multi-stage for External Tools

Pull binaries from official images instead of version-pinning downloads:

```dockerfile
# Pull tools from official images (always latest)
FROM ghcr.io/gitleaks/gitleaks:latest AS gitleaks
FROM aquasec/trivy:latest AS trivy

FROM python:3.11-slim

# Copy binaries
COPY --from=gitleaks /usr/bin/gitleaks /usr/local/bin/gitleaks
COPY --from=trivy /usr/local/bin/trivy /usr/local/bin/trivy

# ... rest of Dockerfile
```

---

## Monorepo Deployment

### Directory Structure

```
project-root/
├── fly.api.toml          # API config (in root)
├── fly.web.toml          # Web config (in root)
├── apps/
│   ├── api/
│   │   ├── Dockerfile    # Paths relative to root
│   │   └── ...
│   └── web/
│       ├── Dockerfile    # Paths relative to root
│       └── ...
```

### Deploy Commands

```bash
# From project root
fly deploy --config fly.api.toml
fly deploy --config fly.web.toml
```

### Dockerfile Paths for Monorepo

Since Dockerfiles are built with root as context:

```dockerfile
# In apps/api/Dockerfile
COPY apps/api/requirements.txt .
COPY apps/api/*.py /app/

# In apps/web/Dockerfile
COPY apps/web/package*.json ./
COPY apps/web/ .
```

---

## Common Commands

```bash
# Create apps
fly apps create my-app --org my-org

# Create volume (pick region with good capacity)
fly volumes create app_data --size 10 --app my-app --region dfw

# Check region capacity first
fly platform regions

# Set secrets
fly secrets set \
  API_KEY="xxx" \
  DB_URL="yyy" \
  --app my-app

# Deploy
fly deploy --config fly.api.toml

# View logs
fly logs --app my-app

# SSH into machine
fly ssh console --app my-app

# Check status
fly status --app my-app

# List volumes
fly volumes list --app my-app
```

---

## Region Selection

Check capacity before choosing:

```bash
fly platform regions
```

Pick regions with **positive capacity scores**. Negative scores mean constrained resources.

Good US options (typically):
- `dfw` - Dallas
- `lax` - Los Angeles
- `ord` - Chicago

---

## Troubleshooting

### "only 1 volume supported"
You have multiple `[[mounts]]` sections. Consolidate to one volume with subdirectories.

### Dockerfile path doubling
Example: `/apps/api/apps/api/Dockerfile`

**Cause:** fly.toml is in a subdirectory with relative dockerfile path.
**Fix:** Place fly.toml in project root with full path: `dockerfile = "apps/api/Dockerfile"`

### Build context wrong
**Symptom:** `COPY apps/web/ .` fails with "not found"
**Fix:** Deploy from project root: `fly deploy --config fly.web.toml`

### TypeScript build fails in Docker
Test locally first:
```bash
cd apps/web && npx tsc --noEmit
```

### App won't start - connection refused
Check that app binds to `0.0.0.0`, not `localhost` or `127.0.0.1`.

### HTTPS/proxy issues
For apps behind Fly's TLS proxy, add `--proxy-headers` to uvicorn or equivalent for your framework.

### Next.js "useX must be used within Provider" during build

**Symptom:** Build fails with errors like:
```
Error: useAuth must be used within an AuthProvider
Error occurred prerendering page "/dashboard"
```

**Cause:** Next.js tries to statically pre-render pages at build time. If pages use React Context hooks (like `useAuth`, `useTheme`, etc.) but the Provider isn't wrapping the component tree during SSG, the build fails.

**Fix:** Ensure your context Provider wraps the entire app in `layout.tsx`:

```tsx
// src/components/Providers.tsx
'use client'

import { ReactNode } from 'react'
import { AuthProvider } from '../hooks/useAuth'

export default function Providers({ children }: { children: ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>
}

// src/app/layout.tsx
import Providers from '../components/Providers'
import AppLayout from '../components/AppLayout'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <AppLayout>{children}</AppLayout>
        </Providers>
      </body>
    </html>
  )
}
```

**Key points:**
- The `Providers` component must have `'use client'` directive
- Wrap providers around any component that uses context hooks
- This applies to any context: Auth, Theme, Query clients, etc.

### Next.js "/app/public": not found

**Symptom:** Build fails with:
```
COPY --from=builder /app/public ./public
failed to calculate checksum: "/app/public": not found
```

**Cause:** The standard Next.js Dockerfile copies the `public` directory, but your project doesn't have one.

**Fix:** Create an empty public directory:
```bash
mkdir -p apps/web/public
touch apps/web/public/.gitkeep
```

**Note:** The `public` directory is where Next.js serves static assets (favicon, images, robots.txt, etc.). Even if empty, the directory must exist for the Dockerfile COPY to succeed.

---

## Cost Optimization

Free tier includes:
- 3 shared-cpu-1x VMs with 256MB RAM
- 3GB persistent storage
- 160GB outbound bandwidth

To minimize costs:
- Use `auto_stop_machines = true` for non-critical apps
- Use `min_machines_running = 0` when possible
- Start with `256mb` memory, increase if needed
- Use single volume with subdirectories instead of multiple volumes
