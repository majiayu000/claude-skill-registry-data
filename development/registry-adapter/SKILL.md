---
name: registry-adapter
description: Generate a new package registry adapter for the worker service. Creates schema, client, mapper, and index files following the npm adapter pattern. Use when adding support for a new package registry.
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
2. **`/skills/services/worker/registries/npm/`** - Primary reference (single API endpoint)
3. **`/skills/services/worker/registries/jsr/`** - Reference for separate endpoints + cross-registry deps
4. **`/skills/services/worker/registries/index.ts`** - Registry dispatcher (add new registry here)

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
   - `distTags` (optional) - release channels like "latest", "next", "beta"
   - `releaseChannels[]` with dependencies

3. Note any API quirks:
   - Authentication requirements
   - Rate limiting headers
   - Pagination for versions
   - Different dependency formats
   - **Separate endpoints** - Some APIs split data across multiple endpoints (e.g., JSR has separate `/dependencies` endpoint)
   - **Cross-registry dependencies** - Can packages depend on other registries? (e.g., JSR packages can depend on npm packages)

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
import { z } from "@package/common";

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
import type { z } from "@package/common";
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
import type { Registry } from "@package/database/server";
import type { DependencyData, PackageData, ReleaseChannelData } from "../types.ts";
import type { {Registry}FetchResult } from "./client.ts";

export function map{Registry}Package(result: {Registry}FetchResult): PackageData {
  return {
    name: result.package.name,
    description: result.package.description,
    homepage: /* extract from response, or undefined if not provided */,
    repository: /* extract from response */,
    latestVersion: /* extract from response */,
    distTags: /* extract from response */,
    releaseChannels: mapReleaseChannels(result),
  };
}

function mapReleaseChannels(result: {Registry}FetchResult): ReleaseChannelData[] {
  // Transform registry-specific format to ReleaseChannelData[]
  // Most registries only have "latest" channel
  // npm has dist-tags: latest, next, beta, etc.
}

function mapDependencies(/* registry-specific deps */): DependencyData[] {
  // Transform to { name, versionRange, type, registry }
  // IMPORTANT: Set registry on each dependency (required field)
  // For cross-registry deps, parse the specifier (e.g., "npm:lodash" → registry: "npm")
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
import * as {registry} from "./{registry}/index.ts";

export * as {registry} from "./{registry}/index.ts";
```

**2. Add to dispatcher switch in registries/index.ts:**

```tsx
export async function getPackages(registry: Registry, names: string[], concurrency = 5) {
  switch (registry) {
    case "npm":
      return npm.getPackages(names, concurrency);
    case "{registry}":
      return {registry}.getPackages(names, concurrency);
    // ... other cases
  }
}
```

**3. Add to registry enum (if not already present):**

In `packages/database/db/schema/enums.ts`:
```tsx
export const registryEnum = pgEnum("registry", ["npm", "jsr", "{registry}"]);
```

Then run: `pnpm database zero && pnpm database migrate`

**4. Validate:**

```bash
pnpm check && pnpm all typecheck
```

**5. Test the adapter:**

```bash
cd /skills/services/worker && pnpm dlx tsx -e "
import { fetchPackageWithVersion } from './registries/{registry}/client.ts';

async function test() {
  const result = await fetchPackageWithVersion('{test-package-name}');
  console.log('Package:', result.package.name);
  console.log('Latest version:', result.package.latestVersion);
  console.log('Dependencies count:', result.dependencies?.length ?? 0);
}

test().catch(console.error);
"
```

Verify:
- Package metadata is fetched correctly
- Dependencies are populated (if the test package has any)
- No schema validation errors

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
  releaseChannels: ReleaseChannelData[];  // NOT versions[]
}

interface ReleaseChannelData {
  channel: string;       // e.g., "latest", "next", "beta"
  version: string;
  publishedAt: Date;
  dependencies: DependencyData[];
}

interface DependencyData {
  name: string;
  versionRange: string;
  type: "runtime" | "dev" | "peer" | "optional";
  registry: Registry;    // REQUIRED - set by the mapper
}
```

## Cross-Registry Dependencies

Some registries (like JSR) can have dependencies from multiple registries:
- `jsr:@std/path` → registry: "jsr", name: "@std/path"
- `npm:lodash` → registry: "npm", name: "lodash"

The mapper is responsible for parsing these specifiers and setting the correct registry on each dependency. The worker's `process-fetch.ts` groups dependencies by registry and creates placeholders in the appropriate registry.

## Registry-Specific Notes

### jsr ✅ IMPLEMENTED
Reference: `/skills/services/worker/registries/jsr/` (separate endpoints, cross-registry deps)

### nuget ✅ IMPLEMENTED
Reference: `/skills/services/worker/registries/nuget/` (paginated responses, dependency groups)

### dockerhub ✅ IMPLEMENTED
Reference: `/skills/services/worker/registries/dockerhub/` (no deps, named tags only)

### homebrew ✅ IMPLEMENTED
Reference: `/skills/services/worker/registries/homebrew/` (simple API, runtime/build/optional deps)

### archlinux ✅ IMPLEMENTED
Reference: `/skills/services/worker/registries/archlinux/` (official repos, depends/optdepends/makedepends)


## Key Principles

1. **Schema validation first** - Catch API changes early
2. **Consistent error types** - Use `{Registry}SchemaError` pattern
3. **Concurrency control** - Respect rate limits with batching
4. **Clean mapping** - Transform all registry quirks in mapper, not elsewhere
5. **Type safety** - All responses validated through Zod before use

## Start

Ask the user which registry they'd like to add support for.
