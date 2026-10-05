---
name: padosoft-hono-api-conventions
description: >-
  Use this skill when writing or reviewing code in a Hono API on Bun — a new endpoint, a middleware, a
  repository or a SQL query — and whenever the user works on a controller/repository/query layer, types a
  Hono context, adds a paginated or localized list, or hits a symptom like "the type of c.get is any", "it
  returns null instead of an empty list", "page 1 skips records", "sometimes the translation is missing" or
  "the middleware types don't line up": it applies the three-layer architecture, the typed-context and
  middleware-factory patterns, and the recurring mistakes that cost the most. Do not use it for the security
  review of an endpoint (padosoft-api-security-review) nor for OpenAPI spec changes.
license: MIT
compatibility: >-
  Hono on Bun with TypeScript. The database patterns assume a driver with named placeholders (mysql2 style);
  the layering and typing rules hold with any driver.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: Three layers one direction, typed context, bound SQL, and the mistakes that keep returning.
  profiles: node, api
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: hono, bun, typescript, api, architecture, repository, sql, middleware, zod
---

# Hono API conventions

The conventions that a Hono/Bun API needs applied consistently, and the mistakes that keep coming back. The
goal: an endpoint that goes through review without the same five comments every time.

---

## 1. Three layers, one direction

**Controller → Repository → Query.** Each layer has exactly one job, and the dependency only ever points
downwards.

| Layer | Does | Never does |
|---|---|---|
| **Controller** (`src/controllers/`) | Reads the validated input (`c.req.valid("query"\|"json"\|"param")`), calls the repository, maps relations, returns `c.json(data, status)`, throws `ApiError` | SQL, business transformations |
| **Repository** (`src/repositories/`) | Calls the query, executes it, **transforms** the data, handles caching and transactions | Builds SQL strings, touches the HTTP context |
| **Query** (`src/query/`) | **Only** SQL building. Returns `[sql, params] as const` | Business logic, execution, transformation |

```ts
// src/query/loyalty/query.ts — returns the tuple, executes nothing
export function queryGetLevels(lang: string) {
    const sql = `SELECT id, COALESCE(t.descr, b.descr) AS descr
                 FROM levels b
                 LEFT JOIN languages l ON l.code = :lang
                 LEFT JOIN level_languages t ON t.level_ID = b.id AND t.languages_ID = l.id
                 ORDER BY b.id`;
    return [sql, { lang }] as const;
}

// src/repositories/loyalty/repository.ts — executes and transforms
export async function getLevelsRepo(lang: string) {
    const [sql, params] = queryGetLevels(lang);
    const [rows] = await client.execute<(RowDataPacket & Level)[]>(sql, params);
    return rows;                   // empty result → [], never null
}
```

Returning the tuple `as const` is what keeps the query layer pure and testable: a query test asserts on the
SQL string and the params, with no database.

## 2. Typed context, no assertions

Define **every** context variable in one central `Env` type, and let inference do the rest.

```ts
// src/types/env.ts
export interface AuthContext { customerId: number }
export interface Variables { auth?: AuthContext }
export interface Env { Variables: Variables }
```

```ts
// ❌ a hand-rolled shape, and a cast at every read
export function getCustomerId(c: { get: (k: string) => any }) { … }
return c.get("auth") as AuthContext | undefined;

// ✅ the real Context type, and the value is already typed
import type { Context } from "hono";
export function getCustomerId(c: Context<Env>) { return getAuth(c)?.customerId; }
return c.get("auth");
```

Every `as` on a context read means the `Variables` type is missing an entry. Fix the type, not the call site.

## 3. Middleware through the factory

```ts
// ❌ hand-typed handler: the Env generic is lost downstream
import type { MiddlewareHandler } from "hono";
export const authMiddleware = (): MiddlewareHandler<Env> => async (c, next) => { … };

// ✅ factory: the context stays typed inside the middleware and after it
import { createFactory } from "hono/factory";
const factory = createFactory<Env>();
export const authMiddleware = () => factory.createMiddleware(async (c, next) => {
    c.set("auth", { customerId });     // no assertion needed
    await next();
});
```

## 4. Environment variables through one module

```ts
import { env } from "bun";        // ❌ unvalidated, no types, fails at runtime
import { env } from "@/lib/env";  // ✅ schema-validated, fails fast at startup
```

The env module parses with a schema and **aborts on startup** when something is missing or inconsistent. A
missing variable has to break the boot, not the first request that needs it.

## 5. SQL: named placeholders and dynamic building

Named placeholders (`:name`) everywhere, never string interpolation — a SELECT literal is injection too
(`padosoft-api-security-review`, `API-SEC-SQL-001`).

```ts
// IN (…) — build the placeholders, and MERGE the params back
let params: Record<string, unknown> = { lang };
const [placeholders, arrayParams] = buildArrayPlaceholders("id", ids);   // ids is an ARRAY
sql += ` WHERE id IN (${placeholders})`;
params = { ...params, ...arrayParams };   // forget this → "Unknown parameter :id_0"
```

**Localize in SQL, not in the application.** `COALESCE(t.descr, b.descr)` beats
`row.descr_translated || row.descr`: one round trip, and the fallback is the same for everyone.

**Constrain the translation join inside its own `ON`** — the language filter on a second `LEFT JOIN` cannot
reduce rows, so you get N rows per source row: inflated pagination, and `rows[0]` picking a random row when
there is no `ORDER BY`. That is the "sometimes it doesn't translate" bug. Full explanation in
`padosoft-api-security-review` (`API-SEC-SQL-001`).


**Keep the placeholders contiguous.** A statement that binds `$1, $2, $5` and never uses `$3` and `$4` is
rejected by the server with a parameter-type error, not by the type system and not by an in-memory double.
The same class of defect hides behind every store that is not the real engine: run the provider contract
whenever a new durable path is added.

**Decode at the durable boundary, not at the call site.** A driver can return a JSON column as a *string* —
including the literal `"null"` for a nullable field — so a cached response read back inside a transaction
can be shaped differently from the same read outside it. Select the column as text at transaction
boundaries, pass everything through one decoder, and guard an absent row explicitly. A type assertion at a
JSON boundary does not strip unknown properties either: an allowlist has to run at runtime, before
persistence and before serialisation.

## 6. Transactions on multi-write

**A repository function that performs two or more writes (INSERT/UPDATE/DELETE) wraps them in a transaction
on a single connection.** Without it a partial failure leaves half the operation applied.

```ts
const conn = await client.getConnection();
try {
    await conn.beginTransaction();
    await conn.execute(sqlDelete, p1);
    await conn.execute(sqlInsert, p2);
    await conn.commit();
} catch (e) {
    await conn.rollback();
    throw e;
} finally {
    conn.release();
}
```

Pre-screen on the staged diff:

```bash
git diff --cached --name-only --diff-filter=ACMR | grep -E '^src/repositories/.*\.ts$' | while read f; do
  execs=$(grep -cE '\b(client|connection|conn)\.execute' "$f")
  writes=$(grep -ciE 'INSERT INTO|UPDATE |DELETE FROM|(insert|update|delete|upsert|remove|save)[A-Za-z]*(Sql|Query|Params)\b' "$f")
  tx=$(grep -cE 'beginTransaction|getConnection' "$f")
  [ "${execs:-0}" -ge 2 ] && [ "${writes:-0}" -ge 1 ] && [ "${tx:-0}" -eq 0 ] \
    && echo "⚠️  $f — $execs execute, $writes write signals, no transaction"
done
```

⚠️ **Do not grep for `execute("INSERT`** — in this architecture the SQL arrives from the query layer as a
*variable* (`connection.execute(deleteSql, deleteParams)`), so the keyword is never next to the call. A check
written that way reports zero on a codebase full of writes, which is the worst possible outcome: a green
check that never looked. The screen above recognises the write through the query it imports instead.

**The screen is file-level, the rule is per function.** A file with fifteen single-write functions is fine
and will still be flagged: it narrows all repositories down to a handful worth opening, and then you count
the writes *inside the function*. Confirm before reporting anything.

Two shapes come back as candidates and are **not** violations — recognise them and move on:

- **Upsert branches.** `SELECT` to check existence, then `INSERT` *or* `UPDATE`. Two writes in the text, one
  per execution path. (Worth a separate look for the check-then-act race, which a unique index closes — but
  it is not the transaction rule.)
- **A read function with many executes.** Four `SELECT`s in a loader are four executes and zero writes.

What survives is the real shape: **two writes on different rows or tables, in sequence, on the same path.**

A function whose name or docstring promises all-or-nothing semantics ("atomic", "bulk replace", "publish",
"transition") and has no transaction is a **critical** finding, not a warning. If the function only delegates
to another repository that already opens the transaction, it is fine.

## 7. Caching with a circuit breaker

Cache in the **repository**, never in the query or the controller. A cache is an optimization: when the cache
store is down the endpoint keeps answering from the database, so the cache client sits behind a circuit
breaker and a failed read is a miss, not a 500. Bound every in-memory cache with a size **and** a TTL.

## 8. Validation at the edge

The schema validates at the route, the controller reads the already-validated value. Never re-validate by
hand inside the controller, and never read `c.req.query()` raw when a validated schema exists.

**Lenient in the request, strict in the response.** An invalid optional parameter (a bad language code) is
treated as *absent* and resolved by the server fallback — never a 422 caused by that field alone. The same
field in a response or an entity stays strict: the documented contract does not bend.

## 8b. Concurrent edits: the conditional write is an API contract

An optimistic editor in the client prevents nothing while the API still accepts an unconditional
last-write-wins update. The rule lives on the server:

- **Reads return a version or content identity**; writes require it; a stale write is rejected with a
  machine-readable precondition failure, and the newer server value is left untouched.
- **The lifecycle crosses the client boundary**: capture the identity when the editor opens, attach it to
  the write, and replace it with the response's identity after a successful save. A test that proves the
  header actually crosses that boundary is the only thing that proves the feature.
- **A precondition failure without a recovery path is a safe dead end.** The client has to say that another
  writer won and offer an explicit reload of the authoritative representation together with its new
  identity — otherwise the operator is stuck holding edits they cannot apply.
- **An atomic lock does not make two incompatible transitions both valid.** Two concurrent transitions out
  of the same state are serialised, and the second one *correctly* fails. A concurrency test asserts
  atomicity **and** explicit conflict handling — never that both writes commit.

## 8c. A stream is transport, and transport does not remember

- **Filter by authenticated tenant before writing to the stream**, emit bounded heartbeats, and clean up the
  subscription on **both** request abort and response close.
- **Reconnect restores a socket, not the events lost while it was down.** Refetch the durable projection on
  the reconnect edge; use individual events only as low-latency invalidation hints.
- **Event ids alone are not replay.** Persist the event before publishing the notification, subscribe before
  replaying, deduplicate the overlap, and signal a missing or expired cursor explicitly rather than
  returning an empty result. See **`padosoft-durable-effects`**.
- **A passing stream-writer test is not a live journey.** The causal proof is: create the subscriber,
  publish a tenant-scoped event, parse it in the real client, render the connection state, assert it there.

---

## Gotchas

These are the ones that come back in review:

**0. An identifier that crosses a trust boundary needs a real random source.** A UUID-shaped string built
from the ordinary pseudo-random generator is not a security identifier, and it looks exactly like one.
Queue, job and event ids cross tenant and retry boundaries: use the runtime's cryptographic generator.

**1. `null` instead of an empty array.** The controller expects a list.

```ts
if (!rows.length) return null;   // ❌ callers crash on .map
if (!rows.length) return [];     // ✅
```

**2. Pagination offset.** `offset = page * perPage` makes page 1 skip the first page.

```ts
const offset = (page - 1) * perPage;   // ✅ page 1 → 0
```

**3. A CSV string passed where an array is expected.** `"1,7,9"` is one element, not three. Split and coerce
to numbers first.

**4. Params of a dynamic `IN` not merged** — see §5. The symptom is `Unknown parameter :id_0`.

**5. Language fallback in application code** instead of SQL `COALESCE` — see §5.

**6. A type assertion on the context** — see §2. It always means a missing `Variables` entry.

**7. `rows[0]` on a query that can return more than one row with no `ORDER BY`.** Which row arrives first is
the engine's choice, so the behaviour changes without the code changing.

**8. `LIMIT`/`OFFSET` are interpolated on purpose.** The driver does not bind them as named placeholders, so
the layering gives way here and the values are inlined. Do not "fix" one back into `:limit`: the query
breaks. Make sure the value is a schema-coerced number and leave it alone.

---

## Checklist before committing

- [ ] Query returns `[sql, params] as const` and contains no business logic
- [ ] Repository returns `[]` and not `null`; transformations live here
- [ ] Controller does no SQL and throws `ApiError` instead of returning an error shape
- [ ] No `as` on a context read; `Variables` updated if one was needed
- [ ] Middleware built with the factory
- [ ] Named placeholders only; `IN` params merged; translation join constrained in its own `ON`
- [ ] Two or more writes in one repository function → transaction
- [ ] `env` imported from the validated module
- [ ] Offset computed as `(page - 1) * perPage`
- [ ] Linter and type check clean

## Final report

```
Endpoint/change: <what>
Layers: controller <file> · repository <file> · query <file>
Conventions: <n> respected, <n> deviations (with reason)
Gotchas checked: null-vs-[] · offset · IN merge · localization · context typing · transactions
Linter/types: PASS | FAIL <detail>
To decide: <…>
```
