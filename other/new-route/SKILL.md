---
name: new-route
description: Use when creating a new API route — scaffolds with ZAO OS conventions (Zod, session, NextResponse, try/catch)
disable-model-invocation: true
argument-hint: "[feature/action] e.g. music/favorites"
---

# New Route — Scaffold a ZAO OS API Route

Creates a new API route following all conventions from `.claude/rules/api-routes.md`.

## Usage

```
/new-route music/favorites
```

## Non-Negotiable Requirements (every generated route MUST satisfy ALL five)

1. **Zod validation:** Import `z` from `zod`, define a schema, and call `.safeParse()` on all input. GET routes validate query params; POST/PUT/PATCH/DELETE validate the request body.
2. **Auth check:** Every exported handler — including GET — MUST call `getSession()` and check `session?.fid`. Return 401 if missing. No exceptions.
3. **try/catch wrapper:** The entire handler body MUST be wrapped in try/catch. The catch block logs the error server-side and returns a sanitized 500 via `NextResponse.json`.
4. **NextResponse.json only:** Every return statement MUST use `NextResponse.json()`. Never use plain `Response`, `new Response()`, or raw strings.
5. **No hardcoded secrets:** NEVER include literal env var values, API keys, tokens, or secrets in the generated code. Access secrets only via `process.env.VAR_NAME` and only in server-side code. Never return env var values in any response body.

## Scaffold Templates

Create `src/app/api/$ARGUMENTS/route.ts`. Use the matching template below based on the HTTP method the user requests.

### POST / PUT / PATCH / DELETE Template

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth/session';
import { supabaseAdmin } from '@/lib/db/supabase';

const RequestSchema = z.object({
  // Define input schema here
});

export async function POST(request: NextRequest) {
  try {
    const session = await getSession();
    if (!session?.fid) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const parsed = RequestSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json(
        { error: 'Invalid input', details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    // Implementation here — use parsed.data for validated input

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('[API] $ARGUMENTS error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### GET Template

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth/session';
import { supabaseAdmin } from '@/lib/db/supabase';

const QuerySchema = z.object({
  // Define query param schema here — all values are strings from URLSearchParams
  // Use z.coerce.number() for numeric params
});

export async function GET(request: NextRequest) {
  try {
    const session = await getSession();
    if (!session?.fid) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const parsed = QuerySchema.safeParse(Object.fromEntries(searchParams));
    if (!parsed.success) {
      return NextResponse.json(
        { error: 'Invalid input', details: parsed.error.flatten() },
        { status: 400 }
      );
    }

    // Implementation here — use parsed.data for validated input

    return NextResponse.json({ data: [] });
  } catch (error) {
    console.error('[API] $ARGUMENTS error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Rules

- Always validate with Zod `safeParse` before processing — GET routes validate query params, mutation routes validate body
- **Every handler (GET included) MUST check `session?.fid` and return 401 if missing** — there are no public API routes unless the user explicitly requests one, and even then add a code comment explaining why auth is skipped
- Always return `NextResponse.json()` — never plain Response
- Always wrap in try/catch with sanitized 500 response
- **NEVER hardcode API keys, tokens, secrets, or env var values in generated code** — only reference them via `process.env.VAR_NAME` and never include their values in response payloads
- Never expose server-only env vars (`SUPABASE_SERVICE_ROLE_KEY`, `NEYNAR_API_KEY`, `SESSION_SECRET`, `APP_SIGNER_PRIVATE_KEY`) in responses
- Use `Promise.allSettled` for parallel fault-tolerant operations
- Ask the user what HTTP method and what the route should do before writing
