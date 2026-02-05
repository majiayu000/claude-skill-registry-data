---
name: api-route
description: Create Next.js 16 API Route Handlers. Use when building REST endpoints (GET, POST, PUT, DELETE), implementing CRUD operations, or creating authenticated APIs with Zod validation.
---

This skill guides creation of API Route Handlers in Next.js 16 App Router.

The user needs to build REST endpoints for data operations, typically CRUD functionality with authentication and validation.

## Before You Start

API routes live in the `app/api/` directory:
- **Collection routes**: `app/api/users/route.ts` - handles GET (list) and POST (create)
- **Resource routes**: `app/api/users/[id]/route.ts` - handles GET (one), PUT, DELETE
- **Export functions**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`

**CRITICAL**: In Next.js 16, dynamic route params are async. You MUST `await params` before using them.

## ⚠️ Prisma Import Pattern - CRITICAL

```typescript
//  CORRECT - separate imports
import { Prisma } from '@prisma/client';  // Types/namespace (BookWhereInput, etc.)
import { prisma } from '@/lib/prisma';     // Instance

// WRONG - @/lib/prisma doesn't export Prisma namespace
import { prisma, Prisma } from '@/lib/prisma';
```

**Rule:**
- `prisma` (instance) → `@/lib/prisma`
- `Prisma` (types like `Prisma.BookWhereInput`) → `@prisma/client`

## ⚠️ Schema Validation - READ FIRST

**BEFORE writing ANY Prisma query:**
1. READ `prisma/schema.prisma` in Pre-loaded Code
2. ONLY use fields that EXIST in schema
3. NEVER invent fields

**Common invented fields that DON'T EXIST:**
- `featured`, `isFeatured` → Check if schema has this!
- `reviews`, `ratings` → Check if relation exists!
- `popularity`, `viewCount`, `soldCount` → Usually not in schema

```typescript
// WRONG - 'featured' doesn't exist in schema
where: { featured: true }

//  CORRECT - check schema first, use isFeatured if exists
where: { isFeatured: true }  // Only if schema has: isFeatured Boolean
```

## Prisma Relationship Matching

**CRITICAL**: Field names trong `include` PHẢI khớp CHÍNH XÁC với schema:

| Schema định nghĩa | Query sử dụng | /|
|-------------------|---------------|------|
| `categories Category[]` | `include: { categories: true }` |  |
| `categories Category[]` | `include: { category: true }` | WRONG |
| `category Category` | `include: { category: true }` |  |

**Rule**: 
- Many-to-many/One-to-many → **PLURAL** (categories, tags, posts)
- One-to-one/Many-to-one → **SINGULAR** (category, user, author)

## Many-to-Many qua Join Table

Khi có join table, PHẢI navigate qua nó:

```prisma
// Schema với join table
model Category {
  books BookCategory[]  // Đây là join table records, KHÔNG PHẢI Book[]!
}
model BookCategory {
  book Book @relation(...)
}
```

```typescript
// WRONG - books là BookCategory[], không có coverImage
const categories = await prisma.category.findMany({
  include: { books: true }
});
categories[0].books[0].coverImage  // ERROR!

//  CORRECT - include nested relation
const categories = await prisma.category.findMany({
  include: { 
    books: { 
      include: { book: { select: { id: true, coverImage: true } } }
    }
  }
});
categories[0].books[0].book.coverImage  // OK
```

## Schema Field Validation

**CRITICAL**: ONLY use fields that EXIST in the Prisma schema.

DON'T invent fields:
- `popularity`, `featuredOrder`, `originalPrice` (common mistakes)

 DO:
- Read `prisma/schema.prisma` in context first
- Only use fields defined there
- Use explicit types instead of `any`

## Route Structure

### Collection Route (List + Create)

```typescript
// app/api/users/route.ts
import { NextRequest } from 'next/server';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';
import { successResponse, handleError, ApiErrors, HttpStatus } from '@/lib/api-response';
import { auth } from '@/auth';

const createSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function GET(request: NextRequest) {
  try {
    const users = await prisma.user.findMany();
    return successResponse(users);
  } catch (error) {
    return handleError(error);
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await auth();
    if (!session) throw ApiErrors.unauthorized();

    const body = await request.json();
    const validated = createSchema.safeParse(body);
    if (!validated.success) return handleError(validated.error);

    const user = await prisma.user.create({ data: validated.data });
    return successResponse(user, 'Created', HttpStatus.CREATED);
  } catch (error) {
    return handleError(error);
  }
}
```

### Dynamic Route (Single Resource)

```typescript
// app/api/users/[id]/route.ts
import { NextRequest } from 'next/server';
import { prisma } from '@/lib/prisma';
import { successResponse, handleError, ApiErrors } from '@/lib/api-response';

interface RouteContext {
  params: Promise<{ id: string }>;
}

export async function GET(request: NextRequest, context: RouteContext) {
  try {
    const { id } = await context.params;  // MUST await in Next.js 16
    
    const user = await prisma.user.findUnique({ where: { id } });
    if (!user) throw ApiErrors.notFound('User');
    
    return successResponse(user);
  } catch (error) {
    return handleError(error);
  }
}

export async function DELETE(request: NextRequest, context: RouteContext) {
  try {
    const { id } = await context.params;
    await prisma.user.delete({ where: { id } });
    return successResponse({ message: 'Deleted' });
  } catch (error) {
    return handleError(error);
  }
}
```

## Error Handling

The `handleError()` function catches all error types automatically:
- **ZodError**: Returns 422 with formatted field errors
- **ApiException**: Returns custom status with error code
- **Generic Error**: Returns 500 with message

Use predefined errors for common cases:

```typescript
throw ApiErrors.unauthorized();      // 401 - Not logged in
throw ApiErrors.forbidden();         // 403 - No permission
throw ApiErrors.notFound('User');    // 404 - Resource not found
throw ApiErrors.badRequest('msg');   // 400 - Invalid request
throw ApiErrors.conflict('msg');     // 409 - Already exists
throw ApiErrors.validation('msg');   // 422 - Validation failed
```

## Response Format

**IMPORTANT**: `successResponse()` always wraps data in an object. Consumers must extract `.data`:

```typescript
// API returns this format:
{ success: true, data: T, message?: string }

// Consumer code:
const res = await fetch('/api/items');
const json = await res.json();
const items = json.data;  // Extract from wrapper!

// NOT this (common mistake):
const items = json;  // Wrong! json is {success, data}, not the array
```

## Handling Decimal Fields

Prisma `Decimal` type doesn't serialize to JSON as number. Convert before response:

```typescript
// Single item
const item = await prisma.item.findUnique({ where: { id } });
return successResponse({
  ...item,
  price: Number(item.price),  // Convert Decimal to number
});

// List of items
const items = await prisma.item.findMany();
return successResponse(
  items.map(item => ({
    ...item,
    price: Number(item.price),
  }))
);
```

**Tip**: Use `Float` instead of `Decimal` in schema to avoid this conversion entirely.

## Filter Parameter Convention - CRITICAL ⚠️

**Frontend gửi comma-separated string, API phải parse:**

```typescript
// WRONG - getAll only works with repeated params (?id=1&id=2)
const categories = searchParams.getAll('categoryId');

//  CORRECT - parse comma-separated string
const categories = searchParams.get('categories')?.split(',').filter(Boolean) ?? [];
const authors = searchParams.get('authors')?.split(',').filter(Boolean) ?? [];
const sort = searchParams.get('sort') || 'relevance';  // NOT 'sortBy'!
```

**Param naming rules:**
| Type | Param Name | Example |
|------|------------|---------|
| Multi-select | `categories`, `authors`, `tags` | `?categories=id1,id2,id3` |
| Single value | `sort`, `page`, `limit` | `?sort=price-asc&page=1` |
| Price range | `minPrice`, `maxPrice` | `?minPrice=10&maxPrice=100` |

**NEVER use:**
- `categoryId`, `authorId` (singular) for multi-select filters
- `sortBy` - always use `sort`

## Common Patterns

- **Search**: Use `where: { field: { contains: query, mode: 'insensitive' } }`
- **Auth check**: Always `const session = await auth()` before mutations
- **Validation**: Always use Zod schema with `safeParse()` for request body

## Pagination Pattern

For list endpoints, always support pagination:

```typescript
// app/api/items/route.ts
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get('page') ?? '1');
    const limit = parseInt(searchParams.get('limit') ?? '20');
    const skip = (page - 1) * limit;

    const [items, total] = await Promise.all([
      prisma.item.findMany({
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      prisma.item.count(),
    ]);

    return successResponse({
      items,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    });
  } catch (error) {
    return handleError(error);
  }
}
```

**Rules:**
- Default limit: 20 items
- Always return `total` count for frontend pagination UI
- Use `Promise.all` for parallel queries

## Query Optimization

**CRITICAL**: Let database do sorting/filtering, NOT JavaScript.

### WRONG - Fetch all, sort in memory
```typescript
const books = await prisma.book.findMany({ 
  include: { orderItems: true } 
});
const top10 = books
  .sort((a, b) => getTotal(b) - getTotal(a))
  .slice(0, 10);  // Fetched 1000 books just to get 10!
```

###  CORRECT - Use orderBy + take
```typescript
// Option 1: Order by relation count
const top10 = await prisma.book.findMany({
  take: 10,
  orderBy: {
    orderItems: { _count: 'desc' }
  }
});

// Option 2: Raw query for complex aggregation
const top10 = await prisma.$queryRaw`
  SELECT b.*, SUM(oi.quantity) as total_qty
  FROM "Book" b
  LEFT JOIN "OrderItem" oi ON b.id = oi."bookId"
  GROUP BY b.id
  ORDER BY total_qty DESC
  LIMIT 10
`;
```

**Rules:**
- Use `take` for LIMIT
- Use `orderBy` for sorting
- Use `_count` for relation counts
- Use `$queryRaw` for complex aggregations

## After Writing Route

Validation (typecheck, lint, tests) runs automatically at the end of implementation.
No need to run manually - proceed to next file.

NEVER:
- Skip `await` on `context.params` in dynamic routes
- Return raw data without `successResponse()` wrapper
- Skip validation on POST/PUT request bodies
- Forget auth checks on mutation endpoints

**IMPORTANT**: Always wrap route logic in try-catch and use `handleError()` for consistent error responses.
