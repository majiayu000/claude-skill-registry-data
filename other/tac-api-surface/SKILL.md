---
name: tac-api-surface
description: >-
  Load when adding or modifying Next.js route handlers, server actions, public API endpoints, edge functions (supabase/functions/*), webhooks, or rate-limited surfaces in tac-express. Covers the security boundary between apps and services, validation patterns, error handling, rate limiting (Upstash), and the public-vs-authenticated split.
---

# TAC Express — API Surface

Use this skill when you cross the **server boundary** — anywhere user input becomes a database write, anywhere internal data leaves through a webhook, anywhere a third party hits the public API. The rules here keep that boundary tight.

> **Architecture rule:** route handlers / server actions are **thin transport layers**. They validate, authorize, and call a service. They never run business logic.

---

## The API Surfaces

| Surface | Location | Auth model |
|---|---|---|
| **Server actions** | `apps/<app>/app/**/actions.ts` (`"use server"`) | Cookie session (Supabase SSR) |
| **Route handlers** | `apps/<app>/app/api/**/route.ts` | Cookie session OR API key OR public |
| **Public tracking** | `apps/dashboard/app/api/public/**/route.ts`, `apps/web/app/track/[awb]` | Public + rate-limited |
| **Webhooks (in)** | `apps/dashboard/app/api/webhooks/**/route.ts` | HMAC signature verification |
| **Webhooks (out)** | `supabase/functions/dispatch-webhook/index.ts` | Service role + signed payloads |
| **Edge functions** | `supabase/functions/<name>/index.ts` | Service role (Deno) |
| **Health** | `apps/<app>/app/api/health/route.ts` | Public |

---

## The Boundary Pattern

Every server-side endpoint follows the same shape:

```
1. Parse + validate input (zod)             ← reject malformed early
2. Resolve identity / authorize              ← Supabase session or API key
3. Call service (packages/services)          ← business logic lives there
4. Map errors to HTTP / action result        ← never leak internals
5. Revalidate / set cookies / return         ← clean exit
```

If any step is missing, the surface is unsafe.

---

## Server Action Pattern

```ts
// apps/dashboard/app/shipments/actions.ts
"use server"

import { revalidatePath } from "next/cache"
import { cookies } from "next/headers"
import { createServerClient } from "@workspace/database/server"
import { createShipmentService } from "@workspace/services/shipment.service"
import {
  createShipmentSchema,
  type CreateShipmentInput,
} from "@workspace/types/schemas/shipment.schema"

type ActionResult<T = void> =
  | { ok: true; data: T }
  | { ok: false; error: string; field?: string }

export async function createShipmentAction(
  input: unknown
): Promise<ActionResult<{ id: string; awbNumber: string }>> {
  // 1. Validate
  const parsed = createShipmentSchema.safeParse(input)
  if (!parsed.success) {
    const issue = parsed.error.issues[0]
    return { ok: false, error: issue?.message ?? "Invalid input", field: issue?.path.join(".") }
  }

  // 2. Authorize
  const db = createServerClient(cookies())
  const { data: { user } } = await db.auth.getUser()
  if (!user) return { ok: false, error: "Unauthorized" }

  // 3. Call service
  const service = createShipmentService(db)
  try {
    const shipment = await service.create(parsed.data)
    revalidatePath("/shipments")
    return { ok: true, data: { id: shipment.id, awbNumber: shipment.awbNumber } }
  } catch (err) {
    // 4. Error mapping — never leak stack
    return { ok: false, error: err instanceof Error ? err.message : "Failed to create shipment" }
  }
}
```

> **Discriminated `ActionResult` over throwing.** Server actions called from forms render raw thrown errors as opaque toasts. A discriminated union surfaces the field-level error to react-hook-form.

---

## Route Handler Pattern (Cookie-authenticated)

```ts
// apps/dashboard/app/api/shipments/[id]/route.ts
import { NextResponse } from "next/server"
import { cookies } from "next/headers"
import { createServerClient } from "@workspace/database/server"
import { createShipmentService } from "@workspace/services/shipment.service"

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params

  const db = createServerClient(cookies())
  const { data: { user } } = await db.auth.getUser()
  if (!user) return NextResponse.json({ error: "Unauthorized" }, { status: 401 })

  try {
    const service = createShipmentService(db)
    const shipment = await service.getById(id)
    if (!shipment) return NextResponse.json({ error: "Not found" }, { status: 404 })
    return NextResponse.json({ data: shipment })
  } catch (err) {
    console.error("[shipments/get]", err)
    return NextResponse.json({ error: "Internal error" }, { status: 500 })
  }
}
```

---

## Public Endpoint Pattern (Rate-limited)

Public surfaces (`/api/public/*`, `/track/[awb]`) **must** be rate-limited. We use `@upstash/ratelimit` + `@upstash/redis` (configured in `apps/dashboard/lib/rate-limit.ts`).

```ts
// apps/dashboard/app/api/public/track/[awb]/route.ts
import { NextResponse } from "next/server"
import { headers } from "next/headers"
import { publicTrackingLimiter } from "@/lib/rate-limit"
import { createPublicTrackingService } from "@workspace/services/public-tracking.service"
import { createServerClient } from "@workspace/database/server"
import { cookies } from "next/headers"
import { isAWB } from "@workspace/types/domain.types"

export async function GET(
  _req: Request,
  { params }: { params: Promise<{ awb: string }> }
) {
  // 1. Rate-limit by IP
  const h = await headers()
  const ip = h.get("x-forwarded-for")?.split(",")[0] ?? "anonymous"
  const { success, remaining } = await publicTrackingLimiter.limit(ip)
  if (!success) {
    return NextResponse.json(
      { error: "Rate limit exceeded" },
      { status: 429, headers: { "X-RateLimit-Remaining": String(remaining) } }
    )
  }

  // 2. Validate input shape
  const { awb } = await params
  if (!isAWB(awb)) return NextResponse.json({ error: "Invalid AWB" }, { status: 400 })

  // 3. Service call (service does its own RLS-aware read)
  const db = createServerClient(cookies())
  const service = createPublicTrackingService(db)
  const result = await service.getByAwb(awb)
  if (!result) return NextResponse.json({ error: "Not found" }, { status: 404 })

  // 4. Return public-safe shape (NEVER leak customer PII or rate-card data)
  return NextResponse.json({ data: service.toPublicView(result) })
}
```

> **The `toPublicView()` helper is mandatory** for public endpoints. It strips internal fields (cost, internal notes, customer email, exception details) before serialization.

---

## API Key Endpoint Pattern

```ts
// apps/dashboard/app/api/v1/shipments/route.ts
import { NextResponse } from "next/server"
import { createApiKeyService } from "@workspace/services/api-key.service"
import { createAdminClient } from "@workspace/database/admin"

export async function POST(req: Request) {
  // Auth via API key header
  const apiKey = req.headers.get("x-api-key")
  if (!apiKey) return NextResponse.json({ error: "Missing API key" }, { status: 401 })

  const admin = createAdminClient()
  const keys = createApiKeyService(admin)
  const ctx = await keys.verifyAndResolveContext(apiKey)
  if (!ctx) return NextResponse.json({ error: "Invalid API key" }, { status: 401 })

  // Now proceed with ctx.customerId / ctx.scopes…
}
```

API keys must be hashed at rest (Argon2id or sha256+salt). The service does that. Never log the raw key.

---

## Webhook Inbound (Receiving from third parties)

```ts
// apps/dashboard/app/api/webhooks/<provider>/route.ts
import { NextResponse } from "next/server"
import { verifyWebhookSignature } from "@workspace/services/webhook.service"

export async function POST(req: Request) {
  const sig = req.headers.get("x-signature")
  const raw = await req.text()  // verify against raw body, not parsed
  if (!sig || !verifyWebhookSignature(raw, sig, process.env.WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: "Invalid signature" }, { status: 401 })
  }

  // … parse, validate, dispatch to service
}
```

> **Always verify signatures against the raw body**, not the parsed JSON. Parsing first opens you up to canonicalization attacks.

---

## Webhook Outbound (Edge function)

`supabase/functions/dispatch-webhook/index.ts` — invoked from a database trigger or scheduled job.

- Sign each payload with HMAC-SHA256 of `JSON.stringify(payload)` using the customer's webhook secret.
- Include `x-signature`, `x-event-id`, `x-event-type`, `x-timestamp`.
- Retry with exponential backoff (1m, 5m, 30m, 4h, 24h). Log each delivery in `webhook_deliveries`.
- Drop the payload after final retry; never block the trigger.

---

## Edge Functions (Deno)

Live in `supabase/functions/<name>/index.ts`. Run on Deno runtime with service-role key.

```ts
// supabase/functions/<name>/index.ts
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 })
  }

  const db = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  )

  // … business logic via direct SQL or RPC calls
})
```

Allowed: `https://esm.sh/@supabase/supabase-js@2`. **Never** install npm modules in `supabase/functions/`.

---

## Common Pitfalls

| Pattern | Issue | Fix |
|---|---|---|
| Server action throws raw `Error` | Form sees opaque toast | Return discriminated `ActionResult` |
| Public endpoint without rate-limit | Abuse vector | Wrap in `publicTrackingLimiter.limit(ip)` |
| Returning full DB row from public endpoint | PII / cost leak | Apply `toPublicView()` |
| Signature verified after `await req.json()` | Canonicalization attack | Read `await req.text()` and verify against raw |
| `console.log(apiKey)` | Credential leak | Hash at rest, log key prefix only (`tac_xxxxxxxx…`) |
| Service called without `safeParse` first | Bad input persists | Validate at the boundary |
| Throwing inside an edge function without try/catch | Function returns 500 with stack | Wrap and return `{ error }` |
| Not calling `revalidatePath` after mutation | Stale UI | Always revalidate the page that listed the entity |
| `redirect()` inside try/catch | Next throws a special error to redirect — your catch swallows it | Move redirect outside the try block |

---

## Pre-flight Checklist

```
[ ] Input validated with zod (.safeParse, never .parse)
[ ] Identity resolved (session or API key)
[ ] Authorization checked (RBAC via @workspace/auth or RLS at the DB)
[ ] Service called — no inline business logic
[ ] Errors mapped to a clean shape (ActionResult / NextResponse with appropriate status)
[ ] Public endpoints rate-limited
[ ] Sensitive fields stripped before returning
[ ] revalidatePath called after mutation
[ ] No raw secrets in logs
[ ] No @supabase/supabase-js imported here — only via @workspace/database
```
