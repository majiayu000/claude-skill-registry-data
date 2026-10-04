---
name: typescript-testing-backend
description: Use when writing or reviewing TypeScript backend tests — Jest unit tests for services/controllers (mocked Prisma) or Supertest integration tests against a real isolated PostgreSQL test database. Triggers on edits to `*.service.test.ts`, `*.controller.test.ts`, `*.integration.test.ts`, service/controller/API test files (`.ts`, not `.tsx`) under `**/__tests__/`, or mentions of "backend test", "service test", "API test", "database test".
when_to_use: |
  Use when writing or reviewing TypeScript backend tests: Jest unit tests for services and controllers (with mocked Prisma), or Supertest integration tests against a real isolated PostgreSQL test database. The key signals are `*.service.test.ts`, `*.controller.test.ts`, `*.integration.test.ts` files, or any request to test backend service logic or HTTP routes.

  Not when: the task is writing tests for React components or hooks — use typescript-testing-frontend. Not when the task is writing the production service/controller code itself — use the appropriate implementation skill.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# TypeScript Testing — Backend

You are operating as a backend test engineer. Mock at the module edge for units, hit a real Postgres for integration, and never assert on internal call shapes.

Reference stack: Jest 29 with `@swc/jest`, Supertest for HTTP, a custom `TestServer` helper that simulates Next.js route handlers, and a `TestDatabase` helper that provisions isolated PostgreSQL instances per run with migrations + seed. Tests live co-located in `__tests__/` folders.

Unit tests mock the Prisma client at the module boundary; integration tests use the real DB plus an auth-state helper for authenticated request flows.

## Universal Rules

1. **Use Jest** — `jest.mock()` / `jest.fn()`, never `vi.*`.
2. **Co-locate tests** in `__tests__/` next to the source.
3. **Mock at the module boundary** — not internal functions.
4. **Literal expected values** — `expect(total).toBe(70)`, never expressions.
5. **Every `it()` asserts** observable behavior with at least one `expect()`.
6. **`beforeEach` cleanup**, scoped to test-created records — never truncate seed data.
7. **Clear auth/state helpers between tests** so authenticated flows don't bleed across cases.
8. **Never `test.skip()`** — fix or delete.
9. **Real DB for integration tests**, mocked Prisma for unit tests.
10. **Internal utils stay real** — only mock external boundaries.

## References

- [references/framework-and-structure.md](references/framework-and-structure.md) — Jest config, test scripts, directory layout, file naming conventions, coverage
- [references/unit-testing.md](references/unit-testing.md) — service unit tests with mocked Prisma, controller unit tests with injected service mocks
- [references/integration-testing.md](references/integration-testing.md) — shared setup, full Supertest example, `TestServer` pattern, `authTestHelpers` API
- [references/database-testing.md](references/database-testing.md) — `setupTestDatabase`, isolated DBs, cleanup rules, accessing seeded data
- [references/mock-policy-and-quality.md](references/mock-policy-and-quality.md) — mock scope table, quality criteria, test failure triage
