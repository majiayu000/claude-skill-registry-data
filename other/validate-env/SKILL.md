---
name: validate-env
description: Use when a frontend project reads import.meta.env - parses it once with a Zod schema at startup, fails fast with a readable message, and exports a typed env object the seams import instead of raw reads.
---

# Validate Env

## 1. Audit current state

```bash
ls src/libs/env.ts .env.example .env.test .claude/stack-profile.md 2>/dev/null
grep -rn "import.meta.env.VITE_" src/ 2>/dev/null | head   # raw, unvalidated reads to migrate
grep -n '"zod"' package.json
```

Read `.claude/stack-profile.md` if present: `package_manager` replaces `pnpm` below; `frontend.meta` of `nuxt` or `next` means this skill does not apply (their env comes from `runtimeConfig` / `NEXT_PUBLIC_*`, validated in their own config); say so and stop.

A missing `VITE_API_URL` today fails *silently at runtime* (the `fetcher` falls back to `''` and every request hits the page origin). This skill turns that into a startup error.

## 2. Decide what to do
- No `env.ts` → create it (steps 4–6) and migrate raw reads (step 6).
- `env.ts` exists → confirm the schema covers every `VITE_*` the app reads.
- The app reads **no** `VITE_*` variable yet → exit; add the skill with the first one.

## 3. Detect framework
None needed: Vite exposes `import.meta.env` the same way to React and Vue.

## 4. Install (if needed)
```bash
pnpm add zod
```
Zod 4 (`z.url()`, `z.prettifyError()`). Zod 3 projects: keep their API, do not mix.

## 5. Schema, parsed once at startup

```ts
// src/libs/env.ts
import { z } from 'zod';

// A blank `VITE_X=` in .env or CI arrives as '' — treat it as unset.
const blankToUndefined = (value: unknown) => (value === '' ? undefined : value);
const httpUrl = z.url({ protocol: /^https?$/ });

const schema = z.object({
  VITE_API_URL: httpUrl,
  VITE_SENTRY_DSN: z.preprocess(blankToUndefined, httpUrl.optional()),
  VITE_ANALYTICS_DOMAIN: z.preprocess(blankToUndefined, z.string().min(1).optional()),
});

const parsed = schema.safeParse(import.meta.env);
if (!parsed.success) {
  throw new Error(`Invalid environment variables:\n${z.prettifyError(parsed.error)}`);
}

/** Validated, typed env. Import this; never read `import.meta.env.VITE_*` directly. */
export const env = parsed.data;
```

Importing `env.ts` anywhere (the seams do) runs the check before the app renders, so a bad deploy fails at boot with the field name, not later with an empty-URL fetch. Keep only the variables the app reads; add a line when a seam needs one (`set-up-realtime` adds `VITE_REALTIME_URL`).

`env`'s type comes from the schema, so there is no second declaration to keep in sync. Do **not** add an `ImportMetaEnv` augmentation: raw reads are banned, so it would only duplicate the schema.

Commit a `.env.example` listing every key with a harmless value, and a `.env.test` with the values Vitest needs (`VITE_API_URL=http://api.test`); Vitest loads `.env.test` because it runs in Vite's `test` mode.

## 6. Migrate the seams

Point each seam at `env`:
```ts
// src/libs/fetcher.ts
import { env } from '@/libs/env';
const BASE_URL = env.VITE_API_URL; // was: import.meta.env.VITE_API_URL ?? ''
```
Do the same in `sentry.ts` (`env.VITE_SENTRY_DSN`) and `analytics.ts` (`env.VITE_ANALYTICS_DOMAIN`).

## 7. Verify

Add the unit test; it proves the check can fail:
```ts
// tests/unit/env.test.ts (needs configure-test-stack and the `@/` alias from configure-typescript; otherwise run the two checks by hand)
import { afterEach, expect, test, vi } from 'vitest';

afterEach(() => {
  vi.unstubAllEnvs();
  vi.resetModules();
});

test('accepts a valid environment and treats blank optionals as unset', async () => {
  vi.stubEnv('VITE_API_URL', 'https://api.example.com');
  vi.stubEnv('VITE_SENTRY_DSN', '');
  const { env } = await import('@/libs/env');
  expect(env.VITE_SENTRY_DSN).toBeUndefined();
});

test('throws at import time with the field name when a variable is invalid', async () => {
  vi.stubEnv('VITE_API_URL', 'javascript:alert(1)');
  await expect(import('@/libs/env')).rejects.toThrow(/VITE_API_URL/);
});
```
`vi.stubEnv` reaches `import.meta.env` only on Vitest versions whose env replacement forwards `process.env` (Vitest 3+); on an older runner the test reads `.env.test` instead, so the "throws" case may not throw. If that happens, assert against the parse function directly instead of the module import.
```bash
pnpm typecheck                 # env is typed from the schema
pnpm vitest run tests/unit/env.test.ts
grep -rn "import.meta.env.VITE_" src/   # only src/libs/env.ts may match
# by hand: blank VITE_API_URL in .env, `pnpm dev` → the console shows "Invalid environment variables: ✖ Invalid URL → at VITE_API_URL"
```

## References
- ./env-patterns.md — fail-fast, one typed object, the `VITE_` prefix, shape not presence, blank values, build-time secrets.
- ../_shared/fetcher.md — the `fetcher` seam that imports `env`.
- ../_shared/conventions.md — `libs/` seam location, the `typecheck` rule.
