---
name: monitoring-setup
description: Configures error tracking (Sentry), product analytics (PostHog), health monitoring, and alerting. Provides verification commands and concrete output templates. Use when the user asks to "set up monitoring", "add error tracking", "configure Sentry", "add analytics", or "set up alerts". Don't use for deployment (use deployment-engineer), security (use security-auditor), or integration linking (use integration-linker).
---

# Monitoring Setup

Sets up production monitoring so you know when things break before your users tell you.

## How It Works

1. Detect what monitoring already exists
2. Set up error tracking (Sentry recommended)
3. Set up product analytics (PostHog recommended)
4. Configure health checks and uptime monitoring
5. Verify everything works

## Step-by-Step Procedure

### Step 1: Detect Current Monitoring
```bash
# Check for error tracking
grep -rn "@sentry/\|sentry-sdk\|SENTRY_DSN" package.json requirements.txt --include="*.env*" . 2>/dev/null | head -5

# Check for analytics
grep -rn "posthog\|gtag\|mixpanel\|amplitude\|NEXT_PUBLIC_POSTHOG\|GA_TRACKING_ID" --include="*.ts" --include="*.tsx" --include="*.env*" . 2>/dev/null | head -5

# Check for logging
grep -rn "winston\|pino\|structlog\|loguru\|bunyan" package.json requirements.txt 2>/dev/null

# Check for health endpoints
grep -rn "health\|healthz\|readyz\|livez" --include="*.ts" --include="*.js" --include="*.py" . 2>/dev/null | head -5

# Check for error boundaries (React/Next.js)
grep -rn "ErrorBoundary\|error.tsx\|error.jsx\|componentDidCatch" --include="*.ts" --include="*.tsx" . 2>/dev/null | head -5
```

### Step 2: Set Up Sentry (Error Tracking)

For **Next.js** (most common vibe-coded stack):
```bash
npx @sentry/wizard@latest -i nextjs
```
This auto-creates: `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`, updates `next.config.js`.

Add to `.env.example`:
```
SENTRY_DSN=
SENTRY_AUTH_TOKEN=
```

**Verify Sentry works:**
```typescript
// Add to any page temporarily:
<button onClick={() => { throw new Error("Sentry test error"); }}>Test Sentry</button>
```

### Step 3: Set Up PostHog (Product Analytics)
```bash
npm install posthog-js posthog-node
```

Create provider (`providers/posthog.tsx`):
```tsx
'use client'
import posthog from 'posthog-js'
import { PostHogProvider } from 'posthog-js/react'

if (typeof window !== 'undefined') {
  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://us.i.posthog.com',
  })
}
export function PHProvider({ children }: { children: React.ReactNode }) {
  return <PostHogProvider client={posthog}>{children}</PostHogProvider>
}
```

### Step 4: Add Health Check Endpoint
```typescript
// app/api/health/route.ts (Next.js App Router)
export function GET() {
  return Response.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || 'unknown',
    uptime: process.uptime(),
  });
}
```

**Verify:** `curl http://localhost:3000/api/health`

### Step 5: Set Up Structured Logging (Replace console.log)
```bash
npm install pino pino-pretty
```

```typescript
// lib/logger.ts
import pino from 'pino'
export const logger = pino({ level: process.env.LOG_LEVEL || 'info' })
// Usage: logger.info({ userId }, 'User logged in')
```

## Output Format

```markdown
## 📊 Monitoring Audit Report

### Error Tracking
| Check | Status | Details |
|-------|--------|---------|
| Sentry SDK installed | {✅/❌} | {version or "not found"} |
| Sentry DSN configured | {✅/❌} | {in .env.example or "missing"} |
| Error boundaries (frontend) | {✅/❌} | {count found or "none"} |
| Server-side error handling | {✅/❌} | {middleware or "none"} |

### Product Analytics
| Check | Status | Details |
|-------|--------|---------|
| PostHog/analytics SDK | {✅/❌} | {provider or "not found"} |
| Page view tracking | {✅/❌} | {auto or manual} |
| Event tracking | {✅/⚠️/❌} | {custom events found or "none"} |

### Health & Logging
| Check | Status | Details |
|-------|--------|---------|
| Health endpoint | {✅/❌} | {path or "not found"} |
| Structured logging | {✅/❌} | {library or "console.log only"} |
| Uptime monitoring | {✅/❌} | {service or "not configured"} |

### Recommendations
1. **{Most critical}** — {why it matters for your users}
2. **{Second priority}** — {why it matters}
3. **{Third priority}** — {why it matters}

### Setup Commands (Copy-Paste Ready)
{Provide exact commands to install and configure each missing component}
```
