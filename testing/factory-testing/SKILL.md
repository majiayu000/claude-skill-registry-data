---
name: factory-testing
description: Testing conventions across builds. Vitest + Playwright as the locked stack; tests co-located in `__tests__` next to the code they verify; shared test primitives (provider wrappers, mock factories) centralized in `src/lib/test-utils.tsx`; coverage thresholds enforced at the merge gate (CI ownership lives in `factory-ci.md`). Read at project kickoff and whenever you write or review a test.
---

# Factory testing

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Vitest / Playwright / test-utils shape we use), and **Failure mode** when there's one to name.

The kit is opinionated on the recipe layer (Vitest + Playwright + `__tests__` co-location + shared test-utils). A reader on a different stack can read the principle and skip the recipe.

## Tests-before-merge — coverage gates, not test-first dogma

**Principle.** Every PR ships with tests that cover the new behavior; CI enforces a coverage floor; the kit does not mandate red-green-refactor authoring.

**Why.** Strict TDD is unenforceable mechanically — a commit hook can't see whether the test was written before or after the code. A coverage floor is enforceable: CI either passes or fails. The trade-off accepted: we lose the design-pressure of test-first authoring; we keep a gate that catches the actual failure mode (un-tested code merging). Strict test-first also contradicts how most of the factory's existing code was written, which would make the rule aspirational from day one — and aspirational rules erode all the others.

**Recipe.** Coverage thresholds live in `vitest.config.ts` and are enforced by `vitest --coverage`:

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'happy-dom',
    globals: true,
    setupFiles: ['./src/lib/test-utils.tsx'],
    exclude: ['node_modules', 'e2e/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/lib/test-utils.tsx',
        '**/*.test.{ts,tsx}',
        '**/*.spec.{ts,tsx}',
        '**/types.ts',
        '**/*.d.ts',
      ],
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 60,
        statements: 70,
      },
    },
  },
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
});
```

Numbers are duezy's: 70/70/60/70 is the conservative floor — raise per-project as coverage matures, never lower. `e2e/**` is excluded because Playwright owns that layer. Enforcement happens in CI (`pnpm test:coverage`); see `factory-ci.md §Coverage floor enforced in CI`.

**Failure mode.** No test coverage and no gate → drift over months until the first real bug, where the missing test is also the missing spec. Right move at project kickoff: install Vitest + the config above and write one smoke test per feature folder. A 70% floor with smoke tests beats a 100% aspiration with none.

## Co-locate tests in `__tests__` next to the code

**Principle.** Tests live in a `__tests__` subdirectory at the feature level, not a root `tests/` directory.

**Why.** Refactors move folders; tests in a parallel `tests/` tree get orphaned silently — the test imports a path that no longer exists, the test file is skipped or fails, and nobody notices until the next coverage report. Co-location makes "move this feature" a single-folder operation and makes "is this code tested" visible from the file tree. The trade-off accepted: the feature folder is slightly noisier; you can always collapse `__tests__/` in your editor.

**Recipe.** Unit and integration tests live next to the code:

```
src/lib/fields/
├── SSNInput.tsx
├── __tests__/
│   ├── SSNInput.test.tsx
│   └── registry.test.ts
└── registry.ts
```

Naming: `*.test.ts(x)` for Vitest unit/integration, `*.spec.ts` for Playwright E2E. E2E lives at `/e2e/` at the repo root because flows transcend features — there is no single feature folder a user-journey test belongs in.

## Shared test primitives — provider wrappers and mock factories

**Principle.** Provider wrappers, query-client factories, and tRPC mock factories are centralized in `src/lib/test-utils.tsx`; per-file inline setup is a smell.

**Why.** Every test that sets up its own QueryClient + ThemeProvider + auth context is a maintenance liability — the day those providers change, you edit N files and miss at least one. Centralized factories mean one edit propagates. The trade-off accepted: test-utils becomes load-bearing infrastructure that needs its own care; every contributor reads it once, and the savings compound.

**Recipe.** The full `src/lib/test-utils.tsx` shape, lifted from duezy:

```tsx
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import '@testing-library/jest-dom';

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

function TestProviders({ children }: { children: React.ReactNode }) {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <MantineProvider>{children}</MantineProvider>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) {
  return render(ui, { wrapper: TestProviders, ...options });
}

export function createMockMutation<TData = unknown, TVariables = unknown>() {
  return {
    mutate: vi.fn<(variables: TVariables) => void>(),
    mutateAsync: vi.fn<(variables: TVariables) => Promise<TData>>(),
    reset: vi.fn(),
    isPending: false,
    isError: false,
    isSuccess: false,
    isIdle: true,
    error: null,
    data: undefined as TData | undefined,
    variables: undefined as TVariables | undefined,
    failureCount: 0,
    failureReason: null,
    status: 'idle' as const,
  };
}

export function createMockQuery<TData = unknown>() {
  return {
    data: undefined as TData | undefined,
    isLoading: false,
    isError: false,
    isSuccess: false,
    error: null,
    refetch: vi.fn(),
    status: 'idle' as const,
  };
}

export * from '@testing-library/react';
export { vi } from 'vitest';
```

Component tests then read as:

```tsx
import { renderWithProviders, screen } from '@/lib/test-utils';
import { SSNInput } from '../SSNInput';

it('masks input on blur', () => {
  renderWithProviders(<SSNInput name="ssn" />);
  // ...
});
```

Swap `MantineProvider` for the project's UI provider if not Mantine; the shape is the contract, not the specific provider.

## Test the boundaries; trust the framework

**Principle.** Tests cover contracts the framework doesn't enforce — auth middleware codes, schema↔registry alignment, conditional field visibility, validator behavior. Tests do not cover that React rendered.

**Why.** Testing framework behavior is testing the framework's tests. The value is in the seams — the procedure boundary, the validator, the conditional logic — because that's where regressions actually land. Coverage of seams catches the bugs that compile-clean code can still produce. Coverage of framework calls is theater: it raises the coverage number without raising the failure-catch rate.

**Recipe — boundary test for a tRPC procedure.** Mock the DB + auth, reconstruct the middleware to assert the contract, test `UNAUTHORIZED` / `FORBIDDEN` codes explicitly:

```ts
// src/lib/trpc/__tests__/banking-application.router.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { TRPCError } from '@trpc/server';

vi.mock('../../../../db', () => ({
  db: { query: { bankingApplication: { findFirst: vi.fn() } }, insert: vi.fn() },
}));
vi.mock('@/lib/auth', () => ({
  auth: { api: { getSession: vi.fn() } },
}));

import { initTRPC } from '@trpc/server';
import superjson from 'superjson';

interface TestContext {
  session: {
    user: { id: string; email: string } | null;
    session: { activeOrganizationId: string | null } | null;
  } | null;
}

const t = initTRPC.context<TestContext>().create({ transformer: superjson });

const enforceOrganizationAccess = t.middleware(async ({ ctx, next }) => {
  if (!ctx.session?.user) throw new TRPCError({ code: 'UNAUTHORIZED' });
  if (!ctx.session.session?.activeOrganizationId) {
    throw new TRPCError({ code: 'FORBIDDEN', message: 'No active organization selected' });
  }
  return next({ ctx });
});

// ... then assert the middleware throws the right codes for each ctx shape
```

**Recipe — schema↔registry alignment test.** Bidirectional coverage with an explicit allowlist for known-planned fields:

```ts
// src/lib/fields/__tests__/registry.test.ts
import { describe, it, expect } from 'vitest';
import { FIELD_REGISTRY } from '@/lib/fields/registry';
import { defaultApplicationDetails } from '@/lib/schemas/banking-form';

describe('FIELD_REGISTRY coverage', () => {
  it('contains metadata entries for each schema field', () => {
    const systemFields = ['attestationTimestamp', 'attestationIpAddress'];
    const missing = Object.keys(defaultApplicationDetails).filter(
      (key) => !FIELD_REGISTRY[key] && !systemFields.includes(key),
    );
    expect(missing).toEqual([]);
  });

  it('does not contain registry entries without schema coverage', () => {
    const schemaKeys = new Set(Object.keys(defaultApplicationDetails));
    const allowlist = new Set([
      // Planned-but-not-yet-in-schema fields — keep this list short
      'conditionalResponses',
    ]);
    const unused = Object.keys(FIELD_REGISTRY).filter(
      (key) => !schemaKeys.has(key) && !allowlist.has(key),
    );
    expect(unused).toEqual([]);
  });
});
```

The allowlist is the explicit acknowledgment that some fields don't match yet — better than commenting out the test or lowering the bar.

**Failure mode.** Mock-only tests passing while prod fails. A test that mocks the DB will not catch a broken migration, an RLS misconfiguration, or a query that throws against real Postgres. Right move: integration tests that hit a real DB run in CI against an ephemeral PR branch (see `factory-ci.md §Ephemeral DB per PR`). Mocks are fine for unit tests; integration tests must not mock the thing they're integrating with.

## E2E owns user flows; unit owns behavior

**Principle.** Unit tests verify one unit; E2E tests verify the user can complete a flow end-to-end. There is no middle layer of integration tests pretending to be both.

**Why.** Integration tests that mock half the stack are the worst of both worlds — slow like E2E because they spin up real providers, fake like unit because they mock the network or DB, debugged like neither because the failure could be in the real half or the mocked half. Two layers, two clear purposes. The trade-off accepted: a few cases where the right boundary is genuinely fuzzy (cross-procedure flows that aren't full user journeys) get pushed to E2E; the gain is that the test pyramid stays interpretable.

**Recipe — Playwright config.** Conservative timeouts, screenshot+video on failure, trace on first retry, `webServer.reuseExistingServer` for fast local iteration:

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'e2e/.auth/user.json' },
      dependencies: ['setup'],
    },
    {
      name: 'unauthenticated',
      testMatch: /.*\.unauth\.spec\.ts/,
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
  timeout: 30 * 1000,
  expect: { timeout: 5 * 1000 },
  outputDir: 'e2e/test-results',
});
```

**Spec naming.** `*.unauth.spec.ts` for public flows (no `storageState`); plain `*.spec.ts` for authenticated flows that inherit the chromium project's `storageState`. The `auth.setup.ts` project writes the storage state once; every authenticated spec reuses it. This is the only convention that keeps E2E runtime tolerable as the flow count grows.

**Failure mode.** Snapshot tests as the only coverage. Snapshots tell you something changed; they do not tell you whether the change is correct. A repo where 80% of "tests" are snapshots has 80% noise and 20% signal. Right move: snapshots are an occasional supplement, never the primary assertion. Assert behavior; snapshot the rare structural artifact (a generated SQL string, a serialized JSON envelope).

## Source patterns

duezy (Vitest + Playwright, `__tests__` co-location, `src/lib/test-utils.tsx` with `renderWithProviders` + `createTestQueryClient` + `createMockMutation`/`createMockQuery`, schema↔registry bidirectional coverage with allowlist, tRPC middleware reconstruction for boundary tests, Playwright `unauthenticated` project + `auth.setup.ts` `storageState` reuse, 70/70/60/70 coverage thresholds).

## Related

- `factory-ci.md` — owns the merge gate that enforces these tests (typecheck, test, build, claude-review)
- `factory-data-layer.md` — schema patterns the schema↔registry alignment test is built against
- `factory-api.md` — tRPC procedure patterns the boundary tests assert
- `factory-pitfalls.md` — cross-skill index entries for "no tests under src/" and "mock-only tests passing while prod fails"
