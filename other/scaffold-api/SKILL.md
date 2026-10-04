---
name: scaffold-api
description: Scaffold a Next.js App Router API route (route.ts) for FixNow with zod validation, auth check via NextAuth, Drizzle ORM access, and proper error handling. Use when user says "tạo API endpoint X", "scaffold POST /api/appointments", "thêm route handler GET /api/parts".
---

# scaffold-api

Tạo API route mới theo pattern FixNow.

## Hỏi user (nếu chưa rõ)

1. HTTP method (GET / POST / PATCH / DELETE).
2. Path (vd: `/api/appointments/[code]/status`).
3. Auth: none / customer / admin / owner-only?
4. Input schema (body / query params)?
5. Response shape mong muốn?

Reference `docs/routes.md` để xem endpoint nào đã định nghĩa sẵn.

## Workflow

### 1. Tạo zod schema (nếu chưa có)

`lib/validations/<feature>.ts`:

```ts
import { z } from 'zod';

export const exampleSchema = z.object({
  field1: z.string().min(1, 'Bắt buộc'),
  field2: z.number().int().positive(),
});

export type ExampleInput = z.infer<typeof exampleSchema>;
```

### 2. Tạo route handler

`app/api/<path>/route.ts`:

```ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { eq } from 'drizzle-orm';
import { db } from '@/db';
import { someTable } from '@/db/schema';
import { auth } from '@/lib/auth';
import { exampleSchema } from '@/lib/validations/feature';

export async function POST(req: NextRequest) {
  try {
    // Auth check
    const session = await auth();
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }
    // Role check (nếu admin only)
    // if ((session.user as any).role !== 'ADMIN') {
    //   return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    // }

    // Parse + validate
    const body = await req.json();
    const data = exampleSchema.parse(body);

    // DB work (transaction nếu multi-step)
    const [row] = await db.insert(someTable).values(data).returning();

    return NextResponse.json({ data: row }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.flatten() },
        { status: 400 }
      );
    }
    console.error('[POST /api/<path>]', error);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}
```

### 3. Dynamic route params (Next.js 15+ async params)

```ts
export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ code: string }> }
) {
  const { code } = await params;
  // ...
}
```

### 4. Query string

```ts
const { searchParams } = req.nextUrl;
const status = searchParams.get('status');
const page = parseInt(searchParams.get('page') ?? '1', 10);
```

### 5. Read explicit columns (KHÔNG trả passwordHash)

```ts
const user = await db.query.users.findFirst({
  where: eq(users.phone, phone),
  columns: { id: true, fullName: true, phone: true, role: true },
});
```

### 6. Test bằng curl

```bash
curl -X POST http://localhost:3000/api/<path> \
  -H "Content-Type: application/json" \
  -d '{"field":"value"}'
```

## Checklist

- [ ] try/catch wrap toàn bộ.
- [ ] zod validate input trước khi dùng.
- [ ] Auth check đúng requirement.
- [ ] Explicit `columns` để loại passwordHash khỏi response.
- [ ] Multi-step writes wrap trong `db.transaction(...)`.
- [ ] Status code đúng (200/201/400/401/403/404/500).
- [ ] Log error với prefix `[METHOD /path]`.
- [ ] Update `docs/routes.md` bảng API.
- [ ] Test curl / Postman.

## Pattern cho từng loại endpoint

| Loại | Auth | Response |
|------|------|----------|
| Public GET | none | 200 |
| Create (POST) | tùy | 201 + body |
| Update (PATCH/PUT) | owner/admin | 200 + body |
| Delete | owner/admin | 204 (no body) |
| Login/register | none | 200 + session cookie |

## Liên kết

- Phức tạp → spawn agent `fixnow-api-builder`.
- Cần đổi schema trước → skill `db-migrate`.
