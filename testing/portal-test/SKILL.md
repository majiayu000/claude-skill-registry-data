---
name: portal-test
description: Add or run a Jest test for a portal file in apps/portal/. Use when the user says "add a test for X", "why is this test failing", "run tests for Y", or imports a new workspace package that needs a Jest moduleNameMapper entry. Pairs with the portal-test-on-edit PostToolUse hook.
disable-model-invocation: true
---

# Portal Test

User-only side-effect skill. Walks the contributor through adding or running a Jest test for a portal file, with explicit handling of the repo's brittle Jest `moduleNameMapper` setup.

## When to use

- User says "add a test for X", "test this file", "run the test for Y"
- User imports a new workspace package (`@repo/*`) subpath in portal code
- A test file is failing with `Cannot find module '@repo/...'` even though the import works at runtime

## When NOT to use

- The work is E2E (Playwright) — point the user to `pnpm test:e2e` and the integration-tester agent
- The work is unit-test scaffolding in a non-portal package (`packages/*`) — those have their own Jest configs

## Workflow

1. **Detect the new import.** Read the file the user wants to test. List every `import` of a `@repo/*` package. Cross-reference with `apps/portal/jest.config.js` `moduleNameMapper` entries.
2. **Check the Jest mapping.** The portal's Jest config uses explicit `moduleNameMapper` entries; wildcards alone don't always resolve subpaths. For each new import, verify the mapping exists. If missing, add it.
3. **If mapping is missing**, add the entry to `apps/portal/jest.config.js`. The pattern is:
   ```js
   '^@repo/<pkg>$': '<rootDir>/../../packages/<pkg>/src',
   '^@repo/<pkg>/<subpath>$': '<rootDir>/../../packages/<pkg>/src/<subpath>',
   ```
4. **Find or create the test file.** Look for `foo.test.ts` (or `.test.tsx`) co-located with `foo.ts`. If absent, scaffold using the project pattern (jest + ts-jest + jsdom + @testing-library/react for components, or just jest + ts-jest for pure logic).
5. **Run the test in isolation** with `pnpm --filter portal test -- --testPathPatterns=<relative/path/to/foo.test.ts>`. Cap at 60s — full suite is part of `pnpm quality`.
6. **Report coverage delta** by running `pnpm --filter portal test -- --coverage --testPathPatterns=<relative/path>` and comparing against the existing baseline (currently 40% lines, 30% branches, 35% functions, 40% statements per CLAUDE.md).
7. **Common pitfalls to surface:**
   - `Cannot find module '@repo/ui/widgets/X'` — wildcard pattern didn't catch it; add an explicit entry
   - `Jest encountered an unexpected token` in TSX — usually a transform config issue, not a mapping issue
   - Test passes locally but fails in CI — usually a missing env var; check `apps/portal/.env.example`

## Agents to consider

| Agent                | When                                                   |
| -------------------- | ------------------------------------------------------ |
| `test-writer`        | New unit test for a pure function or component         |
| `integration-tester` | E2E / cross-app flows                                  |
| `frontend-developer` | Component-level tests, render output, user interaction |

## Anti-patterns

- **Editing `moduleNameMapper` to a wildcard** (`'@repo/.*': '<rootDir>/...'`) — breaks the existing precedence and often silently resolves to the wrong subpath. Always add explicit entries.
- **Mocking `@repo/supabase/server` globally** — break the auth flow tests; mock at the test-file level only.
- **Skipping the mapping check** when the test "fails locally, works in dev" — always check the mapping first, even if the import "should" resolve via the catalog.
- **Running the full suite** when one test fails — the portal Jest config is slow; iterate per-file.

## Hook pairing

The `portal-test-on-edit` PostToolUse hook in `.claude/settings.json` (async) auto-runs the matching test file when a file in `apps/portal/app/api/**` or `apps/portal/lib/ai/**` is edited. This skill handles the slower, more deliberate "add a new test" workflow.
