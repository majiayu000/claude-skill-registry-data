---
name: config-management
description: "Validate config at startup, secrets in memory only. Never read config during requests, never store secrets in env vars. Use node-env-resolver for multi-source config."
version: 1.0.0
libraries: ["node-env-resolver", "zod"]
---

# Config Management

Validate once at startup, fail fast, never leak secrets.

## Core Principle

Configuration is a potential source of runtime errors. Validate at startup so failures happen immediately, not at 3 AM when a code path finally executes.

## Required Behaviors

### 1. Validate Config at Startup

Use [node-env-resolver](https://github.com/jagreehal/node-env-resolver) for multi-source configuration with validation:

```typescript
import { resolveAsync } from 'node-env-resolver';
import { processEnv } from 'node-env-resolver/resolvers';
import { postgres, string, number } from 'node-env-resolver/validators';
import { awsSecrets } from 'node-env-resolver-aws';

const config = await resolveAsync({
  resolvers: [
    // Non-sensitive config from process.env (safe)
    [processEnv(), {
      PORT: number({ default: 3000 }),
      NODE_ENV: ['development', 'production'] as const,
    }],
    // Secrets loaded directly into memory from AWS (never touch process.env)
    [awsSecrets({ secretId: 'my-app' }), {
      DATABASE_URL: postgres(),
      API_KEY: string(),
    }],
  ],
  options: {
    preventProcessEnvWrite: true,  // Secrets never touch process.env
  },
});
```

**Alternative:** Use Zod directly for simpler setups:

```typescript
// config/schema.ts
import { z } from 'zod';

const ConfigSchema = z.object({
  port: z.coerce.number().min(1).max(65535),
  database: z.object({
    host: z.string().min(1),
    port: z.coerce.number(),
    name: z.string().min(1),
  }),
  redis: z.object({
    url: z.string().url(),
  }),
  logLevel: z.enum(['debug', 'info', 'warn', 'error']),
});

export type Config = z.infer<typeof ConfigSchema>;

// main.ts - Validate immediately on startup
const config = ConfigSchema.parse({
  port: process.env.PORT,
  database: {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    name: process.env.DB_NAME,
  },
  redis: {
    url: process.env.REDIS_URL,
  },
  logLevel: process.env.LOG_LEVEL,
});

// If we get here, config is valid and typed
```

### 2. Never Read Config During Requests

Config should be resolved ONCE at startup, then injected:

```typescript
// WRONG - Reading env vars during request
async function getUser(args: { userId: string }, deps: GetUserDeps) {
  const timeout = parseInt(process.env.DB_TIMEOUT || '5000'); // Reads every call!
  return deps.db.findUser(args.userId, { timeout });
}

// CORRECT - Config injected via deps
type GetUserDeps = {
  db: Database;
  config: { dbTimeout: number };
};

async function getUser(args: { userId: string }, deps: GetUserDeps) {
  return deps.db.findUser(args.userId, { timeout: deps.config.dbTimeout });
}
```

### 3. Secrets in Memory Only

Never store secrets in environment variables. Load directly from secret managers into memory:

```typescript
// WRONG - Secret in env, visible in process dumps, /proc/self/environ, child processes
const apiKey = process.env.API_KEY;

// CORRECT - Fetch from secret manager at startup, loaded into memory only
const config = await resolveAsync({
  resolvers: [
    [awsSecrets({ secretId: 'my-app' }), {
      API_KEY: string(),
      DATABASE_PASSWORD: string(),
    }],
  ],
  options: {
    preventProcessEnvWrite: true,  // Secrets never touch process.env
  },
});

// Secrets are in config object in memory, never in process.env
const deps = { db: createDb(config.DATABASE_PASSWORD), apiKey: config.API_KEY };
```

**Why memory is safer:**
- `process.env` is accessible to child processes
- On Linux, `/proc/self/environ` exposes all environment variables
- Error messages and logs may accidentally include environment variables
- Secrets in memory are isolated to your application process

### 3a. Ephemeral Credentials

Prefer short-lived, auto-rotating credentials over long-lived secrets:

```typescript
const config = await resolveAsync({
  resolvers: [
    [awsSecrets({
      secretId: 'prod/db-creds',
      refreshInterval: 3600000,  // Refresh every hour
    }), {
      DB_USERNAME: string(),
      DB_PASSWORD: string(),  // Short-lived, auto-rotated
    }],
  ],
});
```

If a credential leaks, automatic expiration limits the blast radius.

### 3b. Secret Scanning in CI

Runtime policies protect production, but what about the `.env` file that should never exist? Run secret scanning in CI:

```yaml
# .github/workflows/security.yml
name: Security Checks

on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for thorough scanning

      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

Tools like **TruffleHog** and **Gitleaks** scan commit history, catching secrets that were committed and then "deleted" (but still exist in git history).

### 4. Fail Fast on Missing Config

```typescript
// WRONG - Default values hide misconfiguration
const port = process.env.PORT || 3000;
const dbHost = process.env.DB_HOST || 'localhost';

// CORRECT - Fail immediately if missing
const ConfigSchema = z.object({
  port: z.coerce.number(),  // No default - must be provided
  dbHost: z.string().min(1),  // No default - must be provided
});

// Throws ZodError at startup if missing
const config = ConfigSchema.parse(process.env);
```

### 5. Type-Safe Config Access

Use Zod inference to ensure type safety:

```typescript
// Config type is inferred from schema
export type Config = z.infer<typeof ConfigSchema>;

// Deps include typed config
type GetUserDeps = {
  db: Database;
  config: Pick<Config, 'dbTimeout' | 'maxRetries'>;
};
```

## Environment-Specific Config

```typescript
const EnvSchema = z.enum(['development', 'staging', 'production']);

const BaseConfigSchema = z.object({
  env: EnvSchema,
  port: z.coerce.number(),
});

// Environment-specific overrides
const ProductionConfigSchema = BaseConfigSchema.extend({
  env: z.literal('production'),
  sslEnabled: z.literal(true),
});

const DevelopmentConfigSchema = BaseConfigSchema.extend({
  env: z.literal('development'),
  sslEnabled: z.literal(false).default(false),
});

const ConfigSchema = z.discriminatedUnion('env', [
  ProductionConfigSchema,
  DevelopmentConfigSchema,
]);
```

## Dependency Injection for Testability

Configuration resolution should accept resolvers as parameters:

```typescript
// config.ts
import { resolveAsync, type Resolver } from 'node-env-resolver';
import { processEnv } from 'node-env-resolver/resolvers';
import { awsSecrets } from 'node-env-resolver-aws';
import { postgres, string, number } from 'node-env-resolver/validators';

const schema = {
  PORT: number({ default: 3000 }),
  DATABASE_URL: postgres(),
  API_KEY: string(),
};

export async function getConfig(
  resolvers: Resolver[] = [
    processEnv(),
    awsSecrets({ secretId: 'my-app' }),
  ]
) {
  return resolveAsync({
    resolvers: resolvers.map(r => [r, schema]),
  });
}
```

Now your tests can inject mock resolvers:

```typescript
// config.test.ts
import { getConfig } from './config';

it('should resolve configuration', async () => {
  const mockResolver = {
    name: 'test-env',
    load: async () => ({
      DATABASE_URL: 'postgres://test:5432/testdb',
      API_KEY: 'test-key',
    }),
    loadSync: () => ({
      DATABASE_URL: 'postgres://test:5432/testdb',
      API_KEY: 'test-key',
    }),
  };

  const config = await getConfig([mockResolver]);

  expect(config.DATABASE_URL).toBe('postgres://test:5432/testdb');
  expect(config.API_KEY).toBe('test-key');
  expect(config.PORT).toBe(3000); // default value
});
```

No `vi.mock()` needed. Just pass a resolver object. This is the same dependency injection pattern we've been using throughout.

## Config in Tests

```typescript
import { mock } from 'vitest-mock-extended';

const testConfig: Pick<Config, 'dbTimeout'> = {
  dbTimeout: 100, // Fast for tests
};

const deps = {
  db: mock<Database>(),
  config: testConfig,
};

const result = await getUser({ userId: '123' }, deps);
```

## Quick Reference

| Rule | Implementation |
|------|----------------|
| Validate at startup | Zod schema.parse() in main.ts |
| Never read during request | Inject config via deps |
| Secrets in memory | SecretManager.get(), not process.env |
| Fail fast | No defaults for required config |
| Type safety | z.infer<typeof Schema> |
