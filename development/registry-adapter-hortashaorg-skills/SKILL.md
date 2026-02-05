---
name: registry-adapter
description: Generate a new package registry adapter for the worker service. Creates schema, client, mapper, and index files following the npm adapter pattern. Use when adding support for a new package registry (jsr, brew, apt, etc.).
---

# Registry Adapter Generator

Generate a complete registry adapter for fetching package data from a new registry API.

## Output Structure

Each adapter produces 4 files in `services/worker/registries/{registry}/`:

```
registries/{registry}/
├── index.ts     # Public API: getPackages()
├── schema.ts    # Zod schemas for API response validation
├── client.ts    # HTTP client with fetch functions
└── mapper.ts    # Transform API response → PackageData
```

## Required Reading

Before generating, read these reference files:

1. **`/skills/services/worker/registries/types.ts`** - Common types all adapters must return
2. **`/skills/services/worker/registries/npm/schema.ts`** - Schema pattern
3. **`/skills/services/worker/registries/npm/client.ts`** - Client pattern
4. **`/skills/services/worker/registries/npm/mapper.ts`** - Mapper pattern
5. **`/skills/services/worker/registries/npm/index.ts`** - Public API pattern

## Workflow

### Stage 1: Discovery

Gather these requirements:

1. **Registry Name** - lowercase (e.g., "jsr", "brew", "apt")
2. **API Base URL** - The registry's API endpoint
3. **API Documentation URL** - For reference during development
4. **Package endpoint pattern** - How to fetch a single package (e.g., `/packages/{name}`)

### Stage 2: API Research

Before generating, understand the target API:

1. Fetch a sample package response from the API
2. Identify fields that map to `PackageData`:
   - `name` (required)
   - `description` (optional)
   - `homepage` (optional)
   - `repository` (optional)
   - `latestVersion` (optional)
   - `distTags` (optional)
   - `versions[]` with dependencies

3. Note any API quirks:
   - Authentication requirements
   - Rate limiting headers
   - Pagination for versions
   - Different dependency formats

### Stage 3: Confirm

Present summary:
```
I'll create {REGISTRY} adapter with:
- API: {BASE_URL}
- Package endpoint: {ENDPOINT_PATTERN}
- Files: index.ts, schema.ts, client.ts, mapper.ts

Generate?
```

### Stage 4: Generate

**1. schema.ts** - Zod schemas for API validation

```tsx
import { z } from "zod";

// Define schemas matching the actual API response
export const {Registry}VersionSchema = z.object({
  version: z.string(),
  dependencies: z.record(z.string(), z.string()).optional(),
  // ... other fields from API
});

export const {Registry}PackageSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  // ... match actual API response structure
});

export type {Registry}VersionResponse = z.infer<typeof {Registry}VersionSchema>;
export type {Registry}PackageResponse = z.infer<typeof {Registry}PackageSchema>;

export const schemas = {
  version: {Registry}VersionSchema,
  package: {Registry}PackageSchema,
};
```

**2. client.ts** - HTTP client

```tsx
import ky, { HTTPError } from "ky";
import type { z } from "zod";
import type { {Registry}PackageResponse } from "./schema.ts";
import { schemas } from "./schema.ts";

const {REGISTRY}_API = "{BASE_URL}";

export class {Registry}SchemaError extends Error {
  packageName: string;
  registryName = "{registry}";
  zodError: z.ZodError;

  constructor(packageName: string, zodError: z.ZodError) {
    super(
      `{registry} API response for "${packageName}" failed schema validation: ${zodError.message}`,
    );
    this.name = "{Registry}SchemaError";
    this.packageName = packageName;
    this.zodError = zodError;
  }
}

const client = ky.create({
  prefixUrl: {REGISTRY}_API,
  timeout: 30_000,
  retry: {
    limit: 2,
    methods: ["get"],
    statusCodes: [408, 429, 500, 502, 503, 504],
  },
});

export async function fetchPackage(name: string): Promise<{Registry}PackageResponse> {
  const raw = await client.get(/* endpoint pattern */).json();

  const parseResult = schemas.package.safeParse(raw);
  if (!parseResult.success) {
    throw new {Registry}SchemaError(name, parseResult.error);
  }

  return parseResult.data;
}

export async function fetchPackages(
  names: string[],
  concurrency = 5,
): Promise<Map<string, {Registry}PackageResponse | Error>> {
  // Same pattern as npm client - batch with concurrency control
}
```

**3. mapper.ts** - Transform to common format

```tsx
import type { DependencyData, PackageData, VersionData } from "../types.ts";
import type { {Registry}PackageResponse } from "./schema.ts";

export function map{Registry}Package(response: {Registry}PackageResponse): PackageData {
  return {
    name: response.name,
    description: response.description,
    homepage: /* extract from response */,
    repository: /* extract from response */,
    latestVersion: /* extract from response */,
    distTags: /* extract from response */,
    versions: mapVersions(response),
  };
}

function mapVersions(response: {Registry}PackageResponse): VersionData[] {
  // Transform registry-specific version format to common VersionData
}

function mapDependencies(/* registry-specific version */): DependencyData[] {
  // Transform to { name, versionRange, type: "runtime"|"dev"|"peer"|"optional" }
}
```

**4. index.ts** - Public API

```tsx
import type { FetchResult } from "../types.ts";
import { fetchPackages } from "./client.ts";
import { map{Registry}Package } from "./mapper.ts";

export { {Registry}SchemaError } from "./client.ts";

export async function getPackages(
  names: string[],
  concurrency = 5,
): Promise<FetchResult> {
  const rawResults = await fetchPackages(names, concurrency);
  const results: FetchResult = new Map();

  for (const [name, result] of rawResults) {
    if (result instanceof Error) {
      results.set(name, result);
    } else {
      results.set(name, map{Registry}Package(result));
    }
  }

  return results;
}
```

### Stage 5: Register & Validate

**1. Add export to registries/index.ts:**

```tsx
export * as {registry} from "./{registry}/index.ts";
```

**2. Add to registry enum (if not already present):**

In `packages/database/db/schema.ts`:
```tsx
export const registryEnum = pgEnum("registry", ["npm", "jsr", "brew", "apt", "{registry}"]);
```

Then run: `pnpm database zero`

**3. Validate:**

```bash
cd /skills/services/worker && pnpm typecheck
cd /skills/services/worker && pnpm check
```

**Post-generation response:**
```
✅ Generated {REGISTRY} adapter successfully!

Files created:
- services/worker/registries/{registry}/index.ts
- services/worker/registries/{registry}/schema.ts
- services/worker/registries/{registry}/client.ts
- services/worker/registries/{registry}/mapper.ts

Registered in: services/worker/registries/index.ts

Validation: ✅ TypeScript ✅ Biome

Usage:
import { {registry} } from "./registries/index.ts";
const results = await {registry}.getPackages(["package-name"]);
```

## Common Types Reference

All adapters must return data conforming to these types:

```tsx
interface PackageData {
  name: string;
  description?: string;
  homepage?: string;
  repository?: string;
  latestVersion?: string;
  distTags?: Record<string, string>;
  versions: VersionData[];
}

interface VersionData {
  version: string;
  publishedAt: Date;
  isPrerelease: boolean;
  isYanked: boolean;
  dependencies: DependencyData[];
}

interface DependencyData {
  name: string;
  versionRange: string;
  type: "runtime" | "dev" | "peer" | "optional";
}
```

## Registry-Specific Notes

### jsr (jsr.io)
- API: `https://api.jsr.io`
- Endpoint: `/packages/{scope}/{name}`
- Uses scoped packages like `@std/path`
- Has `exports` instead of traditional entry points

### brew (Homebrew)
- API: `https://formulae.brew.sh/api`
- Endpoint: `/formula/{name}.json`
- No version history - only latest
- Dependencies are system-level, not versioned

### apt (Debian/Ubuntu)
- No single API - would need to parse package index files
- Consider using `packages.debian.org` or `api.launchpad.net`
- Complex: multiple distributions, architectures

## Key Principles

1. **Schema validation first** - Catch API changes early
2. **Consistent error types** - Use `{Registry}SchemaError` pattern
3. **Concurrency control** - Respect rate limits with batching
4. **Clean mapping** - Transform all registry quirks in mapper, not elsewhere
5. **Type safety** - All responses validated through Zod before use

## Start

Ask the user which registry they'd like to add support for.
