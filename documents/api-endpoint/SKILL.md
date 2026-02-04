---
name: api-endpoint
description: Creates Next.js API routes with Firebase. Use when adding GET/POST/PATCH/DELETE endpoints, implementing pagination, adding auth checks, or handling file uploads. Includes route templates and error handling.
---

# API Endpoint Skill

## Instructions

1. Create routes in `src/app/api/` following REST conventions
2. Apply security layers: Rate Limiting → Auth → Validation → Business Logic
3. Use `verifyAuth` for protected routes
4. Use `validateString`, `validateUrl` from `security-utils.ts`
5. Return Korean error messages with proper HTTP status codes

## Quick Start

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { verifyAuth } from '@/lib/auth-utils'
import { validateString, CONTENT_LIMITS } from '@/lib/security-utils'
import { checkRateLimit, getClientIdentifier, RATE_LIMIT_CONFIGS } from '@/lib/rate-limiter'

export async function POST(request: NextRequest) {
  // 1. Rate limiting
  const clientIp = getClientIdentifier(request)
  const { allowed } = checkRateLimit(clientIp, RATE_LIMIT_CONFIGS.AUTHENTICATED_WRITE)
  if (!allowed) return NextResponse.json({ error: '요청이 너무 많습니다.' }, { status: 429 })

  // 2. Auth
  const authUser = await verifyAuth(request)
  if (!authUser) return NextResponse.json({ error: '인증이 필요합니다.' }, { status: 401 })

  // 3. Validate & process...
}
```

For complete templates (dynamic routes, pagination, file upload, toggle endpoints), see [reference.md](reference.md).
