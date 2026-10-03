---
name: trace
description: Follow a request end-to-end through the stack from route to database
type: review
version: v0.1
argument-hint: <route, endpoint, or feature to trace, e.g. "/api/products" or "user login flow">
---

# Trace

Follow a request or feature flow end-to-end through the application stack, mapping every layer from the entry point to the database and back.

## Process

1. **Identify the entry point** from `$ARGUMENTS`:
   - API route or page route → find the route handler or page component.
   - Feature name → identify the primary user action and its entry point.
   - tRPC procedure → find the router definition.
   - If unclear, ask the user for specifics.

2. **Read `CLAUDE.md`** for project conventions and architecture.

3. **Trace forward through the stack:**

   **Layer 1 — Entry Point:**
   - Route handler, page component, or API endpoint.
   - What middleware runs before it (auth, rate limiting, etc.).
   - What parameters/inputs it receives.

   **Layer 2 — Business Logic:**
   - Service functions, tRPC procedures, or server actions called.
   - Validation and transformation logic.
   - Authorization checks.

   **Layer 3 — Data Access:**
   - Database queries (Drizzle, Prisma, raw SQL).
   - External API calls.
   - Cache reads/writes.
   - What tables/collections are touched.

   **Layer 4 — Response:**
   - How the response is constructed.
   - What data is returned to the client.
   - Error handling at each layer.

4. **Map the data flow:**
   - What types are used at each boundary.
   - Where data is transformed or mapped.
   - Where validation happens.
   - Where errors are caught and how they propagate.

5. **Identify concerns:**
   - N+1 queries or redundant data fetches.
   - Missing error handling at layer boundaries.
   - Auth/authz gaps.
   - Type mismatches between layers.
   - Performance bottlenecks (large queries, missing indexes, unnecessary joins).

## Output

### Trace: [route/feature name]

```
[Entry] → [Middleware] → [Handler] → [Service] → [DB Query] → [Response]
file.ts:10   auth.ts:5    route.ts:20  svc.ts:45   db.ts:30     route.ts:25
```

### Layer-by-Layer

#### 1. Entry Point
- **File**: `app/api/route.ts:10`
- **Method**: GET/POST
- **Middleware**: auth, rate-limit
- **Input**: params, body, query

#### 2. Business Logic
- **File**: `services/foo.ts:45`
- **Called by**: route handler
- **Validates**: [what]
- **Calls**: [what functions/services]

#### 3. Data Access
- **File**: `db/queries/foo.ts:30`
- **Table(s)**: `products`, `categories`
- **Query type**: SELECT with JOIN
- **Indexes used**: [if identifiable]

#### 4. Response
- **Shape**: `{ data: Product[], count: number }`
- **Error cases**: 401, 404, 500

### Data Flow
```
Input (params) → validated → service call → DB query → transform → response
```

### Concerns Found
- [Any issues identified during the trace]

## Constraints
- Follow the actual code path — do not guess or assume based on naming conventions.
- Read each file in the chain; do not skip layers.
- Keep the output focused on the specific route/feature — do not map the entire application.
- If a layer uses dynamic dispatch or plugin patterns that make the path ambiguous, note the ambiguity.
- Do not modify any code — this is a read-only analysis.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
