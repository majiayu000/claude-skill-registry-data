---
name: web-backend
description: Guidelines for building backend services, API routes, and data access layers in the /web project using TypeScript, Supabase, and service-oriented architecture.
---

# Web Backend Development Skill

This skill provides guidance for developing backend services and API routes in the `/web` project for CRAN/E.

## Tech Stack

- **TypeScript** for type safety
- **React Router v7** server-side capabilities (Vite SSR)
- **Supabase** for database access with generated types
- **Zod** for runtime validation
- **TTLCache** (@isaacs/ttlcache) for caching
- **AI SDK** (@ai-sdk/google) for embeddings
- **MCP** (Model Context Protocol) server implementation

## Architecture Principles

### Service Layer Pattern

All data access is organized into service classes with static methods:

- **PackageService** (`app/data/package.service.ts`) - CRAN package operations
- **AuthorService** (`app/data/author.service.ts`) - Author/maintainer operations
- **SearchService** (`app/data/search.service.ts`) - Universal search
- **PackageInsightService** (`app/data/package-insight.service.server.ts`) - Download stats, trends
- **ArticleService** (`app/data/article.service.server.ts`) - Press/blog content
- **PageInsightService** (`app/data/page-insight.service.ts`) - Analytics

### Generated Database Types

**Always use the generated Supabase types** from `app/data/supabase.types.generated.ts`:

```typescript
import { Database, Tables } from "./supabase.types.generated";

// Type a specific table
type Package = Tables<"cran_packages">;
type Author = Tables<"authors">;

// Type the database client
import { createClient } from "@supabase/supabase-js";
export const supabase = createClient<Database>(url, key);
```

**Regenerate types** when schema changes:
```bash
npm run db.types  # Requires Supabase CLI + credentials
```

### Supabase Client Pattern

Single shared client instance (`app/data/supabase.server.ts`):

```typescript
import { createClient } from "@supabase/supabase-js";
import { Database } from "./supabase.types.generated";

export const supabase = createClient<Database>(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY,
);
```

**Always:**
- Use typed queries with `from()` and typed table names
- Handle errors explicitly with `.error` checks
- Use `.maybeSingle()` for nullable results, `.single()` for required results
- Use `.select("*")` or specific columns for type safety

Example query:
```typescript
const result = await supabase
  .from("cran_packages")
  .select("*")
  .eq("name", packageName)
  .maybeSingle();

if (result.error || !result.data) {
  return null;
}

return result.data;
```

### Validation with Zod

Define schemas in `*.shape.ts` files:

```typescript
import { z } from "zod";

export const packageNameSchema = z.string().min(1).max(300);
export const packageIdSchema = z.number().int().positive().min(1);
export type PackageSlug = z.infer<typeof packageNameSchema>;
```

**Validate inputs** at service boundaries:
```typescript
static async getPackageByName(name: string) {
  packageNameSchema.parse(name);  // Throws if invalid
  // ... proceed with query
}
```

### Caching Strategy

Use TTLCache for expensive operations:

```typescript
import TTLCache from "@isaacs/ttlcache";
import { hoursToMilliseconds, minutesToMilliseconds } from "date-fns";

class PackageService {
  private static cache = new TTLCache<CacheKey, CacheValue>({
    ttl: hoursToMilliseconds(6),
    max: 1000,
  });

  static async getData(key: string) {
    const cached = this.cache.get(key);
    if (cached) return cached;

    const data = await fetchData();
    this.cache.set(key, data);
    return data;
  }
}
```

**Cache keys**: Use string literals or union types for type safety.

**TTL guidelines**:
- Sitemap/metadata: 6 hours
- Search results: 5 minutes
- Download stats: 6 hours
- Dynamic content: 1-5 minutes

### Service Class Structure

```typescript
export class ExampleService {
  // Private static cache
  private static cache = new TTLCache<CacheKey, CacheValue>({
    ttl: hoursToMilliseconds(6),
  });

  // Static methods only (stateless)
  static async getById(id: number) {
    // 1. Validate input
    idSchema.parse(id);

    // 2. Check cache
    const cached = this.cache.get(`id:${id}`);
    if (cached) return cached;

    // 3. Query database
    const result = await supabase
      .from("table_name")
      .select("*")
      .eq("id", id)
      .maybeSingle();

    // 4. Handle errors
    if (result.error) {
      slog.error("Query failed", { error: result.error, id });
      return null;
    }

    // 5. Cache and return
    if (result.data) {
      this.cache.set(`id:${id}`, result.data);
    }
    return result.data;
  }
}
```

### API Route Patterns

#### Action-based API (POST)

File: `app/routes/api.search._index.ts`

```typescript
import { ActionFunction } from "react-router";
import { SearchService } from "../data/search.service";

export const action: ActionFunction = async ({ request }) => {
  const formData = await request.formData();
  const intent = formData.get("intent");

  if (intent === "all") {
    const query = String(formData.get("q")).slice(0, 100);
    const result = await SearchService.searchUniversal(query);
    return Response.json(result);
  }

  throw new Error("Invalid intent");
};
```

**Use for:**
- Search operations
- Mutations
- Form submissions

#### Loader-based API (GET)

```typescript
export const loader: LoaderFunction = async ({ params, request }) => {
  const { packageName } = params;
  const data = await PackageService.getPackageByName(packageName);

  if (!data) {
    throw data(null, { status: 404 });
  }

  return data(data, {
    headers: {
      "Cache-Control": "public, max-age=3600",
    },
  });
};
```

**Use for:**
- Page data loading
- Read-only operations
- SSR data fetching

#### MCP Server Endpoint

File: `app/routes/api.mcp.ts`

Singleton transport pattern for stateful MCP connections:

```typescript
let transport: WebStandardStreamableHTTPServerTransport | null = null;

function getTransport() {
  if (!transport) {
    transport = new WebStandardStreamableHTTPServerTransport({});
    const server = getMcpServer();
    server.connect(transport);
  }
  return transport;
}

export async function loader({ request }: LoaderFunctionArgs) {
  return getTransport().handleRequest(request);
}
```

### Error Handling

Use structured logging (`app/modules/observability.server.ts`):

```typescript
import { slog } from "../modules/observability.server";

try {
  const result = await someOperation();
} catch (error) {
  slog.error("Operation failed", {
    error,
    context: { userId, action },
  });
  throw error;
}
```

**Log levels:**
- `slog.info()` - Informational events
- `slog.warn()` - Warning conditions
- `slog.error()` - Error conditions

### Type Patterns

#### Tables Type Helper

```typescript
import { Tables } from "../data/supabase.types.generated";

type Pkg = Tables<"cran_packages">;
type Author = Tables<"authors"> & { roles: string[] };
```

#### Custom Types

Define in `app/data/types.ts`:

```typescript
export type PackageRelationshipType =
  | "depends"
  | "imports"
  | "suggests"
  | "linking_to"
  | "enhances"
  | "reverse_depends"
  | "reverse_imports"
  | "reverse_suggests"
  | "reverse_enhances"
  | "reverse_linking_to";

export type PackageDependency = {
  relationship_type: PackageRelationshipType;
  version: string | null;
  related_package: { id: number; name: string };
};
```

#### Loader Data Types

```typescript
type LoaderData = {
  item: Tables<"cran_packages">;
  relations: Partial<Record<PackageRelationshipType, PackageDependency[]>>;
  authors: Author[];
  maintainer: Author;
  // ... other fields
};

export const loader: LoaderFunction = async ({ params }) => {
  const data: LoaderData = await buildLoaderData(params);
  return data(data);
};
```

### External API Integration

Example: CRAN Logs API (PackageInsightService)

```typescript
class PackageInsightService {
  private static readonly CRAN_LOGS_URL = "https://cranlogs.r-pkg.org";

  private static async fetchFromCRAN<T>(path: string): Promise<T | null> {
    try {
      const response = await fetch(`${this.CRAN_LOGS_URL}${path}`);
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      slog.error("CRAN API fetch failed", { error, path });
      return null;
    }
  }

  static async getTopDownloadedPackages(period: string, count: number) {
    const cached = this.cache.get(`/top/${period}/${count}`);
    if (cached) return cached;

    const data = await this.fetchFromCRAN<TopDownloadsResponse>(
      `/top/${period}/${count}`
    );

    if (data) this.cache.set(`/top/${period}/${count}`, data);
    return data || [];
  }
}
```

### Async Operations

Use `Promise.allSettled()` for parallel operations with error handling:

```typescript
const [packages, authors] = await Promise.allSettled([
  PackageService.searchPackages(query),
  AuthorService.searchAuthors(query),
]);

if (packages.status === "rejected") {
  slog.error("Package search failed", { error: packages.reason });
}

const packageHits =
  packages.status === "fulfilled"
    ? packages.value
    : { combined: [], isSemanticPreferred: false };
```

### Environment Variables

Define in `app/data/env.ts` with Zod validation:

```typescript
import { z } from "zod";

const envSchema = z.object({
  SUPABASE_URL: z.string().url(),
  SUPABASE_ANON_KEY: z.string().min(1),
  // ... other vars
});

export const env = envSchema.parse(process.env);
```

**Access:** `import { env } from "./data/env";`

### Database Query Patterns

#### Simple Select
```typescript
const packages = await supabase
  .from("cran_packages")
  .select("id, name, title")
  .limit(10);
```

#### With Filters
```typescript
const result = await supabase
  .from("cran_packages")
  .select("*")
  .eq("name", packageName)
  .maybeSingle();
```

#### With Joins (via foreign keys)
```typescript
const result = await supabase
  .from("package_relations")
  .select(`
    relationship_type,
    version,
    related_package:related_package_id (
      id,
      name
    )
  `)
  .eq("package_id", packageId);
```

#### Full-text Search
```typescript
const results = await supabase
  .from("cran_packages")
  .select("name, title, description")
  .textSearch("name", query, { type: "websearch" })
  .limit(50);
```

#### Vector/Embedding Search
```typescript
const embeddings = await supabase.rpc("match_package_embeddings", {
  query_embedding: embedding,
  match_threshold: 0.5,
  match_count: 10,
});
```

### Performance Best Practices

1. **Always limit queries**: Use `.limit()` to prevent over-fetching
2. **Select specific columns**: Avoid `SELECT *` when possible
3. **Cache expensive operations**: Use TTLCache for repeated queries
4. **Parallel fetching**: Use `Promise.all()` or `Promise.allSettled()`
5. **Deduplicate results**: Use `uniqBy()` from `es-toolkit`
6. **Lazy load heavy data**: Split large queries into smaller chunks

### Utility Functions

Use `es-toolkit` for data manipulation:
```typescript
import { groupBy, uniqBy, omit } from "es-toolkit";

const grouped = groupBy(items, (item) => item.type);
const unique = uniqBy(items, (item) => item.id);
const cleaned = omit(obj, ["sensitiveField"]);
```

Use `date-fns` for date operations:
```typescript
import {
  format,
  formatRelative,
  subDays,
  hoursToMilliseconds,
  minutesToSeconds,
} from "date-fns";
```

### AI Integration

Embeddings for semantic search:
```typescript
import { google } from "@ai-sdk/google";
import { embed } from "ai";

const { embedding } = await embed({
  model: google.textEmbeddingModel("text-embedding-004"),
  value: query,
});
```

### File Organization

- **Service classes**: `/web/app/data/*.service.ts` or `*.service.server.ts`
- **Type definitions**: `/web/app/data/*.shape.ts` (Zod), `*.types.generated.ts` (Supabase)
- **Custom types**: `/web/app/data/types.ts`
- **API routes**: `/web/app/routes/api.*.ts`
- **Server utilities**: `/web/app/modules/*.server.ts`

### Server-Only Code

Files with `.server.ts` suffix are excluded from client bundles. Use for:
- Supabase client initialization
- Environment variable access
- External API calls
- Logging/observability
- MCP server logic

## Testing Strategy

- **Typecheck**: `npm run typecheck` catches type errors
- **Build**: `npm run build` validates server code compiles
- **Lint**: `npm run lint` enforces code quality
- No unit tests; rely on TypeScript + runtime validation

## Common Pitfalls to Avoid

1. **Don't instantiate service classes** - Use static methods only
2. **Don't bypass Zod validation** - Always validate at service boundaries
3. **Don't ignore Supabase errors** - Check `.error` property
4. **Don't skip caching** - Cache expensive DB/API calls
5. **Don't use `any` types** - Leverage generated Supabase types
6. **Don't forget `.server.ts` suffix** - Keep server code out of client bundle
7. **Don't hardcode URLs** - Use environment variables

## Environment

- Node >= 20 (v23.3.0 recommended)
- npm with `legacy-peer-deps = true`
- Required env vars: `SUPABASE_URL`, `SUPABASE_ANON_KEY`
- Optional: `GOOGLE_GENERATIVE_AI_API_KEY` for embeddings
